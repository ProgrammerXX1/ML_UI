<template>
  <canvas
    ref="neuralMeshCanvas"
    class="absolute inset-0 z-0 pointer-events-none bg-transparent"
  ></canvas>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const neuralMeshCanvas = ref<HTMLCanvasElement | null>(null)

onMounted(() => {
  const canvas = neuralMeshCanvas.value
  if (!canvas) return

  // ВАЖНО: прозрачный контекст
  const ctx = canvas.getContext('2d', { alpha: true })
  if (!ctx) return

  const resizeCanvas = () => {
    canvas.width = window.innerWidth
    canvas.height = window.innerHeight
  }

  resizeCanvas()
  window.addEventListener('resize', resizeCanvas)

  const nodes = Array.from({ length: 30 }, () => ({
    x: Math.random() * canvas.width,
    y: Math.random() * canvas.height,
    vx: Math.random() * 0.5 - 0.25,
    vy: Math.random() * 0.5 - 0.25,
    radius: Math.random() * 2 + 1,
    isHub: Math.random() < 0.1,
    pulseTime: Math.random() * 5000,
  }))

  const animate = () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    const time = Date.now()

    nodes.forEach(node => {
      node.x += node.vx
      node.y += node.vy

      if (node.x < 0 || node.x > canvas.width) node.vx *= -1
      if (node.y < 0 || node.y > canvas.height) node.vy *= -1

      // точка
      ctx.fillStyle = node.isHub && Math.sin(time * 0.001 + node.pulseTime) > 0.5
        ? 'rgba(192, 132, 252, 0.8)'
        : 'rgba(192, 132, 252, 0.5)'

      ctx.beginPath()
      ctx.arc(node.x, node.y, node.radius, 0, Math.PI * 2)
      ctx.fill()

      // пульсация
      if (node.isHub && Math.sin(time * 0.001 + node.pulseTime) > 0.5) {
        ctx.strokeStyle = 'rgba(96, 165, 250, 0.3)'
        ctx.lineWidth = 1
        ctx.beginPath()
        ctx.arc(node.x, node.y, node.radius + (time % 5000) * 0.01, 0, Math.PI * 2)
        ctx.stroke()
      }

      // связи
      ctx.strokeStyle = 'rgba(96, 165, 250, 0.2)'
      ctx.lineWidth = 0.5
      nodes.forEach(other => {
        const dx = node.x - other.x
        const dy = node.y - other.y
        const distance = Math.sqrt(dx * dx + dy * dy)
        if (distance < 100) {
          ctx.beginPath()
          ctx.moveTo(node.x, node.y)
          ctx.lineTo(other.x, other.y)
          ctx.stroke()
        }
      })
    })

    requestAnimationFrame(animate)
  }

  animate()

  onUnmounted(() => {
    window.removeEventListener('resize', resizeCanvas)
  })
})
</script>
