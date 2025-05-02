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
  <div class="p-2">
    <table>
      <thead>
        <tr
          v-for="headerGroup in table.getHeaderGroups()"
          :key="headerGroup.id"
        >
          <th
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
        </tr>
      </thead>
      <tbody>
        <tr v-for="row in table.getRowModel().rows" :key="row.id">
          <td v-for="cell in row.getVisibleCells()" :key="cell.id">
            <FlexRender
              :render="cell.column.columnDef.cell"
              :props="cell.getContext()"
            />
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
