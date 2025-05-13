<script setup lang="ts">
import { decode } from 'html-entities';
import { defineProps, ref } from 'vue';
import { ModalsContainer, useModal } from 'vue-final-modal'
import Modal from './Modal.vue';

const { name, url, subsites, comments } = defineProps<{
  name: string;
  url: string;
  subsites?: { site_id: string; site_url: string; site_name: string }[];
  comments?: string;
}>();

const decoded_name = decode(name);

// Subsites Modal
const { open: openSubsitesModal, close: closeSubsitesModal } = useModal({
  component: Modal,
  attrs: {
    title: 'Subsites',
    onConfirm() {
      closeSubsitesModal();
    },
  },
  slots: {
    default: subsites
      ? `<ul>${subsites
          .map(
            (subsite) =>
              `<li><a href="${subsite.site_url}" target="_blank" rel="noreferrer">${subsite.site_name}</a></li>`
          )
          .join('')}</ul>`
      : '<p>No subsites available.</p>',
  },
});

// Comments Modal
const { open: openCommentsModal, close: closeCommentsModal } = useModal({
  component: Modal,
  attrs: {
    title: 'Comments',
    onConfirm() {
      closeCommentsModal();
    },
  },
  slots: {
    default: comments
      ? `<p>${comments}</p>`
      : '<p>No comments available.</p>',
  },
});
</script>

<template>
  <div class="flex space-x-1.5 items-center">
    <a :href="url" target="_blank" rel="noreferrer">
      {{ decoded_name }}
    </a>
    <VButton
      v-if="subsites && subsites.length > 0"
      class="text-xs bg-orange-200 text-orange-950 px-1 py-0.5 rounded-sm cursor-help"
      @click="openSubsitesModal"
    >
      multisite
    </VButton>
    <VButton
      v-if="comments && comments.length > 0"
      class="text-xs bg-blue-200 text-blue-950 px-1 py-0.5 rounded-sm cursor-help"
      @click="openCommentsModal"
    >
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" class="w-4 h-4" viewBox="0 0 24 24"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>
    </VButton>

    <ModalsContainer />
  </div>
</template>

<style>
@reference '../assets/main.css';
</style>
