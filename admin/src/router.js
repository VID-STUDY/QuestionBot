import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import Channel from './views/Channels/Channel'
import AddChannel from './views/Channels/AddChannel'
import ChannelMembers from './views/Channels/ChannelMembers'
import User from './views/Users/User'
import ChannelRating from './views/Channels/ChannelRating'
import NewQuiz from './views/Quizzes/NewQuiz'
import QuizzesList from './views/Quizzes/QuizzesList'

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
      path: '/channel/:name', 
      component: Channel,
      props: true,
      children: [
        {
          path: 'quizzes',
          name: 'channelQuizzes',
          component: QuizzesList,
          props: true
        },
        {
          path: 'quizzes/new',
          name: 'newQuiz',
          component: NewQuiz,
          props: true
        },
        {
          path: 'users',
          name: 'channelUsers',
          component: ChannelMembers,
          props: true
        },
        {
          path: 'user/:userId',
          name: 'channelUser',
          component: User,
          props: true
        },
        {
          path: 'rating',
          name: 'channelRating',
          component: ChannelRating,
          props: true
        }
      ]
    },
    {
      path: '/channels/new',
      name: 'newChannel',
      component: AddChannel
    }
  ]
})
