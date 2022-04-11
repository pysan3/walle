<template>
  <div>
    <ion-header>
      <ion-toolbar>
        {{ $t('Utils.pairselect') }}
      </ion-toolbar>
    </ion-header>
    <ion-content>
      <ion-list>
        <ion-item v-for="(pvalue, pairhash, index) in pairList" :key="index">
          <ion-label>
            <h2>
              {{
                pvalue.name
                  .replace($store.getters.getMyUserInfo.username, '')
                  .trim()
                  .replace(' ', ',')
              }}
            </h2>
            <div class="d-flex">
              <ion-avatar
                v-for="(user, uidx) in pvalue.userhashes
                  .filter(uh => uh !== $store.getters.getMyUserInfo.usertoken)
                  .map(uh => pvalue.userinfos[uh])"
                :key="uidx"
              >
                <img :src="`${user.icon}`" :alt="`${user.username}`" />
              </ion-avatar>
            </div>
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
    };
  },
  methods: {},
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
    console.log(this.pairList);
  },
};
</script>
