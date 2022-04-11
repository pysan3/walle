from __future__ import annotations

import datetime as dt
import os
from typing import Any, Callable, Dict, List, Optional, Union

from responder_login import LoginManager, UserMixin
from responder_login.config import COOKIE_NAME

from app.db_connector import Users
from app.sqlalchemy_h import SessionContext, SessionType
from app.websession_manager import WebSessionCache, WebSessionToken, jwt


class WALLE_LM(LoginManager):
    def __init__(self, api=None):
        super(WALLE_LM, self).__init__(api=api)
        self.ws_cache = WebSessionCache(max_length=10, expires=dt.timedelta(days=-1))

    def init_api(self, api):
        self._api = api
        self._api.jinja_values_base = {}

    def _load_user(self, req, resp, *_, **__):
        if not self._user_callback:
            raise UnboundLocalError("Please set LoginManager._user_callback")
        try:
            if req is None or resp is None:
                raise Exception(f'{req=} or {resp=} is None.')
            user = None
            session_token = req.headers.get('SessionToken', None)
            user_cookie = req.cookies.get(COOKIE_NAME['ACCOUNT'])
            if session_token is not None:
                wst = WebSessionToken.from_jwt(session_token)
                if wst is None:
                    raise jwt.InvalidTokenError
                user = self.ws_cache.get(wst.userid) or LMUsers(wst.userid)
            elif user_cookie is not None:
                user = self._user_callback(user_cookie)
            if user is not None:
                self.ws_cache.put(user.id_int, user)
                new_wst = WebSessionToken(user.id_int)
                resp.headers.update(new_wst.to_header())
                req.headers['SessionToken'] = str(new_wst)
                return user
            return self.anonymous_user
        except Exception:
            import traceback
            print('expected error at _load_user')
            traceback.print_exc()
            return self.anonymous_user

    def login_required(self, fn=None, *, cache=True):
        def _decorate(function: Callable):
            async def wrapped_function(*args, **kwargs):
                ret = await super(WALLE_LM, self).login_required(function)(*args, **kwargs)
                if cache is False:
                    self.ws_cache.reset(self.current_member.id_int)
                return ret
            return wrapped_function
        if fn:
            return _decorate(fn)
        return _decorate

    @property
    def current_member(self):
        user = self.current_user
        if isinstance(user, LMUsers):
            return user
        raise Exception('User not Logged In')


lm = WALLE_LM()
lm.config['COOKIE_NAME']['ACCOUNT'] = os.environ.get('WALLE_LM_ACCOUNT_COOKIENAME', 'WALLE_LM_ACCOUNT_COOKIENAME')
lm.config['COOKIE_NAME']['IS_FRESH'] = os.environ.get('WALLE_LM_FRESH_COOKIENAME', 'WALLE_LM_FRESH_COOKIENAME')
lm.config['COOKIE_DURATION'] = dt.timedelta(days=365 * 10)
# ! turn this on after changes done in frontend
# lm.config['COOKIE_SECURE'] = True # needs HTTPS
# lm.config['COOKIE_HTTPONLY'] = True # disable access from JS on clientside


class LMUsers(UserMixin):
    """ ! READONLY
    This class is a wrapper for Users class from app/db_connect.py
    Column data can be accessed by the same attributes.
    The data is "readonly" and will not be committed to DB even if overwritten.
    """

    def __init__(self, user_or_userid: Union[Users, int], session: Optional[SessionType] = None) -> None:
        """Copies all data in Users instance and stores them.

        Data will not be destroyed even after session is closed.

        if `user_or_userid` is Users instance, data is used.
        elif `user_or_userid` is int, data is taken from DB using `session`

        Args:
            user_or_userid (Union[Users,int], optional):
                Instance of Users class or id of user to be wrapped. Defaults to None.
            session (SessionType, optional): Used to access DB, will create new session if None. Defaults to None.
        """
        if isinstance(user_or_userid, int):
            with SessionContext(session=session) as session:
                self.user_data = session.query(Users).get(user_or_userid).get_dict()
        else:
            self.user_data = user_or_userid.get_dict()
        for k, v in self.user_data.items():
            setattr(self, k, v)

    @property
    def id_int(self):
        return int(self.user_data['id'])

    def get_dict(self, privacy_level: int = -1, delete: List[str] = []) -> Dict[str, Any]:
        return {
            k: self.user_data[k] if Users.privacy_settings.get(k, privacy_level) >= privacy_level else None
            for k in (self.user_data.keys() - set(delete))
        }

    def get_id(self) -> str:
        " returns the encrypted key for cookie as `str`"
        return self.user_data['usertoken']


def lm_user_loader(user_token: str) -> Optional[LMUsers]:
    """Returns a LMUser instance of the given token

    Args:
        user_token (str): user_token specified in cookie

    Returns:
        Optional[LMUsers]: instance of LMUser or None(if error)
    """
    if user_token is None:
        return None
    with SessionContext() as session:
        user = session.query(Users).filter_by(usertoken=user_token).one_or_none()
        return LMUsers(user) if user else None


@lm.unauthorized_handler
def lm_unauthorized(req, resp, **__):
    resp.text = lm.config['LOGIN_REQUIRED_MESSAGE']
    resp.status_code = 401


@lm.authorized_handler
def lm_authorized(req, resp, **__):
    resp.text = lm.config['LOGIN_PROHIBITED_MESSAGE']
    resp.status_code = 403
