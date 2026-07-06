import { createRouter, createWebHistory } from 'vue-router'

import LoginView from '../views/LoginView.vue'
import CadastroView from '../views/CadastroView.vue'
import BuilderView from '../views/BuilderView.vue'

const routes = [
  {
    path: '/',
    component: LoginView
  },
  {
    path: '/cadastro',
    component: CadastroView
  },
  {
    path: '/builder',
    component: BuilderView,
    meta: {
      requiresAuth: true
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to) => {
  const usuario = localStorage.getItem('usuario')

  if (to.meta.requiresAuth && !usuario) {
    return '/'
  }

  return true
})

export default router