<template>
  <v-app-bar app color="primary">


    <v-spacer></v-spacer>

    <!-- Theme Toggle -->
    <v-btn
        icon
        variant="text"
        class="text-white mx-2"
        @click="toggleTheme"
    >
      <v-icon :icon="theme.global.name.value === 'light' ? mdiWeatherNight : mdiWhiteBalanceSunny"/>

    </v-btn>


  </v-app-bar>
</template>


<script setup>

import {useTheme} from 'vuetify'
import {mdiWeatherNight, mdiWhiteBalanceSunny} from '@mdi/js'


const theme = useTheme();


const toggleTheme = () => {
  theme.global.name.value = theme.global.name.value === 'light' ? 'dark' : 'light';
  if (import.meta.client) {
    localStorage.setItem('theme', theme.global.name.value);
  }
};


</script>
<style scoped>
.logo-img {
  height: 50px;
  width: 50px;
}

@media (max-width: 599px) {
  .logo-img {
    height: 40px;
    width: 40px;
  }
}


.logo-title {
  color: white;
  font-weight: bold;
  font-size: 1.2rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

@media (min-width: 600px) {
  .logo-title {
    font-size: 1.5rem;
  }
}

.logo-container {
  max-width: 100%;
  overflow: hidden;
}

</style>

