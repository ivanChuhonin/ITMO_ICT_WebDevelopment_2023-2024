import { createRouter, createWebHistory } from 'vue-router'

import MainPage from "@/components/MainPage.vue";

import Auth from "@/components/Auth.vue";
import Registration from "@/components/Registration.vue";
import UserProfile from "@/components/UserProfile.vue";
import Operation from "@/components/Operation.vue";
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '',
      name: 'Auth',
      component: Auth
    },
    {
      path: '/mainpage',
      name: 'MainPage',
      component: MainPage
    },
    {
      path: '/registration',
      name: 'Registration',
      component: Registration
    },
    {
      path: '/userprofile',
      name: 'UserProfile',
      component: UserProfile
    },
    {
      path: '/operation/:id',
      name: 'Operation',
      component: Operation
    },
  ]
})

export default router
