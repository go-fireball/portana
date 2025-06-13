<template>
  <client-only>
    <v-card class="mt-8 pa-4">
      <h3 class="text-h6 mb-2">7-Day Rolling Return</h3>
      <apexchart
          type="line"
          height="300"
          :options="chartOptions7d"
          :series="chartSeries7d"
      />
    </v-card>

    <v-card class="mt-8 pa-4">
      <h3 class="text-h6 mb-2">30-Day Rolling Return</h3>
      <apexchart
          type="line"
          height="300"
          :options="chartOptions30d"
          :series="chartSeries30d"
      />
    </v-card>
  </client-only>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import type { RollingReturnPoint } from '~/types/rollingReturnPoint'
import userService from '~/services/userService'

const authStore = useAuthStore()

// Base chart options
const baseChartOptions = {
  chart: {
    toolbar: { show: true },
    zoom: { enabled: false }
  },
  xaxis: {
    type: 'datetime',
    title: { text: 'Date' }
  },
  yaxis: {
    title: { text: 'Rolling Return (%)' },
    labels: {
      formatter: (val: number) => (val * 100).toFixed(2) + '%'
    }
  },
  tooltip: {
    x: { format: 'yyyy-MM-dd' },
    y: {
      formatter: (val: number) => (val * 100).toFixed(2) + '%'
    }
  }
}

const chartOptions7d = ref({ ...baseChartOptions })
const chartOptions30d = ref({ ...baseChartOptions })

const { data: rollingReturns } = await useAsyncData<RollingReturnPoint[]>(
    'get-rolling-returns',
    async () => {
      const userId = authStore.user!.id
      return await userService.getRollingReturns(userId)
    },
    { lazy: true }
)

const chartSeries7d = computed(() => {
  if (!rollingReturns.value) return []
  const map = new Map<string, { name: string; data: { x: string; y: number }[] }>()
  for (const point of rollingReturns.value) {
    const key = `${point.account_number}`
    if (!map.has(key)) map.set(key, { name: key, data: [] })
    map.get(key)!.data.push({ x: point.snapshot_date, y: point.rolling_return_7d })
  }
  return Array.from(map.values())
})

const chartSeries30d = computed(() => {
  if (!rollingReturns.value) return []
  const map = new Map<string, { name: string; data: { x: string; y: number }[] }>()
  for (const point of rollingReturns.value) {
    const key = `${point.account_number}`
    if (!map.has(key)) map.set(key, { name: key, data: [] })
    map.get(key)!.data.push({ x: point.snapshot_date, y: point.rolling_return_30d })
  }
  return Array.from(map.values())
})
</script>
