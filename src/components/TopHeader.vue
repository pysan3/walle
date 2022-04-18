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
          <ion-chip outline color="light" @click="openPairSelector()" v-if="pairData">
            <ion-label>{{ $_pname(pairData.name) }}</ion-label>
            <ion-avatar
              v-for="(user, uidx) in (pairData.userhashes || [])
                .filter(uh => uh !== $store.getters.getMyUserInfo.usertoken)
                .map(uh => pairData.userinfos[uh])"
              :key="uidx"
            >
              <img
                :src="`${user.icon}`"
                :alt="`${user.username.slice(0, 1).toUpperCase()}`"
                class="border border-light"
              />
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
  data() {
    return {
      pairData: undefined,
    };
  },
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
    async reloadCurrentData() {
      this.pairData = await this.$_completePairData(this.$store.getters.getCurrentPairHash);
    },
  },
  watch: {
    '$store.getters.getCurrentPairHash': function () {
      this.reloadCurrentData();
    },
  },
  async created() {
    await this.reloadCurrentData();
  },
};
</script>
