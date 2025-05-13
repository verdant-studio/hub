<script setup lang="ts">
import { VueFinalModal } from 'vue-final-modal'
import 'vue-final-modal/style.css'

defineProps<{
  title?: string
}>()

const emit = defineEmits<{
  (e: 'confirm'): void
}>()
</script>

<template>
  <VueFinalModal
    class="flex justify-center items-center"
    content-class="max-w-xl mx-4 p-4 bg-stone-900 rounded space-y-2 w-full"
    overlay-transition="vfm-fade"
    content-transition="vfm-fade"
  >
    <h1 class="text-xl">
      {{ title }}
    </h1>
    <slot />
    <footer class="flex justify-end mt-4">
      <button class="rounded-md bg-stone-600 px-4 py-2 font-semibold text-white hover:bg-stone-700 focus:ring-2 focus:ring-stone-500 focus:outline-none cursor-pointer" @click="emit('confirm')">
        Close
      </button>
    </footer>
  </VueFinalModal>
</template>
