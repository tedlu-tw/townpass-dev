import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import RideView from '../views/RideView.vue'
import RidePauseView from '../views/RidePauseView.vue'
import RideFinishView from '../views/RideFinishView.vue'
import HistoryView from '../views/HistoryView.vue'

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
  ]
})

export default router
