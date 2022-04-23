from typing import Tuple
import sys
import uuid
import base64
from app.db_connector import *  # noqa
from app.sqlalchemy_h import SessionContext
from app import backpair, backapp
from app.hashids import payHM
from utils.photoUtils import compressJPG, compressPNG
from utils.staticFiles import staticRef, staticBaseDir

payPhotoDir = backapp.staticFileDir / 'payphotos'
payPhotoDir.mkdir(parents=True, exist_ok=True)


class DateInInt:
    def __init__(self, dateint: int) -> None:
        self.year = dateint // 100
        self.month = dateint % 100

    def __add__(self, duration: int):
        return DateInInt.from_yearmonth(
            self.year + (self.month + duration - 1) // 12,
            (self.month + duration - 1) % 12 + 1
        )

    def __int__(self):
        return self.year * 100 + self.month

    @classmethod
    def from_yearmonth(cls, year: int, month: int):
        return cls(year * 100 + month)


def generatePaymentHash(payid: int, creator: int, payor: int) -> str:
    return payHM.encode(payid, creator, payor)


def decodePaymentHash(payhash: str) -> Tuple[int, int, int]:
    data = payHM.decode(payhash)
    if len(data) != 3:
        raise Exception(f'Payment Hash decode error: {payhash}')
    return data


def addpayment(pairhash: str, userid: int, payor: int, payment: int, description: str = '', createdAt: str = ''):
    try:
        created_dt = datetime.datetime.fromisoformat(createdAt).replace(tzinfo=None)
    except ValueError:
        print(f'Invalid date format for {createdAt=}. ', file=sys.stderr)
        created_dt = datetime.datetime.now()
    if payment == 0:
        return None
    with SessionContext() as session:
        new = Payments(
            pairid=backpair.pairhash2dbid(pairhash, session),
            payment=payment,
            payor=payor,
            creator=userid,
            description=description,
            createdIn=int(DateInInt.from_yearmonth(created_dt.year, created_dt.month)),
            created_at=created_at(created_dt - datetime.datetime.now()),
        )
        session.add(new)
        session.flush()
        return generatePaymentHash(int(new.id), userid, payor)  # type: ignore


def updatepayment(
        payhash: str,
        pairhash: str,
        userid: int,
        payor: int,
        payment: int,
        description: str = '',
        createdAt: str = ''):
    try:
        payid, creator, payor = decodePaymentHash(payhash)
    except Exception as e:
        print(f'updatepayment: payhash invalid {payhash=}, errmsg: {e}', file=sys.stderr)
        return False, 'Invalid payhash'
    try:
        created_dt = datetime.datetime.fromisoformat(createdAt.replace('Z', '+00:00')).replace(tzinfo=None)
    except ValueError:
        print(f'Invalid date format for {createdAt=}.', file=sys.stderr)
        created_dt = datetime.datetime.now()
    if payment == 0:
        return False, f'Payment should be > 0. Payment sent: {payment}'
    with SessionContext() as session:
        data = session.query(Payments).get(payid)
        if data is None:
            return False, f'Data corresponding to {payhash=} not found.'
        updatable = userid in [data.payor, data.creator]
        if payment != data.payment and not updatable:
            return False, 'User does not have permission to change `payment`'
        if payor != data.payor and not updatable:
            return False, 'User does not have permission to change `payor`'
        prev_created_dt = datetime.datetime.fromisoformat(data.created_at).replace(tzinfo=None)
        if created_dt.date() != prev_created_dt.date() and not updatable:
            return False, 'User does not have permission to change `created datetime`'
        data.payment = payment
        data.payor = payor
        data.description = description
        data.createdIn = int(DateInInt.from_yearmonth(created_dt.year, created_dt.month))
        data.created_at = created_at(created_dt - datetime.datetime.now())
        return True, ''


def getPaysInPeriod(pfrom: int = 0, duration: int = 0, *, pairhash: Optional[str] = None, pairid: Optional[int] = None):
    if pairhash is None and pairid is None:
        raise Exception(f'{pairhash=} or {pairid=} must be non-none value')
    with SessionContext() as session:
        if pairhash is not None:
            pairid = backpair.pairhash2dbid(pairhash, session)
        query = session.query(Payments).filter_by(pairid=pairid)
        if duration > 0 and pfrom >= 0:
            fromint = DateInInt(pfrom)
            toint = fromint + duration
            query = query.filter(int(fromint) <= Payments.createdIn, Payments.createdIn < int(toint))
        data = query.all()
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


def getPayPhotos(*, payid: Optional[int] = None, payhash: Optional[str] = None):
    if payhash is None and payid is None:
        raise Exception(f'{payhash=} or {payid=} must be non-none value')
    with SessionContext() as session:
        if payhash is not None:
            payid = decodePaymentHash(payhash)[0]
        return [p.photopath for p in session.query(PaymentPhotos).filter_by(payid=payid).all()]


def uploadPayPhoto(data64: str, format: str = 'jpeg', *, payid: Optional[int] = None, payhash: Optional[str] = None):
    if payhash is None and payid is None:
        raise Exception(f'{payhash=} or {payid=} must be non-none value')
    filepath = payPhotoDir / (str(uuid.uuid4()) + f'.{format}')
    data = base64.b64decode(data64)
    if format.lower() in ['jpg', 'jpeg']:
        data = compressJPG(data)
    elif format.lower() == 'png':
        data = compressPNG(data)
    with filepath.open('wb') as f:
        f.write(data)
    with SessionContext() as session:
        if payhash is not None:
            payid = decodePaymentHash(payhash)[0]
        session.add(PaymentPhotos(
            payid=payid,
            photopath=str(staticRef(filepath)),
        ))
        return str(filepath)


def deletePayPhoto(photopath: str):
    filepath = staticBaseDir / photopath
    if filepath.exists():
        filepath.unlink()
    else:
        return False
    with SessionContext() as session:
        data = session.query(PaymentPhotos).filter_by(photopath=str(staticRef(filepath))).one_or_none()
        if data is not None:
            session.delete(data)
        else:
            return False
    return True
