<template>
  <ion-header>
    <ion-toolbar translucent>
      <ion-title>メニュー</ion-title>
    </ion-toolbar>
  </ion-header>
  <ion-content>
    <ion-list>
      <ion-item>
        <ion-icon :src="$i('mail')" slot="start" color="secondary"></ion-icon>
        <ion-label>Inbox</ion-label>
      </ion-item>
      <ion-item>
        <ion-icon :src="$i('paper-plane')" slot="start"></ion-icon>
        <ion-label>Outbox</ion-label>
      </ion-item>
      <ion-item>
        <ion-icon :src="$i('heart')" slot="start"></ion-icon>
        <ion-label>Favorites</ion-label>
      </ion-item>
      <ion-item>
        <ion-icon :src="$i('archive')" slot="start"></ion-icon>
        <ion-label>Archived</ion-label>
      </ion-item>
      <ion-item>
        <ion-icon :src="$i('trash')" slot="start"></ion-icon>
        <ion-label>Trash</ion-label>
      </ion-item>
      <ion-item>
        <ion-icon :src="$i('warning')" slot="start"></ion-icon>
        <ion-label>Spam</ion-label>
      </ion-item>
    </ion-list>
  </ion-content>
</template>
