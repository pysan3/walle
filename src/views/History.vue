<template>
  <ion-page>
    <ion-content>
      <ion-header>
        <ion-toolbar>
          <ion-searchbar
            inputmode="search"
            showCancelButton="focus"
            type="text"
            @ionInput="search"
            class="pt-3"
          ></ion-searchbar>
          <p class="mx-1 my-0">Sort v</p>
        </ion-toolbar>
      </ion-header>
      <ion-list>
        <ion-item v-for="(p, payindex) in payList.slice().reverse()" :key="payindex">
          <ion-label>
            <div class="d-flex align-items-baseline">
              <ion-chip outline class="mr-auto">
                <ion-avatar>
                  <img
                    :src="`${pairData.userinfos[p.payinfo.payorhash].icon}`"
                    :alt="`${pairData.userinfos[p.payinfo.payorhash].username.slice(0, 1).toUpperCase()}`"
                    class="border border-light"
                  />
                </ion-avatar>
                <ion-label>{{ pairData.userinfos[p.payinfo.payorhash].username }}</ion-label>
              </ion-chip>
              <h4 class="mx-1">
                <ion-icon :src="$i('cloud-upload-outline')"></ion-icon>
                {{ pairData.userinfos[p.payinfo.creatorhash].username }}
              </h4>
              <h4 class="mx-1">
                <ion-icon :src="$i('calendar-number-outline')"></ion-icon>
                {{ $_timeInLanguage(p.payinfo.createdAt, $t('Utils.spelltime')) }}
              </h4>
            </div>
            <div class="d-flex align-items-baseline">
              <h1 class="mx-2" style="min-width: 120px">
                <ion-icon :src="$i('logo-yen')"></ion-icon> {{ $c(p.payinfo.payment) }}
              </h1>
              <p>{{ p.payinfo.description }}</p>
            </div>
          </ion-label>
        </ion-item>
      </ion-list>
    </ion-content>
  </ion-page>
</template>

<script lang="js">
export default {
  name: 'history',
  data() {
    return {
      pairData: {}
    };
  },
  computed: {
    payList() {
      return (this.pairData.payments || []).map(e => this.pairData.payinfos[e])
    }
  },
  methods: {
    search(ev) {
      if (!ev) return;
      const query = ev.target.value;
      if (query && query !== '') {
        console.log(`Searching for '${query}'.`);
      }
    },
  },
  async created() {
    this.pairData = await this.$_completePairData(this.$store.getters.getCurrentPairHash)
  }
};
</script>
