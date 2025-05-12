<script setup lang="ts">
import { decode } from 'html-entities';
import { defineProps, onMounted } from 'vue';
import tippy from 'tippy.js';
import 'tippy.js/dist/tippy.css'; // Import Tippy.js styles

const { name, url, subsites, comments } = defineProps<{
  name: string;
  url: string;
  subsites?: { site_id: string; site_url: string; site_name: string }[];
  comments?: string;
}>();

const decoded_name = decode(name);

onMounted(() => {
  if (subsites && subsites.length > 0) {
    const tooltipTriggers = document.querySelectorAll('.tooltip-trigger');
    const tooltipContent = document.querySelector('.tooltip-content');
    if (tooltipContent) {
      tippy(tooltipTriggers, {
        content: tooltipContent,
        allowHTML: true,
        interactive: true,
        placement: 'top',
      });
    }
  }
});
</script>

<template>
  <div class="flex space-x-2 items-center">
    <a :href="url" target="_blank" rel="noreferrer">
      {{ decoded_name }}
    </a>
    <span v-if="subsites && subsites.length > 0" class="tooltip-trigger">multisite</span>
    <div class="tooltip-content">
      <ul>
        <li v-for="subsite in subsites" :key="subsite.site_id">
          <a :href="subsite.site_url" target="_blank" rel="noreferrer">
            {{ subsite.site_name }}
          </a>
        </li>
      </ul>
    </div>
    <span v-if="comments && comments.length > 0" class="tooltip-trigger-2">info</span>
  </div>
</template>

<style>
@reference '../assets/main.css';

.tooltip-trigger {
  @apply text-xs bg-orange-200 text-orange-950 px-1 py-0.5 cursor-pointer rounded-sm;
}

.tooltip-trigger-2 {
  @apply text-xs bg-blue-200 text-blue-950 px-1 py-0.5 cursor-pointer rounded-sm;
}
</style>
