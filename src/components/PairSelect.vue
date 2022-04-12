<template>
  <div>
    <ion-header>
      <ion-toolbar class="mx-auto">
        {{ $t('Utils.pairselect') }}
      </ion-toolbar>
    </ion-header>
    <ion-content>
      <ion-list>
        <ion-item v-for="(pvalue, pairhash, index) in pairList" :key="index" @click="choosePair(pairhash)">
          <ion-label>
            <h2>w/ {{ $_pname(pvalue.name) }}</h2>
            <div class="d-flex">
              <ion-item>
                <ion-avatar
                  v-for="(user, uidx) in pvalue.userhashes
                    .filter(uh => uh !== $store.getters.getMyUserInfo.usertoken)
                    .map(uh => pvalue.userinfos[uh])"
                  :key="uidx"
                >
                  <img :src="`${user.icon}`" :alt="`${user.username}`" />
                </ion-avatar>
              </ion-item>
            </div>
            <ion-row responsive-sm class="my-0" v-show="!pvalue.accepted">
              <ion-col>
                <ion-button @click="acceptPair(pairhash)" expand="block">Accept</ion-button>
              </ion-col>
              <ion-col>
                <ion-button @click="declinePair(pairhash)" color="light" expand="block">Decline</ion-button>
              </ion-col>
            </ion-row>
          </ion-label>
        </ion-item>
      </ion-list>
    </ion-content>
  </div>
</template>

<script>
import Axios from '@/axios';

export default {
  data() {
    return {
      pairList: {},
      connecting: false,
    };
  },
  methods: {
    choosePair(pairhash) {
      if (this.connecting) return;
      this.$store.commit('setCurrentPairHash', pairhash);
      window.location.reload(false);
    },
    acceptPair(pairhash) {
      this.connecting = true;
      Axios.post('/api/acceptpair', { pairhash }).then(response => {
        if (response.data.success) {
          this.pairList[pairhash].accepted = true;
        }
        this.connecting = false;
      });
    },
    declinePair(pairhash) {
      console.error('Not Implemented');
    },
  },
  async created() {
    this.pairList = await Axios.post('/api/mypairs', {}).then(async r =>
      Object.fromEntries(
        await Promise.all(
          r.data.pairs.map(async pidx => [
            pidx.pairhash,
            { ...(await this.$_completePairData(pidx.pairhash)), ...pidx },
          ])
        )
      )
    );
  },
};
</script>
