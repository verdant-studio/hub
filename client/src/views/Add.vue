<template>
  <section>
    <div class="container max-w-3xl p-8">
      <div class="flex items-center mb-6 space-x-2">
        <RouterLink to="/">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2">
            <path d="M19 12H5M12 19l-7-7 7-7"/>
          </svg>
        </RouterLink>
        <h1 class="text-4xl font-bold">Add</h1>
      </div>
      <form @submit.prevent="submitForm" class="space-y-5 rounded bg-stone-800 p-4">
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
            placeholder="https://www.example.com"
            required
          />
        </div>
        <div>
          <label for="api-key" class="block text-lg font-medium text-stone-400 cursor-pointer"
            >API Key</label
          >
          <input
            v-model="form.api_key"
            id="api-key"
            type="password"
            class="mt-1 block w-full rounded-md border-stone-300 bg-stone-700 p-2 focus:border-green-500 focus:ring-green-500"
            placeholder="Enter the API key"
            required
          />
        </div>
        <button
          type="submit"
          class="rounded-md bg-green-600 px-4 py-2 font-semibold text-white hover:bg-green-700 focus:ring-2 focus:ring-green-500 focus:outline-none mt-4 cursor-pointer"
        >
          Add
        </button>
      </form>
    </div>
  </section>
</template>

<script lang="ts">
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL;

export default {
  data() {
    return {
      form: {
        name: '',
        url: '',
        api_key: ''
      }
    };
  },
  methods: {
    async submitForm() {
      try {
        await axios.post(`${API_URL}/v1/websites`, this.form)
        this.$router.push('/')
        this.form = { name: '', url: '', api_key: '' }
      } catch (err) {
        console.error(err)
      }
    }
  }
}
</script>
