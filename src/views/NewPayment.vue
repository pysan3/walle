<template>
  <ion-page>
    <ion-header v-if="pairData">
      <ion-toolbar>
        <ion-buttons slot="start">
          <ion-back-button default-href="/"></ion-back-button>
        </ion-buttons>
        <ion-title>{{ $t(`Newitem.${$route.name}`) }}</ion-title>
        <ion-buttons slot="end">
          <ion-button color="medium" href="/">
            <ion-icon class="mx-2" :src="$i('home')"></ion-icon>
          </ion-button>
        </ion-buttons>
      </ion-toolbar>
    </ion-header>
    <ion-content v-if="pairData">
      <ion-list class="my-3">
        <ion-item>
          <ion-radio-group v-model="payorhash">
            <ion-label position="stacked" color="primary">
              {{ $t('Newitem.payor') }}: {{ pairData.userinfos[this.payorhash].username || '?' }}
            </ion-label>
            <ion-item v-for="(userhash, index) in pairData.userhashes" :key="index">
              <ion-radio slot="start" :value="userhash" :disabled="!updatable"></ion-radio>
              <ion-chip outline>
                <ion-avatar>
                  <img
                    :src="`${pairData.userinfos[userhash].icon}`"
                    :alt="`${pairData.userinfos[userhash].username.slice(0, 1).toUpperCase()}`"
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
            type="tel"
            spellcheck="false"
            autocapitalize="off"
            required
            :readonly="!updatable"
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
            <ion-label class="ml-3" position="stacked" color="primary">^ {{ $t('Newitem.templates') }}</ion-label>
            <ion-item v-for="(pDesc, idx) in uniqueRevDesc" :key="idx" v-show="pDesc" @click="description += pDesc">
              <p class="m-0 p-0">・{{ pDesc }}</p>
            </ion-item>
          </ion-list>
        </ion-item>
        <ion-item>
          <ion-label position="stacked" color="primary">{{ $t('Newitem.date') }}</ion-label>
          <ion-datetime v-model="createdAt" presentation="date" :disabled="!updatable"></ion-datetime>
        </ion-item>
        <ion-item>
          <ion-label position="stacked" color="primary">{{ $t('Newitem.photos') }}</ion-label>
          <ion-item v-for="(photo, idx) in payPhotos" :key="idx">
            <div class="rounded border border-secondary p-2" style="position: relative;">
              <a @click="deletePayPhoto(photo)" class="clipboard h4 leader" style="cursor: pointer;">
                <ion-icon :src="$i('trash-outline')"></ion-icon>
              </a>
              <img :src="photo" alt="Payment Photo, Unreachable" />
            </div>
          </ion-item>
          <ion-item v-for="(photo, idx) in newPhotos" :key="idx">
            <div class="rounded border border-secondary p-2" style="position: relative;">
              <a @click="deleteNewPhoto(idx)" class="clipboard h4 leader" style="cursor: pointer;">
                <ion-icon :src="$i('trash-outline')"></ion-icon>
              </a>
              <img :src="`data:image/${photo.format};base64,${photo.data64}`" alt="Possibly Invalid Format" />
            </div>
          </ion-item>
        </ion-item>
      </ion-list>
      <ion-fab vertical="bottom" horizontal="end" slot="fixed" class="d-flex">
        <ion-fab-button @click="bootCamera()" class="mr-3" color="dark">
          <ion-icon :src="$i('camera-sharp')"></ion-icon>
        </ion-fab-button>
        <ion-fab-button @click="submit()">
          <ion-icon :src="$i('send-sharp')"></ion-icon>
        </ion-fab-button>
      </ion-fab>
    </ion-content>
  </ion-page>
</template>

<script>
import { defineComponent } from 'vue';
import {
  IonItem,
  IonLabel,
  IonList,
  IonRadio,
  IonRadioGroup,
  IonInput,
  IonTextarea,
  IonFab,
  IonFabButton,
  IonDatetime,
} from '@ionic/vue';
import { Camera, CameraResultType } from '@capacitor/camera';
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
    IonFab,
    IonFabButton,
    IonDatetime,
  },
  data() {
    return {
      payorhash: this.$store.getters.getMyUserInfo.usertoken,
      payment: undefined,
      description: '',
      pairData: undefined,
      createdAt: new Date().toISOString(),
      payhash: '',
      payPhotos: [],
      newPhotos: [],
    };
  },
  computed: {
    uniqueRevDesc() {
      const descSet = new Set();
      return this.pairData.payments
        .map((e) => this.pairData.payinfos[e].description)
        .reverse()
        .filter((e) => {
          if (descSet.has(e)) return false;
          descSet.add(e);
          return true;
        })
        .slice(0, 5);
    },
    updatable() {
      return (
        this.$route.name !== 'updatepayment'
        || this.pairData.payinfos[this.payhash].creatorhash === this.$store.getters.getMyUserInfo.usertoken
        || this.pairData.payinfos[this.payhash].payorhash === this.$store.getters.getMyUserInfo.usertoken
      );
    },
  },
  methods: {
    async bootCamera() {
      const photo = await Camera.getPhoto({
        resultType: CameraResultType.Base64,
        allowEditing: true,
        quality: 100,
      });
      this.newPhotos.push({
        data64: photo.base64String,
        format: photo.format,
        payhash: this.payhash,
      });
    },
    deleteNewPhoto(idx) {
      alert(this.$t('Utils.rusure'));
      this.newPhotos.splice(idx, 1);
    },
    deletePayPhoto(photo) {
      alert(this.$t('Utils.rusure'));
      Axios.post('/api/deletepayphoto', {
        photopath: photo,
      }).then((response) => {
        if (!response.data.success) {
          alert('Something went wrong');
          return;
        }
        const index = this.payPhotos.indexOf(photo);
        if (index !== -1) {
          this.payPhotos.splice(index, 1);
        }
      });
    },
    submit() {
      Axios.post(`/api/${this.$route.name}`, {
        payhash: this.payhash,
        pairhash: this.$store.getters.getCurrentPairHash,
        payorhash: this.payorhash,
        payment: this.payment,
        description: this.description,
        createdAt: this.createdAt,
      }).then((response) => {
        if (response.data.success) {
          this.$store.commit('removePairData', { pairhash: this.$store.getters.getCurrentPairHash });
          if (this.$route.name === 'newpayment') this.payhash = response.data.token;
          Promise.all(
            this.newPhotos
              .filter((e) => e)
              .map((e) => Axios.post('/api/uploadpayphoto', e)
                .then((response) => {
                  if (!response.data.success) alert(response.data.msg);
                  return response.data.success;
                })
                .catch((err) => alert(err))),
          ).then((success) => {
            if (success) {
              this.$store.commit('removePayData', { payhash: this.payhash });
              this.$router.back();
            }
          });
        } else {
          alert(response.data.msg);
        }
      });
    },
    updateInputs(payhash) {
      this.payhash = payhash;
      const payinfo = this.pairData.payinfos[payhash];
      this.payorhash = payinfo.payorhash;
      this.payment = payinfo.payment;
      this.description = payinfo.description;
      this.createdAt = payinfo.createdAt.toISOString();
      this.payhash = payinfo.payhash;
      this.payPhotos.push(...payinfo.photopath);
    },
  },
  async created() {
    this.pairData = await this.$_completePairData(this.$store.getters.getCurrentPairHash);
    if (this.$route.name === 'updatepayment') {
      this.updateInputs(this.$route.params.payhash);
    }
    console.log(this.pairData);
  },
});
</script>

<style lang="stylus" scoped>
.clipboard
  position absolute
  right .5rem
</style>
