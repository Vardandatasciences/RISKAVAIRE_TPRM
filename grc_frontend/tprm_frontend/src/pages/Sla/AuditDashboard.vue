<template>
  <div class="space-y-4 lg:space-y-6 p-4 lg:p-6">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <h1 class="text-2xl lg:text-3xl font-bold tracking-tight text-foreground">Audit Dashboard</h1>
        <p class="text-sm lg:text-base text-muted-foreground">Monitor and manage all SLA audit activities (Admin View)</p>
      </div>
      <Button 
        @click="navigateToCreate"
        variant="ghost"
        class="button button--create w-full sm:w-auto"
      >
        <Shield class="mr-2 h-4 w-4" />
        Create New Audit
      </Button>
    </div>

    <!-- Statistics Cards -->
    <div class="kpi-cards-grid-audits">
      <div 
        v-for="(stat, index) in stats" 
        :key="index" 
        class="kpi-card"
      >
        <div class="kpi-card-content">
          <div :class="['kpi-card-icon-wrapper', stat.iconColor]">
            <component :is="stat.icon" />
          </div>
          <div class="kpi-card-text">
            <h3 class="kpi-card-title">{{ stat.title }}</h3>
            <div class="kpi-card-value">{{ stat.value }}</div>
            <p class="kpi-card-subheading">{{ stat.description }}</p>
            <p class="kpi-card-subheading" v-if="stat.trend">{{ stat.trend }}</p>
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
        <CardContent class="p-4 audit-card-content">
          <div class="space-y-3">
            <div 
              v-for="audit in recentAudits" 
              :key="audit.audit_id"
              class="flex flex-col sm:flex-row sm:items-center sm:justify-between p-3 border border-border rounded-lg hover:bg-muted/30 transition-colors cursor-pointer gap-2 audit-list-item"
              @click="navigateToAudit(audit.audit_id)"
            >
              <div class="flex-1 min-w-0 audit-text-container">
                <h3 class="font-medium text-foreground text-sm lg:text-base audit-title">{{ audit.title }}</h3>
                <div class="flex flex-col sm:flex-row sm:items-center sm:space-x-2 mt-1 text-xs lg:text-sm text-muted-foreground audit-details">
                  <span class="truncate">SLA: {{ audit.sla_name || 'Unknown SLA' }}</span>
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
              @click="navigateToReview"
            >
              <CheckCircle class="mr-2 h-4 w-4" />
              Review Queue
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

        <!-- SLA Overview -->
        <Card class="shadow-card">
          <CardHeader>
            <CardTitle class="text-base flex items-center">
              <Shield class="mr-2 h-4 w-4 text-primary" />
              Active SLAs (Admin View)
            </CardTitle>
          </CardHeader>
          <CardContent class="p-4 sla-card-content">
            <div class="space-y-3">
              <div v-for="sla in availableSLAs" :key="sla.sla_id" class="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-2 sla-list-item">
                <div class="min-w-0 flex-1 sla-text-container">
                  <p class="text-sm font-medium text-foreground sla-name">{{ sla.sla_name }}</p>
                  <p class="text-xs text-muted-foreground sla-details">
                    {{ sla.company_name }} - {{ sla.sla_type }}
                  </p>
                </div>
                <Badge variant="outline" class="text-xs flex-shrink-0 sla-badge">
                  {{ sla.business_service_impacted || 'Active' }}
                </Badge>
              </div>
            </div>
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
  Shield
} from 'lucide-vue-next'
import apiService from '@/services/api.js'
import Card from '@/components/ui/card.vue'
import CardHeader from '@/components/ui/card-header.vue'
import CardTitle from '@/components/ui/card-title.vue'
import CardDescription from '@/components/ui/card-description.vue'
import CardContent from '@/components/ui/card-content.vue'
import Button from '@/components/ui/button.vue'
import Badge from '@/components/ui/badge.vue'
import { useNotifications } from '@/composables/useNotifications'
import loggingService from '@/services/loggingService'
import '@/assets/components/main.css'

const router = useRouter()
const { showSuccess, showError, showWarning, showInfo } = useNotifications()

// API data
const dashboardStats = ref({})
const recentAudits = ref([])
const availableSLAs = ref([])
const loading = ref(true)

// Load dashboard data
const loadDashboardData = async () => {
  try {
    loading.value = true
    
    // Load dashboard stats
    const statsData = await apiService.getAuditDashboardStats()
    dashboardStats.value = statsData
    
    // Load recent audits
    const auditsData = await apiService.getAudits({ limit: 5 })
    recentAudits.value = auditsData.results || auditsData || []
    
    // Load available SLAs
    const slasData = await apiService.getAvailableSLAs()
    availableSLAs.value = slasData || []
    
  } catch (error) {
    console.error('Error loading dashboard data:', error)
    
    // Show error notification
    await showError('Dashboard Loading Failed', 'Failed to load audit dashboard data. Some features may not be available.', {
      action: 'dashboard_loading_failed',
      error_message: error.message
    })
    
    // Fallback to empty data
    dashboardStats.value = {
      total_audits: 0,
      active_audits: 0,
      completed_audits: 0,
      overdue_audits: 0
    }
    recentAudits.value = []
    availableSLAs.value = []
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
    description: "All audit records",
    trend: "+12% from last month",
    iconColor: "kpi-card-icon-blue"
  },
  {
    title: "Created",
    value: dashboardStats.value.created_audits || 0,
    icon: Clock,
    description: "Ready to start",
    trend: "Click to begin",
    iconColor: "kpi-card-icon-gray"
  },
  {
    title: "In Progress",
    value: inProgressAudits.value,
    icon: Clock,
    description: "Currently active audits",
    trend: `${inProgressAudits.value} pending completion`,
    iconColor: "kpi-card-icon-orange"
  },
  {
    title: "Completed",
    value: completedAudits.value,
    icon: CheckCircle,
    description: "Successfully completed",
    trend: "+8% completion rate",
    iconColor: "kpi-card-icon-green"
  },
  {
    title: "Overdue",
    value: overdueAudits.value,
    icon: AlertTriangle,
    description: "Past due date",
    trend: overdueAudits.value > 0 ? "Requires attention" : "All on track",
    iconColor: "kpi-card-icon-red"
  }
])

// Load data on component mount
onMounted(async () => {
  await loggingService.logAuditView()
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
const navigateToMyAudits = () => router.push('/audit/my-audits')
const navigateToReview = () => router.push('/audit/review')
const navigateToReports = () => router.push('/audit/reports')
const navigateToAudit = (auditId) => router.push(`/audit/${auditId}`)
</script>

<style scoped>
@import '@/assets/components/main.css';
@import '@/assets/components/badge.css';

/* Prevent overflow in SLA card */
.sla-card-content {
  overflow-x: hidden !important;
  overflow-y: visible;
  max-width: 100%;
  width: 100%;
}

/* Text wrapping for SLA list items */
.sla-list-item {
  word-wrap: break-word;
  overflow-wrap: break-word;
  max-width: 100%;
  width: 100%;
  overflow: hidden;
  min-width: 0;
}

.sla-text-container {
  min-width: 0;
  max-width: 100%;
  overflow: hidden;
  word-wrap: break-word;
  overflow-wrap: break-word;
}

.sla-name {
  word-wrap: break-word;
  overflow-wrap: break-word;
  word-break: break-word;
  hyphens: auto;
  max-width: 100%;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  text-overflow: ellipsis;
  line-height: 1.4;
}

.sla-details {
  word-wrap: break-word;
  overflow-wrap: break-word;
  word-break: break-word;
  hyphens: auto;
  max-width: 100%;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  text-overflow: ellipsis;
  line-height: 1.4;
  margin-top: 0.25rem;
}

.sla-badge {
  word-wrap: break-word;
  overflow-wrap: break-word;
  word-break: break-word;
  white-space: normal;
  max-width: 100%;
  min-width: fit-content;
  flex-shrink: 0;
  text-align: center;
}

/* Ensure card itself doesn't overflow */
.shadow-card {
  overflow-x: hidden !important;
  max-width: 100%;
}

/* Prevent any horizontal scroll */
.space-y-3 {
  overflow-x: hidden;
  max-width: 100%;
}

/* Prevent overflow in Recent Audits card */
.audit-card-content {
  overflow-x: hidden !important;
  overflow-y: visible;
  max-width: 100%;
  width: 100%;
}

.audit-list-item {
  max-width: 100%;
  width: 100%;
  overflow: hidden;
  min-width: 0;
}

.audit-text-container {
  min-width: 0;
  max-width: 100%;
  overflow: hidden;
}

.audit-title {
  word-wrap: break-word;
  overflow-wrap: break-word;
  word-break: break-word;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  text-overflow: ellipsis;
  line-height: 1.4;
  max-width: 100%;
}

.audit-details {
  word-wrap: break-word;
  overflow-wrap: break-word;
  max-width: 100%;
  overflow: hidden;
}

.audit-details span {
  word-wrap: break-word;
  overflow-wrap: break-word;
  max-width: 100%;
}

/* Ensure main container doesn't overflow */
.space-y-4,
.space-y-6 {
  overflow-x: hidden;
  max-width: 100%;
}

/* Grid container overflow protection */
.grid {
  overflow-x: hidden;
  max-width: 100%;
}
</style>
