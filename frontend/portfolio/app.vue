<!-- app.vue -->
<template>
  <NuxtLayout />
</template>
<script setup lang="ts">

const config = useRuntimeConfig();
const route = useRoute();
const baseUrl = `${config.public.baseUrl}`

useHead({
  meta:[
    {
      property: 'og:url',
      content: `${baseUrl}${route.path.replace(/\/$/, '')}`
    },
  ],
  link: [
    {
      rel: 'canonical',
      href: `${baseUrl}${route.path.replace(/\/$/, '')}`
    }
  ]
})
</script>
