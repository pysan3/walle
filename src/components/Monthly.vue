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
    <ion-fab vertical="bottom" horizontal="end" slot="fixed">
      <ion-fab-button>
        <ion-icon :src="$i('add')"></ion-icon>
      </ion-fab-button>
      <ion-fab-list side="start">
        <ion-fab-button color="light">
          <ion-icon :src="$i('pricetags-outline')"></ion-icon>
        </ion-fab-button>
        <ion-fab-button color="light">
          <ion-icon :src="$i('images-outline')"></ion-icon>
        </ion-fab-button>
        <ion-fab-button color="light">
          <ion-icon :src="$i('book-outline')"></ion-icon>
        </ion-fab-button>
      </ion-fab-list>
    </ion-fab>
  </ion-content>
</template>

<script lang="js">
import WorkbookCard from '@/components/WorkbookCard.vue';

export default {
  name: 'Home',
  components: {
    WorkbookCard,
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
};
</script>
