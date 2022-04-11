<template>
  <ion-page>
    <ion-tabs>
      <TopHeader :currentTab="$route.name" />
      <ion-tab-bar slot="bottom">
        <ion-tab-button tab="history" href="/history">
          <ion-icon :src="$i('people-outline')"></ion-icon>
          <ion-label>{{ $t('Top.history') }}</ion-label>
        </ion-tab-button>
        <ion-tab-button tab="monthly" href="/monthly">
          <ion-icon :src="$i('calendar-outline')"></ion-icon>
          <ion-label>{{ $t('Top.monthly') }}</ion-label>
        </ion-tab-button>
        <ion-tab-button tab="stats" href="/stats">
          <ion-icon :src="$i('stats-chart')"></ion-icon>
          <ion-label>{{ $t('Top.stats') }}</ion-label>
        </ion-tab-button>
      </ion-tab-bar>
    </ion-tabs>
    <ion-fab vertical="bottom" horizontal="end" slot="fixed" class="fab-btn">
      <ion-fab-button>
        <ion-icon :src="$i('add')"></ion-icon>
      </ion-fab-button>
      <ion-fab-list side="start">
        <ion-fab-button color="light">
          <ion-icon :src="$i('create-outline')"></ion-icon>
        </ion-fab-button>
      </ion-fab-list>
    </ion-fab>
  </ion-page>
</template>

<script>
import { IonIcon, IonLabel, IonPage, IonTabBar, IonTabButton, IonTabs } from '@ionic/vue';
import TopHeader from '@/components/TopHeader';

export default {
  components: {
    IonIcon,
    IonLabel,
    IonPage,
    IonTabBar,
    IonTabButton,
    IonTabs,
    TopHeader,
  },
  created() {
    console.log(this.$route.name);
  },
};
</script>

<style lang="stylus" scoped>
.fab-btn
  margin-bottom 100px
</style>
