import { createStore } from 'vuex';

const sessionManager = {
  sessiontoken: undefined,
  expiresAt: -1,
  refresher: undefined,
};

const state = {
  isLoggedIn: false,
  sessionManager,
  sessionReload: false,
  menuController: undefined,
  currentPairHash: localStorage.getItem('WALLE_CURRENTPAIRHASH'),
  myUserInfo: {
    userhash: undefined,
    userName: undefined,
  },
  userInfos: {},
  // - username: str
  // - email: str
  pairDatas: {},
  // - userhashes: List[userhash]
  // - payments: List[payhash]
  // - pfrom: int
  // - duration: int
  payDatas: {},
  // - payment: int
  // - payorhash: userhash
  // - creatorhash: userhash
  // - description: str
  // - createdAt: Data Object
  // - pairhash: pairhash
};

String.prototype.capitalize = function () {
  return this.charAt(0).toUpperCase() + this.slice(1);
};

const gettersDefault = Object.fromEntries(
  Object.keys(state).map((key) => [`get${key.capitalize()}`, (state) => state[key]]),
);
const getters = Object.assign(gettersDefault, {});

const mutationsDefault = Object.fromEntries(
  Object.keys(state).map((key) => [
    `set${key.capitalize()}`,
    (state, value) => {
      state[key] = value;
    },
  ]),
);
const mutations = Object.assign(mutationsDefault, {
  setSessionManager(state, sessionManager) {
    if (state.sessionManager.refresher !== undefined) {
      clearTimeout(state.sessionManager.refresher);
    }
    state.sessionManager = sessionManager;
  },
  setUserInfo(state, data) {
    state.userInfos[data.userhash] = data.value;
  },
  setPairData(state, data) {
    state.pairDatas[data.pairhash] = data;
  },
  removePairData(state, data) {
    state.pairDatas[data.pairhash] = undefined;
  },
  setPayData(state, data) {
    state.payDatas[data.payhash] = data;
  },
  removePayData(state, data) {
    state.payDatas[data.payhash] = undefined;
  },
  setCurrentPairHash(state, data) {
    state.currentPairHash = data;
    localStorage.setItem('WALLE_CURRENTPAIRHASH', data);
  },
});

const actions = {};

export default createStore({
  state,
  getters,
  mutations,
  actions,
});
