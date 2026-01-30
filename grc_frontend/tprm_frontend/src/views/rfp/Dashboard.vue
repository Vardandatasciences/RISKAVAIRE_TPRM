<template>
  <div class="space-y-4">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
      <div>
        <h1 class="text-3xl font-bold tracking-tight">Dashboard</h1>
        <p class="text-muted-foreground">
          Welcome back! Here's an overview of your RFP activities.
        </p>
      </div>
      <div class="flex gap-2">
        <a href="/rfp-list" class="button dashboard-action-link">
          <FileText class="h-4 w-4 text-blue-600" />
          Manage RFPs
        </a>
        <a href="/rfp-analytics" class="button dashboard-action-link">
          <BarChart3 class="h-4 w-4 text-blue-600" />
          View Analytics
        </a>
        <a href="/rfp-creation" class="button button--create">
          <Plus class="h-4 w-4" />
          Create RFP
        </a>
      </div>
    </div>

    <!-- KPI Cards -->
    <div class="kpi-cards-grid">
      <div v-for="(kpi, index) in kpiData" :key="index" class="kpi-card">
        <div class="kpi-card-content">
          <div :class="`kpi-card-icon-wrapper ${kpi.iconColor || 'kpi-card-icon-blue'}`">
            <component :is="kpi.icon" />
          </div>
          <div class="kpi-card-text">
            <h3 class="kpi-card-title">{{ kpi.title }}</h3>
            <div class="kpi-card-value">{{ kpi.value }}</div>
            <p class="kpi-card-subheading">{{ kpi.subheading || kpi.change }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent RFPs -->
    <Card class="phase-card">
      <div class="p-6">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h3 class="text-lg font-semibold">Recent RFPs</h3>
            <p class="text-sm text-muted-foreground">
              Your most recent RFP activities
            </p>
          </div>
          <a href="/rfp-list" class="button button--view text-sm font-semibold">
            View All
            <ArrowRight class="h-4 w-4" />
          </a>
        </div>
        <div class="space-y-4">
          <div 
            v-for="rfp in recentRFPs" 
            :key="rfp.id" 
            class="flex flex-col sm:flex-row sm:items-center justify-between p-4 border border-border rounded-lg hover-lift cursor-pointer overflow-hidden"
            @click="navigateToPhase(rfp.phase)"
          >
            <div class="space-y-2 sm:space-y-1 flex-1 min-w-0 pr-4">
              <div class="flex items-center gap-2 flex-wrap">
                <span class="font-medium">{{ rfp.id }}</span>
                <span :class="getStatusColor(rfp.status)">
                  {{ formatStatusText(rfp.status) }}
                </span>
              </div>
              <h3 class="font-medium truncate">{{ rfp.title }}</h3>
              <div class="flex items-center gap-4 text-sm text-muted-foreground flex-wrap">
                <span class="whitespace-nowrap">Phase {{ rfp.phase }}/{{ rfp.totalPhases }}</span>
                <span class="whitespace-nowrap">{{ rfp.value }}</span>
                <span class="flex items-center gap-1 whitespace-nowrap">
                  <Clock class="h-3 w-3 flex-shrink-0" />
                  <span class="truncate">{{ rfp.deadline }}</span>
                </span>
                <span class="flex items-center gap-1 whitespace-nowrap">
                  <Users class="h-3 w-3 flex-shrink-0" />
                  {{ rfp.vendors }} vendors
                </span>
              </div>
            </div>
            <div class="mt-3 sm:mt-0 sm:w-32 flex-shrink-0">
              <Progress :value="(rfp.phase / rfp.totalPhases) * 100" class="h-2" />
              <span class="text-xs text-muted-foreground mt-1 block">
                {{ Math.round((rfp.phase / rfp.totalPhases) * 100) }}% complete
              </span>
            </div>
          </div>
        </div>
      </div>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { ref, markRaw, onMounted, computed } from 'vue'
import Card from '@/components_rfp/Card.vue'
import Button from '@/components_rfp/Button.vue'
import Progress from '@/components_rfp/rfpProgress.vue'
import '@/assets/components/main.css'
import '@/assets/components/badge.css'
import '@/assets/components/rfp_darktheme.css'
import { useNotifications } from '@/composables/useNotifications'
import loggingService from '@/services/loggingService'
// Router removed - using MPA navigation
import { useRFPStore } from '@/store/index_rfp'
// Import global KPI card styles
import '@/assets/components/main.css'

// Icons
const FileText = markRaw({
  template: '<svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>'
})

const Building2 = markRaw({
  template: '<svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" /></svg>'
})

const Target = markRaw({
  template: '<svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>'
})

const DollarSign = markRaw({
  template: '<svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" /></svg>'
})

const TrendingUp = markRaw({
  template: '<svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" /></svg>'
})

const TrendingDown = markRaw({
  template: '<svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6" /></svg>'
})

const Clock = markRaw({
  template: '<svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>'
})

const Users = markRaw({
  template: '<svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" /></svg>'
})

const Plus = markRaw({
  template: '<svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" /></svg>'
})

const ArrowRight = markRaw({
  template: '<svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>'
})

const BarChart3 = markRaw({
  template: '<svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" /></svg>'
})

// Navigation functions for MPA
const navigateToPage = (url: string) => {
  window.location.href = url
}
const rfpStore = useRFPStore()

// Fetch RFPs when component mounts
onMounted(async () => {
  await loggingService.logRFPView()
  try {
    await rfpStore.fetchRFPs()
    console.log('RFPs loaded:', rfpStore.rfps)
  } catch (error) {
    console.error('Error loading RFPs:', error)
  }
})

// Computed properties for KPIs based on real data
const { showSuccess, showError, showWarning, showInfo } = useNotifications()

const kpiData = computed(() => {
  const activeRFPs = rfpStore.rfps.filter((rfp: any) => rfp.status === 'in_review' || rfp.status === 'published' || rfp.status === 'submission_open').length
  const draftRFPs = rfpStore.rfps.filter((rfp: any) => rfp.status === 'draft').length
  const totalRFPs = rfpStore.rfps.length
  const evaluationCriteria = rfpStore.rfps.reduce((total: number, rfp: any) => total + (rfp.criteriaCount || 0), 0)
  
  return [
    {
      title: "Active RFPs",
      value: activeRFPs.toString(),
      change: "Real-time data",
      subheading: `${activeRFPs} active RFPs`,
      trend: "up",
      icon: FileText,
      iconColor: "kpi-card-icon-green",
    },
    {
      title: "Draft RFPs",
      value: draftRFPs.toString(),
      change: "Real-time data",
      subheading: `${draftRFPs} draft RFPs`,
      trend: "up",
      icon: Building2,
      iconColor: "kpi-card-icon-orange",
    },
    {
      title: "Total RFPs",
      value: totalRFPs.toString(),
      change: "Real-time data",
      subheading: `${totalRFPs} total RFPs`,
      trend: "up",
      icon: Target,
      iconColor: "kpi-card-icon-red",
    },
    {
      title: "Evaluation Criteria",
      value: evaluationCriteria.toString(),
      change: "Real-time data",
      subheading: `${evaluationCriteria} total criteria`,
      trend: "up",
      icon: DollarSign,
      iconColor: "kpi-card-icon-blue",
    },
  ]
})

// Recent RFPs Data - use real data from store
const recentRFPs = computed(() => {
  return rfpStore.rfps.slice(0, 4).map((rfp: any) => ({
    id: rfp.rfp_number || rfp.id,
    title: rfp.title,
    status: rfp.status,
    phase: getPhaseFromStatus(rfp.status),
    totalPhases: 10,
    value: formatBudget(rfp.budgetMin, rfp.budgetMax),
    deadline: formatDate(rfp.deadline),
    vendors: 0, // TODO: Add vendor count when available
  }))
})

// Helper functions
const getPhaseFromStatus = (status: string) => {
  switch (status) {
    case 'draft': return 1
    case 'in_review': return 2
    case 'published': return 3
    case 'submission_open': return 4
    case 'evaluation': return 6
    case 'awarded': return 9
    case 'cancelled': return 10
    default: return 1
  }
}

const formatBudget = (min: string, max: string) => {
  if (!min && !max) return 'Not specified'
  if (min && max) return `$${Number(min).toLocaleString()} - $${Number(max).toLocaleString()}`
  if (min) return `$${Number(min).toLocaleString()}+`
  if (max) return `Up to $${Number(max).toLocaleString()}`
  return 'Not specified'
}

const formatDate = (dateString: string) => {
  if (!dateString) return 'Not set'
  return new Date(dateString).toLocaleDateString()
}

// Helper functions
const getStatusColor = (status: string) => {
  const normalizedStatus = status?.toLowerCase() || ''
  switch (normalizedStatus) {
    case "draft": return "badge-draft"
    case "in_review":
    case "in-review":
    case "review": return "badge-in-review"
    case "approved":
    case "awarded": return "badge-approved"
    case "active": return "badge-approved"
    case "evaluation": return "badge-in-review"
    case "rejected": return "status-badge rejected"
    default: return "badge-draft"
  }
}

// Format status text for display
const formatStatusText = (status: string) => {
  const normalizedStatus = status?.toLowerCase() || ''
  switch (normalizedStatus) {
    case "draft": return "Draft"
    case "in_review":
    case "in-review": return "In Review"
    case "review": return "In Review"
    case "approved": return "Approved"
    case "awarded": return "Approved"
    case "active": return "Approved"
    case "evaluation": return "In Review"
    case "rejected": return "Rejected"
    default: return status || "Draft"
  }
}

const navigateToPhase = (phase: number) => {
  // Map phase numbers to new route names
  const phaseRoutes = {
    1: '/rfp-creation',
    2: '/rfp-approval', 
    3: '/rfp-vendor-selection',
    4: '/rfp-url-generation',
    5: '/vendor-portal',
    6: '/rfp-evaluation',
    7: '/rfp-comparison',
    8: '/rfp-consensus',
    9: '/rfp-consensus', // Award is now combined with Consensus
    10: '/rfp-dashboard'
  }
  
  const route = phaseRoutes[phase] || '/rfp-creation'
  window.location.href = route
}
</script>

<style scoped>
/* Dashboard-specific styles to match React version */
.phase-card {
  @apply bg-white border border-gray-200 rounded-lg shadow-sm;
}

.enhanced-card {
  @apply transition-all duration-200 hover:shadow-lg hover:border-gray-300;
}

.compact-card {
  @apply overflow-hidden;
  min-height: auto;
  background: linear-gradient(145deg, #ffffff 0%, #f9fafb 100%);
}

.dashboard-action-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.35rem;
  min-width: 150px;
  height: 44px;
  box-sizing: border-box;
  border: 1px solid #d1d5dd;
  background: #ffffff;
  color: #1d4ed8;
  text-decoration: none;
  transition: background 0.2s ease, transform 0.2s ease;
}

.dashboard-action-link:hover {
  background: #f4f6fb;
  transform: translateY(-1px);
}

.icon-wrapper-compact {
  @apply p-2 rounded-lg flex items-center justify-center flex-shrink-0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
  transition: all 0.2s ease-in-out;
}

.enhanced-card:hover .icon-wrapper-compact {
  transform: scale(1.05);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.12);
}

.icon-wrapper {
  @apply p-3 rounded-xl flex items-center justify-center flex-shrink-0;
}

.hover-lift {
  @apply transition-all duration-200 hover:shadow-md hover:-translate-y-0.5;
}

.text-muted-foreground {
  @apply text-gray-500;
}

.text-success {
  @apply text-green-600;
}

.text-destructive {
  @apply text-red-600;
}

.text-warning {
  @apply text-yellow-600;
}

.text-info {
  @apply text-blue-600;
}

.text-primary {
  @apply text-blue-600;
}

.bg-destructive {
  @apply bg-red-100;
}

.text-destructive-foreground {
  @apply text-red-800;
}

.bg-warning {
  @apply bg-yellow-100;
}

.text-warning-foreground {
  @apply text-yellow-800;
}

.bg-muted {
  @apply bg-gray-100;
}

.text-muted-foreground {
  @apply text-gray-600;
}

/* Badge styles are now imported from badge.css */
.status-badge.rejected {
  @apply bg-red-100 text-red-800 px-2 py-1 text-xs font-medium rounded-full;
}

.gradient-primary {
  @apply bg-gradient-to-r from-blue-600 to-blue-700 text-white hover:from-blue-700 hover:to-blue-800;
}
</style>
