<script setup lang="ts">
import { decode } from 'html-entities';

const { name } = defineProps<{
  name: string;
  url: string;
}>();

const decoded_name = decode(name);
</script>

<template>
  <a :href="url" target="_blank" rel="noreferrer">
		{{ decoded_name }}
	</a>
</template>
