<template>
  <ion-page>
    <ion-content>
      <ion-header>
        <ion-toolbar>
          <ion-buttons slot="start">
            <ion-button color="medium" @click="changeMonth(currentYear, currentMonth - 1)">
              <ion-icon class="mx-2" :src="$i('chevron-back-outline')"></ion-icon>
            </ion-button>
          </ion-buttons>
          <div class="d-flex justify-content-center align-items-end">
            <ion-select v-model="currentYear">
              <ion-select-option
                v-for="year in Array.from({ length: 10 }, (_, i) => now.getFullYear() - i)"
                :key="year"
                :value="year"
              >
                {{ year }}
              </ion-select-option>
            </ion-select>
            <ion-label class="h4">/</ion-label>
            <ion-select v-model="currentMonth">
              <ion-select-option v-for="month in 12" :key="month" :value="month">
                {{ month }}
              </ion-select-option>
            </ion-select>
          </div>
          <ion-buttons slot="end">
            <ion-button color="medium" @click="changeMonth(currentYear, currentMonth + 1)">
              <ion-icon class="mx-2" :src="$i('chevron-forward-outline')"></ion-icon>
            </ion-button>
          </ion-buttons>
        </ion-toolbar>
      </ion-header>
      <template v-if="pairData">
        <div class="border-bottom border-secondary d-flex align-items-baseline justify-content-between px-2">
          <p>sum:</p>
          <h3>
            <ion-icon :src="$i('logo-yen')"></ion-icon>
            {{ $c(payAllSum) }}
          </h3>
          <p class="ml-auto">avg:</p>
          <h3>
            <ion-icon :src="$i('logo-yen')"></ion-icon>
            {{ $c(payAllSum / (pairData.userhashes || [0]).length) }}
          </h3>
        </div>
        <ion-row>
          <ion-col v-for="(uhash, idx) in pairData.userhashes" :key="idx" size="6" class="p-2">
            <ion-chip outline class="">
              <ion-avatar>
                <img
                  :src="`${pairData.userinfos[uhash].icon}`"
                  :alt="`${pairData.userinfos[uhash].username.slice(0, 1).toUpperCase()}`"
                  class="border border-light"
                />
              </ion-avatar>
              <ion-label>{{ pairData.userinfos[uhash].username }}</ion-label>
            </ion-chip>
            <ion-label>
              <p>sum:</p>
              <h1 class="mx-auto text-center">{{ paySums[uhash] }}</h1>
            </ion-label>
            <ion-label>
              <p>diff:</p>
              <h1 class="mx-auto text-center">{{ payAllSum / 2 - paySums[uhash] }}</h1>
            </ion-label>
          </ion-col>
        </ion-row>
        <ion-list class="border-top">
          <ion-item
            v-for="(p, idx) in payListRev"
            :key="idx"
            class="d-flex align-items-center"
            style="cursor: pointer;"
            @click="$router.push(`/update/${p.payhash}`)"
          >
            <div class="text-secondary">{{ new Date(p.createdAt).getDate() }}</div>
            <ion-chip outline class="">
              <ion-avatar>
                <img
                  :src="`${pairData.userinfos[p.payorhash].icon}`"
                  :alt="`${pairData.userinfos[p.payorhash].username.slice(0, 1).toUpperCase()}`"
                  class="border border-light"
                />
              </ion-avatar>
            </ion-chip>
            <div class="text-nowrap text-truncate">{{ p.description }}</div>
            <div class="ml-auto">
              <ion-icon :src="$i('logo-yen')"></ion-icon>
              {{ $c(p.payment) }}
            </div>
          </ion-item>
        </ion-list>
      </template>
    </ion-content>
  </ion-page>
</template>

<script lang="js">
import { defineComponent } from 'vue';
import {
  IonItem, IonLabel, IonList, IonRadio, IonRadioGroup, IonInput, IonTextarea, IonDatetime, IonSelect, IonSelectOption,
} from '@ionic/vue';
import Axios from '@/axios';

const now = new Date();
export default defineComponent({
  name: 'monthly',
  components: {
    IonLabel,
    IonSelect,
    IonSelectOption,
  },
  data() {
    return {
      pairData: undefined,
      currentYear: now.getFullYear(),
      currentMonth: now.getMonth() + 1,
      now,
      paySums: {},
      payAllSum: 0,
    };
  },
  computed: {
    dateInInt() {
      return this.currentYear * 100 + this.currentMonth;
    },
    payListRev() {
      return Object.values(this.pairData.payinfos || []).sort((a, b) => a.createdAt > b.createdAt);
    },
  },
  methods: {
    search(ev) {
      if (!ev) return;
      const query = ev.target.value;
      if (query && query !== '') {
        console.log(`Searching for '${query}'.`);
      }
    },
    changeMonth(year, month) {
      this.currentMonth = ((month - 1) % 12) + 1;
      this.currentYear = year - (month < 1 ? 1 : 0) + (month > 12 ? 1 : 0);
    },
    async updateData() {
      this.pairData = await this.$_completePairDataPeriod(
        this.$store.getters.getCurrentPairHash,
        this.dateInInt,
        1,
      );
      this.payAllSum = 0;
      this.pairData.userhashes.forEach((e) => { this.paySums[e] = 0; });
      Object.values(this.pairData.payinfos).forEach((p) => {
        this.paySums[p.payorhash] += p.payment;
        this.payAllSum += p.payment;
      });
    },
  },
  watch: {
    async dateInInt() {
      await this.updateData();
      this.$forceUpdate();
    },
  },
  async created() {
    await this.updateData();
  },
});
</script>
