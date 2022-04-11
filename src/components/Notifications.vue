<template>
  <div>
    <ion-header>
      <ion-toolbar>
        {{ $t('Notifications.header') }}
        <ion-buttons slot="end">
          <ion-button>
            <ion-icon :src="$i('checkbox-outline')"></ion-icon>
            <ion-label>read</ion-label>
          </ion-button>
        </ion-buttons>
      </ion-toolbar>
    </ion-header>
    <ion-content>
      <ion-list>
        <ion-item>
          <ion-avatar slot="start">
            <img src="@/assets/profile.jpg" alt="">
          </ion-avatar>
          <ion-label>
            <h2>Finn</h2>
            <h3>I'm a big deal!!</h3>
            <p>Listen, I've had a pretty messed up day...</p>
          </ion-label>
        </ion-item>
      </ion-list>
    </ion-content>
  </div>
</template>
