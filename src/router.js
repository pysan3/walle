import { createRouter, createWebHashHistory } from '@ionic/vue-router';
import store from '@/store';
import mixin from '@/mixin';

const mixins = mixin.methods;

const routerMap = (route, isView) => {
  if (route.redirect !== undefined) return route;
  const ret = {
    ...route,
    ...{
      name: route.component.toLowerCase(),
      component: () => import(`@/${isView ? 'views' : 'components'}/${route.component}.vue`),
      meta: {
        requiredAuth: route.requiredAuth === true,
      },
    },
  };
  return ret;
};
const routerMapView = route => routerMap(route, true);

const topChildren = [
  { path: '', redirect: 'history' },
  { path: 'history', component: 'History', requiredAuth: true },
  { path: 'monthly', component: 'Monthly', requiredAuth: true },
  { path: 'stats', component: 'Stats', requiredAuth: true },
];
const routerOptions = [
  { path: '/new', component: 'NewItem', requiredAuth: true },
  { path: '/tryaccess/:page', component: 'TryAccess', requiredAuth: false },
  { path: '/:pathMatch(.*)*', component: 'Top', children: topChildren.map(e => routerMap(e, true)) },
];

const routes = routerOptions.map(routerMapView);

const router = createRouter({
  history: createWebHashHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach(async (to, from, next) => {
  // eslint-disable-line no-unused-vars
  if (to.matched.some(record => record.meta.requiredAuth)) {
    // check if login is needed
    if (!(await mixins.$_checkIsLoggedin())) {
      to.query.nexturl = to.path;
      next({
        name: 'tryaccess',
        params: { page: 'login' },
        query: to.query,
      });
      return;
    }
    if (Object.values(store.getters.getMyUserInfo).filter(e => e === undefined).length > 0) {
      await mixins.$_fillUserInfo();
    }
  }
  next();
});

export default router;
