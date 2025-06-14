<script setup lang="tsx">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import {
  createColumnHelper,
  FlexRender,
  getCoreRowModel,
  type SortingState,
  getSortedRowModel,
  useVueTable,
} from '@tanstack/vue-table'
import TableHealth from './TableHealth.vue'
import TableSiteName from './TableSiteName.vue'

const API_URL = import.meta.env.VITE_API_URL;

type Site = {
  id: number
  name: string
  url: string
  maintainers: string
  comments: string
  latest_crawl: {
    id: number
    status_code: number
    response_time_ms: number
    timestamp: string
    wp_version: string
    health_rating: number
    updates_available: number
    multisite: boolean
    subsites: any
  }
}

const data = ref<Site[]>([])

const sorting = ref<SortingState>([])

onMounted(async () => {
  try {
    const res = await axios.get<Site[]>(`${API_URL}/v1/websites`)
    data.value = res.data
  } catch (err) {
    console.error('Failed to fetch websites', err)
  }
})

const columnHelper = createColumnHelper<Site>()
const columns = [
  columnHelper.accessor('name', {
    header: () => 'Name',
    cell: ({ row }) => {
      const subsites = row.original.latest_crawl?.subsites;
      const comments = row.original.comments;
      return (<TableSiteName name={row.original.name} url={row.original.url} subsites={subsites} comments={comments} />)
    },
  }),
  columnHelper.accessor('latest_crawl.health_rating', {
    header: 'Health',
    cell: ({ row }) => {
      const record = row.original.latest_crawl?.health_rating;
      return record !== null && record !== undefined ? (
        <TableHealth rating={record} />
      ) : (
        <span class="text-stone-400">-</span>
      );
    },
  }),
  columnHelper.accessor('latest_crawl.wp_version', {
    header: 'WP Version',
    cell: ({ row }) => {
      const record = row.original.latest_crawl?.wp_version;
      return record ? (
        <span class="text-stone-400">{record}</span>
      ) : (
        <span class="text-stone-400">-</span>
      );
    },
  }),
  columnHelper.accessor('latest_crawl.updates_available', {
    header: 'Updates Available',
    cell: ({ row }) => {
      const record = row.original.latest_crawl?.updates_available;
      return record ? (
        <span class="text-stone-400">{record}</span>
      ) : (
        <span class="text-stone-400">-</span>
      );
    },
  }),
  columnHelper.accessor('maintainers', {
    header: 'Maintainers',
    cell: ({ row }) => {
      const record = row.original.maintainers;
      return record ? (
        <span class="text-stone-400">{record}</span>
      ) : (
        <span class="text-stone-400">-</span>
      );
    },
  }),
]

const table = useVueTable({
  get data() {
    return data.value
  },
  columns,
  state: {
    get sorting() {
      return sorting.value
    },
  },
  onSortingChange: updaterOrValue => {
    sorting.value =
      typeof updaterOrValue === 'function'
        ? updaterOrValue(sorting.value)
        : updaterOrValue
  },
  getCoreRowModel: getCoreRowModel(),
  getSortedRowModel: getSortedRowModel(),
})
</script>

<template>
  <div class="relative flex flex-col w-full overflow-x-auto">
    <h1 class="text-4xl font-bold mb-6">Hub</h1>
    <table class="bg-stone-800 rounded w-full text-left table-auto min-w-max overflow-hidden">
      <thead>
        <tr
          v-for="headerGroup in table.getHeaderGroups()"
          :key="headerGroup.id"
        >
          <th
            class="px-4 py-3 font-normal"
            v-for="header in headerGroup.headers"
            :key="header.id"
            :colSpan="header.colSpan"
            :class="
              header.column.getCanSort() ? 'cursor-pointer select-none' : ''
            "
            @click="header.column.getToggleSortingHandler()?.($event)"
          >
          {{
                { asc: ' 🔼', desc: ' 🔽' }[
                  header.column.getIsSorted() as string
                ]
              }}
            <FlexRender
              v-if="!header.isPlaceholder"
              :render="header.column.columnDef.header"
              :props="header.getContext()"
            />
          </th>
          <th class="px-4 py-3">
            <div class="flex justify-end">
              <RouterLink to="/add">
                <svg
                  class="w-5 h-5 flex"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  stroke="currentColor"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  viewBox="0 0 24 24"
                >
                  <circle cx="12" cy="12" r="10"/><path d="M12 8v8M8 12h8"/>
                </svg>
              </RouterLink>
            </div>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="row in table.getRowModel().rows" :key="row.id" class="odd:bg-stone-700">
          <td
            class="px-4 py-3"
            v-for="cell in row.getVisibleCells()"
            :key="cell.id"
          >
            <FlexRender
              :render="cell.column.columnDef.cell"
              :props="cell.getContext()"
            />
          </td>
          <td class="px-4 py-3">
            <div class="flex justify-end">
              <RouterLink :to="`/edit/${row.original.id}`">
                <svg
                  class="w-4 h-4"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  stroke="currentColor"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  viewBox="0 0 24 24"
                >
                  <path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z" />
                </svg>
              </RouterLink>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style>
@reference '../assets/main.css';
</style>
