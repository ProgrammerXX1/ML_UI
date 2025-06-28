// nuxt.config.ts
export default defineNuxtConfig({
  ssr: true, // серверный рендеринг включён
  target: 'server',

  devServer: {
    host: '0.0.0.0',
    port: 3000
  },

  runtimeConfig: {
    public: {
      apiBase: process.env.API_BASE || 'http://localhost:8000' // URL FastAPI
    }
  },

  css: ['@/assets/css/tailwind.css'],

   modules: [
    "@nuxt/eslint",
    "shadcn-nuxt",
    "@nuxtjs/tailwindcss",
    "@nuxtjs/color-mode"
  ],

  colorMode: {
    classSuffix: ''
  },

  shadcn: {
    prefix: '',
    componentDir: './components/ui'
  },
  tailwindcss: {
    viewer: false
  },

  app: {
    head: {
      title: 'Chat UI',
      meta: [
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: 'Multichat system with ML backend' }
      ]
    }
  },

  nitro: {
    preset: 'node-server', // для запуска в Docker/Node
  }
})
