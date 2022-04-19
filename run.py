import responder
from protobuf.protowrap import *  # noqa
from utils.responderd import Request, Response
from rich import print
from rich.traceback import install

from app import backapp, backpair, backpays
from app.login_manager import LMUsers, lm, lm_user_loader

install(show_locals=True)

api = responder.API(
    static_route='/',
    templates_dir='static',
)
api.add_route('/', static=True)

lm.init_api(api)
lm_user_loader = lm.user_loader(lm_user_loader)


@api.route('/api/login')
@proto_wrap(REQlogin, RESPtoken)
async def login(_req: Request, resp: Response, *, preq: REQlogin, presp: RESPtoken):
    token = backapp.login(preq.username, preq.password)
    presp.success = token is not None
    if token is not None:
        presp.token = token
        userid = backapp.searchTokenTable(token)
        print(f'api login {userid=}')
        lm.login_user(LMUsers(user_or_userid=userid))
        resp.headers.update(backapp.returnwebsessiontoken(userid))


@api.route('/api/loggedin')
@proto_wrap(REQnone, RESPsuccess)
async def loggedin(_req: Request, _resp: Response, *, preq: REQnone, presp: RESPsuccess):
    if lm.current_user.is_authenticated:
        lm.login_user(lm.current_user)
    presp.success = lm.current_user.is_authenticated


# @api.route('/api/signup')
# @proto_wrap(REQsignup, RESPtoken)
# async def signup(_req: Request, resp: Response, *, preq: REQsignup, presp: RESPtoken):
#     # TODO: validate email
#     token = backapp.signup(preq.username, preq.password, preq.email)
#     if token is not None:
#         presp.token = token
#         userid: int = backapp.userid_from_token(token)  # type: ignore
#         lm.login_user(LMUsers(user_or_userid=userid))
#         resp.headers.update(backapp.returnwebsessiontoken(userid))

@api.route('/api/getmytoken')
@lm.login_required
@proto_wrap(REQnone, RESPtoken)
async def getmytoken(_req: Request, _resp: Response, *, preq: REQnone, presp: RESPtoken):
    presp.success = True
    presp.token = backapp.userid2token(lm.current_member.id_int)


@api.route('/api/getmyuserinfo')
@lm.login_required
@proto_wrap(REQnone, PBUserData)
async def getmyuserinfo(_req: Request, _resp: Response, *, preq: REQnone, presp: PBUserData):
    data = backapp.getUserData(lm.current_member.id_int)
    data['createdAt'] = data.pop('created_at')
    presp.MergeFrom(json_format.ParseDict(data, PBUserData(), ignore_unknown_fields=True))


@api.route('/api/getuserinfo')
@proto_wrap(REQasignpair, PBUserData)
async def getuserinfo(_req: Request, _resp: Response, *, preq: REQasignpair, presp: PBUserData):
    print(f'{preq=}')
    data = backapp.getUserData(backapp.usertoken2id(preq.usertoken))
    data['createdAt'] = data.pop('created_at')
    data.pop('email', None)
    presp.MergeFrom(json_format.ParseDict(data, PBUserData(), ignore_unknown_fields=True))


@api.route('/api/requestpair')
@lm.login_required
@proto_wrap(REQrequestpair, RESPsuccess)
async def requestpair(_req: Request, _resp: Response, *, preq: REQrequestpair, presp: RESPsuccess):
    presp.success = backpair.addnewpair(
        lm.current_member.id_int,
        *[backapp.usertoken2id(token) for token in preq.usertokens]
    )


@api.route('/api/acceptpair')
@proto_wrap(REQpairinfo, RESPsuccess)
async def acceptpair(_req: Request, _resp: Response, *, preq: REQpairinfo, presp: RESPsuccess):
    if not backpair.validPairAccess(lm.current_member.id_int, preq.pairhash):
        print(f'acceptpair: {lm.current_member.id_int=}, {preq.pairhash} not valid')
        return
    backpair.acceptpair(lm.current_member.id_int, pairhash=preq.pairhash)
    presp.success = True


@api.route('/api/mypairs')
@lm.login_required
@proto_wrap(REQnone, RESPmypairs)
async def mypairs(_req: Request, _resp: Response, *, preq: REQnone, presp: RESPmypairs):
    pairs = backpair.mypairs(lm.current_member.id_int)
    presp.pairs.extend([PBPairsIndex(**p) for p in pairs])


@api.route('/api/pairinfo')
@proto_wrap(REQpairinfo, RESPpairinfo)
async def pairinfo(_req: Request, _resp: Response, *, preq: REQpairinfo, presp: RESPpairinfo):
    if not backpair.validPairAccess(lm.current_member.id_int, preq.pairhash):
        print(f'pairinfo: {lm.current_member.id_int=}, {preq.pairhash} not valid')
        return
    # presp.userhashes.extend(backpair.getpairlist(preq.pairhash))
    data = backpair.getPairData(preq.pairhash)
    data['userhashes'] = backpair.getpairlist(preq.pairhash)
    presp.MergeFrom(json_format.ParseDict(data, RESPpairinfo(), ignore_unknown_fields=True))


@api.route('/api/newpayment')
@proto_wrap(PBREQPayment, RESPtoken)
async def newpayment(_req: Request, _resp: Response, *, preq: PBREQPayment, presp: RESPtoken):
    if not backpair.validPairAccess(lm.current_member.id_int, preq.pairhash):
        print(f'newpayment: {lm.current_member.id_int=}, {preq.pairhash} not valid')
        return
    token = backpays.addpayment(
        preq.pairhash,
        lm.current_member.id_int,
        backapp.usertoken2id(preq.payorhash),
        preq.payment,
        preq.description,
        preq.createdAt,
    )
    presp.success = bool(token)
    if token is not None:
        presp.token = token


@api.route('/api/updatepayment')
@proto_wrap(PBREQPayment, RESPsuccess)
async def updatepayment(_req: Request, _resp: Response, *, preq: PBREQPayment, presp: RESPsuccess):
    if not backpair.validPairAccess(lm.current_member.id_int, preq.pairhash):
        print(f'updatepayment: {lm.current_member.id_int=}, {preq.pairhash} not valid')
        return
    success, msg = backpays.updatepayment(
        preq.payhash,
        preq.pairhash,
        lm.current_member.id_int,
        backapp.usertoken2id(preq.payorhash),
        preq.payment,
        preq.description,
        preq.createdAt,
    )
    presp.success = success
    presp.msg = msg


@api.route('/api/getpaymentsinperiod')
@proto_wrap(REQpairinfo, RESPgetpaymentlist)
async def getpaymentsinperiod(_req: Request, _resp: Response, *, preq: REQpairinfo, presp: RESPgetpaymentlist):
    if not backpair.validPairAccess(lm.current_member.id_int, preq.pairhash):
        print(f'getpaymentlist: {lm.current_member.id_int=}, {preq.pairhash} not valid')
        return
    presp.payhashlist.extend(backpays.getPaysInPeriod(preq.pfrom, preq.duration, pairhash=preq.pairhash))


@api.route('/api/getpayinfo')
@proto_wrap(REQpayinfo, RESPgetpayinfo)
async def getpayinfo(_req: Request, _resp: Response, *, preq: REQpayinfo, presp: RESPgetpayinfo):
    data = backpays.getPayInfo(hashing=True, payhash=preq.payhash)
    data['createdAt'] = data.pop('created_at')
    presp.payinfo.MergeFrom(json_format.ParseDict(data, PBRESPPayment(), ignore_unknown_fields=True))

if __name__ == '__main__':
    api.run(port=5042, address='0.0.0.0')
