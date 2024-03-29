import mixins from '@/mixin';
import {
  IonContent,
  IonPage,
  IonHeader,
  IonFooter,
  IonTitle,
  IonToolbar,
  IonList,
  IonItem,
  IonCheckbox,
  IonLabel,
  IonNote,
  IonBadge,
  IonFab,
  IonFabButton,
  IonAvatar,
  IonIcon,
  IonButton,
  IonButtons,
  IonBackButton,
  IonMenu,
  IonMenuButton,
  IonChip,
  IonTabBar,
  IonTabButton,
  IonCard,
  IonCardContent,
  IonCardHeader,
  IonCardSubtitle,
  IonCardTitle,
  IonTabs,
  IonSearchbar,
  IonRow,
  IonCol,
  IonItemSliding,
  IonItemOptions,
  IonItemOption,
  IonFabList,
} from '@ionic/vue';

const mixin = mixins.methods;

const components = [
  IonContent,
  IonPage,
  IonHeader,
  IonFooter,
  IonCard,
  IonCardContent,
  IonCardHeader,
  IonCardSubtitle,
  IonCardTitle,
  IonTitle,
  IonToolbar,
  IonList,
  IonItemSliding,
  IonItemOptions,
  IonItemOption,
  IonItem,
  IonCheckbox,
  IonLabel,
  IonNote,
  IonBadge,
  IonFab,
  IonFabButton,
  IonFabList,
  IonAvatar,
  IonChip,
  IonIcon,
  IonButton,
  IonButtons,
  IonBackButton,
  IonMenu,
  IonMenuButton,
  IonTabs,
  IonTabBar,
  IonTabButton,
  IonSearchbar,
  IonRow,
  IonCol,
];

export default (app) => {
  components.forEach((e) => {
    app.component(mixin.$_camel2kebab(e.name) || e.displayName, e);
  });
};
