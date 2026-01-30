<template>
  <div class="space-y-4 lg:space-y-6 p-4 lg:p-6">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <h1 class="text-2xl lg:text-3xl font-bold tracking-tight text-foreground">Audit Dashboard</h1>
        <p class="text-sm lg:text-base text-muted-foreground">Monitor and manage all contract audit activities (Admin View)</p>
      </div>
      <Button 
        variant="ghost"
        @click="navigateToCreate"
        class="button button--create gap-2 w-full sm:w-auto"
      >
        <Shield class="mr-2 h-4 w-4" />
        Create New Audit
      </Button>
    </div>

    <!-- Statistics Cards -->
    <div class="kpi-cards-grid">
      <div 
        v-for="(stat, index) in stats" 
        :key="index" 
        class="kpi-card"
      >
        <div class="kpi-card-content">
          <div :class="`kpi-card-icon-wrapper ${stat.iconColor}`">
            <component :is="stat.icon" />
          </div>
          <div class="kpi-card-text">
            <h3 class="kpi-card-title">{{ stat.title }}</h3>
            <div class="kpi-card-value">{{ stat.value }}</div>
            <p class="kpi-card-subheading">{{ stat.description }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content Grid -->
    <div class="grid grid-cols-1 xl:grid-cols-3 gap-4 lg:gap-6">
      <!-- Recent Audits -->
      <Card class="xl:col-span-2 shadow-card">
        <CardHeader>
          <CardTitle class="flex items-center">
            <FileText class="mr-2 h-5 w-5 text-primary" />
            Recent Audits
          </CardTitle>
          <CardDescription>
            Latest audit activities and their current status (All audits visible to admin)
          </CardDescription>
        </CardHeader>
        <CardContent class="p-4">
          <div class="space-y-3">
            <div 
              v-for="audit in recentAudits" 
              :key="audit.audit_id"
              class="flex flex-col sm:flex-row sm:items-center sm:justify-between p-3 border border-border rounded-lg hover:bg-muted/30 transition-colors cursor-pointer gap-2"
              @click="navigateToAudit(audit.audit_id)"
            >
              <div class="flex-1 min-w-0">
                <h3 class="font-medium text-foreground text-sm lg:text-base truncate">{{ audit.title }}</h3>
                <div class="flex flex-col sm:flex-row sm:items-center sm:space-x-2 mt-1 text-xs lg:text-sm text-muted-foreground">
                  <span class="truncate">Contract: {{ audit.contract_title || 'Unknown Contract' }}</span>
                  <span class="hidden sm:inline">•</span>
                  <span class="truncate">Auditor: {{ audit.auditor_name || 'Unknown Auditor' }}</span>
                  <span class="hidden sm:inline">•</span>
                  <span>Due: {{ formatDate(audit.due_date) }}</span>
                </div>
              </div>
              <div class="flex-shrink-0">
                <span :class="getAuditStatusBadgeClass(audit.status)">
                  {{ formatAuditStatusText(audit.status) }}
                </span>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      <!-- Quick Actions & Overview -->
      <div class="space-y-4 lg:space-y-6">
        <!-- Quick Actions -->
        <Card class="shadow-card">
          <CardHeader>
            <CardTitle class="text-base">Quick Actions</CardTitle>
          </CardHeader>
          <CardContent class="p-4 space-y-2">
            <Button 
              variant="outline" 
              class="w-full justify-start text-sm"
              @click="navigateToCreate"
            >
              <Shield class="mr-2 h-4 w-4" />
              Create New Audit
            </Button>
            <Button 
              variant="outline" 
              class="w-full justify-start text-sm"
              @click="navigateToMyAudits"
            >
              <FileText class="mr-2 h-4 w-4" />
              View All Audits
            </Button>
            <Button 
              variant="outline" 
              class="w-full justify-start text-sm"
              @click="navigateToReports"
            >
              <BarChart3 class="mr-2 h-4 w-4" />
              View Reports
            </Button>
          </CardContent>
        </Card>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { 
  BarChart3, 
  FileText, 
  Clock, 
  CheckCircle, 
  AlertTriangle,
  TrendingUp,
  Shield
} from 'lucide-vue-next'
import contractAuditApi from '@/services/contractAuditApi.js'
import loggingService from '@/services/loggingService'
import { 
  Card, CardHeader, CardTitle, CardDescription, CardContent, Button
} from '@/components/ui_contract'
import StatusBadge from '@/components/StatusBadge.vue'
import '@/assets/components/main.css'

const router = useRouter()

// API data
const dashboardStats = ref({})
const recentAudits = ref([])
const loading = ref(true)

// Load dashboard data
const loadDashboardData = async () => {
  try {
    loading.value = true
    
    // Load dashboard stats
    const statsResponse = await contractAuditApi.getContractAuditDashboardStats()
    dashboardStats.value = statsResponse.success ? statsResponse.data : {}
    
    // Load recent audits
    const auditsResponse = await contractAuditApi.getContractAudits({ limit: 5 })
    recentAudits.value = auditsResponse.success ? (auditsResponse.data.results || auditsResponse.data || []) : []
    
  } catch (error) {
    console.error('Error loading dashboard data:', error)
    // Fallback to empty data
    dashboardStats.value = {
      total_audits: 0,
      active_audits: 0,
      completed_audits: 0,
      overdue_audits: 0
    }
    recentAudits.value = []
  } finally {
    loading.value = false
  }
}

// Calculate metrics
const totalAudits = computed(() => dashboardStats.value.total_audits || 0)
const inProgressAudits = computed(() => dashboardStats.value.active_audits || 0)
const completedAudits = computed(() => dashboardStats.value.completed_audits || 0)
const overdueAudits = computed(() => dashboardStats.value.overdue_audits || 0)

const stats = computed(() => [
  {
    title: "Total Audits",
    value: totalAudits.value,
    icon: FileText,
    iconColor: "kpi-card-icon-blue",
    description: "All audit records",
    trend: "+12% from last month"
  },
  {
    title: "In Progress",
    value: inProgressAudits.value,
    icon: Clock,
    iconColor: "kpi-card-icon-yellow",
    description: "Currently active audits",
    trend: `${inProgressAudits.value} pending completion`
  },
  {
    title: "Completed",
    value: completedAudits.value,
    icon: CheckCircle,
    iconColor: "kpi-card-icon-green",
    description: "Successfully completed",
    trend: "+8% completion rate"
  },
  {
    title: "Overdue",
    value: overdueAudits.value,
    icon: AlertTriangle,
    iconColor: "kpi-card-icon-red",
    description: "Past due date",
    trend: overdueAudits.value > 0 ? "Requires attention" : "All on track"
  }
])

// Load data on component mount
onMounted(async () => {
  await loggingService.logPageView('Contract', 'Contract Audit Dashboard')
  await loadDashboardData()
})

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString()
}

const formatAuditStatusText = (status) => {
  if (!status) return 'UNKNOWN'
  
  // Convert underscores to spaces and uppercase
  return String(status)
    .replace(/_/g, ' ')
    .toUpperCase()
}

const getAuditStatusBadgeClass = (status) => {
  if (!status) return 'badge-draft'
  
  const statusUpper = String(status).toUpperCase()
  
  // Map audit statuses to badge classes
  if (statusUpper === 'COMPLETED') {
    return 'badge-completed' // Green
  } else if (statusUpper === 'REJECTED') {
    return 'badge-rejected' // Red
  } else if (statusUpper === 'IN_PROGRESS' || statusUpper === 'IN PROGRESS') {
    return 'badge-in-review' // Orange
  } else if (statusUpper === 'UNDER_REVIEW' || statusUpper === 'UNDER REVIEW') {
    return 'badge-in-review' // Orange
  } else if (statusUpper === 'CREATED') {
    return 'badge-created' // Blue
  }
  
  return 'badge-draft' // Default gray
}

const navigateToCreate = () => router.push('/audit/create')
const navigateToMyAudits = () => router.push('/audit/all')
const navigateToReview = () => router.push('/audit/review')
const navigateToReports = () => router.push('/audit/reports')
const navigateToAudit = (auditId) => router.push(`/audit/${auditId}`)
</script>

<style scoped>
@import '@/assets/components/main.css';
@import '@/assets/components/badge.css';
</style>
