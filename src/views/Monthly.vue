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
        </ion-toolbar>
      </ion-header>
      <ion-row class="mt-2">
        <ion-col size="6" no-padding>
          <WorkbookCard />
        </ion-col>
        <ion-col size="6" no-padding>
          <WorkbookCard />
        </ion-col>
        <ion-col size="6" no-padding>
          <WorkbookCard />
        </ion-col>
      </ion-row>
    </ion-content>
  </ion-page>
</template>

<script lang="js">
import WorkbookCard from '@/components/WorkbookCard.vue';

export default {
  name: 'monthly',
  components: {
    WorkbookCard,
  },
  data() {
    return {
      pairData: {}
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
  async computed() {
    this.pairData = await this.$_completePairData(this.$store.getters.getCurrentPairHash)
  }
};
</script>
