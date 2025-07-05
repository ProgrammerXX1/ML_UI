<template>
  <div class="min-h-screen bg-[#1e1e1e] text-white text-[130%]">
    <Header />

    <div class="flex h-[calc(100vh-56px)] relative">
  <!-- Левая часть -->
  <div class="flex flex-col w-[90%] border-r border-neutral-800 p-6 space-y-6 overflow-y-auto transition-all duration-300 ease-in-out">
    <PlaygroundHeader />
    <MessageEditor />
    <MessageActions />
  </div>

  <!-- Правая часть -->
  <div class="w-100 flex-shrink-0 bg-[#1e1e1e] border-l border-neutral-800 overflow-y-auto">
    <ControlPanel />
  </div>
</div>

  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import Header from '~/components/Header.vue'
import PlaygroundHeader from '~/components/PlaygroundHeader.vue'
import MessageEditor from '~/components/MessageEditor.vue'
import MessageActions from '~/components/MessageActions.vue'
import ControlPanel from '~/components/ControlPanel.vue'

const isCollapsed = ref(false)
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>