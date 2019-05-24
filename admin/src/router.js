import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/channels/:name/users',
      name: 'channelUsers'
    },
    {
      path: '/channels/:name/tests',
      name: 'channelTests'
    },
    {
      path: '/channels/:name/rating',
      name: 'channelRating'
    },
    {
      path: '/addChannel',
      name: 'newChannel'
    }
  ]
})
