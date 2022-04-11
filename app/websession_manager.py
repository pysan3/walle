from __future__ import annotations

import os
import datetime
from collections import deque
from typing import TYPE_CHECKING, Any, Dict, Optional, Tuple

import jwt
from cryptography.fernet import Fernet
from itsdangerous.exc import BadSignature
from itsdangerous.url_safe import URLSafeSerializer

from app.hashids import accessHM

if TYPE_CHECKING:
    from app.login_manager import LMUsers

os.environ['WELLE_WSM_JWT_SALT'] = 'test'
os.environ['WELLE_WSM_SERIALIZER_KEY'] = 'test'
os.environ['WELLE_WSM_SERIALIZER_SALT'] = 'test'
os.environ['WELLE_WSM_ACCESSTOKEN_ENCRYPT'] = 'false'


class WebSessionCache:
    def __init__(self, max_length: int = 100, expires: datetime.timedelta = datetime.timedelta(0)) -> None:
        self.max_length = max_length
        self.expires = expires
        self.data_queue = deque()
        self.cache: Dict[int, Tuple[LMUsers, datetime.datetime]] = {}
        # { userid: (LMUsers, expires_at) }

    def put(self, userid: int, user: Optional[LMUsers]):
        if user is None:
            return
        self.data_queue.append(userid)
        self.cache[userid] = (user, datetime.datetime.now() + self.expires)
        self._del_exceed()
        if self.expires is not None:
            self._del_old()

    def get(self, userid: int) -> Optional[LMUsers]:
        if userid is not None and userid in self.cache:
            return self.cache[userid][0]
        return None

    def reset(self, userid: int):
        self.cache.pop(userid, None)

    def _del_old(self):
        now = datetime.datetime.now()
        while len(self.data_queue) != 0:
            userid = self.data_queue[0]
            if userid not in self.cache or self.cache[userid][1] < now:
                self.data_queue.popleft()
                self.cache.pop(userid, None)
            else:
                break

    def _del_exceed(self):
        while len(self.data_queue) > self.max_length:
            self.cache.pop(self.data_queue.popleft(), None)


class WebSessionToken:
    WST_SALT = os.environ.get('WELLE_WSM_JWT_SALT', 'WELLE_WSM_JWT_SALT')
    CRYPTO = None
    if os.environ.get('WELLE_WSM_ACCESSTOKEN_ENCRYPT', 'false') != 'false':
        CRYPTO = Fernet(Fernet.generate_key())
    SERILAIZER = URLSafeSerializer(
        os.environ.get('WELLE_WSM_SERIALIZER_KEY', 'WELLE_WSM_SERIALIZER_KEY'),
        salt=os.environ.get('WELLE_WSM_SERIALIZER_SALT', 'WELLE_WSM_SERIALIZER_SALT'),
    )

    def __init__(self, userid: int, expires: Optional[datetime.timedelta]
                 = None, expires_at: Optional[datetime.datetime] = None) -> None:
        self.userid = userid
        self.expires = expires or datetime.timedelta(minutes=30)
        self.expires_at = expires_at or datetime.datetime.now() + self.expires

    @classmethod
    def from_jwt(cls, st: str):
        try:
            data = jwt.decode(st, cls.WST_SALT, algorithms=['HS256'])
            session_token = data['session_token']
            expires_at = data['exp']
            if cls.CRYPTO is not None:
                session_token = cls.CRYPTO.decrypt(session_token.encode()).decode()
            userhash: str = cls.SERILAIZER.loads(session_token)
            return cls(accessHM.parse(userhash).ids, expires_at=datetime.datetime.fromtimestamp(expires_at)) or None
        except BadSignature as e:
            # Someone on clientside has changed the cookies
            # TODO: Logger warn here
            # logger.warn(e)
            print('BadSignatureError:', e)
            return None
        except jwt.ExpiredSignatureError as e:
            print('ExpiredSignatureError:', e)
            return None
        except Exception as e:
            print('UserLoadError:', e)
            return None

    def __str__(self) -> str:
        session_token: str = str(WebSessionToken.SERILAIZER.dumps(accessHM.stringify(self.userid, 'user')))
        if WebSessionToken.CRYPTO is not None:
            session_token = WebSessionToken.CRYPTO.encrypt(session_token.encode()).decode()
        return jwt.encode({
            'session_token': session_token,
            'exp': self.expires_at
        }, WebSessionToken.WST_SALT, algorithm='HS256')

    def to_header(self) -> Dict[str, Any]:
        return {
            'setsessiontoken': str(self),
            'expiresat': self.expires_at.strftime('%s')
        }
