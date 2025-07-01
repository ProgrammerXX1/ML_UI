```vue
<template>
  <div class="fixed bottom-4 left-4 z-10 hidden sm:block">
    <svg class="h-16 w-16 animate-neural-vortex" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
      <g class="nodes">
        <circle cx="50" cy="50" r="8" fill="none" stroke="#c084fc" stroke-width="2" class="node node-main" />
        <circle cx="40" cy="40" r="6" fill="none" stroke="#60a5fa" stroke-width="1.5" class="node node-1" />
        <circle cx="60" cy="40" r="6" fill="none" stroke="#60a5fa" stroke-width="1.5" class="node node-2" />
        <circle cx="50" cy="60" r="6" fill="none" stroke="#60a5fa" stroke-width="1.5" class="node node-3" />
        <circle cx="50" cy="50" r="10" fill="none" stroke="#a5b4fc" stroke-width="1" class="signal-pulse" />
      </g>
      <g class="connections">
        <path d="M50 50 L40 40" stroke="#a5b4fc" stroke-width="1" class="connection" />
        <path d="M50 50 L60 40" stroke="#a5b4fc" stroke-width="1" class="connection" />
        <path d="M50 50 L50 60" stroke="#a5b4fc" stroke-width="1" class="connection" />
      </g>
    </svg>
  </div>
</template>

<script setup lang="ts"></script>
```