import json
from typing import Set
from app import backapp
from app.db_connector import *  # noqa
from app.sqlalchemy_h import SessionContext
from app.hashids import pairHM


def generatePairHash(*ids: int):
    return pairHM.encode(*set(ids))


def decodePairHash(pairhash: str) -> Set[int]:
    return set(pairHM.decode(pairhash))


def validPairAccess(userid: int, pairhash: str):
    return userid in decodePairHash(pairhash)


def addnewpair(userid: int, *ids: int):
    users = sorted([userid, *ids])
    print(users)
    if len(users) <= 1:
        return False
    pairhash = generatePairHash(*users)
    with SessionContext() as session:
        pair: Optional[Pairs] = session.query(Pairs).filter_by(pairhash=pairhash).one_or_none()
        if pair is not None:
            return acceptpair(userid, pairid=int(pair.id))  # type: ignore
        pair = Pairs(
            pairhash=pairhash,
            name=' '.join([backapp.getUserData(i, session)['username'] for i in users]),
            users=json.dumps(users),
            waitingnum=len(users) - 1,
        )
        session.add(pair)
        session.flush()
        pairid = int(pair.id)  # type: ignore
    with SessionContext(session=None) as session:
        session.add(PairsIndex(userid=userid, pairid=pairid, pairhash=pairhash, accepted=True))
        for i in ids:
            session.add(PairsIndex(userid=i, pairid=pairid, pairhash=pairhash, accepted=False))
        return True


def acceptpair(userid: int, *, pairhash: Optional[str] = None, pairid: Optional[int] = None):
    with SessionContext(session=None) as session:
        pair: Optional[Pairs] = None
        if pairhash is not None:
            pair = session.query(Pairs).filter_by(pairhash=pairhash).one_or_none()
        elif pairid is not None:
            pair = session.query(Pairs).get(pairid)
        if pair is None:
            raise Exception(f'Pair not Found {userid=}, {pairhash=}, {pairid=}')
        pair.waitingnum -= 1  # type: ignore
        pairindex = session.query(PairsIndex).filter_by(userid=userid, pairid=pair.id).one()
        pairindex.accepted = True
        return True


def mypairs(userid: int, session=None):
    with SessionContext(session=session) as session:
        pair_list: List[PairsIndex] = session.query(PairsIndex).filter_by(userid=userid).all()
        return [p.get_dict(delete=['id', 'userid', 'pairid']) for p in pair_list]


def getPairData(pairhash: str, session=None):
    with SessionContext(session=session) as session:
        data: Pairs = session.query(Pairs).filter_by(pairhash=pairhash).one_or_none()
        if data is None:
            raise Exception(f'{pairhash=} not found')
        return data.get_dict()


def pairisvalid(userid: int, *ids: int):
    with SessionContext(session=None) as session:
        pair: Pairs = session.query(Pairs).filter_by(pairhash=generatePairHash(userid, *ids)).one_or_none()
        if pair is None:
            return False
        return pair.waitingnum == 0


def getpairlist(pairhash: str, session=None):
    with SessionContext(session=session) as session:
        return [backapp.userid2token(pid, session) for pid in decodePairHash(pairhash)]


def pairhash2dbid(pairhash: str, session=None):
    with SessionContext(session=session) as session:
        data: Pairs = session.query(Pairs).filter_by(pairhash=pairhash).one_or_none()
        if data is None:
            raise Exception(f'{pairhash=} not found')
        return int(data.id)  # type: ignore
