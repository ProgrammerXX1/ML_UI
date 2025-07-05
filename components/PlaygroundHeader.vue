<template>
  <div class="flex flex-col w-full space-y-4">
    <!-- Header Controls -->
    <div class="flex items-center justify-between w-full space-x-4">
      <!-- Левая часть: Playground + Toggle -->
      <div class="flex items-center space-x-4">
        <h1 class="text-xl font-semibold text-white">Playground</h1>

        <!-- Toggle Chat/Studio -->
        <div class="flex items-center bg-[#2e2e2e] rounded-full px-1 py-1 space-x-1 border border-[#3a3a3a]">
          <button
            class="px-3 py-1 rounded-full text-xs"
            :class="mode === 'chat' ? 'bg-black text-white' : 'text-gray-400'"
            @click="mode = 'chat'"
          >
            Chat
          </button>
          <button
            class="px-3 py-1 rounded-full text-xs"
            :class="mode === 'studio' ? 'bg-black text-white' : 'text-gray-400'"
            @click="mode = 'studio'"
          >
            Studio
          </button>
        </div>
      </div>

      <!-- Правая часть: Model selector + View Code -->
      <div class="flex items-center space-x-2">
        <select
          v-model="selectedModel"
          class="bg-[#2e2e2e] text-white text-sm rounded-md px-3 py-1 focus:outline-none border border-neutral-700 max-w-xs truncate"
        >
          <option
            v-for="model in models"
            :key="model"
            :value="model"
          >
            {{ model }}
          </option>
        </select>

        <button
          @click="showCode = !showCode"
          class="flex items-center space-x-2 px-3 py-1 rounded-md border border-red-700 text-red-700 hover:bg-red-700 hover:text-white transition text-sm"
        >
          <Icon icon="lucide:code" class="text-sm" />
          <span>{{ showCode ? 'Hide code' : 'View code' }}</span>
        </button>
      </div>
    </div>

    <!-- Контент Studio и Code -->
    <div class="flex w-full space-x-6">
      <!-- Studio Panel -->
      <transition name="fade">
        <div v-if="mode === 'studio'" class="flex-1 bg-[#121212] text-white border border-neutral-700 rounded-md p-6 text-sm space-y-2">
          <h2 class="text-lg font-bold">Добро пожаловать в Studio!</h2>
          <ul class="list-disc pl-5">
            <li>Создавайте, редактируйте и тестируйте ваши промпты</li>
            <li>Настраивайте параметры вывода модели</li>
            <li>Изучайте примеры использования</li>
          </ul>
        </div>
      </transition>

      <!-- Code Panel -->
      <transition name="fade">
        <div v-if="showCode" class="flex-1 bg-[#121212] text-green-400 border border-neutral-700 rounded-md p-6 text-sm font-mono whitespace-pre-wrap">
<pre>
from groq import Groq

client = Groq()
completion = client.chat.completions.create(
  model="{{ selectedModel }}",
  messages=[
    {"role": "user", "content": "Hello!"}
  ]
)

for chunk in completion:
  print(chunk.choices[0].delta.content or "", end="")
</pre>
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Icon } from '@iconify/vue'

const mode = ref<'chat' | 'studio'>('chat')
const showCode = ref(false)
const selectedModel = ref('meta-llama/llama-4-scout-17b-16e-instruct')

const models = [
  'meta-llama/llama-4-scout-17b-16e-instruct',
  'openai/gpt-4o',
  'google/gemma-7b',
  'mistral/mixtral-8x7b'
]
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
