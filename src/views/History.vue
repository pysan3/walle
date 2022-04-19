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
        <ion-item
          v-for="(p, idx) in payList"
          :key="idx"
          style="cursor: pointer;"
          @click="$router.push(`/update/${p.payhash}`)"
        >
          <ion-label>
            <div class="d-flex align-items-baseline">
              <ion-chip outline class="mr-auto">
                <ion-avatar>
                  <img
                    :src="`${pairData.userinfos[p.payorhash].icon}`"
                    :alt="`${pairData.userinfos[p.payorhash].username.slice(0, 1).toUpperCase()}`"
                    class="border border-light"
                  />
                </ion-avatar>
                <ion-label>{{ pairData.userinfos[p.payorhash].username }}</ion-label>
              </ion-chip>
              <h4 class="mx-1">
                <ion-icon :src="$i('cloud-upload-outline')"></ion-icon>
                {{ pairData.userinfos[p.creatorhash].username }}
              </h4>
              <h4 class="mx-1">
                <ion-icon :src="$i('calendar-number-outline')"></ion-icon>
                {{ $_timeInLanguage(p.createdAt, $t('Utils.spelltime')) }}
              </h4>
            </div>
            <div class="d-flex align-items-baseline">
              <h1 class="mx-2" style="min-width: 120px">
                <ion-icon :src="$i('logo-yen')"></ion-icon> {{ $c(p.payment) }}
              </h1>
              <p>{{ p.description }}</p>
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
      pairData: {},
    };
  },
  computed: {
    payList() {
      return Object.values(this.pairData.payinfos || []).sort((a, b) => a.createdAt < b.createdAt);
    },
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
    this.pairData = await this.$_completePairData(this.$store.getters.getCurrentPairHash);
  },
};
</script>
