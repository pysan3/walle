import Axios from 'axios';
import store from '@/store';

const axiosConfig = {
  baseURL: process.env.VUE_APP_PUBLICPATH,
  timeout: 300000,
};

const axios = Axios.create(axiosConfig);
axios.interceptors.request.use(
  request => {
    const sessiontoken = store.getters.getSessionToken;
    if (sessiontoken !== undefined) {
      request.headers.sessiontoken = sessiontoken;
    }
    return request;
  },
  err => Promise.reject(err)
);
axios.interceptors.response.use(
  response => {
    const sessiontoken = response.headers.setsessiontoken;
    if (sessiontoken !== undefined) {
      const expiresAt = response.headers.expiresat;
      const timeleft = expiresAt * 1000 - Date.now();
      if (timeleft > 0) {
        const refresher = setTimeout(() => {
          store.commit('setSessionReload', true);
        }, timeleft);
        store.commit('setSessionManager', {
          sessiontoken,
          expiresAt,
          refresher,
        });
      }
    }
    return response;
  },
  err => Promise.reject(err)
);

export default axios;
