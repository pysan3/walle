<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-buttons slot="start">
          <ion-back-button default-href="/"></ion-back-button>
        </ion-buttons>
        <ion-title>{{ $t('Newitem.newitem') }}</ion-title>
      </ion-toolbar>
    </ion-header>
    <ion-content>
      <ion-list>
        <ion-radio-group value="biff">
          <ion-list-header>
            <ion-label>Name</ion-label>
          </ion-list-header>
          <ion-item>
            <ion-label>Biff</ion-label>
            <ion-radio slot="start" value="biff"></ion-radio>
          </ion-item>
          <ion-item>
            <ion-label>Griff</ion-label>
            <ion-radio slot="start" value="griff"></ion-radio>
          </ion-item>
          <ion-item>
            <ion-label>Buford</ion-label>
            <ion-radio slot="start" value="buford"></ion-radio>
          </ion-item>
        </ion-radio-group>
      </ion-list>
    </ion-content>
  </ion-page>
</template>

<script>
import { defineComponent } from 'vue';
import { IonItem, IonLabel, IonList, IonListHeader, IonRadio, IonRadioGroup } from '@ionic/vue';

export default defineComponent({
  name: 'NewItem',
  components: {
    IonItem,
    IonLabel,
    IonList,
    IonListHeader,
    IonRadio,
    IonRadioGroup,
  },
});
</script>
