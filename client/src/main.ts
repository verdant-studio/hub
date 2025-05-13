import './assets/main.css'

import { createApp } from 'vue'
import { createVfm } from 'vue-final-modal'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(createVfm())
app.use(router)

app.mount('#app')
