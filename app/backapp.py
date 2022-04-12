import datetime as dt
import hashlib
import secrets
from pathlib import Path

from app.db_connector import *  # noqa
from app.sqlalchemy_h import SessionContext
from app.websession_manager import WebSessionToken

staticFileDir = Path('./dist')
staticFileDir.mkdir(parents=True, exist_ok=True)


def login(username: str, password: str):
    with SessionContext() as session:
        users = session.query(Users).filter_by(username=username).all()
        password = hashlib.sha256(password.encode()).hexdigest()
        if len(users) == 1:
            user: Users = users[0]
            if user.password == password:
                userid = user.id_int
                return new_token(userid)
    return None


def signup(username: str, password: str, email: str):
    with SessionContext() as session:
        if len(session.query(Users).filter_by(username=username).all()) != 0:
            return None
    usericonsDir = staticFileDir / 'usericons'
    usericonsDir.mkdir(parents=True, exist_ok=True)
    new = Users(
        username=username,
        password=hashlib.sha256(password.encode()).hexdigest(),
        created_at=dt.datetime.now().isoformat(' ', 'seconds'),
        usertoken=secrets.token_urlsafe(),
        icon=str((usericonsDir / f'{username}.jpg')),
        email=email,
    )
    with SessionContext() as session:
        session.add(new)
        session.flush()
        userid = int(new.id_int)
    return new_token(userid)


def getUserData(userid: int, session=None):
    with SessionContext(session=session) as session:
        return session.query(Users).get(userid).get_dict()


def new_token(userid: int, session=None):
    with SessionContext(session=session) as session:
        token = secrets.token_hex()
        session.add(TokenTable(
            token=token,
            userid=userid,
        ))
        return token


def usertoken2id(token: str, session=None):
    print(f'{token=}')
    with SessionContext(session=session) as session:
        user = session.query(Users).filter_by(usertoken=token).one_or_none()
        if user is None:
            raise Exception('User not Found')
        return int(user.id)  # type: ignore


def searchTokenTable(token: str, session=None):
    with SessionContext(session=session) as session:
        token = session.query(TokenTable).filter_by(token=token).one_or_none()
        if token is None:
            raise Exception(f'Token: {token} Is Not Found in Tokentable')
        return int(token.userid)  # type: ignore


def userid2token(userid: int, session=None) -> str:
    with SessionContext(session=session) as session:
        user = session.query(Users).get(userid)
        if user is None:
            raise Exception(f'User: {userid} Not Found')
        return user.usertoken


def returnwebsessiontoken(userid: int):
    return WebSessionToken(userid).to_header()
