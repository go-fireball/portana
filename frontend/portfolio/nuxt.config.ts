// https://nuxt.com/docs/api/configuration/nuxt-config

import vuetify from "vite-plugin-vuetify";
const baseUrl = process.env.NUXT_PUBLIC_BASE_URL || 'http://localhost:3000'
const apiUrl =  process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000'

export default defineNuxtConfig({
  compatibilityDate: '2025-05-15',
  devtools: { enabled: true },
  router: {
    options: {
      strict: false
    }
  },
  css: [
    'vuetify/styles',
  ],
  build: {
    transpile: ['vuetify'],
  },
  features:{
    inlineStyles: false,
  },
  modules: [
    '@pinia/nuxt',
    'pinia-plugin-persistedstate/nuxt',
  ],
  pinia: {
    storesDirs: ['./stores'],
  },
  runtimeConfig: {
    jwtSecret: '47c854fc16e617a25ad83a56a83c710d0538ffaf92a317020fb814ab1cb90757',
    public: {
      baseUrl: baseUrl,
      apiUrl: apiUrl
    },
  },
  vite: {
    ssr: {
      noExternal: ['vuetify'],
    },
    css: {
      preprocessorOptions: {
        less: {
          javascriptEnabled: true, // Example: Enable inline JavaScript in LESS
        },
      },
    },
    plugins: [
      vuetify({ autoImport: true }) // helps reduce bundle size
    ],
  },
})
