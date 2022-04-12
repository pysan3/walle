from typing import Tuple
from app.db_connector import *  # noqa
from app.sqlalchemy_h import SessionContext
from app import backpair, backapp
from app.hashids import payHM


def generatePaymentHash(payid: int, creator: int, payor: int) -> str:
    return payHM.encode(payid, creator, payor)


def decodePaymentHash(payhash: str) -> Tuple[int, int, int]:
    data = payHM.decode(payhash)
    if len(data) != 3:
        raise Exception(f'Payment Hash decode error: {payhash}')
    return data


def addpayment(pairhash: str, userid: int, payor: int, payment: int, description: str = ''):
    with SessionContext() as session:
        new = Payments(
            pairid=backpair.pairhash2dbid(pairhash, session),
            payment=payment,
            payor=payor,
            creator=userid,
            description=description,
            created_at=created_at(),
        )
        session.add(new)
        session.flush()
        return generatePaymentHash(int(new.id), userid, payor)  # type: ignore


def getPaysList(*, pairhash: Optional[str] = None, pairid: Optional[int] = None):
    if pairhash is None and pairid is None:
        raise Exception(f'{pairhash=} or {pairid=} must be non-none value')
    with SessionContext() as session:
        if pairhash is not None:
            pairid = backpair.pairhash2dbid(pairhash, session)
        data = session.query(Payments).filter_by(pairid=pairid).all()
        return [generatePaymentHash(p.id, p.creator, p.payor) for p in data]


def getPayInfo(hashing: bool = False, *, payid: Optional[int] = None, payhash: Optional[str] = None):
    if payhash is None and payid is None:
        raise Exception(f'{payhash=} or {payid=} must be non-none value')
    with SessionContext() as session:
        if payhash is not None:
            payid = decodePaymentHash(payhash)[0]
        data: Optional[Payments] = session.query(Payments).get(payid)
        if data is None:
            raise Exception(f'Payment data not found: {payid=}, {payhash=}')
        datadict = data.get_dict()
        if hashing:
            datadict['payorhash'] = backapp.userid2token(datadict.pop('payor'))
            datadict['creatorhash'] = backapp.userid2token(datadict.pop('creator'))
            datadict['pairhash'] = session.query(Pairs).get(datadict.pop('pairid')).pairhash
        return datadict
