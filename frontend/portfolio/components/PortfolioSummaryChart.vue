<template>
  <!--  ~/components/PortfolioSummaryChart.vue-->
  <client-only>
    <v-card class="mt-8 pa-4">
      <apexchart
          type="line"
          height="350"
          :options="chartOptions"
          :series="chartSeries"
      />
    </v-card>
  </client-only>
</template>

<script setup lang="ts">

// 👇 Build ApexChart options and series
import {ref} from "vue";
import type {PortfolioPoint} from "~/types/positionSummary";
import userService from "~/services/userService";

const chartOptions = ref({
  chart: {
    id: 'portfolio-line-chart',
    toolbar: {show: false},
    zoom: {enabled: false}
  },
  xaxis: {
    type: 'datetime',
    title: {text: 'Date'}
  },
  yaxis: {
    title: {text: 'Portfolio Value ($)'},
    labels: {
      formatter: (value: number) => value.toFixed(2)
    }
  },
  tooltip: {
    x: {format: 'yyyy-MM-dd'},
    y: {
      formatter: (val: number) => `$${val.toFixed(2)}`
    }
  }
})
// 👇 Generate series data reactively
const chartSeries = computed(() => {
  if (!portfolioSummary.value) return []
  return [
    {
      name: 'Portfolio Value',
      data: portfolioSummary.value.map(point => ({
        x: point.as_of_date,
        y: point.total_value
      }))
    }
  ]
})
const authStore = useAuthStore()

const {data: portfolioSummary} = await useAsyncData<PortfolioPoint[]>(`get-portfolio-summary-by-user-id`, async () => {
  const userId = authStore.user!.id
  const positionSummaries = await userService.getPortfolioSummaries(userId)
  return positionSummaries;
}, {lazy: true});

</script>
