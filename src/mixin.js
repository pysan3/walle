import { menuController } from '@ionic/vue';
import * as allIcons from 'ionicons/icons';
import store from '@/store';
import Axios from '@/axios';

export default {
  data() {
    return {
      ionicons: allIcons,
    };
  },
  methods: {
    $_fillUserInfo() {
      return Axios.post('/api/getmyuserinfo', {}).then(response => {
        store.commit('setMyUserInfo', response.data);
      });
    },
    $_timeInLanguage(time, format) {
      const date = new Date(time);
      const lpad = a => `00${a}`.slice(-2);
      const correspond = {
        '%Y': date.getFullYear(),
        '%m': date.getMonth() + 1,
        '%d': date.getDate(),
        '%H': lpad(date.getHours()),
        '%M': lpad(date.getMinutes()),
        '%S': lpad(date.getSeconds()),
      };
      return Object.entries(correspond).reduce((c, [k, v]) => c.replaceAll(k, v), format);
    },
    $_checkIsLoggedin() {
      if (store.getters.getIsLoggedIn) return true;
      return Axios.post('/api/loggedin', {})
        .then(response => {
          if (response.data.success) {
            store.commit('setIsLoggedIn', true);
            return true;
          }
          return false;
        })
        .catch(error => {
          if (process.env.NODE_ENV !== 'production') alert(error);
          return false;
        });
    },
    $i(iconname) {
      return this.ionicons[this.$_kebab2camel(iconname)];
    },
    $c(n) {
      return n.toLocaleString('en-US');
    },
    $_pname(name) {
      return (name || '')
        .replace(store.getters.getMyUserInfo.username, '')
        .trim()
        .replace(' ', ',');
    },
    async $_controlMenu(menuname, status) {
      switch (status) {
        case 'open':
          menuController.open(menuname);
          break;
        case 'close':
          menuController.close(menuname);
          break;
        default:
          menuController.toggle(menuname);
          break;
      }
    },
    $_getUserInfo(userhash) {
      if (!userhash) return undefined;
      if (store.getters.getMyUserInfo.usertoken === userhash) {
        console.debug(`$_getUserInfo called to getMyUserInfo: ${userhash}`);
        return store.getters.getMyUserInfo;
      }
      const info = store.getters.getUserInfos[userhash];
      if (info) return info;
      return Axios.post('/api/getuserinfo', { usertoken: userhash })
        .then(response => {
          if (response.data) {
            store.commit('setUserInfo', {
              userhash,
              value: response.data,
            });
            return response.data;
          }
          return undefined;
        })
        .catch(() => {
          console.error(`Error while $_getUserInfo: ${userhash}, ${info}`);
          return undefined;
        });
    },
    async $_fetchPairDataPeriod(pairhash, from, duration) {
      if (!pairhash) return undefined;
      const data = store.getters.getPairDatas[pairhash];
      if (data) return data;
      const respdata = {
        ...(await Axios.post('/api/pairinfo', { pairhash })
          .then(r => r.data)
          .catch(() => ({}))),
        ...{
          pairhash,
          payments: await Axios.post('/api/getpaymentsinperiod', { pairhash, from, duration })
            .then(r => r.data.payhashlist)
            .catch(() => []),
        },
      };
      store.commit('setPairData', respdata);
      return respdata;
    },
    $_fetchPairData(pairhash) {
      return this.$_fetchPairData(pairhash, 0, -1);
    },
    async $_fetchPayData(payhash) {
      if (!payhash) return undefined;
      const data = store.getters.getPayDatas[payhash];
      if (data) return data;
      return Axios.post('/api/getpayinfo', { payhash })
        .then(response => {
          const respdata = {
            ...response.data,
            ...{
              payhash,
              createdAt: new Date(response.data.created_at),
            },
          };
          store.commit('setPayData', respdata);
          return respdata;
        })
        .catch(() => {
          console.error(`Error while $_fetchPayData: ${payhash}, ${data}`);
          return undefined;
        });
    },
    async $_completePairData(pairhash) {
      if (!pairhash) return {};
      const data = await this.$_fetchPairData(pairhash);
      data.userinfos = Object.fromEntries(
        await Promise.all(data.userhashes.map(async uh => [uh, await this.$_getUserInfo(uh)]))
      );
      data.payinfos = Object.fromEntries(
        await Promise.all(data.payments.map(async ph => [ph, await this.$_fetchPayData(ph)]))
      );
      return data;
    },
    $_camel2kebab(s) {
      return s.replace(/([^A-Z])([A-Z])/g, '$1-$2').toLowerCase();
    },
    $_kebab2camel(s) {
      return s.replace(/-./g, x => x[1].toUpperCase());
    },
  },
};
