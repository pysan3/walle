import responder
from protobuf.protowrap import *  # noqa
from utils.responderd import Request, Response
from rich import print
from rich.traceback import install

from app import backapp, backpair, backpays
from app.login_manager import LMUsers, lm, lm_user_loader

install(show_locals=True)

api = responder.API(
    static_dir='./dist',
    static_route='/',
    templates_dir='./dist',
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
        userid = backapp.usertoken2id(token)
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
@proto_wrap(REQasignpair, RESPsuccess)
async def requestpair(_req: Request, _resp: Response, *, preq: REQasignpair, presp: RESPsuccess):
    backpair.addnewpair(lm.current_member.id_int, backapp.usertoken2id(preq.usertoken))
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
        return
    # presp.userhashes.extend(backpair.getpairlist(preq.pairhash))
    data = backpair.getPairData(preq.pairhash)
    data['userhashes'] = backpair.getpairlist(preq.pairhash)
    presp.MergeFrom(json_format.ParseDict(data, RESPpairinfo(), ignore_unknown_fields=True))


@api.route('/api/addpayment')
@proto_wrap(REQaddpayment, RESPtoken)
async def addpayment(_req: Request, _resp: Response, *, preq: REQaddpayment, presp: RESPtoken):
    paydata = preq.payment
    if not backpair.validPairAccess(lm.current_member.id_int, paydata.pairhash):
        return
    presp.token = backpays.addpayment(
        paydata.pairhash,
        lm.current_member.id_int,
        backapp.usertoken2id(paydata.payorhash),
        paydata.payment,
        paydata.description,
    )
    presp.success = True


@api.route('/api/getpaymentlist')
@proto_wrap(REQpairinfo, RESPgetpaymentlist)
async def getpaymentlist(_req: Request, _resp: Response, *, preq: REQpairinfo, presp: RESPgetpaymentlist):
    if not backpair.validPairAccess(lm.current_member.id_int, preq.pairhash):
        return
    presp.payhashlist.extend(backpays.getPaysList(pairhash=preq.pairhash))


@api.route('/api/getpayinfo')
@proto_wrap(REQpayinfo, RESPgetpayinfo)
async def getpayinfo(_req: Request, _resp: Response, *, preq: REQpayinfo, presp: RESPgetpayinfo):
    data = backpays.getPayInfo(hashing=True, payhash=preq.payhash)
    data['createdAt'] = data.pop('created_at')
    presp.payinfo.MergeFrom(json_format.ParseDict(data, PBRESPPayment(), ignore_unknown_fields=True))

if __name__ == '__main__':
    api.run()
