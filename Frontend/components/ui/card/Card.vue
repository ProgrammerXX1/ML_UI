<script setup lang="ts">
import type { HTMLAttributes } from 'vue'
import { cn } from '~/lib/utils'

const props = defineProps<{
  class?: HTMLAttributes['class']
}>()
</script>

<template>
  <div
    :class="
      cn(
        'rounded-lg border border-white/10 bg-gray-900/30 text-white backdrop-blur shadow-sm',
        props.class,
      )
    "
  >
    <slot />
  </div>
</template>
