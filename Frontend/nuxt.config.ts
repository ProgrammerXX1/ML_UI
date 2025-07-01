// nuxt.config.ts
export default defineNuxtConfig({
  ssr: true, // серверный рендеринг включён
  target: 'server',

  devServer: {
    host: 'localhost',
    port: 3000
  },

  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_URL,
      apiUrl: process.env.NUXT_PUBLIC_API_URL 
    }
  },

  css: ['@/assets/css/main.css'],

   modules: [
    "@nuxt/eslint",
    "shadcn-nuxt",
    "@nuxtjs/tailwindcss",
    "@nuxtjs/color-mode",
    '@pinia/nuxt'
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
