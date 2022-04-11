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
      <ion-item @click="console.log('clicked')">
        <ion-label>
          <div class="d-flex">
            <h2 class="mr-2">title</h2>
            <h4 class="mx-1 mr-auto">
              <ion-icon :src="$i('people-outline')"></ion-icon>
              11
            </h4>
            <h4 class="mx-1">
              <ion-icon :src="$i('cloud-upload-outline')"></ion-icon>
              user
            </h4>
            <h4 class="mx-1">
              <ion-icon :src="$i('calendar-number-outline')"></ion-icon>
              1. Feb
            </h4>
          </div>
          <p>description</p>
        </ion-label>
      </ion-item>
      <ion-item @click="console.log('clicked')">
        <ion-label>
          <div class="d-flex">
            <h2 class="mr-2">title</h2>
            <h4 class="mx-1 mr-auto">
              <ion-icon :src="$i('people-outline')"></ion-icon>
              11
            </h4>
            <h4 class="mx-1">
              <ion-icon :src="$i('cloud-upload-outline')"></ion-icon>
              user
            </h4>
            <h4 class="mx-1">
              <ion-icon :src="$i('calendar-number-outline')"></ion-icon>
              1. Feb
            </h4>
          </div>
          <p>description</p>
        </ion-label>
      </ion-item>
      <ion-item @click="console.log('clicked')">
        <ion-label>
          <div class="d-flex">
            <h2 class="mr-2">title</h2>
            <h4 class="mx-1 mr-auto">
              <ion-icon :src="$i('people-outline')"></ion-icon>
              11
            </h4>
            <h4 class="mx-1">
              <ion-icon :src="$i('cloud-upload-outline')"></ion-icon>
              user
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
  name: 'Class',
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
