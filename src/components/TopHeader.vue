<template>
  <div id="topheader">
    <ion-header>
      <ion-toolbar color="dark">
        <ion-buttons slot="start">
          <ion-button @click="$_controlMenu('topmenu')">
            <ion-icon :src="$i('menu-outline')"></ion-icon>
          </ion-button>
          <ion-button size="large">
            <h4>{{ $t(`Top.${currentTab}`) }}</h4>
          </ion-button>
        </ion-buttons>
        <ion-buttons slot="end">
          <ion-button @click="openNotification()">
            <ion-icon :src="$i('notifications-outline')"></ion-icon>
          </ion-button>
          <ion-chip outline color="light" @click="openPairSelector()">
            <ion-label>Takuto</ion-label>
            <ion-avatar>
              <img src="@/assets/profile.jpg" alt="Prof" class="border border-light" />
            </ion-avatar>
          </ion-chip>
        </ion-buttons>
      </ion-toolbar>
    </ion-header>
  </div>
</template>

<script>
import { popoverController } from '@ionic/vue';
import Notifications from '@/components/Notifications.vue';
import PairSelect from '@/components/PairSelect.vue';

export default {
  props: ['currentTab'],
  methods: {
    async openNotification(ev) {
      const popover = await popoverController.create({
        component: Notifications,
        event: ev,
        translucent: true,
      });
      return popover.present();
    },
    async openPairSelector(ev) {
      const popover = await popoverController.create({
        component: PairSelect,
        event: ev,
        translucent: true,
      });
      return popover.present();
    },
  },
};
</script>
