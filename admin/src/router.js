import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import AddChannel from './views/AddChannel'
import ChannelTest from './views/Tests/ChannelTests'
import NewTest from './views/Tests/NewTest'

Vue.use(Router);

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
      name: 'channelTests',
      component: ChannelTest,
      props: true
    },
    {
      path: '/channels/:name/tests/create',
      name: 'newTest',
      component: NewTest,
      props: true
    },
    {
      path: '/channels/:name/rating',
      name: 'channelRating'
    },
    {
      path: '/addChannel',
      name: 'newChannel',
      component: AddChannel
    }
  ]
})
