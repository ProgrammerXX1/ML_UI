<template>
  <aside class="w-80 bg-# from-gray-900 via-black to-gray-800 border-l border-gray-700 p-6 space-y-6 text-sm shadow-2xl rounded-r-lg transform transition-all duration-300 hover:scale-101">
    <h2 class="bg-gray text-lg font-extrabold uppercase tracking-widest">PARAMETERS</h2>

    <!-- Temperature -->
    <div class="space-y-2.5">
      <label class="block text-sm font-semibold text-gray-200">Temperature</label>
      <div class="flex items-center space-x-5">
        <input
          type="range"
          min="0"
          max="2"
          step="0.1"
          v-model="temperature"
          class="w-full h-3 bg-gradient-to-r from-blue-500 to-orange-400 rounded-lg appearance-none cursor-pointer accent-transparent"
        />
        <span class="w-14 text-center bg-gradient-to-r from-gray-700 to-black text-white text-sm py-2 rounded-lg shadow-md">{{ temperature }}</span>
      </div>
    </div>

    <!-- Max Completion Tokens -->
    <div class="space-y-2.5">
      <label class="block text-sm font-semibold text-gray-200">Max Completion Tokens</label>
      <div class="flex items-center space-x-5">
        <input
          type="range"
          min="1"
          max="4096"
          step="1"
          v-model="maxTokens"
          class="w-full h-3 bg-gradient-to-r from-blue-500 to-orange-400 rounded-lg appearance-none cursor-pointer accent-transparent"
        />
        <span class="w-14 text-center bg-gradient-to-r from-gray-700 to-black text-white text-sm py-2 rounded-lg shadow-md">{{ maxTokens }}</span>
      </div>
    </div>

    <!-- Stream toggle -->
    <div class="flex items-center justify-between">
      <span class="text-sm font-semibold text-gray-200">Stream</span>
      <label class="relative inline-flex items-center cursor-pointer">
        <input type="checkbox" v-model="stream" class="sr-only peer">
        <div class="w-12 h-6 bg-gradient-to-r from-gray-600 to-gray-800 peer-checked:bg-gradient-to-r peer-checked:from-green-400 peer-checked:to-emerald-500 rounded-full peer-focus:ring-2 peer-focus:ring-emerald-300 transition-all duration-300">
          <div class="absolute top-0.5 left-0.5 h-5 w-5 bg-white rounded-full shadow-lg transform transition-transform duration-300 peer-checked:translate-x-6"></div>
        </div>
      </label>
    </div>

    <!-- JSON Mode toggle -->
    <div class="flex items-center justify-between">
      <span class="text-sm font-semibold text-gray-200">JSON Mode</span>
      <label class="relative inline-flex items-center cursor-pointer">
        <input type="checkbox" v-model="jsonMode" class="sr-only peer">
        <div class="w-12 h-6 bg-gradient-to-r from-gray-600 to-gray-800 peer-checked:bg-gradient-to-r peer-checked:from-green-400 peer-checked:to-emerald-500 rounded-full peer-focus:ring-2 peer-focus:ring-emerald-300 transition-all duration-300">
          <div class="absolute top-0.5 left-0.5 h-5 w-5 bg-white rounded-full shadow-lg transform transition-transform duration-300 peer-checked:translate-x-6"></div>
        </div>
      </label>
    </div>

    <!-- Advanced Section -->
    <details class="mt-6">
      <summary class="text-sm font-semibold text-gray-200 cursor-pointer hover:text-yellow-400 transition-colors duration-200">Advanced</summary>
      <div class="mt-4 space-y-4">
        <div class="flex items-center justify-between">
          <span class="text-sm font-semibold text-gray-200">Moderation: llamaguard</span>
          <label class="relative inline-flex items-center cursor-pointer">
            <input type="checkbox" v-model="moderation" class="sr-only peer">
            <div class="w-12 h-6 bg-gradient-to-r from-gray-600 to-gray-800 peer-checked:bg-gradient-to-r peer-checked:from-green-400 peer-checked:to-emerald-500 rounded-full peer-focus:ring-2 peer-focus:ring-emerald-300 transition-all duration-300">
              <div class="absolute top-0.5 left-0.5 h-5 w-5 bg-white rounded-full shadow-lg transform transition-transform duration-300 peer-checked:translate-x-6"></div>
            </div>
          </label>
        </div>
        <div class="space-y-2.5">
          <label class="block text-sm font-semibold text-gray-200">Top P</label>
          <div class="flex items-center space-x-5">
            <input
              type="range"
              min="0"
              max="1"
              step="0.01"
              v-model="topP"
              class="w-full h-3 bg-gradient-to-r from-blue-500 to-orange-400 rounded-lg appearance-none cursor-pointer accent-transparent"
            />
            <span class="w-10 text-center bg-gradient-to-r from-gray-700 to-black text-white text-sm py-2 rounded-lg shadow-md">{{ topP }}</span>
          </div>
        </div>
        <div class="space-y-2.5">
          <label class="block text-sm font-semibold text-gray-200">Seed</label>
          <input
            type="text"
            v-model="seed"
            class="w-full bg-gradient-to-r from-gray-700 to-black text-white text-sm py-2 px-4 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-400 shadow-md"
            placeholder=""
          />
        </div>
        <div class="space-y-2.5">
          <label class="block text-sm font-semibold text-gray-200">Stop Sequence</label>
          <input
            type="text"
            v-model="stopSequence"
            class="w-full bg-gradient-to-r from-gray-700 to-black text-white text-sm py-2 px-4 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-400 shadow-md"
            placeholder=""
          />
        </div>
      </div>
    </details>
  </aside>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const temperature = ref(1)
const maxTokens = ref(1024)
const stream = ref(false)
const jsonMode = ref(false)
const moderation = ref(false)
const topP = ref(1)
const seed = ref('')
const stopSequence = ref('')
</script>

<style scoped>
input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 14px;
  height: 14px;
  background: #ffffff;
  border: 2px solid #ffcc00;
  border-radius: 50%;
  cursor: pointer;
  box-shadow: 0 0 5px rgba(255, 204, 0, 0.5);
  transition: transform 0.3s ease;
}

input[type="range"]::-moz-range-thumb {
  width: 14px;
  height: 14px;
  background: #ffffff;
  border: 2px solid #ffcc00;
  border-radius: 50%;
  cursor: pointer;
  box-shadow: 0 0 5px rgba(255, 204, 0, 0.5);
  transition: transform 0.3s ease;
}

input[type="range"]:hover::-webkit-slider-thumb {
  transform: scale(1.2);
}

input[type="range"]:hover::-moz-range-thumb {
  transform: scale(1.2);
}
</style>