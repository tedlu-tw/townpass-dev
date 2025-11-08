import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import RideView from '../views/RideView.vue'
import RidePauseView from '../views/RidePauseView.vue'
import RideFinishView from '../views/RideFinishView.vue'
import HistoryView from '../views/HistoryView.vue'
import MapDemoView from '../views/MapDemoView.vue'
import StationsMapView from '../views/StationsMapView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/home'
    },
    {
      path: '/home',
      name: 'home',
      component: HomeView
    },
    {
      path: '/ride',
      name: 'ride',
      component: RideView
    },
    {
      path: '/ride/pause',
      name: 'ride-pause',
      component: RidePauseView
    },
    {
      path: '/ride/finish',
      name: 'ride-finish',
      component: RideFinishView
    },
    {
      path: '/history',
      name: 'history',
      component: HistoryView
    },
    {
      path: '/map-demo',
      name: 'map-demo',
      component: MapDemoView
    },
    {
      path: '/stations',
      name: 'stations',
      component: StationsMapView
    }
  ]
})

export default router
