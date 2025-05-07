<script setup lang="ts">
defineProps<{
  rating: number
}>();

const stars = Array.from({ length: 4 }, (_, i) => i + 1);
</script>

<template>
  <div class="flex items-center">
    <svg
      :class="star <= rating ? 'filled' : 'empty'"
      :key="star"
      class="star"
      fill="currentColor"
      v-for="star in stars"
      viewBox="0 0 24 24"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"
      />
    </svg>
  </div>
</template>

<style scoped>
@reference '../assets/main.css';
.star {
  @apply mr-0.5 text-amber-400 h-5 w-5;
}

.filled {
  @apply text-amber-400;
}

.empty {
  @apply text-stone-300
}
</style>
