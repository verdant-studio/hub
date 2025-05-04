<script setup lang="tsx">
import {
  FlexRender,
  getCoreRowModel,
  useVueTable,
  createColumnHelper,
} from '@tanstack/vue-table'
import { ref } from 'vue'
import TableSiteName from './TableSiteName.vue'

type Site = {
  site_name: string
  site_url: string
  wp_version: string
  health_rating: number
  updates_available: number
  clients: string
  maintainers: number
}

const defaultData: Site[] = [
  {
    site_name: 'Verdant Studio',
    site_url: 'https://www.verdant.studio',
    wp_version: '6.8.1',
    health_rating: 5,
    updates_available: 0,
    clients: 'Green Leaf',
    maintainers: 'Robert',
  },
  {
    site_name: 'Eight Vein',
    site_url: 'https://www.google.com',
    wp_version: '6.7.2',
    health_rating: 4,
    updates_available: 11,
    clients: null,
    maintainers: null,
  },
]

const columnHelper = createColumnHelper<Site>()

const columns = [
  columnHelper.accessor('site_name', {
    header: () => 'Name',
    cell: ({ row }) => {
			return (
				<TableSiteName
					name={row.original.site_name}
					url={row.original.site_url}
				/>
			);
		},
  }),
  columnHelper.accessor('health_rating', {
    header: () => 'Health',
    footer: props => props.column.id,
  }),
  columnHelper.accessor('wp_version', {
    header: 'WP Version',
    footer: props => props.column.id,
  }),
  columnHelper.accessor('updates_available', {
    header: 'Updates available',
    footer: props => props.column.id,
  }),
]

const data = ref(defaultData)

const rerender = () => {
  data.value = defaultData
}

const table = useVueTable({
  get data() {
    return data.value
  },
  columns,
  getCoreRowModel: getCoreRowModel(),
})
</script>

<template>
  <div class="relative flex flex-col w-full overflow-x-auto">
    <h1 class="text-4xl font-bold mb-6">Hub</h1>
    <table class="bg-stone-800 rounded w-full text-left table-auto min-w-max">
      <thead>
        <tr
          v-for="headerGroup in table.getHeaderGroups()"
          :key="headerGroup.id"
        >
          <th
            class="p-3 font-normal text-left text-white"
            v-for="header in headerGroup.headers"
            :key="header.id"
            :colSpan="header.colSpan"
          >
            <FlexRender
              v-if="!header.isPlaceholder"
              :render="header.column.columnDef.header"
              :props="header.getContext()"
            />
          </th>
          <th>
            <RouterLink to="/add">
              <svg
                class="w-5 h-5"
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
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="row in table.getRowModel().rows" :key="row.id" class="odd:bg-stone-700">
          <td
            class="p-3"
            v-for="cell in row.getVisibleCells()"
            :key="cell.id"
          >
            <FlexRender
              :render="cell.column.columnDef.cell"
              :props="cell.getContext()"
            />
          </td>
          <td>
            <RouterLink to="/edit/1">
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
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style>
  @reference '../assets/main.css';

</style>
