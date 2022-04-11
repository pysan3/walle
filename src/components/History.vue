<template>
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
      <ion-item v-for="(payment, payindex) in payList" :key="payindex">
        <ion-label>
          <div class="d-flex">
            <h4 class="mx-1">O</h4>
            <h2 class="mx-1 mr-auto">{{ `${$t('Top.currency')} ${$c(payment.payment)}` }}</h2>
            <h4 class="mx-1">
              <ion-icon :src="$i('cloud-upload-outline')"></ion-icon>
              username
            </h4>
            <h4 class="mx-1">
              <ion-icon :src="$i('calendar-number-outline')"></ion-icon>
              1. Feb
            </h4>
          </div>
          <p>description</p>
        </ion-label>
      </ion-item>
    </ion-list>
  </ion-content>
</template>

<script lang="js">
export default {
  name: 'History',
  data() {
    return {
      payData: {}
    };
  },
  computed: {
    payList() {
      return this.payData.payments || []
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
    this.payData = await this.$_completePairData(this.$store.getters.getCurrentPairHash)
  }
};
</script>
