<template>
  <div class="space-y-4 lg:space-y-6 p-4 lg:p-6 contract-audits-page">
    <!-- Header -->
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 class="text-2xl lg:text-3xl font-bold tracking-tight text-foreground">My Audits</h1>
          <p class="text-sm lg:text-base text-muted-foreground">Manage your assigned audits and review queue</p>
        </div>
        <Button 
          variant="ghost"
          @click="navigateToCreate"
          class="button button--create gap-2 w-full sm:w-auto"
        >
          <FileText class="mr-2 h-4 w-4" />
          Create New Audit
        </Button>
      </div>

    <!-- Search -->
    <Card class="shadow-card">
      <CardContent class="p-4">
        <!-- Component-level styling from main.css -->
        <div class="search-container">
          <div class="search-input-wrapper">
            <Search class="search-icon" />
            <input
              placeholder="Search audits by title or contract..."
              v-model="searchTerm"
              type="text"
              class="search-input search-input--medium search-input--default"
              style="min-width: 540px;"
            />
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- Statistics -->
    <div class="kpi-cards-grid-audits">
      <div class="kpi-card">
        <div class="kpi-card-content">
          <div class="kpi-card-icon-wrapper kpi-card-icon-blue">
            <FileText />
          </div>
          <div class="kpi-card-text">
            <div class="kpi-card-title">Created</div>
            <div class="kpi-card-value">{{ groupedAudits.created.length }}</div>
            <div class="kpi-card-subheading">Newly created audits</div>
          </div>
        </div>
      </div>

      <div class="kpi-card">
        <div class="kpi-card-content">
          <div class="kpi-card-icon-wrapper kpi-card-icon-orange">
            <Clock />
          </div>
          <div class="kpi-card-text">
            <div class="kpi-card-title">In Progress</div>
            <div class="kpi-card-value">{{ groupedAudits.in_progress.length }}</div>
            <div class="kpi-card-subheading">Currently being audited</div>
          </div>
        </div>
      </div>

      <div class="kpi-card">
        <div class="kpi-card-content">
          <div class="kpi-card-icon-wrapper kpi-card-icon-purple">
            <Eye />
          </div>
          <div class="kpi-card-text">
            <div class="kpi-card-title">Under Review</div>
            <div class="kpi-card-value">{{ groupedAudits.under_review.length }}</div>
            <div class="kpi-card-subheading">Awaiting review</div>
          </div>
        </div>
      </div>

      <div class="kpi-card">
        <div class="kpi-card-content">
          <div class="kpi-card-icon-wrapper kpi-card-icon-green">
            <CheckCircle />
          </div>
          <div class="kpi-card-text">
            <div class="kpi-card-title">Completed</div>
            <div class="kpi-card-value">{{ groupedAudits.completed.length }}</div>
            <div class="kpi-card-subheading">Successfully completed</div>
          </div>
        </div>
      </div>

      <div class="kpi-card">
        <div class="kpi-card-content">
          <div class="kpi-card-icon-wrapper kpi-card-icon-red">
            <AlertTriangle />
          </div>
          <div class="kpi-card-text">
            <div class="kpi-card-title">Rejected</div>
            <div class="kpi-card-value">{{ groupedAudits.rejected.length }}</div>
            <div class="kpi-card-subheading">Rejected audits</div>
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
          <Button 
            variant="ghost"
            @click="navigateToCreate"
            class="button button--create gap-2"
          >
            Create Your First Audit
          </Button>
        </div>
        
        <!-- Grid View -->
        <div v-else-if="viewMode === 'grid'" class="grid gap-4">
          <ContractAuditCard 
            v-for="audit in currentAudits" 
            :key="audit.audit_id" 
            :audit="audit"
            :currentUserId="currentUser?.userid || currentUser?.user_id"
            @click="navigateToAudit(audit.audit_id)"
          />
        </div>
        
        <!-- List View -->
        <div v-else-if="viewMode === 'list'" class="space-y-2">
          <!-- List Header -->
          <div class="grid grid-cols-12 gap-4 px-4 py-3 bg-muted/50 rounded-lg text-sm font-medium text-muted-foreground">
            <div class="col-span-3">Audit Details</div>
            <div class="col-span-2">Contract</div>
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
            </div>
            
            <!-- Contract -->
            <div class="col-span-2">
              <div class="text-sm text-foreground">{{ audit.contract_title || 'N/A' }}</div>
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
                <button
                  @click="navigateToAudit(audit.audit_id)"
                  class="button button--view flex items-center gap-1"
                >
                  <Eye class="h-3 w-3" />
                  View
                </button>
                
                <!-- Status-specific actions -->
                <template v-if="audit.status === 'created' && isCurrentUserAuditor(audit)">
                  <Button
                    @click="startAudit(audit)"
                    variant="default"
                    size="sm"
                    class="flex items-center gap-1 bg-green-600 hover:bg-green-700"
                  >
                    <Play class="h-3 w-3" />
                    Start Audit
                  </Button>
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
                    Edit
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
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import PopupModal from '@/popup/PopupModal.vue'
import { PopupService } from '@/popup/popupService'
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
  Play
} from 'lucide-vue-next'
import contractAuditApi from '@/services/contractAuditApi.js'
import loggingService from '@/services/loggingService'
import '@/assets/components/main.css'
import { 
  Card, CardContent, Button, Input
} from '@/components/ui_contract'
import ContractAuditCard from '@/components/ContractAuditCard.vue'
import '@/assets/components/main.css'

const router = useRouter()
const store = useStore()
const searchTerm = ref('')
const activeTab = ref('all')
const loading = ref(true)
const allAudits = ref([])
const viewMode = ref('grid') // 'grid' or 'list'

// Get current user from store
const currentUser = computed(() => store.getters['auth/currentUser'])

// Load audits from API
const loadAudits = async (searchQuery = '') => {
  try {
    loading.value = true
    const params = {}
    if (searchQuery) {
      params.search = searchQuery
    }
    const response = await contractAuditApi.getContractAudits(params)
    if (response.success) {
      allAudits.value = response.data.results || response.data || []
    } else {
      console.error('Error loading contract audits:', response.error)
      allAudits.value = []
    }
  } catch (error) {
    console.error('Error loading contract audits:', error)
    allAudits.value = []
  } finally {
    loading.value = false
  }
}

// Filter audits to show only those assigned to current user, where user is auditor, or where user is reviewer
const myAudits = computed(() => {
  if (!currentUser.value) return []
  
  const currentUserId = currentUser.value.userid || currentUser.value.user_id
  
  return allAudits.value.filter(audit => 
    audit.assignee_id == currentUserId || 
    audit.auditor_id == currentUserId || 
    audit.reviewer_id == currentUserId
  )
})

// Filter by search term
const filteredAudits = computed(() => {
  if (!searchTerm.value || searchTerm.value.trim() === '') {
    return myAudits.value
  }
  
  const searchLower = searchTerm.value.toLowerCase().trim()
  
  return myAudits.value.filter(audit => {
    const titleMatch = audit.title && audit.title.toLowerCase().includes(searchLower)
    const contractMatch = audit.contract_title && audit.contract_title.toLowerCase().includes(searchLower)
    const scopeMatch = audit.scope && audit.scope.toLowerCase().includes(searchLower)
    
    return titleMatch || contractMatch || scopeMatch
  })
})

// Group audits by status
const groupedAudits = computed(() => ({
  created: filteredAudits.value.filter(audit => audit.status === 'created'),
  in_progress: filteredAudits.value.filter(audit => audit.status === 'in_progress'),
  under_review: filteredAudits.value.filter(audit => audit.status === 'under_review'),
  completed: filteredAudits.value.filter(audit => audit.status === 'completed'),
  rejected: filteredAudits.value.filter(audit => audit.status === 'rejected')
}))


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

// Watch search term for debugging
watch(searchTerm, (newValue) => {
  console.log('Search term changed:', newValue)
  console.log('Filtered audits count:', filteredAudits.value.length)
  console.log('Current audits count:', currentAudits.value.length)
})

// Load data on component mount
onMounted(async () => {
  await loggingService.logPageView('Contract', 'Contract Audits')
  await loadAudits()
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
  }
  
  return 'badge-draft' // Default gray
}

// Navigation functions
const navigateToCreate = () => router.push('/contract-audit/create')
const navigateToAudit = (auditId) => router.push(`/contract-audit/${auditId}`)
const navigateToAllAudits = () => router.push('/contract-audit/all')

// Action functions
const editAudit = (auditId) => {
  router.push(`/contract-audit/${auditId}`)
}

const reviewAudit = (auditId) => {
  router.push(`/contract-audit/${auditId}/review`)
}

const generateReport = (audit) => {
  // This would integrate with the report generation from AuditReports.vue
  PopupService.success(`Generating report for audit: ${audit.title}`, 'Report Generation')
  // You could import and call the generateAuditReport function here
}

// Check if current user is the auditor for an audit
const isCurrentUserAuditor = (audit) => {
  if (!currentUser.value || !audit.auditor_id) return false
  const currentUserId = currentUser.value.userid || currentUser.value.user_id
  return currentUserId == audit.auditor_id
}

// Start audit function
const startAudit = async (audit) => {
  PopupService.confirm(
    `Are you sure you want to start the audit "${audit.title}"?`,
    'Start Audit',
    async () => {
      await performStartAudit(audit)
    }
  )
}

const performStartAudit = async (audit) => {
  try {
    loading.value = true
    const response = await contractAuditApi.startContractAudit(audit.audit_id)
    
    if (response.success) {
      PopupService.success(response.message, 'Audit Started')
      // Reload audits to show updated status
      await loadAudits()
    } else {
      PopupService.error(response.error || 'Failed to start audit. Please try again.', 'Start Failed')
    }
  } catch (error) {
    console.error('Error starting audit:', error)
    PopupService.error(error.response?.data?.error || 'Failed to start audit. Please try again.', 'Start Error')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
@import '@/assets/components/main.css';
@import '@/assets/components/badge.css';
</style>

<style>
/* Remove border and outline from search input */
.contract-audits-page .search-input,
.contract-audits-page .search-input:focus,
.contract-audits-page .search-input:focus-visible,
.contract-audits-page .search-input-wrapper input {
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
}

/* Also target the Card wrapper if needed */
.contract-audits-page .shadow-card,
.contract-audits-page .shadow-card [class*="Card"] {
  border: none !important;
  box-shadow: none !important;
  outline: none !important;
}

/* Remove hover effects from KPI cards */
.contract-audits-page .kpi-card:hover,
.contract-audits-page .kpi-card:hover .kpi-card-content,
.contract-audits-page .kpi-card-content:hover {
  background-color: #ffffff !important;
  background: #ffffff !important;
  box-shadow: inherit !important;
  transform: none !important;
  transition: none !important;
}

/* Remove all left borders (including dashed) from the entire page */
.contract-audits-page *,
.contract-audits-page *::before,
.contract-audits-page *::after {
  border-left: none !important;
}

/* Specifically target any activity items or list items with left borders */
.contract-audits-page [class*="activity"],
.contract-audits-page [class*="Activity"],
.contract-audits-page .list-item,
.contract-audits-page [class*="border-l"],
.contract-audits-page [class*="border-left"] {
  border-left: none !important;
}
</style>
