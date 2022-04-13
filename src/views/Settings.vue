<template>
  <ion-page v-if="pairData">
    <ion-header>
      <ion-toolbar>
        <ion-buttons slot="start">
          <ion-back-button default-href="/"></ion-back-button>
        </ion-buttons>
        <ion-title>{{ $t('Top.settings') }}</ion-title>
      </ion-toolbar>
    </ion-header>
    <ion-content>
      <ion-list class="my-3">
        <ion-item>
          <ion-label position="stacked" color="primary">usertoken</ion-label>
          <ion-label>{{ $store.getters.getMyUserInfo.usertoken }}</ion-label>
          <ion-icon
            @click="copyText($store.getters.getMyUserInfo.usertoken)"
            slot="end"
            :src="$i('clipboard-outline')"
          ></ion-icon>
        </ion-item>
      </ion-list>
    </ion-content>
  </ion-page>
</template>

<script>
import { defineComponent } from 'vue';
import { IonItem, IonLabel, IonList } from '@ionic/vue';

export default defineComponent({
  name: 'Settings',
  components: {
    IonItem,
    IonLabel,
    IonList,
  },
  data() {
    return {
      pairData: undefined,
    };
  },
  methods: {
    copyText(txt) {
      navigator.clipboard.writeText(txt);
    },
  },
  async created() {
    this.pairData = await this.$_completePairData(this.$store.getters.getCurrentPairHash);
  },
});
</script>
