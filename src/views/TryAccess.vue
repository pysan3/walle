<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-buttons slot="start">
          <ion-back-button default-href="/"></ion-back-button>
        </ion-buttons>
        <ion-title>{{ $t(`Tryaccess.${$route.params.page}`) }}</ion-title>
      </ion-toolbar>
    </ion-header>
    <ion-content>
      <div class="login-logo">
        <img src="@/assets/logo.png" alt="Ionic logo" />
      </div>
      <form novalidate>
        <ion-list>
          <ion-item>
            <ion-label position="stacked" color="primary">{{ $t('Tryaccess.username') }}</ion-label>
            <ion-input
              v-model="username"
              name="username"
              type="text"
              spellcheck="false"
              autocapitalize="off"
              required
            ></ion-input>
          </ion-item>
          <ion-text color="danger" class="mx-auto">
            <p v-show="!username.match(/[a-zA-Z0-9]+/)">
              {{ `${$t('Tryaccess.username')}${$t('Tryaccess.isreq')}.` }}
              Alphabet / Numbers Only
            </p>
          </ion-text>
          <ion-item>
            <ion-label position="stacked" color="primary">{{ $t('Tryaccess.password') }}</ion-label>
            <ion-input v-model="password" name="password" type="password" required></ion-input>
          </ion-item>
          <ion-text color="danger" class="mx-auto">
            <p v-show="!password.match(/[a-zA-Z0-9]+/)">
              {{ `${$t('Tryaccess.password')}${$t('Tryaccess.isreq')}.` }}
              Alphabet / Numbers Only
            </p>
            <p v-show="password.length < 12">
              {{ ` > 12 ${$t('Tryaccess.letters')}.` }}
            </p>
          </ion-text>
        </ion-list>
        <ion-row responsive-sm class="my-3">
          <ion-col>
            <ion-button @click="onLogin" expand="block">Login</ion-button>
          </ion-col>
          <ion-col>
            <ion-button @click="onSignup" color="light" expand="block">Signup</ion-button>
          </ion-col>
        </ion-row>
      </form>
    </ion-content>
  </ion-page>
</template>

<script>
import { defineComponent } from 'vue';
import { IonItem, IonLabel, IonList, IonText, IonInput, IonButton } from '@ionic/vue';
import Axios from '@/axios';

export default defineComponent({
  name: 'TryAccess',
  components: {
    IonItem,
    IonLabel,
    IonList,
    IonInput,
    IonText,
    IonButton,
  },
  data() {
    return {
      username: '',
      password: '',
      submitted: false,
    };
  },
  computed: {
    nextpath() {
      return (this.$route.query.nexturl || '/').replace('-', '/');
    },
  },
  methods: {
    onLogin() {
      Axios.post('/api/login', {
        username: this.username,
        password: this.password,
      }).then(response => {
        if (response.data.success === true) {
          this.$store.commit('setIsLoggedIn', true);
          this.$router.push(this.nextpath);
        }
      });
    },
    onSignup() {
      alert('This Operation is not Implemented');
    },
  },
});
</script>

<style scoped>
.login-logo {
  padding: 20px 0;
  min-height: 200px;
  text-align: center;
}
.login-logo img {
  max-width: 150px;
}
.list {
  margin-bottom: 0;
}
p {
  margin-bottom: 0;
}
</style>
