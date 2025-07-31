<template>
  <div>
    <h3 class="text-h5 mb-4">Portfolio Metrics</h3>
    <v-tabs v-model="activeTab" slider-color="primary" centered>
      <v-tab value="performance">Performance</v-tab>
      <v-tab value="risk">Risk & Returns</v-tab>
    </v-tabs>

    <v-window v-model="activeTab" class="mt-4">
      <!-- Performance Metrics -->
      <v-window-item value="performance">
        <v-row>
          <v-col cols="12" md="6" v-for="(metric, index) in performanceMetrics" :key="index">
            <v-card class="pa-4">
              <div class="d-flex flex-column align-center">
                <div class="text-subtitle-1 mb-1 text-center">{{ metric.label }}</div>
                <div class="d-flex align-center">
                  <div :class="[`text-h4`, getValueColorClass(metric.value, metric.isPercentage)]">
                    {{ formatMetricValue(metric.value, metric.isPercentage) }}
                  </div>
                </div>
                <div class="text-caption text-medium-emphasis">{{ metric.description }}</div>
              </div>
            </v-card>
          </v-col>
        </v-row>
      </v-window-item>

      <!-- Risk Metrics -->
      <v-window-item value="risk">
        <v-row>
          <v-col cols="12" md="6" v-for="(metric, index) in riskMetrics" :key="index">
            <v-card class="pa-4">
              <div class="d-flex flex-column align-center">
                <div class="text-subtitle-1 mb-1 text-center">{{ metric.label }}</div>
                <div class="d-flex align-center">
                  <div :class="[`text-h4`, getValueColorClass(metric.value, metric.isPercentage)]">
                    {{ formatMetricValue(metric.value, metric.isPercentage) }}
                  </div>
                </div>
                <div class="text-caption text-medium-emphasis">{{ metric.description }}</div>
              </div>
            </v-card>
          </v-col>
        </v-row>
      </v-window-item>
    </v-window>

    <!-- Historical Metrics Chart -->
    <div v-if="portfolioMetrics && portfolioMetrics.length > 0" class="mt-6">
      <h4 class="text-subtitle-1 mb-3">Historical Portfolio Metrics</h4>
      <client-only>
        <apexchart
          type="line"
          height="400"
          :options="chartOptions"
          :series="chartSeries"
        />
      </client-only>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '~/stores/auth'
import userService from '~/services/userService'
import type { UserPortfolioMetric } from '~/types/portfolioPoint'

const authStore = useAuthStore()
const activeTab = ref('performance')

const {data: portfolioMetrics} = await useAsyncData('portfolio-metrics', async () => {
  const userId = authStore.user!.id
  return await userService.getUserPortfolioMetrics(userId)
}, {lazy: true})



// Format number as currency or percentage
const formatMetricValue = (value: number, isPercentage = false) => {
  if (isPercentage) {
    return `${value.toFixed(2)}%`
  } else {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    }).format(value)
  }
}

// Get color class based on value
const getValueColorClass = (value: number, isPercentage = false) => {
  if (!isPercentage) return ''
  return value > 0 ? 'text-success' : value < 0 ? 'text-error' : ''
}

// Get latest metrics
const latestMetrics = computed(() => {
  if (!portfolioMetrics.value || !portfolioMetrics.value.length) return null
  return portfolioMetrics.value.sort((a, b) => 
    new Date(b.snapshot_date).getTime() - new Date(a.snapshot_date).getTime()
  )[0]
})

// Performance metrics
const performanceMetrics = computed(() => {
  if (!latestMetrics.value) return []

  const metrics = [
    {
      label: 'Portfolio Value',
      value: latestMetrics.value.portfolio_value || 0,
      isPercentage: false,
      description: 'Total value of all portfolio holdings'
    },
    {
      label: 'Cash Balance',
      value: latestMetrics.value.cash_balance || 0,
      isPercentage: false,
      description: 'Available cash in your portfolio'
    },
    {
      label: 'Daily Return',
      value: (latestMetrics.value.daily_return || 0) * 100,
      isPercentage: true,
      description: 'Portfolio return for the most recent day'
    },
    {
      label: 'Time-Weighted Return',
      value: (latestMetrics.value.twr_to_date || 0) * 100,
      isPercentage: true,
      description: 'Total time-weighted return since inception'
    }
  ]

  return metrics
})

// Risk metrics
const riskMetrics = computed(() => {
  if (!latestMetrics.value) return []

  const metrics = [
    {
      label: '7-Day Rolling Return',
      value: (latestMetrics.value.rolling_return_7d || 0) * 100,
      isPercentage: true,
      description: 'Return over the last 7 days'
    },
    {
      label: '30-Day Rolling Return',
      value: (latestMetrics.value.rolling_return_30d || 0) * 100,
      isPercentage: true,
      description: 'Return over the last 30 days'
    },
    {
      label: 'Sharpe Ratio',
      value: latestMetrics.value.sharpe_to_date || 0,
      isPercentage: false,
      description: 'Risk-adjusted return metric (higher is better)'
    },
    {
      label: 'Maximum Drawdown',
      value: (latestMetrics.value.drawdown_to_date || 0) * 100,
      isPercentage: true,
      description: 'Largest peak-to-trough decline in portfolio value'
    }
  ]

  return metrics
})

const chartOptions = ref({
  chart: {
    id: 'metrics-chart',
    type: 'line',
    height: 350,
    toolbar: { show: true },
    zoom: { enabled: false }
  },
  stroke: {
    curve: 'smooth',
    width: 2
  },
  xaxis: {
    type: 'datetime',
    title: { text: 'Date' }
  },
  yaxis: {
    title: { text: 'Value (%)' },
    labels: {
      formatter: (val:number) => val.toFixed(2) + '%'
    }
  },
  tooltip: {
    x: { format: 'yyyy-MM-dd' },
    y: {
      formatter: (val:number) => val.toFixed(2) + '%'
    }
  },
  legend: {
    position: 'top'
  }
})

// Chart series data
const chartSeries = computed(() => {
  if (!portfolioMetrics.value || !portfolioMetrics.value.length) return []

  const sortedMetrics = [...portfolioMetrics.value].sort(
    (a, b) => new Date(a.snapshot_date).getTime() - new Date(b.snapshot_date).getTime()
  )

  return [
    {
      name: 'Time-Weighted Return',
      data: sortedMetrics.map(m => ({ 
        x: new Date(m.snapshot_date).getTime(),
        y: parseFloat(((m.twr_to_date || 0) * 100).toFixed(2)) 
      }))
    },
    {
      name: '7-Day Return',
      data: sortedMetrics.map(m => ({ 
        x: new Date(m.snapshot_date).getTime(),
        y: parseFloat(((m.rolling_return_7d || 0) * 100).toFixed(2)) 
      }))
    },
    {
      name: '30-Day Return',
      data: sortedMetrics.map(m => ({ 
        x: new Date(m.snapshot_date).getTime(),
        y: parseFloat(((m.rolling_return_30d || 0) * 100).toFixed(2)) 
      }))
    }
  ]
})
</script>

<style scoped>
.chart {
  width: 100%;
  height: 400px;
}
</style>
