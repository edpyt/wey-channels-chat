import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SignupView from "@/views/SignupView.vue";
import LoginView from "@/views/LoginView.vue";
import FeedView from "@/views/FeedView.vue";
import SearchView from "@/views/SearchView.vue";
import ProfileView from "@/views/ProfileView.vue";
import Friends from "@/views/Friends.vue";
import PostView from "@/views/PostView.vue";
import ChatView from "@/views/ChatView.vue";


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/feed',
      name: 'feed',
      component: FeedView,
      meta: {
        requireLogin: true
      }
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/search',
      name: 'search',
      component: SearchView
    },
    {
      path: '/profile/:id',
      name: 'profile',
      component: ProfileView
    },
    {
      path: '/profile/:id/friends',
      name: 'friends',
      component: Friends
    },
    {
      path: '/:id',
      name: 'postview',
      component: PostView
    },
    {
      path: '/chat',
      name: 'chat',
      component: ChatView
    },
  ]
})

export default router
