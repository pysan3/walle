<template>
  <div id="app">
    <ion-app>
      <ion-menu menu-id="topmenu" side="start" content-id="content">
        <TopMenu />
      </ion-menu>
      <router-view />
    </ion-app>
  </div>
</template>

<script lang="js">
import { IonApp, menuController } from '@ionic/vue';
import TopMenu from '@/components/TopMenu.vue';

export default {
  name: 'App',
  components: {
    IonApp,
    TopMenu,
  },
  created() {
    this.$store.state.menuController = menuController;
  },
};
</script>

<style lang="stylus">
body {
  width: 100%;
  height: 100%;
  background-color: aliceblue;
  * {
    overflow-y: visible;
  }
}
html {
  @extend body;
  overflow-y: scroll;
}
</style>
