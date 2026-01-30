<template>
  <div class="space-y-4 lg:space-y-6 p-4 lg:p-6">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <h1 class="text-2xl lg:text-3xl font-bold tracking-tight text-foreground">My Audits</h1>
        <p class="text-sm lg:text-base text-muted-foreground">Manage audits assigned to you as auditor or reviewer</p>
      </div>
      <Button 
        @click="navigateToCreate"
        variant="ghost"
        class="button button--create w-full sm:w-auto"
      >
        <FileText class="mr-2 h-4 w-4" />
        Create New Audit
      </Button>
    </div>

    <!-- Search -->
    <!-- Component-level styling from main.css -->
    <div class="search-container">
      <div class="search-input-wrapper">
        <Search class="search-icon" />
        <input
          type="text"
          class="search-input search-input--medium search-input--default"
          style="min-width: 1150px;"
          placeholder="Search audits by title or SLA..."
          v-model="searchTerm"
        />
      </div>
    </div>

    <!-- Statistics -->
    <div class="kpi-cards-grid-audits">
      <div 
        v-for="stat in statistics" 
        :key="stat.label" 
        class="kpi-card"
      >
        <div class="kpi-card-content">
          <div :class="['kpi-card-icon-wrapper', stat.iconColor]">
            <component :is="stat.icon" />
          </div>
          <div class="kpi-card-text">
            <h3 class="kpi-card-title">{{ stat.label }}</h3>
            <div class="kpi-card-value">{{ stat.count }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- View Toggle - Top Right -->
    <div class="flex justify-end">
      <div class="flex items-center gap-2">
        <span class="text-sm text-muted-foreground">View:</span>
        <div class="flex bg-muted rounded-lg p-1">
          <button
            @click="viewMode = 'grid'"
            :class="[
              'px-3 py-1.5 text-sm font-medium rounded-md transition-colors flex items-center gap-2',
              viewMode === 'grid' 
                ? 'bg-background text-foreground shadow-sm' 
                : 'text-muted-foreground hover:text-foreground'
            ]"
          >
            <Grid3X3 class="h-4 w-4" />
            Grid
          </button>
          <button
            @click="viewMode = 'list'"
            :class="[
              'px-3 py-1.5 text-sm font-medium rounded-md transition-colors flex items-center gap-2',
              viewMode === 'list' 
                ? 'bg-background text-foreground shadow-sm' 
                : 'text-muted-foreground hover:text-foreground'
            ]"
          >
            <List class="h-4 w-4" />
            List
          </button>
        </div>
      </div>
    </div>

    <!-- Audit Tabs -->
    <div class="space-y-4 lg:space-y-6">
      <div class="grid grid-cols-2 lg:grid-cols-6 w-full bg-muted rounded-lg p-1 gap-1">
        <button
          v-for="tab in tabs"
          :key="tab.value"
          :class="[
            'px-2 lg:px-3 py-2 text-xs lg:text-sm font-medium rounded-md transition-colors',
            activeTab === tab.value 
              ? 'bg-background text-foreground shadow-sm' 
              : 'text-muted-foreground hover:text-foreground'
          ]"
          @click="activeTab = tab.value"
        >
          {{ tab.label }}
        </button>
      </div>

      <!-- Tab Content -->
      <div class="space-y-4">
        <div v-if="currentAudits.length === 0" class="text-center py-8">
          <FileText class="w-12 h-12 mx-auto mb-4 text-muted-foreground" />
          <h3 class="text-lg font-medium mb-2">No audits found</h3>
          <p class="text-muted-foreground mb-4">
            {{ searchTerm ? "Try adjusting your search criteria" : "No audits found in the system" }}
          </p>
          <Button @click="navigateToCreate">
            Create Your First Audit
          </Button>
        </div>
        
        <!-- Grid View -->
        <div v-else-if="viewMode === 'grid'" class="grid gap-4">
          <AuditCard 
            v-for="audit in currentAudits" 
            :key="audit.audit_id" 
            :audit="audit"
            :currentUserId="currentUserId"
            @click="navigateToAudit(audit.audit_id)"
          />
        </div>
        
        <!-- List View -->
        <div v-else-if="viewMode === 'list'" class="space-y-2">
          <!-- List Header -->
          <div class="grid grid-cols-12 gap-4 px-4 py-3 bg-muted/50 rounded-lg text-sm font-medium text-muted-foreground">
            <div class="col-span-3">Audit Details</div>
            <div class="col-span-2">SLA</div>
            <div class="col-span-2">Auditor</div>
            <div class="col-span-2">Due Date</div>
            <div class="col-span-1">Status</div>
            <div class="col-span-2">Actions</div>
          </div>
          
          <!-- List Items -->
          <div v-for="audit in currentAudits" :key="audit.audit_id" 
               class="grid grid-cols-12 gap-4 px-4 py-4 border border-border rounded-lg hover:bg-muted/30 transition-colors">
            <!-- Audit Details -->
            <div class="col-span-3">
              <div class="font-medium text-foreground cursor-pointer hover:text-primary" @click="navigateToAudit(audit.audit_id)">
                {{ audit.title }}
              </div>
              <div class="text-sm text-muted-foreground">ID: {{ audit.audit_id }}</div>
              <div class="text-xs text-muted-foreground flex items-center gap-1 mt-1">
                <Paperclip class="w-3 h-3" />
                Evidence docs: {{ getEvidenceDocCount(audit.audit_id) }}
                <span v-if="getEvidenceUpdatedLabel(audit.audit_id)" class="text-[11px] text-muted-foreground/80">
                  • Updated {{ getEvidenceUpdatedLabel(audit.audit_id) }}
                </span>
              </div>
            </div>
            
            <!-- SLA -->
            <div class="col-span-2">
              <div class="text-sm text-foreground">{{ audit.sla_name || 'N/A' }}</div>
              <div v-if="audit.metrics_count > 0" class="text-xs text-muted-foreground">
                {{ audit.metrics_count }} metrics: {{ audit.metrics_names }}
              </div>
            </div>
            
            <!-- Auditor -->
            <div class="col-span-2">
              <div class="text-sm text-foreground">{{ audit.auditor_name || 'N/A' }}</div>
            </div>
            
            <!-- Due Date -->
            <div class="col-span-2">
              <div class="text-sm text-foreground">
                {{ audit.due_date ? new Date(audit.due_date).toLocaleDateString() : 'N/A' }}
              </div>
            </div>
            
            <!-- Status -->
            <div class="col-span-1">
              <span :class="getStatusBadgeClass(audit.status)">
                {{ formatStatusText(audit.status) }}
              </span>
            </div>
            
            <!-- Actions -->
            <div class="col-span-2">
              <div class="flex items-center gap-2">
                <Button
                  @click="navigateToAudit(audit.audit_id)"
                  variant="ghost"
                  size="sm"
                  class="flex items-center gap-1"
                >
                  <Eye class="h-3 w-3" />
                  View
                </Button>
                
                <!-- Status-specific actions -->
                <template v-if="audit.status === 'created'">
                  <button
                    type="button"
                    @click="startAudit(audit.audit_id)"
                    class="button button--start flex items-center gap-1"
                  >
                    <Activity class="h-3 w-3" />
                    Start Audit
                  </button>
                </template>
                
                <template v-else-if="audit.status === 'completed'">
                  <Button
                    @click="generateReport(audit)"
                    variant="outline"
                    size="sm"
                    class="flex items-center gap-1"
                  >
                    <Download class="h-3 w-3" />
                    Report
                  </Button>
                </template>
                
                <template v-else-if="audit.status === 'in_progress' || audit.status === 'rejected'">
                  <Button
                    @click="editAudit(audit.audit_id)"
                    variant="ghost"
                    size="sm"
                    class="flex items-center gap-1"
                  >
                    <Edit class="h-3 w-3" />
                    Continue
                  </Button>
                </template>
                
                <template v-else-if="audit.status === 'under_review'">
                  <Button
                    @click="reviewAudit(audit.audit_id)"
                    variant="ghost"
                    size="sm"
                    class="flex items-center gap-1"
                  >
                    <Eye class="h-3 w-3" />
                    Review
                  </Button>
                </template>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Popup Modal -->
  <PopupModal />
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { 
  FileText, 
  Search, 
  Clock,
  CheckCircle,
  AlertTriangle,
  Eye,
  Grid3X3,
  List,
  Edit,
  Trash2,
  Download,
  Activity,
  Paperclip
} from 'lucide-vue-next'
import apiService from '@/services/api.js'
import '@/assets/components/main.css'
import Card from '@/components/ui/card.vue'
import CardContent from '@/components/ui/card-content.vue'
import Button from '@/components/ui/button.vue'
import Input from '@/components/ui/input.vue'
import AuditCard from '@/components/AuditCard.vue'
import PopupModal from '@/popup/PopupModal.vue'
import { PopupService } from '@/popup/popupService'
import { useNotifications } from '@/composables/useNotifications'
import loggingService from '@/services/loggingService'
import '@/assets/components/main.css'

const router = useRouter()
const store = useStore()
const { showSuccess, showError, showWarning, showInfo } = useNotifications()

// Get current user from store or localStorage (for GRC users)
const currentUser = computed(() => {
  // First try store
  if (store.state.auth.currentUser) {
    return store.state.auth.currentUser
  }
  
  // Fallback to localStorage (for GRC users in iframe mode)
  try {
    const storedUser = localStorage.getItem('current_user')
    if (storedUser) {
      return JSON.parse(storedUser)
    }
    
    // Also check for GRC user
    const grcUser = localStorage.getItem('grc_user')
    if (grcUser) {
      return JSON.parse(grcUser)
    }
  } catch (error) {
    console.error('Error parsing user from localStorage:', error)
  }
  
  return null
})

// Get current user ID with flexible matching
const currentUserId = computed(() => {
  if (!currentUser.value) {
    console.log('[MyAudits] No current user found')
    return null
  }
  
  const userId = currentUser.value.id || currentUser.value.user_id || currentUser.value.userid || currentUser.value.userId
  console.log('[MyAudits] Current user ID:', userId, 'User object:', currentUser.value)
  return userId ? String(userId) : null
})

const searchTerm = ref('')
const activeTab = ref('all')
const loading = ref(true)
const allAudits = ref([])
const viewMode = ref('grid') // 'grid' or 'list'
const evidenceStorageKey = 'auditEvidenceDocuments'
const auditEvidenceMap = ref({})
let storageListener = null
let evidenceBroadcastListener = null

const loadEvidenceFromStorage = () => {
  if (typeof window === 'undefined') return
  try {
    const stored = JSON.parse(localStorage.getItem(evidenceStorageKey)) || {}
    auditEvidenceMap.value = stored
  } catch (error) {
    console.error('Failed to parse evidence storage payload:', error)
    auditEvidenceMap.value = {}
  }
}

const attachEvidenceMetadata = (audits = []) => {
  if (!Array.isArray(audits)) return []
  return audits.map(audit => {
    const evidenceInfo = auditEvidenceMap.value?.[audit.audit_id] || {}
    return {
      ...audit,
      evidence_docs_count: evidenceInfo.count || 0,
      evidence_docs_last_updated: evidenceInfo.updatedAt || null
    }
  })
}

const getEvidenceDocCount = (auditId) => auditEvidenceMap.value?.[auditId]?.count || 0

const getEvidenceUpdatedLabel = (auditId) => {
  const updatedAt = auditEvidenceMap.value?.[auditId]?.updatedAt
  if (!updatedAt) return null
  return new Date(updatedAt).toLocaleDateString()
}

// Load audits from API
const loadAudits = async () => {
  try {
    loading.value = true
    console.log('[MyAudits] Loading audits...')
    const auditsData = await apiService.getAudits()
    let audits = auditsData.results || auditsData || []
    console.log('[MyAudits] Loaded audits from API:', audits.length)
    
    // Load SLA data to populate SLA names
    let slasData = []
    try {
      slasData = await apiService.getAvailableSLAs()
      console.log('Loaded SLAs:', slasData)
    } catch (slaError) {
      console.error('Error loading SLAs:', slaError)
      // Continue without SLA data - will show "Unknown SLA" for all audits
    }
    
    // Create a map of SLA ID to SLA name for quick lookup
    const slaMap = {}
    if (Array.isArray(slasData)) {
      slasData.forEach(sla => {
        if (sla.sla_id && sla.sla_name) {
          slaMap[sla.sla_id] = sla.sla_name
        }
      })
    } else if (slasData && slasData.results && Array.isArray(slasData.results)) {
      slasData.results.forEach(sla => {
        if (sla.sla_id && sla.sla_name) {
          slaMap[sla.sla_id] = sla.sla_name
        }
      })
    }
    
    // Populate SLA names and metrics in audits
    audits = await Promise.all(audits.map(async (audit) => {
      const auditWithSLA = {
        ...audit,
        sla_name: audit.sla_id ? (slaMap[audit.sla_id] || 'Unknown SLA') : 'No SLA Assigned'
      }
      
      // Fetch metrics for this audit's SLA
      const slaExists = audit.sla_id && slaMap[audit.sla_id]
      if (slaExists) {
        try {
          const metricsData = await apiService.getSLAMetrics(audit.sla_id)
          console.log(`Metrics for SLA ${audit.sla_id}:`, metricsData)
          
          // Handle different response formats
          let metrics = []
          if (Array.isArray(metricsData)) {
            metrics = metricsData
          } else if (metricsData && metricsData.metrics && Array.isArray(metricsData.metrics)) {
            metrics = metricsData.metrics
          } else if (metricsData && metricsData.results && Array.isArray(metricsData.results)) {
            metrics = metricsData.results
          }
          
          auditWithSLA.metrics = metrics
          auditWithSLA.metrics_count = metrics.length
          auditWithSLA.metrics_names = metrics.map(m => m.metric_name).join(', ')
        } catch (error) {
          console.error(`Error loading metrics for SLA ${audit.sla_id}:`, error)
          auditWithSLA.metrics = []
          auditWithSLA.metrics_count = 0
          auditWithSLA.metrics_names = 'Metrics unavailable'
        }
      } else {
        auditWithSLA.metrics = []
        auditWithSLA.metrics_count = 0
        auditWithSLA.metrics_names = audit.sla_id ? 'SLA not accessible' : 'No SLA assigned'
      }
      
      return auditWithSLA
    }))
    
    console.log('Audits with SLA names and metrics:', audits)
    allAudits.value = attachEvidenceMetadata(audits)
    
  } catch (error) {
    console.error('Error loading audits:', error)
    
    // Show error notification
    await showError('Audits Loading Failed', 'Failed to load audits. Please try refreshing the page.', {
      action: 'audits_loading_failed',
      error_message: error.message
    })
    
    allAudits.value = []
  } finally {
    loading.value = false
  }
}

// Filter audits to show only those assigned to the current user
const myAudits = computed(() => {
  console.log('[MyAudits] Filtering audits. Total audits:', allAudits.value.length)
  console.log('[MyAudits] Current user ID:', currentUserId.value)
  
  if (!currentUserId.value) {
    console.log('[MyAudits] No user ID found. Showing all audits (admin view)')
    // If no user is logged in, show all audits (admin view)
    return allAudits.value
  }
  
  // Filter audits where user is the assigned auditor or reviewer
  // Convert IDs to strings for comparison to handle number/string mismatches
  const userIdStr = String(currentUserId.value)
  const filtered = allAudits.value.filter(audit => {
    const auditorMatch = audit.auditor_id && String(audit.auditor_id) === userIdStr
    const reviewerMatch = audit.reviewer_id && String(audit.reviewer_id) === userIdStr
    return auditorMatch || reviewerMatch
  })
  
  console.log('[MyAudits] Filtered audits count:', filtered.length)
  console.log('[MyAudits] Sample audit IDs:', allAudits.value.slice(0, 3).map(a => ({
    audit_id: a.audit_id,
    auditor_id: a.auditor_id,
    reviewer_id: a.reviewer_id
  })))
  
  return filtered
})

// Filter by search term
const filteredAudits = computed(() => myAudits.value.filter(audit =>
  audit.title.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
  (audit.sla_name && audit.sla_name.toLowerCase().includes(searchTerm.value.toLowerCase()))
))

// Group audits by status
const groupedAudits = computed(() => ({
  created: filteredAudits.value.filter(audit => audit.status === 'created'),
  in_progress: filteredAudits.value.filter(audit => audit.status === 'in_progress'),
  under_review: filteredAudits.value.filter(audit => audit.status === 'under_review'),
  completed: filteredAudits.value.filter(audit => audit.status === 'completed'),
  rejected: filteredAudits.value.filter(audit => audit.status === 'rejected')
}))

const statistics = computed(() => [
  { label: "Created", count: groupedAudits.value.created.length, icon: FileText, iconColor: "kpi-card-icon-blue" },
  { label: "In Progress", count: groupedAudits.value.in_progress.length, icon: Clock, iconColor: "kpi-card-icon-orange" },
  { label: "Under Review", count: groupedAudits.value.under_review.length, icon: Eye, iconColor: "kpi-card-icon-purple" },
  { label: "Completed", count: groupedAudits.value.completed.length, icon: CheckCircle, iconColor: "kpi-card-icon-green" },
  { label: "Rejected", count: groupedAudits.value.rejected.length, icon: AlertTriangle, iconColor: "kpi-card-icon-red" }
])

const tabs = computed(() => [
  { value: 'all', label: `All (${filteredAudits.value.length})` },
  { value: 'created', label: `Created (${groupedAudits.value.created.length})` },
  { value: 'in_progress', label: `In Progress (${groupedAudits.value.in_progress.length})` },
  { value: 'under_review', label: `Review (${groupedAudits.value.under_review.length})` },
  { value: 'completed', label: `Completed (${groupedAudits.value.completed.length})` },
  { value: 'rejected', label: `Rejected (${groupedAudits.value.rejected.length})` }
])

const currentAudits = computed(() => {
  if (activeTab.value === 'all') {
    return filteredAudits.value
  }
  return groupedAudits.value[activeTab.value] || []
})

watch(auditEvidenceMap, () => {
  allAudits.value = attachEvidenceMetadata(allAudits.value)
})

// Watch for user changes and reload audits if user was not set initially
watch(currentUserId, async (newUserId, oldUserId) => {
  if (newUserId && !oldUserId && allAudits.value.length === 0) {
    console.log('[MyAudits] User ID detected, reloading audits...')
    await loadAudits()
  }
}, { immediate: false })

// Load data on component mount
onMounted(async () => {
  loadEvidenceFromStorage()
  if (typeof window !== 'undefined') {
    storageListener = (event) => {
      if (event.key === evidenceStorageKey) {
        loadEvidenceFromStorage()
      }
    }
    evidenceBroadcastListener = () => loadEvidenceFromStorage()
    window.addEventListener('storage', storageListener)
    window.addEventListener('audit-evidence-updated', evidenceBroadcastListener)
  }
  
  // Wait a bit for auth to sync if in iframe mode
  const isInIframe = window.self !== window.top
  if (isInIframe) {
    console.log('[MyAudits] In iframe mode, waiting for auth to sync...')
    await new Promise(resolve => setTimeout(resolve, 500))
  }
  
  try {
    await loggingService.logPageView('Audit', 'My Audits')
  } catch (error) {
    console.warn('[MyAudits] Failed to log page view:', error)
  }
  
  await loadAudits()
})

onBeforeUnmount(() => {
  if (typeof window === 'undefined') return
  if (storageListener) {
    window.removeEventListener('storage', storageListener)
    storageListener = null
  }
  if (evidenceBroadcastListener) {
    window.removeEventListener('audit-evidence-updated', evidenceBroadcastListener)
    evidenceBroadcastListener = null
  }
})

// Helper functions for status display
const formatStatusText = (status) => {
  if (!status) return 'UNKNOWN'
  
  // Convert underscores to spaces and uppercase
  return String(status)
    .replace(/_/g, ' ')
    .toUpperCase()
}

const getStatusBadgeClass = (status) => {
  if (!status) return 'badge-draft'
  
  const statusLower = String(status).toLowerCase()
  
  // Map audit statuses to badge classes
  if (statusLower === 'completed') {
    return 'badge-completed' // Green
  } else if (statusLower === 'rejected') {
    return 'badge-rejected' // Red
  } else if (statusLower === 'in_progress' || statusLower === 'in progress') {
    return 'badge-in-review' // Orange
  } else if (statusLower === 'under_review' || statusLower === 'under review') {
    return 'badge-in-review' // Orange
  } else if (statusLower === 'created') {
    return 'badge-created' // Blue
  } else if (statusLower === 'overdue') {
    return 'badge-overdue' // Red
  }
  
  return 'badge-draft' // Default gray
}

// Navigation functions
const navigateToCreate = () => router.push('/audit/create')
const navigateToAudit = (auditId) => router.push(`/audit/${auditId}`)

// Action functions
const startAudit = async (auditId) => {
  try {
    // Update audit status to in_progress
    await apiService.updateAudit(auditId, { status: 'in_progress' })
    
    // Show success notification
    await showSuccess('Audit Started', 'Audit has been started successfully. You can now begin the audit process.', {
      audit_id: auditId,
      action: 'audit_started'
    })
    
    router.push(`/audit/${auditId}`)
  } catch (error) {
    console.error('Error starting audit:', error)
    
    // Show error notification
    await showError('Start Failed', 'Error starting audit. Please try again.', {
      audit_id: auditId,
      action: 'audit_start_failed',
      error_message: error.message
    })
    
    PopupService.error('Error starting audit. Please try again.', 'Start Failed')
  }
}

const editAudit = (auditId) => {
  router.push(`/audit/${auditId}`)
}

const reviewAudit = (auditId) => {
  router.push(`/audit/${auditId}/review`)
}

const generateReport = async (audit) => {
  try {
    // Show info notification
    await showInfo('Report Generation', `Generating report for audit: ${audit.title}`, {
      audit_id: audit.audit_id,
      audit_title: audit.title,
      action: 'report_generation_initiated'
    })
    
    // This would integrate with the report generation from AuditReports.vue
    PopupService.warning(`Generating report for audit: ${audit.title}`, 'Report Generation')
    // You could import and call the generateAuditReport function here
  } catch (error) {
    console.error('Error generating report:', error)
    
    // Show error notification
    await showError('Report Generation Failed', 'Error generating report. Please try again.', {
      audit_id: audit.audit_id,
      audit_title: audit.title,
      action: 'report_generation_failed',
      error_message: error.message
    })
  }
}
</script>

<style scoped>
@import '@/assets/components/main.css';
@import '@/assets/components/badge.css';
</style>
