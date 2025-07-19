import VueApexCharts from "vue3-apexcharts";
import type { Plugin } from 'vue'

export default defineNuxtPlugin((nuxtApp) => {
    nuxtApp.vueApp.use(VueApexCharts as Plugin)
    // nuxtApp.vueApp.component('apexchart', VueApexCharts)
})
