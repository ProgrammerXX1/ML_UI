<template>
  <div class="space-y-4">
    <!-- System input -->
    <div>
      <label class="text-xs text-neutral-400">SYSTEM</label>
      <input
        type="text"
        placeholder="Enter system message (Optional)"
        class="w-full mt-1 px-4 py-2 rounded-md bg-[#1a1a1a] border border-[#333] text-sm text-white"
      />
    </div>

    <!-- User input -->
    <div>
      <label class="text-xs text-neutral-400 mb-1 block">USER</label>
      <textarea
        rows="8"
        placeholder="Enter user message or drag image here..."
        class="w-full px-4 py-3 rounded-md bg-[#1a1a1a] border border-[#333] text-sm text-white resize-none"
      ></textarea>
    </div>
  </div>
</template>
