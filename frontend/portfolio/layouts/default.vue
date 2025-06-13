<!-- layouts/default.vue -->
<template>
  <v-app>
    <NavBar />
    <v-main min-height="850px">
      <NuxtPage />
    </v-main>
    <Footer/>
  </v-app>
</template>

<script setup lang="ts">

import NavBar from '~/components/NavBar.vue';
import Footer from '~/components/Footer.vue';
import {useTheme} from "vuetify";


const theme = useTheme();

onMounted(() => {
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme === 'light' || savedTheme === 'dark') {
    theme.global.name.value = savedTheme;
  }
});
</script>
