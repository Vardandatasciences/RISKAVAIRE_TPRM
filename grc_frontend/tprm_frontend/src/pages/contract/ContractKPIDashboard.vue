<template>
  <div class="space-y-6 contract-kpi-dashboard-page">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold text-foreground">Contract Management KPI Dashboard</h1>
        <p class="text-muted-foreground">Track key performance indicators and contract metrics</p>
      </div>
      <div class="flex items-center gap-2 text-sm text-muted-foreground">
        <CalendarIcon class="h-4 w-4" />
        <span>Period: Jan 2024 - Dec 2024</span>
      </div>
    </div>

    <!-- Top Important KPIs Row -->
    <div class="mb-8">
      <h2 class="text-xl font-semibold text-foreground mb-4 flex items-center gap-2">
        <TrendingUpIcon class="h-5 w-5" />
        Key Performance Indicators
      </h2>
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
        <!-- Contract Risk Exposure -->
        <Card class="kpi-card border-2 border-primary/20 shadow-lg">
          <CardHeader class="pb-2">
            <CardTitle class="text-lg font-bold text-primary">Contract Risk Exposure</CardTitle>
            <CardDescription>Contracts by risk level</CardDescription>
          </CardHeader>
          <CardContent>
            <div class="w-full h-[250px]">
              <canvas ref="riskExposureChart" width="400" height="250"></canvas>
            </div>
          </CardContent>
        </Card>

        <!-- Compliance Rate -->
        <Card class="kpi-card border-2 border-primary/20 shadow-lg">
          <CardHeader class="pb-2">
            <CardTitle class="text-lg font-bold text-primary">Compliance Rate</CardTitle>
            <CardDescription>Overall contract compliance</CardDescription>
          </CardHeader>
          <CardContent>
            <div class="w-full h-[250px]">
              <canvas ref="complianceChart" width="400" height="250"></canvas>
            </div>
            <div class="text-center mt-2">
              <span class="text-2xl font-bold text-primary">92%</span>
              <p class="text-xs text-muted-foreground">Compliant</p>
            </div>
          </CardContent>
        </Card>

        <!-- Vendor Performance Score -->
        <Card class="kpi-card border-2 border-primary/20 shadow-lg">
          <CardHeader class="pb-2">
            <CardTitle class="text-lg font-bold text-primary">Vendor Performance</CardTitle>
            <CardDescription>Multi-dimensional assessment</CardDescription>
          </CardHeader>
          <CardContent>
            <div class="w-full h-[250px]">
              <canvas ref="vendorPerformanceChart" width="400" height="250"></canvas>
            </div>
          </CardContent>
        </Card>

        <!-- Amendments per Contract -->
        <Card class="kpi-card border-2 border-primary/20 shadow-lg">
          <CardHeader class="pb-2">
            <CardTitle class="text-lg font-bold text-primary">Contract Amendments</CardTitle>
            <CardDescription>Amendments by contract</CardDescription>
          </CardHeader>
          <CardContent>
            <div class="w-full h-[250px]">
              <canvas ref="amendmentsChart" width="400" height="250"></canvas>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>

    <!-- Row 2 - Three KPIs -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <!-- Time to Finalize Contract -->
      <Card class="kpi-card">
        <CardHeader>
          <CardTitle>Time to Approve Contract</CardTitle>
          <CardDescription>Average days to complete contract finalization</CardDescription>
        </CardHeader>
        <CardContent>
          <div class="w-full h-[300px]">
            <canvas ref="timeToFinalizeChart" width="400" height="300"></canvas>
          </div>
        </CardContent>
      </Card>

      <!-- Contracts Expiring Soon -->
      <Card class="kpi-card">
        <CardHeader>
          <CardTitle>Contracts Expiring Soon</CardTitle>
          <CardDescription>Number of contracts expiring by period</CardDescription>
        </CardHeader>
        <CardContent>
          <div class="w-full h-[300px]">
            <canvas ref="contractsExpiringChart" width="400" height="300"></canvas>
          </div>
          <!-- Contract Breakdown Stats -->
          <div class="mt-4 pt-4 border-t border-border">
            <div class="grid grid-cols-2 gap-3 text-xs">
              <div class="flex items-center justify-between">
                <span class="text-muted-foreground">Future Expiring:</span>
                <span class="font-semibold text-primary">{{ expiringStatistics.total_future_expiring }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-muted-foreground">Already Expired:</span>
                <span class="font-semibold text-red-600">{{ expiringStatistics.already_expired }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-muted-foreground">No End Date:</span>
                <span class="font-semibold text-yellow-600">{{ expiringStatistics.no_end_date }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-muted-foreground font-bold">Total Contracts:</span>
                <span class="font-bold text-lg text-primary">{{ expiringStatistics.total_all_contracts }}</span>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      <!-- Business Criticality -->
      <Card class="kpi-card">
        <CardHeader>
          <CardTitle>Business Critical Contracts</CardTitle>
          <CardDescription>Contracts by strategic importance level</CardDescription>
        </CardHeader>
        <CardContent>
          <div class="w-full h-[300px]">
            <canvas ref="businessCriticalityChart" width="400" height="300"></canvas>
          </div>
          <!-- Statistics -->
          <div class="mt-4 pt-4 border-t border-border">
            <div class="grid grid-cols-2 gap-3 text-xs">
              <div class="flex items-center justify-between">
                <span class="text-muted-foreground">Critical:</span>
                <span class="font-semibold text-red-600">{{ criticalityStatistics.critical_contracts }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-muted-foreground">High Risk:</span>
                <span class="font-semibold text-orange-600">{{ criticalityStatistics.high_risk_contracts }}</span>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- Row 3 - Three KPIs -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <!-- Early Termination Rate -->
      <Card class="kpi-card">
        <CardHeader>
          <CardTitle>Early Termination Rate</CardTitle>
          <CardDescription>Termination percentage by contract type</CardDescription>
        </CardHeader>
        <CardContent>
          <div class="w-full h-[300px]">
            <canvas ref="terminationRateChart" width="400" height="300"></canvas>
          </div>
        </CardContent>
      </Card>

      <!-- Average Contract Value by Type -->
      <Card class="kpi-card">
        <CardHeader>
          <CardTitle>Average Contract Value by Type</CardTitle>
          <CardDescription>Compare contract values across different types</CardDescription>
        </CardHeader>
        <CardContent>
          <div class="w-full h-[300px]">
            <canvas ref="avgValueByTypeChart" width="400" height="300"></canvas>
          </div>
          <!-- Statistics -->
          <div class="mt-4 pt-4 border-t border-border">
            <div class="grid grid-cols-2 gap-3 text-xs">
              <div class="flex items-center justify-between">
                <span class="text-muted-foreground">Total Portfolio:</span>
                <span class="font-semibold text-primary">${{ formatCurrency(avgValueStatistics.total_portfolio_value) }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-muted-foreground">Overall Average:</span>
                <span class="font-semibold text-primary">${{ formatCurrency(avgValueStatistics.overall_average) }}</span>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      <!-- Total Liability Exposure -->
      <Card class="kpi-card">
        <CardHeader>
          <CardTitle>Total Liability Exposure</CardTitle>
          <CardDescription>Contract liability with risk threshold</CardDescription>
        </CardHeader>
        <CardContent>
          <div class="w-full h-[300px]">
            <canvas ref="liabilityExposureChart" width="400" height="300"></canvas>
          </div>
          <!-- Statistics -->
          <div class="mt-4 pt-4 border-t border-border">
            <div class="grid grid-cols-2 gap-3 text-xs">
              <div class="flex items-center justify-between">
                <span class="text-muted-foreground">Total Exposure:</span>
                <span class="font-semibold" :style="{ color: contract_getColorBlindFriendlyColor(liabilityData.risk_assessment.color, liabilityData.risk_assessment.level === 'low' ? 'success' : liabilityData.risk_assessment.level === 'medium' ? 'warning' : 'error') }">
                  ${{ formatCurrency(liabilityData.total_liability_exposure) }}
                </span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-muted-foreground">Risk Level:</span>
                <span class="font-semibold" :style="{ color: contract_getColorBlindFriendlyColor(liabilityData.risk_assessment.color, liabilityData.risk_assessment.level === 'low' ? 'success' : liabilityData.risk_assessment.level === 'medium' ? 'warning' : 'error') }">
                  {{ liabilityData.risk_assessment.label }}
                </span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-muted-foreground">Avg Liability:</span>
                <span class="font-semibold text-primary">${{ formatCurrency(liabilityData.average_liability) }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-muted-foreground">Contracts:</span>
                <span class="font-semibold text-primary">{{ liabilityData.contracts_with_liability }}</span>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import loggingService from '@/services/loggingService'
import contractsApi from '@/services/contractsApi'
import { 
  Card, CardContent, CardDescription, CardHeader, CardTitle
} from '@/components/ui_contract'
import { 
  CalendarIcon, TrendingUpIcon 
} from 'lucide-vue-next'
import { useColorBlindness } from '@/assets/components/useColorBlindness.js'

// Chart.js imports
import Chart from 'chart.js/auto'

// Chart refs
const riskExposureChart = ref(null)
const complianceChart = ref(null)
const vendorPerformanceChart = ref(null)
const amendmentsChart = ref(null)
const timeToFinalizeChart = ref(null)
const contractsExpiringChart = ref(null)
const businessCriticalityChart = ref(null)
const terminationRateChart = ref(null)
const avgValueByTypeChart = ref(null)
const liabilityExposureChart = ref(null)

// Get color-blindness state
const { colorBlindness } = useColorBlindness()

// Helper function to get computed CSS variable value
const getComputedCSSVariable = (variableName) => {
  if (typeof document === 'undefined') return null
  return getComputedStyle(document.documentElement).getPropertyValue(variableName).trim()
}

// Helper function to get color-blind friendly color
const contract_getColorBlindFriendlyColor = (defaultColor, type) => {
  if (colorBlindness.value === 'off') {
    return defaultColor
  }

  // Map colors to CSS variables based on type
  const colorMap = {
    primary: {
      protanopia: 'var(--cb-primary)',
      deuteranopia: 'var(--cb-primary)',
      tritanopia: 'var(--cb-primary)',
    },
    success: {
      protanopia: 'var(--cb-success)',
      deuteranopia: 'var(--cb-success)',
      tritanopia: 'var(--cb-success)',
    },
    error: {
      protanopia: 'var(--cb-error)',
      deuteranopia: 'var(--cb-error)',
      tritanopia: 'var(--cb-error)',
    },
    warning: {
      protanopia: 'var(--cb-warning)',
      deuteranopia: 'var(--cb-warning)',
      tritanopia: 'var(--cb-warning)',
    },
    accent: {
      protanopia: 'var(--cb-accent-purple)',
      deuteranopia: 'var(--cb-accent-purple)',
      tritanopia: 'var(--cb-accent-purple)',
    },
  }

  const cssVar = colorMap[type]?.[colorBlindness.value]
  if (!cssVar) return defaultColor
  
  // For Chart.js, get the actual computed color value
  if (cssVar.startsWith('var(')) {
    const varName = cssVar.match(/var\(--([^)]+)\)/)?.[1]
    if (varName) {
      const computedValue = getComputedCSSVariable(`--${varName}`)
      return computedValue || defaultColor
    }
  }
  
  return cssVar || defaultColor
}

// Color constants with color-blind friendly support
const COLORS = computed(() => ({
  primary: contract_getColorBlindFriendlyColor('hsl(var(--primary))', 'primary'),
  secondary: 'hsl(var(--secondary))',
  accent: contract_getColorBlindFriendlyColor('hsl(var(--accent))', 'accent'),
  muted: 'hsl(var(--muted))',
  green: contract_getColorBlindFriendlyColor('hsl(142, 76%, 36%)', 'success'),
  yellow: contract_getColorBlindFriendlyColor('hsl(48, 96%, 53%)', 'warning'),
  red: contract_getColorBlindFriendlyColor('hsl(0, 84%, 60%)', 'error'),
  blue: contract_getColorBlindFriendlyColor('hsl(217, 91%, 60%)', 'primary'),
  purple: contract_getColorBlindFriendlyColor('hsl(271, 91%, 65%)', 'accent'),
  orange: contract_getColorBlindFriendlyColor('hsl(24, 95%, 53%)', 'warning')
}))

// Time to approve data - will be fetched from API
const timeToFinalizeData = ref([
  { month: 'Jan', days: 0 },
  { month: 'Feb', days: 0 },
  { month: 'Mar', days: 0 },
  { month: 'Apr', days: 0 },
  { month: 'May', days: 0 },
  { month: 'Jun', days: 0 },
  { month: 'Jul', days: 0 },
  { month: 'Aug', days: 0 },
  { month: 'Sep', days: 0 },
  { month: 'Oct', days: 0 },
  { month: 'Nov', days: 0 },
  { month: 'Dec', days: 0 }
])

// Time to approve statistics
const timeToApproveStatistics = ref({
  year: new Date().getFullYear(),
  overall_average_days: 0,
  fastest_month: '',
  fastest_days: 0,
  slowest_month: '',
  slowest_days: 0,
  total_approvals: 0,
  months_with_data: 0
})

const complianceData = computed(() => [
  { name: 'Compliant', value: 92, color: COLORS.value.blue },
  { name: 'Non-Compliant', value: 8, color: 'hsl(var(--muted))' }
])

// Risk exposure data - will be fetched from API
const riskExposureData = ref([
  { level: 'Low', count: 0, color: 'hsl(var(--primary))' },
  { level: 'Medium', count: 0, color: 'hsl(142, 76%, 36%)' },
  { level: 'High', count: 0, color: 'hsl(48, 96%, 53%)' },
  { level: 'Critical', count: 0, color: 'hsl(0, 84%, 60%)' }
])

// Risk exposure statistics
const riskExposureStatistics = ref({
  total_contracts: 0,
  total_risk_records: 0,
  contracts_with_critical: 0,
  contracts_with_high: 0,
  contracts_with_critical_or_high: 0,
  average_risks_per_contract: 0
})

// Contracts expiring data - will be fetched from API
const contractsExpiringDataRaw = ref([
  { period: '0-30 days', count: 0, start_date: null, end_date: null },
  { period: '31-60 days', count: 0, start_date: null, end_date: null },
  { period: '61-90 days', count: 0, start_date: null, end_date: null },
  { period: '90+ days', count: 0, start_date: null, end_date: null }
])

const contractsExpiringData = computed(() => {
  return contractsExpiringDataRaw.value.map(item => {
    let color = COLORS.value.green
    if (item.period === '0-30 days') color = COLORS.value.red
    else if (item.period === '31-60 days') color = COLORS.value.yellow
    else if (item.period === '61-90 days') color = COLORS.value.blue
    return { ...item, color }
  })
})

const vendorPerformanceData = ref([
  { metric: 'Quality', score: 88, fullMark: 100 },
  { metric: 'Timeliness', score: 92, fullMark: 100 },
  { metric: 'SLA', score: 85, fullMark: 100 },
  { metric: 'Cost', score: 90, fullMark: 100 },
  { metric: 'Communication', score: 87, fullMark: 100 },
  { metric: 'Innovation', score: 83, fullMark: 100 }
])

// Business criticality data - will be fetched from API
const businessCriticalityData = ref([])

// Business criticality statistics
const criticalityStatistics = ref({
  total_with_criticality: 0,
  critical_contracts: 0,
  high_risk_contracts: 0,
  no_criticality_data: 0,
  total_contracts: 0
})

// Termination rate data - will be fetched from API
const terminationRateData = ref([])

// Termination rate statistics
const terminationRateStatistics = ref({
  total_contracts: 0,
  total_early_terminated: 0,
  overall_termination_rate: 0,
  highest_rate_type: '',
  lowest_rate_type: '',
  contract_types_analyzed: 0
})

// Amendments data - will be fetched from API
const amendmentsData = ref([])

// Contracts expiring soon statistics
const expiringStatistics = ref({
  total_future_expiring: 0,
  urgent_expiring: 0,
  already_expired: 0,
  no_end_date: 0,
  total_with_end_dates: 0,
  total_all_contracts: 0
})

// Average contract value by type data - will be fetched from API
const avgValueByTypeData = ref([])

// Average value statistics
const avgValueStatistics = ref({
  overall_average: 0,
  total_portfolio_value: 0,
  total_contracts: 0,
  types_count: 0
})

// Total liability exposure data
const liabilityData = ref({
  total_liability_exposure: 0,
  average_liability: 0,
  contracts_with_liability: 0,
  contracts_without_liability: 0,
  total_contracts: 0,
  risk_assessment: {
    level: 'low',
    label: 'Low Risk',
    color: '#22c55e' // Will be converted to color-blind friendly in chart
  },
  thresholds: [],
  currency: 'USD'
})

// Currency formatter helper
const formatCurrency = (value) => {
  if (!value) return '0'
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(value)
}

// Fetch amendments KPI data from API
const fetchAmendmentsKPI = async () => {
  try {
    const response = await contractsApi.getContractAmendmentsKPI(6) // Get top 6 contracts
    if (response.success && response.data) {
      const amendments = response.data.amendments_by_contract
      // Transform API data to match chart format
      amendmentsData.value = amendments.map(item => ({
        contract: item.contract_code,
        amendments: item.amendment_count,
        contract_id: item.contract_id,
        contract_title: item.contract_title
      }))
    }
  } catch (error) {
    console.error('Error fetching amendments KPI:', error)
    // Fallback to empty data if API fails
    amendmentsData.value = []
  }
}

// Fetch contracts expiring soon KPI data from API
const fetchContractsExpiringSoonKPI = async () => {
  try {
    console.log('🔍 Fetching Contracts Expiring Soon KPI...')
    const response = await contractsApi.getContractsExpiringSoonKPI()
    console.log('📊 Full API Response:', response)
    
    if (response.success && response.data) {
      const expiring = response.data.expiring_contracts
      console.log('📅 Expiring Contracts Data:', expiring)
      console.log('📈 Statistics:', response.data.statistics)
      
      // Transform API data to match chart format
      const expiringData = expiring.map(item => {
        // Assign colors based on period
        let color = COLORS.value.green
        if (item.period === '0-30 days') color = COLORS.value.red
        else if (item.period === '31-60 days') color = COLORS.value.yellow
        else if (item.period === '61-90 days') color = COLORS.value.blue
        
        console.log(`  Period: ${item.period}, Count: ${item.count}, Color: ${color}`)
        
        return {
          period: item.period,
          count: item.count,
          color: color,
          start_date: item.start_date,
          end_date: item.end_date
        }
      })
      
      // Update the raw data
      contractsExpiringDataRaw.value = expiringData.map(item => ({
        period: item.period,
        count: item.count,
        start_date: item.start_date,
        end_date: item.end_date
      }))
      
      // Update statistics
      expiringStatistics.value = response.data.statistics
      
      // Log breakdown for debugging
      console.log('📊 CONTRACT BREAKDOWN:')
      console.log(`  ✅ Future Expiring (shown in chart): ${response.data.statistics.total_future_expiring}`)
      console.log(`  ⚠️  Urgent (0-30 days): ${response.data.statistics.urgent_expiring}`)
      console.log(`  ❌ Already Expired: ${response.data.statistics.already_expired}`)
      console.log(`  ❓ No End Date: ${response.data.statistics.no_end_date}`)
      console.log(`  📝 Total with End Dates: ${response.data.statistics.total_with_end_dates}`)
      console.log(`  🎯 TOTAL ALL CONTRACTS: ${response.data.statistics.total_all_contracts}`)
      console.log(`  🔢 Sum Check: ${response.data.statistics.total_future_expiring} + ${response.data.statistics.already_expired} + ${response.data.statistics.no_end_date} = ${response.data.statistics.total_future_expiring + response.data.statistics.already_expired + response.data.statistics.no_end_date}`)
    }
  } catch (error) {
    console.error('❌ Error fetching contracts expiring soon KPI:', error)
    // Keep default data if API fails
  }
}

// Fetch average contract value by type KPI data from API
const fetchAvgValueByTypeKPI = async () => {
  try {
    console.log('💰 Fetching Average Contract Value by Type KPI...')
    const response = await contractsApi.getAverageContractValueByTypeKPI()
    console.log('📊 Avg Value Response:', response)
    
    if (response.success && response.data) {
      avgValueByTypeData.value = response.data.contract_types
      avgValueStatistics.value = response.data.statistics
      
      console.log('💵 Contract Value Data:', avgValueByTypeData.value)
      console.log('📈 Statistics:', avgValueStatistics.value)
    }
  } catch (error) {
    console.error('❌ Error fetching average contract value by type KPI:', error)
    // Keep empty data if API fails
  }
}

// Fetch business criticality KPI data from API
const fetchBusinessCriticalityKPI = async () => {
  try {
    console.log('🎯 Fetching Business Criticality KPI...')
    const response = await contractsApi.getBusinessCriticalityKPI()
    console.log('📊 Criticality Response:', response)
    
    if (response.success && response.data) {
      businessCriticalityData.value = response.data.criticality_levels
      criticalityStatistics.value = response.data.statistics
      
      console.log('🎯 Criticality Data:', businessCriticalityData.value)
      console.log('📊 CRITICALITY BREAKDOWN:')
      console.log(`  🔴 Critical: ${criticalityStatistics.value.critical_contracts}`)
      console.log(`  ⚠️  High Risk (Critical + High): ${criticalityStatistics.value.high_risk_contracts}`)
      console.log(`  📝 Total with data: ${criticalityStatistics.value.total_with_criticality}`)
      console.log(`  ❓ No criticality data: ${criticalityStatistics.value.no_criticality_data}`)
      console.log(`  🎯 Total contracts: ${criticalityStatistics.value.total_contracts}`)
    }
  } catch (error) {
    console.error('❌ Error fetching business criticality KPI:', error)
    // Keep empty data if API fails
  }
}

// Fetch total liability exposure KPI data from API
const fetchTotalLiabilityKPI = async () => {
  try {
    console.log('💼 Fetching Total Liability Exposure KPI...')
    const response = await contractsApi.getTotalLiabilityExposureKPI()
    console.log('📊 Liability Response:', response)
    
    if (response.success && response.data) {
      liabilityData.value = response.data
      
      console.log('💰 Liability Data:', liabilityData.value)
      console.log('📊 LIABILITY BREAKDOWN:')
      console.log(`  💵 Total Exposure: $${liabilityData.value.total_liability_exposure.toLocaleString()}`)
      console.log(`  📊 Average: $${liabilityData.value.average_liability.toLocaleString()}`)
      console.log(`  ⚠️  Risk Level: ${liabilityData.value.risk_assessment.label}`)
      console.log(`  📝 Contracts with Liability: ${liabilityData.value.contracts_with_liability}`)
      console.log(`  ❓ Contracts without Liability: ${liabilityData.value.contracts_without_liability}`)
    }
  } catch (error) {
    console.error('❌ Error fetching total liability exposure KPI:', error)
    // Keep default data if API fails
  }
}

// Fetch contract risk exposure KPI data from API
const fetchContractRiskExposureKPI = async () => {
  try {
    console.log('🛡️  Fetching Contract Risk Exposure KPI...')
    const response = await contractsApi.getContractRiskExposureKPI()
    console.log('📊 Risk Exposure Response:', response)
    
    if (response.success && response.data) {
      // Update risk exposure data from API
      riskExposureData.value = response.data.risk_levels
      riskExposureStatistics.value = response.data.statistics
      
      console.log('🛡️  Risk Exposure Data:', riskExposureData.value)
      console.log('📊 RISK EXPOSURE BREAKDOWN:')
      console.log(`  📄 Total Contracts: ${riskExposureStatistics.value.total_contracts}`)
      console.log(`  📝 Total Risk Records: ${riskExposureStatistics.value.total_risk_records}`)
      console.log(`  🔴 Contracts with Critical Risk: ${riskExposureStatistics.value.contracts_with_critical}`)
      console.log(`  ⚠️  Contracts with High Risk: ${riskExposureStatistics.value.contracts_with_high}`)
      console.log(`  🚨 Critical or High Risk: ${riskExposureStatistics.value.contracts_with_critical_or_high}`)
      console.log(`  📊 Avg Risks per Contract: ${riskExposureStatistics.value.average_risks_per_contract}`)
    }
  } catch (error) {
    console.error('❌ Error fetching contract risk exposure KPI:', error)
    // Keep default data if API fails
  }
}

// Fetch early termination rate KPI data from API
const fetchEarlyTerminationRateKPI = async () => {
  try {
    console.log('⚠️  Fetching Early Termination Rate KPI...')
    const response = await contractsApi.getEarlyTerminationRateKPI()
    console.log('📊 Termination Rate Response:', response)
    
    if (response.success && response.data) {
      // Transform API data to match chart format
      terminationRateData.value = response.data.termination_rates.map(item => ({
        type: item.contract_type_display,
        rate: item.termination_rate,
        total_contracts: item.total_contracts,
        early_terminated_count: item.early_terminated_count
      }))
      terminationRateStatistics.value = response.data.statistics
      
      console.log('⚠️  Termination Rate Data:', terminationRateData.value)
      console.log('📊 TERMINATION RATE BREAKDOWN:')
      console.log(`  📄 Total Contracts: ${terminationRateStatistics.value.total_contracts}`)
      console.log(`  ❌ Total Early Terminated: ${terminationRateStatistics.value.total_early_terminated}`)
      console.log(`  📊 Overall Rate: ${terminationRateStatistics.value.overall_termination_rate}%`)
      console.log(`  📈 Highest Rate: ${terminationRateStatistics.value.highest_rate_type}`)
      console.log(`  📉 Lowest Rate: ${terminationRateStatistics.value.lowest_rate_type}`)
    }
  } catch (error) {
    console.error('❌ Error fetching early termination rate KPI:', error)
    // Keep default data if API fails
  }
}

// Fetch time to approve contract KPI data from API
const fetchTimeToApproveContractKPI = async () => {
  try {
    console.log('⏱️  Fetching Time to Approve Contract KPI...')
    const response = await contractsApi.getTimeToApproveContractKPI()
    console.log('📊 Time to Approve Response:', response)
    
    if (response.success && response.data) {
      // Update time to approve data from API
      timeToFinalizeData.value = response.data.time_to_approve
      timeToApproveStatistics.value = response.data.statistics
      
      console.log('⏱️  Time to Approve Data:', timeToFinalizeData.value)
      console.log('📊 TIME TO APPROVE BREAKDOWN:')
      console.log(`  📅 Year: ${timeToApproveStatistics.value.year}`)
      console.log(`  📊 Overall Average: ${timeToApproveStatistics.value.overall_average_days} days`)
      console.log(`  ⚡ Fastest Month: ${timeToApproveStatistics.value.fastest_month} (${timeToApproveStatistics.value.fastest_days} days)`)
      console.log(`  🐌 Slowest Month: ${timeToApproveStatistics.value.slowest_month} (${timeToApproveStatistics.value.slowest_days} days)`)
      console.log(`  ✅ Total Approvals: ${timeToApproveStatistics.value.total_approvals}`)
      console.log(`  📈 Months with Data: ${timeToApproveStatistics.value.months_with_data}`)
    }
  } catch (error) {
    console.error('❌ Error fetching time to approve contract KPI:', error)
    // Keep default data if API fails
  }
}

// Chart creation functions
const createRiskExposureChart = () => {
  if (!riskExposureChart.value) return null
  const ctx = riskExposureChart.value.getContext('2d')
  
  // Map risk levels to color-blind friendly colors
  const riskColors = riskExposureData.value.map(d => {
    if (d.level === 'Low') return contract_getColorBlindFriendlyColor('hsl(var(--primary))', 'primary')
    if (d.level === 'Medium') return contract_getColorBlindFriendlyColor('hsl(142, 76%, 36%)', 'success')
    if (d.level === 'High') return contract_getColorBlindFriendlyColor('hsl(48, 96%, 53%)', 'warning')
    if (d.level === 'Critical') return contract_getColorBlindFriendlyColor('hsl(0, 84%, 60%)', 'error')
    return COLORS.value.orange
  })
  
  return new Chart(ctx, {
    type: 'bar',
    data: {
      labels: riskExposureData.value.map(d => d.level),
      datasets: [{
        label: 'Count',
        data: riskExposureData.value.map(d => d.count),
        backgroundColor: riskColors,
        borderRadius: 4,
        borderSkipped: false
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: 'rgba(255, 255, 255, 0.95)',
          titleColor: '#333',
          bodyColor: '#666',
          borderColor: '#ddd',
          borderWidth: 1,
          padding: 12,
          displayColors: true,
          boxPadding: 6
        }
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { color: 'hsl(var(--muted-foreground))', font: { size: 10 } },
          border: { color: 'hsl(var(--muted))' }
        },
        y: {
          grid: { display: false },
          ticks: { color: 'hsl(var(--muted-foreground))', font: { size: 10 } },
          border: { color: 'hsl(var(--muted))' }
        }
      }
    }
  })
}

const createComplianceChart = () => {
  if (!complianceChart.value) return null
  const ctx = complianceChart.value.getContext('2d')
  return new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: complianceData.value.map(d => d.name),
      datasets: [{
        data: complianceData.value.map(d => d.value),
        backgroundColor: [
          COLORS.value.blue,   // Blue color for compliant (92%) - professional primary
          'grey'        // White color for non-compliant (8%) - clean contrast
        ],
        borderWidth: 1,
        borderColor: 'hsl(var(--border))'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '60%',
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: 'rgba(255, 255, 255, 0.95)',
          titleColor: '#333',
          bodyColor: '#666',
          borderColor: '#ddd',
          borderWidth: 1,
          padding: 12,
          displayColors: true,
          boxPadding: 6
        }
      }
    }
  })
}

const createVendorPerformanceChart = () => {
  if (!vendorPerformanceChart.value) return null
  const ctx = vendorPerformanceChart.value.getContext('2d')
  return new Chart(ctx, {
    type: 'radar',
    data: {
      labels: vendorPerformanceData.value.map(d => d.metric),
      datasets: [{
        label: 'Score',
        data: vendorPerformanceData.value.map(d => d.score),
        backgroundColor: 'rgba(96, 150, 236, 0.2)',
        borderColor: COLORS.value.primary,
        borderWidth: 2,
        pointBackgroundColor: COLORS.value.primary,
        pointBorderColor: 'hsl(var(--background))',
        pointBorderWidth: 2,
        pointRadius: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        r: {
          beginAtZero: true,
          max: 100,
          grid: { display: false },
          ticks: { 
            color: 'hsl(var(--muted-foreground))', 
            font: { size: 8 },
            stepSize: 20
          },
          pointLabels: { 
            color: 'hsl(var(--muted-foreground))', 
            font: { size: 8 }
          },
          border: { color: 'hsl(var(--muted))' }
        }
      },
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: 'rgba(255, 255, 255, 0.95)',
          titleColor: '#333',
          bodyColor: '#666',
          borderColor: '#ddd',
          borderWidth: 1,
          padding: 12,
          displayColors: true,
          boxPadding: 6
        }
      }
    }
  })
}

const createAmendmentsChart = () => {
  if (!amendmentsChart.value) return null
  const ctx = amendmentsChart.value.getContext('2d')
  return new Chart(ctx, {
    type: 'bar',
    data: {
      labels: amendmentsData.value.map(d => d.contract),
      datasets: [{
        label: 'Amendments',
        data: amendmentsData.value.map(d => d.amendments),
        backgroundColor: COLORS.value.purple,
        borderRadius: 4,
        borderSkipped: false
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: 'rgba(255, 255, 255, 0.95)',
          titleColor: '#333',
          bodyColor: '#666',
          borderColor: '#ddd',
          borderWidth: 1,
          padding: 12,
          displayColors: true,
          boxPadding: 6
        }
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { color: 'hsl(var(--muted-foreground))', font: { size: 8 } },
          border: { color: 'hsl(var(--muted))' }
        },
        y: {
          grid: { display: false },
          ticks: { color: 'hsl(var(--muted-foreground))', font: { size: 10 } },
          border: { color: 'hsl(var(--muted))' }
        }
      }
    }
  })
}

const createTimeToFinalizeChart = () => {
  if (!timeToFinalizeChart.value) return null
  const ctx = timeToFinalizeChart.value.getContext('2d')
  return new Chart(ctx, {
    type: 'line',
    data: {
      labels: timeToFinalizeData.value.map(d => d.month),
      datasets: [{
        label: 'Days',
        data: timeToFinalizeData.value.map(d => d.days),
        borderColor: COLORS.value.primary,  // Primary color instead of black
        backgroundColor: 'lrgba(133, 227, 194, 0.1)',
        borderWidth: 3,
        pointBackgroundColor: COLORS.value.primary,
        pointBorderColor: 'hsl(var(--background))',
        pointBorderWidth: 2,
        pointRadius: 4,
        tension: 0.4,
        fill: false
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: 'rgba(255, 255, 255, 0.95)',
          titleColor: '#333',
          bodyColor: '#666',
          borderColor: '#ddd',
          borderWidth: 1,
          padding: 12,
          displayColors: true,
          boxPadding: 6
        }
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { color: 'hsl(var(--muted-foreground))', font: { size: 12 } },
          border: { color: 'hsl(var(--muted))' }
        },
        y: {
          grid: { display: false },
          ticks: { color: 'hsl(var(--muted-foreground))', font: { size: 12 } },
          border: { color: 'hsl(var(--muted))' }
        }
      }
    }
  })
}

const createContractsExpiringChart = () => {
  if (!contractsExpiringChart.value) return null
  const ctx = contractsExpiringChart.value.getContext('2d')
  return new Chart(ctx, {
    type: 'bar',
    data: {
      labels: contractsExpiringData.value.map(d => d.period),
      datasets: [{
        label: 'Contracts',
        data: contractsExpiringData.value.map(d => d.count),
        backgroundColor: contractsExpiringData.value.map(d => d.color),
        borderRadius: 4,
        borderSkipped: false
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: 'rgba(255, 255, 255, 0.95)',
          titleColor: '#333',
          bodyColor: '#666',
          borderColor: '#ddd',
          borderWidth: 1,
          padding: 12,
          displayColors: true,
          boxPadding: 6
        }
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { 
            color: 'hsl(var(--muted-foreground))', 
            font: { size: 10 },
            maxRotation: -45
          },
          border: { color: 'hsl(var(--muted))' }
        },
        y: {
          grid: { display: false },
          ticks: { color: 'hsl(var(--muted-foreground))', font: { size: 12 } },
          border: { color: 'hsl(var(--muted))' }
        }
      }
    }
  })
}

const createBusinessCriticalityChart = () => {
  if (!businessCriticalityChart.value) return null
  
  const ctx = businessCriticalityChart.value.getContext('2d')
  
  // Extract colors from the API data and convert to color-blind friendly
  const colors = businessCriticalityData.value.map(d => {
    // Map API colors to color-blind friendly colors
    const colorLower = (d.color || '').toLowerCase()
    if (colorLower.includes('red') || colorLower.includes('#ef') || colorLower.includes('#dc')) {
      return contract_getColorBlindFriendlyColor(d.color, 'error')
    }
    if (colorLower.includes('orange') || colorLower.includes('yellow') || colorLower.includes('#f5') || colorLower.includes('#f9')) {
      return contract_getColorBlindFriendlyColor(d.color, 'warning')
    }
    if (colorLower.includes('green') || colorLower.includes('#10') || colorLower.includes('#22')) {
      return contract_getColorBlindFriendlyColor(d.color, 'success')
    }
    if (colorLower.includes('blue') || colorLower.includes('#3b') || colorLower.includes('#25')) {
      return contract_getColorBlindFriendlyColor(d.color, 'primary')
    }
    return contract_getColorBlindFriendlyColor(d.color, 'primary')
  })
  
  return new Chart(ctx, {
    type: 'bar',
    data: {
      labels: businessCriticalityData.value.map(d => d.level_display),
      datasets: [{
        label: 'Contracts',
        data: businessCriticalityData.value.map(d => d.count),
        backgroundColor: colors,
        borderRadius: 4,
        borderSkipped: false
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: 'rgba(255, 255, 255, 0.95)',
          titleColor: '#333',
          bodyColor: '#666',
          borderColor: '#ddd',
          borderWidth: 1,
          padding: 12,
          displayColors: true,
          boxPadding: 6,
          callbacks: {
            label: function(context) {
              return `Contracts: ${context.parsed.y}`
            }
          }
        }
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { 
            color: 'hsl(var(--muted-foreground))', 
            font: { size: 11 }
          },
          border: { color: 'hsl(var(--muted))' }
        },
        y: {
          grid: { display: false },
          ticks: { 
            color: 'hsl(var(--muted-foreground))', 
            font: { size: 12 },
            stepSize: 1
          },
          border: { color: 'hsl(var(--muted))' }
        }
      }
    }
  })
}

const createTerminationRateChart = () => {
  if (!terminationRateChart.value) return null
  const ctx = terminationRateChart.value.getContext('2d')
  return new Chart(ctx, {
    type: 'bar',
    data: {
      labels: terminationRateData.value.map(d => d.type),
      datasets: [{
        label: 'Termination Rate',
        data: terminationRateData.value.map(d => d.rate),
        backgroundColor: COLORS.value.red,
        borderRadius: [0, 4, 4, 0],
        borderSkipped: false
      }]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: 'rgba(255, 255, 255, 0.95)',
          titleColor: '#333',
          bodyColor: '#666',
          borderColor: '#ddd',
          borderWidth: 1,
          padding: 12,
          displayColors: true,
          boxPadding: 6,
          callbacks: {
            label: function(context) {
              return `${context.parsed.x}%`
            }
          }
        }
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { color: 'hsl(var(--muted-foreground))', font: { size: 12 } },
          border: { color: 'hsl(var(--muted))' }
        },
        y: {
          grid: { display: false },
          ticks: { color: 'hsl(var(--muted-foreground))', font: { size: 10 } },
          border: { color: 'hsl(var(--muted))' }
        }
      }
    }
  })
}

const createAvgValueByTypeChart = () => {
  if (!avgValueByTypeChart.value) return null
  
  const ctx = avgValueByTypeChart.value.getContext('2d')
  
  // Generate colors for each contract type with color-blind friendly support
  const backgroundColors = [
    COLORS.value.blue,
    COLORS.value.green,
    COLORS.value.orange,
    COLORS.value.purple,
    COLORS.value.yellow,
    COLORS.value.red
  ]
  
  return new Chart(ctx, {
    type: 'bar',
    data: {
      labels: avgValueByTypeData.value.map(d => d.contract_type_display),
      datasets: [{
        label: 'Average Value (USD)',
        data: avgValueByTypeData.value.map(d => d.average_value),
        backgroundColor: backgroundColors.slice(0, avgValueByTypeData.value.length),
        borderRadius: 4,
        borderSkipped: false
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: 'rgba(255, 255, 255, 0.95)',
          titleColor: '#333',
          bodyColor: '#666',
          borderColor: '#ddd',
          borderWidth: 1,
          padding: 12,
          displayColors: true,
          boxPadding: 6,
          callbacks: {
            label: function(context) {
              const item = avgValueByTypeData.value[context.dataIndex]
              return [
                `Average: $${formatCurrency(item.average_value)}`,
                `Total: $${formatCurrency(item.total_value)}`,
                `Contracts: ${item.contract_count}`
              ]
            }
          }
        }
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { 
            color: 'hsl(var(--muted-foreground))', 
            font: { size: 10 },
            maxRotation: 45,
            minRotation: 0
          },
          border: { color: 'hsl(var(--muted))' }
        },
        y: {
          grid: { display: false },
          ticks: { 
            color: 'hsl(var(--muted-foreground))', 
            font: { size: 12 },
            callback: function(value) {
              return '$' + (value >= 1000 ? (value/1000).toFixed(0) + 'K' : value)
            }
          },
          border: { color: 'hsl(var(--muted))' }
        }
      }
    }
  })
}

const createLiabilityExposureChart = () => {
  if (!liabilityExposureChart.value) return null
  
  const ctx = liabilityExposureChart.value.getContext('2d')
  
  // Create gauge-style doughnut chart with threshold segments
  const totalLiability = liabilityData.value.total_liability_exposure
  const thresholds = liabilityData.value.thresholds
  
  // Find the current risk level position
  let currentThresholdIndex = 0
  for (let i = 0; i < thresholds.length; i++) {
    if (totalLiability < thresholds[i].max) {
      currentThresholdIndex = i
      break
    }
  }
  
  // Calculate the percentage within the current threshold
  const lowerBound = currentThresholdIndex > 0 ? thresholds[currentThresholdIndex - 1].max : 0
  const upperBound = thresholds[currentThresholdIndex].max
  const percentage = ((totalLiability - lowerBound) / (upperBound - lowerBound)) * 100
  
  // Create data for visualization
  const chartData = [
    percentage,  // Current position
    100 - percentage  // Remaining to next threshold
  ]
  
  return new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Current Exposure', 'Remaining to Next Level'],
      datasets: [{
        data: chartData,
        backgroundColor: [
          contract_getColorBlindFriendlyColor(liabilityData.value.risk_assessment.color, 
            liabilityData.value.risk_assessment.level === 'low' ? 'success' : 
            liabilityData.value.risk_assessment.level === 'medium' ? 'warning' : 'error'),
          'hsl(var(--muted))'
        ],
        borderWidth: 0,
        circumference: 180,
        rotation: 270
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '70%',
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: 'rgba(255, 255, 255, 0.95)',
          titleColor: '#333',
          bodyColor: '#666',
          borderColor: '#ddd',
          borderWidth: 1,
          padding: 12,
          displayColors: true,
          boxPadding: 6,
          callbacks: {
            label: function(context) {
              if (context.dataIndex === 0) {
                return [
                  `Exposure: $${formatCurrency(totalLiability)}`,
                  `Risk: ${liabilityData.value.risk_assessment.label}`,
                  `Current Level: ${thresholds[currentThresholdIndex].level}`
                ]
              }
              return `To Next Threshold: ${context.parsed.toFixed(1)}%`
            }
          }
        }
      }
    },
    plugins: [{
      id: 'centerText',
      afterDraw: (chart) => {
        const ctx = chart.ctx
        ctx.save()
        
        const centerX = chart.chartArea.left + (chart.chartArea.right - chart.chartArea.left) / 2
        const centerY = chart.chartArea.top + (chart.chartArea.bottom - chart.chartArea.top) / 2 + 20
        
        // Draw risk level
        ctx.font = 'bold 16px sans-serif'
        const riskColor = contract_getColorBlindFriendlyColor(liabilityData.value.risk_assessment.color,
          liabilityData.value.risk_assessment.level === 'low' ? 'success' : 
          liabilityData.value.risk_assessment.level === 'medium' ? 'warning' : 'error')
        ctx.fillStyle = riskColor
        ctx.textAlign = 'center'
        ctx.textBaseline = 'middle'
        ctx.fillText(liabilityData.value.risk_assessment.label, centerX, centerY)
        
        // Draw amount below
        ctx.font = '12px sans-serif'
        ctx.fillStyle = 'hsl(var(--muted-foreground))'
        ctx.fillText(`$${(totalLiability / 1000000).toFixed(1)}M`, centerX, centerY + 20)
        
        ctx.restore()
      }
    }]
  })
}

// Chart instances for cleanup
const chartInstances = ref({})

// Helper function to destroy existing chart
const destroyChart = (chartKey) => {
  if (chartInstances.value[chartKey]) {
    chartInstances.value[chartKey].destroy()
    chartInstances.value[chartKey] = null
  }
}

// Helper function to create or recreate chart
const recreateChart = (chartRef, chartKey, createFn) => {
  if (!chartRef.value) return
  destroyChart(chartKey)
  const chart = createFn()
  if (chart) {
    chartInstances.value[chartKey] = chart
  }
}

// Watch for color-blindness changes and recreate charts
watch(colorBlindness, () => {
  // Recreate all charts when color-blindness mode changes
  if (riskExposureChart.value) recreateChart(riskExposureChart, 'riskExposure', createRiskExposureChart)
  if (complianceChart.value) recreateChart(complianceChart, 'compliance', createComplianceChart)
  if (vendorPerformanceChart.value) recreateChart(vendorPerformanceChart, 'vendorPerformance', createVendorPerformanceChart)
  if (amendmentsChart.value) recreateChart(amendmentsChart, 'amendments', createAmendmentsChart)
  if (timeToFinalizeChart.value) recreateChart(timeToFinalizeChart, 'timeToFinalize', createTimeToFinalizeChart)
  if (contractsExpiringChart.value) recreateChart(contractsExpiringChart, 'contractsExpiring', createContractsExpiringChart)
  if (businessCriticalityChart.value) recreateChart(businessCriticalityChart, 'businessCriticality', createBusinessCriticalityChart)
  if (terminationRateChart.value) recreateChart(terminationRateChart, 'terminationRate', createTerminationRateChart)
  if (avgValueByTypeChart.value) recreateChart(avgValueByTypeChart, 'avgValueByType', createAvgValueByTypeChart)
  if (liabilityExposureChart.value) recreateChart(liabilityExposureChart, 'liabilityExposure', createLiabilityExposureChart)
})

// Initialize all charts when component mounts
onMounted(async () => {
  await loggingService.logPageView('Contract', 'Contract KPI Dashboard')
  
  // Fetch KPI data from APIs first
  await fetchContractRiskExposureKPI()
  await fetchAmendmentsKPI()
  await fetchContractsExpiringSoonKPI()
  await fetchAvgValueByTypeKPI()
  await fetchBusinessCriticalityKPI()
  await fetchTotalLiabilityKPI()
  await fetchEarlyTerminationRateKPI()
  await fetchTimeToApproveContractKPI()
  
  // Create all charts
  if (riskExposureChart.value) {
    chartInstances.value.riskExposure = createRiskExposureChart()
  }
  if (complianceChart.value) {
    chartInstances.value.compliance = createComplianceChart()
  }
  if (vendorPerformanceChart.value) {
    chartInstances.value.vendorPerformance = createVendorPerformanceChart()
  }
  if (amendmentsChart.value) {
    chartInstances.value.amendments = createAmendmentsChart()
  }
  if (timeToFinalizeChart.value) {
    chartInstances.value.timeToFinalize = createTimeToFinalizeChart()
  }
  if (contractsExpiringChart.value) {
    chartInstances.value.contractsExpiring = createContractsExpiringChart()
  }
  if (businessCriticalityChart.value) {
    chartInstances.value.businessCriticality = createBusinessCriticalityChart()
  }
  if (terminationRateChart.value) {
    chartInstances.value.terminationRate = createTerminationRateChart()
  }
  if (avgValueByTypeChart.value) {
    chartInstances.value.avgValueByType = createAvgValueByTypeChart()
  }
  if (liabilityExposureChart.value) {
    chartInstances.value.liabilityExposure = createLiabilityExposureChart()
  }
})
</script>

<style scoped>
@import '@/assets/components/contract_darktheme.css';
</style>

<style>
/* Remove hover effects from KPI cards */
.contract-kpi-dashboard-page .kpi-card:hover,
.contract-kpi-dashboard-page .kpi-card:hover .kpi-card-content,
.contract-kpi-dashboard-page .kpi-card-content:hover {
  background-color: #ffffff !important;
  background: #ffffff !important;
  box-shadow: inherit !important;
  transform: none !important;
  transition: none !important;
}
</style>
