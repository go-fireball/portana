<template>
  <v-sheet color="background" class="pa-6" min-height="100vh">
    <v-container>
      <v-data-table
          :items="positions || []"
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
      </v-data-table>

      <!-- 📊 Portfolio Line Chart -->
      <client-only>
        <v-card class="mt-8 pa-4">

          <PortfolioSummaryChart />

        </v-card>
      </client-only>
    </v-container>
  </v-sheet>
</template>

<script setup lang="ts">
import {ref, onMounted} from 'vue'
import type {PortfolioPoint, PositionSummary} from '~/types/positionSummary'
import userService from "~/services/userService";
import PortfolioSummaryChart from "~/components/PortfolioSummaryChart.vue";


const headers = [
  {title: 'Symbol', value: 'symbol', sortable: true},
  {title: 'Quantity', value: 'quantity'},
  {title: 'Total Cost', value: 'total_cost'},
]

const authStore = useAuthStore()

const loading = ref(false)

const {data: positions} = await useAsyncData<PositionSummary[]>(`get-position-summary-by-user-id`, async () => {
  const userId = authStore.user!.id
  const positionSummaries = await userService.getPositionSummaries(userId)
  return [...positionSummaries].sort((a, b) =>
      a.symbol.localeCompare(b.symbol)
  )
}, {lazy: true});


</script>
