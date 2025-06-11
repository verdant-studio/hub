<template>
  <section>
    <div class="container max-w-3xl p-8 space-y-7">
      <div class="flex items-center space-x-2">
        <RouterLink to="/">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2">
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
            placeholder="https://www.example.com"
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
          />
        </div>
        <hr class="border-stone-700" />
        <div>
          <label for="maintainers" class="block text-lg font-medium text-stone-400 cursor-pointer">Maintainer(s)</label>
          <input
            v-model="form.maintainers"
            id="maintainers"
            type="text"
            class="mt-1 block w-full rounded-md border-stone-300 bg-stone-700 p-2 focus:border-green-500 focus:ring-green-500"
            placeholder="Enter the names of the people who maintain this site"
          />
        </div>
        <div>
          <label for="comments" class="block text-lg font-medium text-stone-400 cursor-pointer">Comments</label>
          <textarea
            v-model="form.comments"
            id="comments"
            type="text"
            class="mt-1 block w-full rounded-md border-stone-300 bg-stone-700 p-2 focus:border-green-500 focus:ring-green-500"
            placeholder=""
          />
        </div>
        <div class="pt-4 flex justify-between">
          <button
            type="submit"
            class="rounded-md bg-green-600 px-4 py-2 font-semibold text-white hover:bg-green-700 focus:ring-2 focus:ring-green-500 focus:outline-none cursor-pointer"
          >
            Update
          </button>
          <button
            @click.prevent="deleteWebsite"
            type="button"
            class="rounded-md bg-red-600 px-4 py-2 font-semibold text-white hover:bg-red-700 focus:ring-2 focus:ring-red-500 focus:outline-none cursor-pointer"
          >
            Delete
          </button>
        </div>
      </form>

      <div>
        <h2 class="text-3xl font-bold mb-5">Directory Sizes</h2>
        <div class="rounded bg-stone-800 overflow-hidden">
          <table class="table-auto w-full text-left text-stone-400">
            <tbody>
              <tr
                v-for="entry in filteredDirectorySizes"
                :key="entry.key"
                class="odd:bg-stone-700 odd:text-stone-300 text-sm"
              >
                <td class="p-3">{{ entry.key }}</td>
                <td class="p-3">{{ entry.size }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div>
        <h2 class="text-3xl font-bold mb-5">Log</h2>
        <div class="rounded bg-stone-800 overflow-hidden">
          <table class="table-auto w-full text-left text-stone-400">
            <thead>
              <tr>
                <th class="p-3">Status Code</th>
                <th class="p-3">Response Time (ms)</th>
                <th class="p-3">Timestamp</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="result in crawlResults" :key="result.timestamp" class="odd:bg-stone-700 odd:text-stone-300 text-sm">
                <td class="p-3">{{ result.status_code || 'N/A' }}</td>
                <td class="p-3">{{ result.response_time_ms || 'N/A' }}</td>
                <td class="p-3">{{ new Date(result.timestamp).toLocaleString() }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL;

const route = useRoute()
const router = useRouter()
const id = route.params.id

const form = ref({
  name: '',
  url: '',
  username: '',
  app_password: '',
  maintainers: '',
  comments: '',
})

interface CrawlResult {
  status_code?: number
  response_time_ms?: number
  timestamp: string
  directory_sizes?: Record<string, { size: string; debug: string, raw: number }>
}

const crawlResults = ref<CrawlResult[]>([])

const filteredDirectorySizes = computed(() => {
  const directorySizes = crawlResults.value[0]?.directory_sizes || {}
  return Object.entries(directorySizes)
    .filter(([, value]) => value)
    .map(([key, value]) => ({
      key: key
        .replace('_size', '')
        .replace(/_/g, ' ')
        .replace(/^./, (char) => char.toUpperCase())
        .replace('Wordpress', 'WordPress'),
      size: value.size || 'N/A',
      debug: value.debug || 'N/A',
    }))
})

onMounted(async () => {
  // Fetch website data
  const { data } = await axios.get(`${API_URL}/api/v1/websites/${id}`)
  form.value = {
    name: data.name,
    url: data.url,
    username: data.username,
    app_password: '',
    maintainers: data.maintainers,
    comments: data.comments,
  }

  // Fetch last 5 crawl results
  try {
    const results = await axios.get(`${API_URL}/api/v1/crawl-results/${id}`)
    crawlResults.value = results.data.slice(0, 5)
  } catch (err) {
    console.error('Failed to fetch crawl results:', err)
    crawlResults.value = []
  }
})

const updateWebsite = async () => {
  await axios.put(`${API_URL}/api/v1/websites/${id}`, form.value)
  router.push('/')
}

const deleteWebsite = async () => {
  const confirmDelete = confirm('Are you sure you want to delete this website?')
  if (!confirmDelete) return

  try {
    await axios.delete(`${API_URL}/api/v1/websites/${id}`)
    alert('Website deleted.')
    router.push('/')
  } catch (err) {
    console.error(err)
    alert('Failed to delete website.')
  }
}
</script>
