import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/Home.vue'),
    },
    {
      path: '/add',
      name: 'add',
      component: () => import('../views/Add.vue'),
    },
    {
      path: '/edit/:id',
      name: 'edit',
      component: () => import('../views/Edit.vue'),
    },
  ],
})

export default router
