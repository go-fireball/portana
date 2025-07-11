<template>
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
import userService from "~/services/userService";
import type {RealizedPnlPoint, UnrealizedPnlPoint} from "~/types/portfolioPoint";

const authStore = useAuthStore()

const {data: realizedPnl} = await useAsyncData<RealizedPnlPoint[]>(`get-realized-pnl`, async () => {
  const userId = authStore.user!.id
  const realizedPnlPoints = await userService.getRealizedPnl(userId)
  return realizedPnlPoints;
}, {lazy: true});

const {data: unrealizedPnl} = await useAsyncData<UnrealizedPnlPoint[]>(`get-unrealized-pnl`, async () => {
  const userId = authStore.user!.id
  const unrealizedPnlPoints = await userService.getUnrealizedPnl(userId)
  return unrealizedPnlPoints;
}, {lazy: true});

const totalPnlSeries = computed(() => {
  const realized = realizedPnl.value || [];
  const unrealized = unrealizedPnl.value || [];

  // Convert to map for fast lookup by date
  const realizedMap = new Map(realized.map(p => [p.date, p.realized_pnl]));
  const unrealizedMap = new Map(unrealized.map(p => [p.date, p.unrealized_pnl]));

  // Merge dates from both sources
  const allDates = new Set([...realizedMap.keys(), ...unrealizedMap.keys()]);
  const sortedDates = Array.from(allDates).sort();

  return sortedDates.map(date => ({
    x: date,
    y: Math.round((realizedMap.get(date) || 0) + (unrealizedMap.get(date) || 0))
  }));
});

// Chart options
const chartOptions = {
  chart: {
    type: "line",
    zoom: { enabled: false }
  },
  stroke: {
    curve: "smooth"
  },
  xaxis: {
    type: "datetime",
    title: { text: "Date" }
  },
  yaxis: [
    {
      opposite: true,
      title: {
        text: "Realized PnL ($)"
      }
    },
    {
      title: {
        text: "Unrealized PnL ($)"
      }
    }
  ],
  tooltip: {
    x: {
      format: "yyyy-MM-dd"
    },
    y: {
      formatter: (val: number) => Math.round(val).toString()
    }
  },
  legend: {
    position: "top"
  }
};


// Build chart series
const chartSeries = computed(() => {
  return [
    {
      name: "Realized PnL",
      data: realizedPnl.value?.map(p => ({
        x: p.date,
        y: Math.round(p.realized_pnl)
      })) || [],
      yAxisIndex: 0 // Right axis (Realized)
    },
    {
      name: "Unrealized PnL",
      data: unrealizedPnl.value?.map(p => ({
        x: p.date,
        y: Math.round(p.unrealized_pnl)
      })) || [],
      yAxisIndex: 1 // Right axis (Realized)
    },
    {
      name: "Total PnL",
      data: totalPnlSeries.value,
      yAxisIndex: 0  // or a third axis if scale differs a lot
    }
  ];
});
</script>
