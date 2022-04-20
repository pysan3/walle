<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-buttons slot="start">
          <ion-back-button default-href="/"></ion-back-button>
        </ion-buttons>
        <ion-title>{{ $t('Newitem.newpair') }}</ion-title>
        <ion-buttons slot="end">
          <ion-button color="medium" href="/">
            <ion-icon class="mx-2" :src="$i('home')"></ion-icon>
          </ion-button>
        </ion-buttons>
      </ion-toolbar>
    </ion-header>
    <ion-content>
      <ion-list class="my-3">
        <ion-label class="ml-3" position="stacked" color="primary">{{ $t('Newitem.addfriends') }}:</ion-label>
        <ion-item v-for="(userhash, index) in this.friendList" :key="index">
          <ion-chip outline>
            <ion-avatar>
              <img
                :src="`${userinfos[userhash].icon}`"
                :alt="`${userinfos[userhash].username.slice(0, 1).toUpperCase()}`"
                class="border border-light"
              />
            </ion-avatar>
            <ion-label>{{ userinfos[userhash].username }}</ion-label>
          </ion-chip>
          <ion-checkbox
            slot="start"
            @update:modelValue="nameSelected[userhash] = true"
            :modelValue="nameSelected[userhash]"
          ></ion-checkbox>
        </ion-item>
        <ion-item></ion-item>
        <ion-label class="ml-3" position="stacked" color="primary">{{ $t('Newitem.addtoken') }}:</ion-label>
        <template v-for="(_, idx) in 100" :key="idx">
          <ion-input
            v-model="tokenList[idx]"
            :name="`tokenId_${idx}`"
            type="text"
            spellcheck="false"
            autocapitalize="off"
            class="form-control ml-3 my-1"
            style="width: 90%"
            v-show="idx === 0 || idx === 1 || tokenList[idx - 2] !== undefined"
          ></ion-input>
        </template>
      </ion-list>
      <ion-button class="px-3 my-2" @click="submit()" expand="block">{{ $t('Newitem.submit') }}</ion-button>
    </ion-content>
  </ion-page>
</template>

<script>
import { defineComponent } from 'vue';
import {
  IonItem, IonLabel, IonList, IonCheckbox, IonInput,
} from '@ionic/vue';
import Axios from '@/axios';

export default defineComponent({
  name: 'newpair',
  components: {
    IonItem,
    IonLabel,
    IonList,
    IonInput,
    IonCheckbox,
  },
  data() {
    return {
      allPairInfo: undefined,
      nameSelected: {},
      userinfos: {},
      tokenList: new Array(100),
    };
  },
  computed: {
    friendList() {
      if (!this.allPairInfo) return [];
      return Object.values(this.allPairInfo)
        .map((e) => {
          this.userinfos = { ...this.userinfos, ...e.userinfos };
          return e.userhashes;
        })
        .flat()
        .filter((e) => e !== this.$store.getters.getMyUserInfo.usertoken)
        .sort((a, b) => this.userinfos[a].username.localeCompare(this.userinfos[b].username));
    },
  },
  methods: {
    async submit() {
      Axios.post('/api/requestpair', {
        usertokens: [
          ...Object.entries(this.nameSelected)
            .map(([k, v]) => (v ? k : null))
            .filter((e) => e),
          ...this.tokenList.map((e) => (e || '').trim()).filter((e) => e.length > 0),
        ],
      }).then((response) => {
        if (response.data.success) {
          this.$router.back();
        } else {
          alert('Invitation Failed for some Reason');
        }
      });
    },
    async getAllPairInfos() {
      return Axios.post('/api/mypairs', {}).then(async (r) => Object.fromEntries(
        await Promise.all(
          r.data.pairs.map(async (pidx) => [
            pidx.pairhash,
            { ...(await this.$_completePairData(pidx.pairhash)), ...pidx },
          ]),
        ),
      ));
    },
  },
  async created() {
    this.allPairInfo = await this.getAllPairInfos();
  },
});
</script>
