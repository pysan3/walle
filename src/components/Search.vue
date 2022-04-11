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
    <ion-list>
      <WorkbookCard />
      <WorkbookCard />
      <WorkbookCard />
      <WorkbookCard />
      <WorkbookCard />
      <WorkbookCard />
      <WorkbookCard />
      <WorkbookCard />
      <WorkbookCard />
      <WorkbookCard />
    </ion-list>
  </ion-content>
</template>

<script lang="js">
import WorkbookCard from '@/components/WorkbookCard.vue';

export default {
  name: 'Search',
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
