<template>
  <ion-page v-if="pairData">
    <ion-header>
      <ion-toolbar>
        <ion-buttons slot="start">
          <ion-back-button default-href="/"></ion-back-button>
        </ion-buttons>
        <ion-title>{{ $t('Newitem.newitem') }}</ion-title>
      </ion-toolbar>
    </ion-header>
    <ion-content>
      <ion-list class="my-3">
        <ion-item>
          <ion-radio-group v-model="payorhash">
            <ion-label position="stacked" color="primary">
              {{ $t('Newitem.payor') }}: {{ pairData.userinfos[this.payorhash].username || '?' }}
            </ion-label>
            <ion-item v-for="(userhash, index) in pairData.userhashes" :key="index">
              <ion-radio slot="start" :value="userhash"></ion-radio>
              <ion-chip outline>
                <ion-avatar>
                  <img
                    :src="`${pairData.userinfos[userhash].icon}`"
                    :alt="`${pairData.userinfos[userhash].username}`"
                    class="border border-light"
                  />
                </ion-avatar>
                <ion-label>{{ pairData.userinfos[userhash].username }}</ion-label>
              </ion-chip>
            </ion-item>
          </ion-radio-group>
        </ion-item>
        <ion-item>
          <ion-label position="stacked" color="primary">{{ $t('Newitem.payment') }}</ion-label>
          <ion-input
            v-model="payment"
            name="payment"
            type="number"
            spellcheck="false"
            autocapitalize="off"
            required
          ></ion-input>
        </ion-item>
        <ion-item>
          <ion-label position="stacked" color="primary">{{ $t('Newitem.description') }}</ion-label>
          <ion-textarea
            v-model="description"
            name="description"
            type="text"
            spellcheck="True"
            autocapitalize="off"
          ></ion-textarea>
          <ion-list>
            <ion-label class="ml-3" position="stacked" color="primary">: {{ $t('Newitem.templates') }}</ion-label>
            <ion-item
              v-for="pay in pairData.payments
                .slice(-8)
                .reverse()
                .map(e => pairData.payinfos[e].payinfo)"
              :key="pay"
              v-show="pay.description"
              @click="description += pay.description"
            >
              <p class="m-0 p-0">・{{ pay.description }}</p>
            </ion-item>
          </ion-list>
        </ion-item>
      </ion-list>
      <ion-button class="px-3 my-2" @click="submit()" expand="block">{{ $t('Newitem.submit') }}</ion-button>
    </ion-content>
  </ion-page>
</template>

<script>
import { defineComponent } from 'vue';
import { IonItem, IonLabel, IonList, IonRadio, IonRadioGroup, IonInput, IonTextarea } from '@ionic/vue';
import Axios from '@/axios';

export default defineComponent({
  name: 'newitem',
  components: {
    IonItem,
    IonLabel,
    IonList,
    IonRadio,
    IonRadioGroup,
    IonInput,
    IonTextarea,
  },
  data() {
    return {
      payorhash: this.$store.getters.getMyUserInfo.usertoken,
      payment: undefined,
      description: '',
      pairData: undefined,
    };
  },
  methods: {
    submit() {
      Axios.post('/api/addpayment', {
        payment: {
          pairhash: this.$store.getters.getCurrentPairHash,
          payorhash: this.payorhash,
          payment: this.payment,
          description: this.description,
        },
      }).then(response => {
        if (response.data.success) {
          this.$router.back();
          this.$store.commit('removePairData', { pairhash: this.$store.getters.getCurrentPairHash });
        }
      });
    },
  },
  async created() {
    this.pairData = await this.$_completePairData(this.$store.getters.getCurrentPairHash);
  },
});
</script>
