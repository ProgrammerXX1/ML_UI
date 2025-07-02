<template>
  <Sheet :open="isOpen" @update:open="val => emit('update:isOpen', val)">
    <SheetContent class="bg-gray-900/30 text-white border-indigo-700/50 backdrop-blur-lg">
      <div v-if="localChat" class="grid gap-4 py-4">
        <h2 class="text-lg font-semibold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent animate-flicker">
          Edit Chat
        </h2>

        <div class="grid gap-2">
          <label for="name" class="text-gray-300 animate-glow-text">Name</label>
          <Input
            id="name"
            v-model="localChat.name"
            class="bg-gray-800/20 text-white border-indigo-700/50 focus:border-purple-500 transition-all duration-300 shadow-glow"
          />

          <label for="status" class="text-gray-300 animate-glow-text">Status</label>
          <select
            id="status"
            v-model="localChat.status"
            class="bg-gray-800/20 text-white border-indigo-700/50 rounded-md p-2 focus:border-purple-500 transition-all duration-300 shadow-glow"
          >
            <option value="Active">Active</option>
            <option value="Draft">Draft</option>
            <option value="Archived">Archived</option>
          </select>
        </div>

        <Button
          class="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white transition-all duration-300 shadow-glow"
          @click="handleSave"
        >
          Save
        </Button>
      </div>

      <div v-else>
        <p class="text-gray-300 animate-pulse">Ошибка: данные чата недоступны</p>
      </div>
    </SheetContent>
  </Sheet>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

type ChatStatus = 'Active' | 'Draft' | 'Archived'

type Chat = {
  id: number
  name: string
  status: ChatStatus
  created_at: string
  image?: string
}

const props = defineProps<{
  chat: Chat | null
  isOpen: boolean
}>()

const emit = defineEmits<{
  (e: 'update:isOpen', value: boolean): void
  (e: 'saveChat', updated: Chat): void
}>()

const localChat = ref<Chat | null>(null)

watch(
  () => props.chat,
  (newVal) => {
    localChat.value = newVal ? { ...newVal } : null
  },
  { immediate: true }
)

function handleSave() {
  if (localChat.value) {
    emit('saveChat', localChat.value)
    emit('update:isOpen', false)
  }
}
</script>
