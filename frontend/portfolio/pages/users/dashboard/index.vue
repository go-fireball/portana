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
          <div class="text-end pe-4">{{ formatCurrency(item.total_cost) }}</div>
        </template>
        <template #item.current_price="{ item }">
          <div class="text-end pe-4">{{ formatCurrency(item.current_price) }}</div>
        </template>

        <template #item.total_value="{ item }">
          <div class="text-end pe-4">{{ formatCurrency(item.total_value) }}</div>
        </template>

        <template #item.pnl="{ item }">
          <div class="text-end pe-4">{{ formatCurrency(item.pnl) }}</div>
        </template>

        <template v-slot:tfoot>
          <tr>
            <td class="text-end pe-4">TOTAL</td>
            <td class="text-end pe-4"> </td>
            <td class="text-end pe-4">{{ formatCurrency(computedTotal?.totalCost) }}</td>
            <td class="text-end pe-4">&nbsp;</td> <!-- No total current price -->
            <td class="text-end pe-4">{{ formatCurrency(computedTotal?.totalValue) }}</td>
            <td class="text-end pe-4">{{ formatCurrency(computedTotal?.totalPnl) }}</td>
          </tr>
        </template>

      </v-data-table>

      <!-- 📊 Portfolio Line Chart -->
      <client-only>
        <v-card class="mt-8 pa-4">
          <PortfolioSummaryChart/>
        </v-card>
      </client-only>

      <client-only>
        <v-card class="mt-8 pa-4">
          <PortfolioRollingReturnChart/>
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
  {title: 'Current Price', value: 'current_price'},
  {title: 'Total Value', value: 'total_value'},
  {title: 'P/L', value: 'pnl'},

]

const authStore = useAuthStore()

const loading = ref(false)
const formatCurrency = (value: any, decimals = 2, locale = 'en-US', currency = 'USD') => {
  if (typeof value !== 'number' || isNaN(value)) {
    return '-'; // Or '$0.00' or ''
  }

  // Create a formatter for currency with accounting style for negatives
  const formatter = new Intl.NumberFormat(locale, {
    style: 'currency',
    currency: currency,
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
    currencySign: 'accounting', // This is the key for parentheses on negatives
  });

  return formatter.format(value);
}
const computedTotal = computed(() => {
  if (!computedPositions.value.length) return null;

  let totalQuantity = 0;
  let totalCost = 0;
  let totalValue = 0;
  let totalPnl = 0;

  for (const pos of computedPositions.value) {
    totalQuantity += pos.quantity;
    totalCost += pos.total_cost;
    totalValue += pos.total_value;
    totalPnl += pos.pnl;
  }

  return {
    totalQuantity,
    totalCost,
    totalValue,
    totalPnl,
  };
});


const computedPositions = computed(() => {
  if (!positions.value || !prices.value) return []

  const priceMap = new Map(prices.value.map(p => [p.symbol, p.price]))

  return positions.value.map(pos => {
    const isOptions = pos.symbol.includes('_')
    const current_price = priceMap.get(pos.symbol) ?? 0
    const quantity = pos.quantity
    const total_cost = pos.total_cost ?? 0

    let total_value = quantity * current_price
    total_value = isOptions ? total_value * 100 : total_value
    const pnl = total_value - total_cost
    const pnl_percent = total_cost !== 0 ? (pnl / total_cost) * 100 : 0

    return {
      ...pos,
      current_price: current_price,
      total_value: total_value,
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

const {data: prices} = await useAsyncData<Price[]>('get-prices', async () => {
  const userId = authStore.user!.id
  return await priceService.getPrices()
}, {lazy: true})


</script>
