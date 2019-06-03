import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import Channel from './views/Channels/Cahnnel'
import AddChannel from './views/Channels/AddChannel'
import CahnnelMembers from './views/Channels/CahnnelMembers'
import ChannelRating from './views/Channels/ChannelRating'
import EditQuiz from './views/Quizzes/EditQuiz'
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
          path: 'quiz/:id',
          name: 'editQuiz',
          component: EditQuiz,
          props: true
        },
        {
          path: 'users',
          name: 'channelUsers',
          component: CahnnelMembers,
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
