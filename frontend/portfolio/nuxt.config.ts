// https://nuxt.com/docs/api/configuration/nuxt-config

import vuetify from "vite-plugin-vuetify";

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
