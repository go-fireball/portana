<template>
  <v-sheet color="background" class="pa-6" min-height="100vh">
    <v-container>
      <v-data-table
          :items="computedPositions || []"
          class="elevation-1 mt-4"
          :headers="headers"
          :loading="loading"
      >
        <template #item.quantity="{ item }">
          <div class="text-end pe-4">{{ item.quantity.toFixed(4) }}</div>
        </template>
        <template #item.total_cost="{ item }">
          <div class="text-end pe-4">{{ item.total_cost.toFixed(4) }}</div>
        </template>
        <template #item.current_price="{ item }">
          <div class="text-end pe-4">{{ item.current_price.toFixed(2) }}</div>
        </template>

        <template #item.total_value="{ item }">
          <div class="text-end pe-4">{{ item.total_value.toFixed(2) }}</div>
        </template>

        <template #item.pnl="{ item }">
          <div class="text-end pe-4">{{ item.pnl.toFixed(2) }}</div>
        </template>
      </v-data-table>

      <!-- 📊 Portfolio Line Chart -->
      <client-only>
        <v-card class="mt-8 pa-4">
          <PortfolioSummaryChart />
        </v-card>
      </client-only>

      <client-only>
        <v-card class="mt-8 pa-4">
          <PortfolioRollingReturnChart />
        </v-card>
      </client-only>
    </v-container>
  </v-sheet>
</template>

<script setup lang="ts">
import {ref, onMounted} from 'vue'
import type {PositionSummary} from '~/types/positionSummary'
import userService from "~/services/userService";
import PortfolioSummaryChart from "~/components/PortfolioSummaryChart.vue";
import type {Price} from "~/types/portfolioPoint";
import priceService from "~/services/priceService";


const headers = [
  {title: 'Symbol', value: 'symbol', sortable: true},
  {title: 'Quantity', value: 'quantity'},
  {title: 'Total Cost', value: 'total_cost'},
  { title: 'Current Price', value: 'current_price' },
  { title: 'Total Value', value: 'total_value' },
  { title: 'P/L', value: 'pnl' },

]

const authStore = useAuthStore()

const loading = ref(false)

const computedPositions = computed(() => {
  if (!positions.value || !prices.value) return []

  const priceMap = new Map(prices.value.map(p => [p.symbol, p.price]))

  return positions.value.map(pos => {
    const isOptions = pos.symbol.includes('_')
    const current_price = priceMap.get(pos.symbol) ?? 0
    const quantity = pos.quantity
    let total_cost = pos.total_cost ?? 0
    total_cost =  isOptions ? total_cost * 100 : total_cost
    let total_value = quantity * current_price
    total_value = isOptions ? total_value * 100 : total_value
    const pnl = total_value - total_cost
    const pnl_percent = total_cost !== 0 ? (pnl / total_cost) * 100 : 0

    return {
      ...pos,
      current_price,
      total_value,
      pnl,
      pnl_percent,
    }
  })
})


const {data: positions} = await useAsyncData<PositionSummary[]>(`get-position-summary-by-user-id`, async () => {
  const userId = authStore.user!.id
  const positionSummaries = await userService.getPositionSummaries(userId)
  return [...positionSummaries].sort((a, b) =>
      a.symbol.localeCompare(b.symbol)
  )
}, {lazy: true});

const{data:prices} = await useAsyncData<Price[]>('get-prices', async () => {
  const userId = authStore.user!.id
  return await priceService.getPrices()
}, {lazy: true})


</script>
