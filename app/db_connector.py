import json
from typing import Any, Dict, List, Optional
import datetime
from sqlalchemy import Column, Integer, String, Boolean, Text
from app.sqlalchemy_h import Base


class UsersTyping:
    __tablename__ = 'users'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    username = Column('username', String(64))
    password = Column('password', String(64))
    created_at = Column('created_at', String(20))
    usertoken = Column('usertoken', String(63))
    icon = Column('icon', String(64))
    email = Column('email', String(256))


class Users(Base, UsersTyping):
    privacy_settings = {}

    def get_dict(self, privacy_level: int = -1, delete: List[str] = []) -> Dict[str, Any]:
        data = DBtoDict(self, delete)
        data = DBtoJSON(data, [])
        return {
            k: v if self.privacy_settings.get(k, privacy_level) >= privacy_level else None
            for k, v in data.items()
        }

    @property
    def id_int(self):
        return int(self.id)


class PairsIndex(Base):
    __tablename__ = 'pairsindex'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    userid = Column('userid', Integer)
    pairid = Column('pairid', Integer)
    pairhash = Column('pairhash', String(20))
    accepted = Column('accepted', Boolean)

    privacy_settings = {}

    def get_dict(self, privacy_level: int = -1, delete: List[str] = []) -> Dict[str, Any]:
        data = DBtoDict(self, delete)
        data = DBtoJSON(data, [])
        return {
            k: v if self.privacy_settings.get(k, privacy_level) >= privacy_level else None
            for k, v in data.items()
        }


class Pairs(Base):
    __tablename__ = 'pairs'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    pairhash = Column('pairhash', String(20))
    name = Column('name', String(60))
    users = Column('users', Text)
    waitingnum = Column('waitingnum', Integer)

    privacy_settings = {}

    def get_dict(self, privacy_level: int = -1, delete: List[str] = []) -> Dict[str, Any]:
        data = DBtoDict(self, delete)
        data = DBtoJSON(data, ['users'])
        return {
            k: v if self.privacy_settings.get(k, privacy_level) >= privacy_level else None
            for k, v in data.items()
        }


class Payments(Base):
    __tablename__ = 'payments'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    payment = Column('payment', Integer)
    payor = Column('payor', Integer)
    creator = Column('creator', Integer)
    description = Column('description', Text)
    created_at = Column('created_at', String(20))
    createdIn = Column('createdIn', Integer)
    pairid = Column('pairid', Integer)

    privacy_settings = {}

    def get_dict(self, privacy_level: int = -1, delete: List[str] = []) -> Dict[str, Any]:
        data = DBtoDict(self, delete)
        data = DBtoJSON(data, [])
        return {
            k: v if self.privacy_settings.get(k, privacy_level) >= privacy_level else None
            for k, v in data.items()
        }


class TokenTable(Base):
    __tablename__ = 'tokentable'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    token = Column('token', String(65))
    userid = Column('userid', Integer)

    privacy_settings = {}

    def get_dict(self, privacy_level: int = -1, delete: List[str] = []) -> Dict[str, Any]:
        data = DBtoDict(self, delete)
        data = DBtoJSON(data, [])
        return {
            k: v if self.privacy_settings.get(k, privacy_level) >= privacy_level else None
            for k, v in data.items()
        }


def DBtoDict(obj, delete=[]):
    tmp: Dict[str, Any] = obj.__dict__
    tmp.pop('_sa_instance_state', None)
    return {k: tmp[k] for k in (tmp.keys() - set(delete))}


def DBtoJSON(data: Dict[str, Any], keys: List[str] = []):
    for k in keys:
        data[k] = json.loads(data[k])
    return data


def created_at(timeshift: Optional[datetime.timedelta] = None):
    if timeshift is None:
        timeshift = datetime.timedelta(0)
    return (datetime.datetime.now() + timeshift).isoformat('T', 'seconds')
