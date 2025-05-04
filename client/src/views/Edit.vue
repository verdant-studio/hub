<template>
  <section>
    <div class="container max-w-3xl p-8">
      <div class="flex items-center mb-6 space-x-2">
        <RouterLink to="/">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" class="feather feather-arrow-left">
            <path d="M19 12H5M12 19l-7-7 7-7"/>
          </svg>
        </RouterLink>
        <h1 class="text-4xl font-bold">Edit {{ $route.params.id }}</h1>
      </div>
      <form @submit.prevent="updateWebsite" class="space-y-5 rounded bg-stone-800 p-4">
        <div>
          <label for="name" class="block text-lg font-medium text-stone-400 cursor-pointer">Name</label>
          <input
            v-model="form.name"
            id="name"
            type="text"
            class="mt-1 block w-full rounded-md border-stone-300 bg-stone-700 p-2 focus:border-green-500 focus:ring-green-500"
            placeholder="Enter a name for the site"
            required
          />
        </div>
        <div>
          <label for="url" class="block text-lg font-medium text-stone-400 cursor-pointer">Site URL</label>
          <input
            v-model="form.url"
            id="url"
            type="url"
            class="mt-1 block w-full rounded-md border-stone-300 bg-stone-700 p-2 focus:border-green-500 focus:ring-green-500"
            placeholder="https://www.example.com/wp-json"
            required
          />
        </div>
        <div>
          <label for="username" class="block text-lg font-medium text-stone-400 cursor-pointer">Username</label>
          <input
            v-model="form.username"
            id="username"
            type="text"
            class="mt-1 block w-full rounded-md border-stone-300 bg-stone-700 p-2 focus:border-green-500 focus:ring-green-500"
            placeholder="Enter your username"
            required
          />
        </div>
        <div>
          <label for="app-password" class="block text-lg font-medium text-stone-400 cursor-pointer"
            >Application Password</label
          >
          <input
            v-model="form.app_password"
            id="app-password"
            type="password"
            class="mt-1 block w-full rounded-md border-stone-300 bg-stone-700 p-2 focus:border-green-500 focus:ring-green-500"
            placeholder="Enter your application password"
            required
          />
        </div>
        <button
          type="submit"
          class="rounded-md bg-green-600 px-4 py-2 font-semibold text-white hover:bg-green-700 focus:ring-2 focus:ring-green-500 focus:outline-none mt-4 cursor-pointer"
        >
          Update
        </button>
      </form>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const id = route.params.id

const form = ref({
  name: '',
  url: '',
  username: '',
  app_password: '',
})

onMounted(async () => {
  const { data } = await axios.get(`http://localhost:8000/api/v1/websites/${id}`)
  form.value = {
    name: data.name,
    url: data.url,
    username: data.username,
    app_password: data.app_password,
  }
})

const updateWebsite = async () => {
  await axios.put(`http://localhost:8000/api/v1/websites/${id}`, form.value)
  router.push('/')
}
</script>
