import { createRouter, createWebHistory } from 'vue-router'
import PracticeView from '../views/PracticeView.vue'
import ReviewQueue from '../views/ReviewQueue.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/review' },
    { path: '/practice/:id', component: PracticeView },
    { path: '/review', component: ReviewQueue },
  ]
})

export default router
