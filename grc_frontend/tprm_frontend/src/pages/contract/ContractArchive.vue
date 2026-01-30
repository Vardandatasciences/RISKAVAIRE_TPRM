<template>
  <div class="space-y-6 contract-archive-page">
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-3xl font-bold text-foreground">Archive</h1>
        <p class="text-muted-foreground">Archived and completed contracts</p>
      </div>
      <div class="flex gap-2">
        <button class="button button--export">
          <Download class="w-4 h-4" />
          Export Archive
        </button>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="kpi-cards-grid">
      <div class="kpi-card">
        <div class="kpi-card-content">
          <div class="kpi-card-icon-wrapper kpi-card-icon-blue">
            <ArchiveIcon />
          </div>
          <div class="kpi-card-text">
            <h3 class="kpi-card-title">Archived Contracts</h3>
            <div class="kpi-card-value">{{ pagination.total_count || archivedContracts.length }}</div>
          </div>
        </div>
      </div>
      
      <div class="kpi-card">
        <div class="kpi-card-content">
          <div class="kpi-card-icon-wrapper kpi-card-icon-green">
            <CheckCircle />
          </div>
          <div class="kpi-card-text">
            <h3 class="kpi-card-title">Completed</h3>
            <div class="kpi-card-value">{{ completedCount }}</div>
          </div>
        </div>
      </div>

      <div class="kpi-card">
        <div class="kpi-card-content">
          <div class="kpi-card-icon-wrapper kpi-card-icon-red">
            <XCircle />
          </div>
          <div class="kpi-card-text">
            <h3 class="kpi-card-title">Terminated</h3>
            <div class="kpi-card-value">{{ terminatedCount }}</div>
          </div>
        </div>
      </div>

      <div class="kpi-card">
        <div class="kpi-card-content">
          <div class="kpi-card-icon-wrapper kpi-card-icon-orange">
            <DollarSign />
          </div>
          <div class="kpi-card-text">
            <h3 class="kpi-card-title">Total Archived Value</h3>
            <div class="kpi-card-value">${{ totalValue.toLocaleString() }}</div>
            <p class="kpi-card-subheading">
              From {{ archivedContracts.length }} archived contracts
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Filters -->
    <Card>
      <CardHeader>
        <CardTitle>Filters</CardTitle>
        <CardDescription>Filter archived contracts by reason</CardDescription>
      </CardHeader>
      <CardContent>
        <div class="flex justify-start">
          <Select v-model="reasonFilter">
            <SelectTrigger class="w-[300px]">
              <SelectValue>
                {{ getReasonFilterLabel(reasonFilter) }}
              </SelectValue>
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Archive Reasons</SelectItem>
              <SelectItem value="CONTRACT_EXPIRED">Contract Expired</SelectItem>
              <SelectItem value="EARLY_TERMINATION">Early Termination</SelectItem>
              <SelectItem value="PROJECT_COMPLETED">Project Completed</SelectItem>
              <SelectItem value="MUTUAL_AGREEMENT">Mutual Agreement</SelectItem>
              <SelectItem value="BREACH">Breach of Contract</SelectItem>
              <SelectItem value="OTHER">Other</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </CardContent>
    </Card>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
      <p class="mt-4 text-muted-foreground">Loading archived contracts...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-12">
      <div class="text-destructive mb-4">
        <ArchiveIcon class="mx-auto h-12 w-12" />
      </div>
      <h3 class="text-lg font-semibold text-foreground mb-2">Error Loading Archived Contracts</h3>
      <p class="text-muted-foreground mb-4">{{ error }}</p>
      <Button @click="loadArchivedContracts" variant="outline">
        <RotateCcw class="w-4 h-4 mr-2" />
        Try Again
      </Button>
    </div>

    <!-- Archive Table -->
    <Card v-else>
      <CardHeader>
        <CardTitle>Archived Contracts</CardTitle>
        <CardDescription>Historical contract records</CardDescription>
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Contract</TableHead>
              <TableHead>Vendor</TableHead>
              <TableHead>Value</TableHead>
              <TableHead>Duration</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Archive Reason</TableHead>
              <TableHead>Archived By</TableHead>
              <TableHead>Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            <TableRow v-for="contract in filteredContracts" :key="contract.contract_id">
              <TableCell>
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 bg-muted rounded-lg flex items-center justify-center">
                    <ArchiveIcon class="w-5 h-5 text-muted-foreground" />
                  </div>
                  <div>
                    <div class="font-medium text-foreground">{{ contract.contract_title || 'N/A' }}</div>
                    <div class="text-sm text-muted-foreground">{{ contract.contract_number || 'N/A' }}</div>
                  </div>
                </div>
              </TableCell>
              <TableCell class="text-foreground">{{ contract.vendor?.company_name || 'N/A' }}</TableCell>
              <TableCell class="font-medium">
                ${{ (parseFloat(contract.contract_value) || 0).toLocaleString() }} {{ contract.currency || 'USD' }}
              </TableCell>
              <TableCell>
                <div class="flex items-center gap-2 text-sm">
                  <Calendar class="w-3 h-3 text-muted-foreground" />
                  {{ contract.start_date ? new Date(contract.start_date).toLocaleDateString() : 'N/A' }} - 
                  {{ contract.end_date ? new Date(contract.end_date).toLocaleDateString() : 'N/A' }}
                </div>
                <div class="text-xs text-muted-foreground">
                  Archived: {{ contract.archived_date ? new Date(contract.archived_date).toLocaleDateString() : 'N/A' }}
                </div>
              </TableCell>
              <TableCell>
                <span :class="getStatusBadgeClass(contract.status)">
                  {{ formatStatusText(contract.status) }}
                </span>
              </TableCell>
              <TableCell>
                <span :class="getReasonBadgeClass(contract.archive_reason)">
                  {{ formatReasonText(contract.archive_reason) }}
                </span>
              </TableCell>
              <TableCell class="text-sm text-muted-foreground">{{ contract.archived_by || 'N/A' }}</TableCell>
              <TableCell>
                <div class="flex gap-2">
                  <Button variant="outline" size="sm" class="gap-1">
                    <Download class="w-3 h-3" />
                    Download
                  </Button>
                  <Button 
                    variant="outline" 
                    size="sm" 
                    class="gap-1"
                    @click="restoreContract(contract)"
                    :disabled="!contract.can_be_restored"
                  >
                    <RotateCcw class="w-3 h-3" />
                    Restore
                  </Button>
                </div>
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>

        <div v-if="filteredContracts.length === 0 && !loading" class="text-center py-12">
          <ArchiveIcon class="mx-auto h-12 w-12 text-muted-foreground" />
          <h3 class="mt-2 text-sm font-semibold text-foreground">No archived contracts found</h3>
          <p class="mt-1 text-sm text-muted-foreground">
            Try adjusting your search or filter criteria.
          </p>
        </div>
      </CardContent>
    </Card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { 
  Card, CardContent, CardDescription, CardHeader, CardTitle,
  Button, Select, SelectContent, SelectItem, SelectTrigger, SelectValue,
  Table, TableBody, TableCell, TableHead, TableHeader, TableRow
} from '@/components/ui_contract'
import { 
  RotateCcw, Download, Archive as ArchiveIcon, Calendar, CheckCircle, XCircle, DollarSign
} from 'lucide-vue-next'
import contractsApi from '../../services/contractsApi'
import loggingService from '@/services/loggingService'
import { PopupService } from '@/popup/popupService'
import '@/assets/components/main.css'
import '@/assets/components/badge.css'
import '@/assets/components/main.css'

const router = useRouter()

// State
const reasonFilter = ref('all')
const loading = ref(false)
const error = ref(null)

// Data
const archivedContracts = ref([])
const pagination = ref({
  page: 1,
  page_size: 20,
  total_pages: 1,
  total_count: 0,
  has_next: false,
  has_previous: false
})

// Computed
const totalValue = computed(() => {
  return archivedContracts.value.reduce((sum, contract) => {
    const value = parseFloat(contract.contract_value) || 0
    return sum + value
  }, 0)
})

const completedCount = computed(() => {
  return archivedContracts.value.filter(c => {
    return c.status === "COMPLETED" || 
           c.archive_reason === "PROJECT_COMPLETED" || 
           c.archive_reason === "CONTRACT_EXPIRED"
  }).length
})

const terminatedCount = computed(() => {
  return archivedContracts.value.filter(c => {
    return c.status === "TERMINATED" || 
           c.archive_reason === "EARLY_TERMINATION" || 
           c.archive_reason === "BREACH"
  }).length
})

const filteredContracts = computed(() => {
  return archivedContracts.value.filter(contract => {
    // Reason filter
    if (reasonFilter.value !== 'all' && contract.archive_reason !== reasonFilter.value) {
      return false
    }

    return true
  })
})

// Methods
const loadArchivedContracts = async () => {
  try {
    loading.value = true
    error.value = null
    
    const params = {
      page: pagination.value.page,
      page_size: pagination.value.page_size,
      ordering: '-archived_date'
    }
    
    const response = await contractsApi.getArchivedContracts(params)
    
    if (response.success) {
      archivedContracts.value = response.data || []
      pagination.value = response.pagination || pagination.value
    } else {
      throw new Error(response.message || 'Failed to load archived contracts')
    }
  } catch (err) {
    console.error('Error loading archived contracts:', err)
    error.value = err.message || 'Failed to load archived contracts'
    archivedContracts.value = []
  } finally {
    loading.value = false
  }
}

const restoreContract = async (contract) => {
  if (!confirm(`Are you sure you want to restore contract "${contract.contract_title}"?`)) {
    return
  }

  try {
    const response = await contractsApi.restoreContract(contract.contract_id, {
      restore_reason: 'Restored from archive'
    })
    
    if (response.success) {
      // Remove from archived list
      archivedContracts.value = archivedContracts.value.filter(c => c.contract_id !== contract.contract_id)
      pagination.value.total_count = Math.max(0, pagination.value.total_count - 1)
      console.log('Contract restored successfully')
    } else {
      throw new Error(response.message || 'Failed to restore contract')
    }
  } catch (err) {
    console.error('Error restoring contract:', err)
    PopupService.error('Failed to restore contract: ' + err.message, 'Restore Failed')
  }
}

// Lifecycle
onMounted(async () => {
  await loggingService.logPageView('Contract', 'Contract Archive')
  await loadArchivedContracts()
})

// Helper functions for badge classes
const formatStatusText = (status) => {
  if (!status) return 'N/A'
  
  // Convert underscores to spaces and uppercase
  return String(status)
    .replace(/_/g, ' ')
    .toUpperCase()
}

const formatReasonText = (reason) => {
  if (!reason) return 'N/A'
  
  const reasonTexts = {
    "CONTRACT_EXPIRED": "CONTRACT EXPIRED",
    "EARLY_TERMINATION": "EARLY TERMINATION",
    "PROJECT_COMPLETED": "PROJECT COMPLETED",
    "MUTUAL_AGREEMENT": "MUTUAL AGREEMENT",
    "BREACH": "BREACH OF CONTRACT",
    "OTHER": "OTHER"
  }
  return reasonTexts[reason] || String(reason).replace(/_/g, ' ').toUpperCase()
}

const getStatusBadgeClass = (status) => {
  if (!status) return 'badge-draft'
  
  const statusUpper = String(status).toUpperCase()
  
  // Map contract statuses to badge classes
  if (statusUpper === 'COMPLETED') {
    return 'badge-completed' // Green
  } else if (statusUpper === 'TERMINATED') {
    return 'badge-terminated' // Red
  } else if (statusUpper === 'EXPIRED' || statusUpper === 'CANCELLED') {
    return 'badge-expired' // Gray
  } else if (statusUpper === 'ACTIVE' || statusUpper === 'APPROVED') {
    return 'badge-approved' // Green
  } else if (statusUpper === 'PENDING_ASSIGNMENT' || statusUpper.includes('PENDING')) {
    return 'badge-pending-assignment' // Light orange (#fb923c)
  }
  
  return 'badge-draft' // Default gray
}

const getReasonBadgeClass = (reason) => {
  if (!reason) return 'badge-draft'
  
  const reasonUpper = String(reason).toUpperCase()
  
  // Map archive reasons to badge classes
  if (reasonUpper === 'EARLY_TERMINATION' || reasonUpper === 'BREACH') {
    return 'badge-early-termination' // Red
  } else if (reasonUpper === 'PROJECT_COMPLETED' || reasonUpper === 'CONTRACT_EXPIRED') {
    return 'badge-completed' // Green
  } else if (reasonUpper === 'MUTUAL_AGREEMENT') {
    return 'badge-approved' // Green
  }
  
  return 'badge-draft' // Default gray for OTHER
}

// Helper function for dropdown label
const getReasonFilterLabel = (reason) => {
  const labels = {
    'all': 'All Archive Reasons',
    'CONTRACT_EXPIRED': 'Contract Expired',
    'EARLY_TERMINATION': 'Early Termination',
    'PROJECT_COMPLETED': 'Project Completed',
    'MUTUAL_AGREEMENT': 'Mutual Agreement',
    'BREACH': 'Breach of Contract',
    'OTHER': 'Other'
  }
  return labels[reason] || reason
}
</script>

<style scoped>
@import '@/assets/components/contract_darktheme.css';

/* Remove black/dark hover effect from KPI cards */
.contract-archive-page .kpi-card:hover {
  background-color: #ffffff !important;
  background: #ffffff !important;
}

.dark-theme .contract-archive-page .kpi-card:hover {
  background-color: #374151 !important;
  background: #374151 !important;
}

.contract-archive-page .kpi-card:hover .kpi-card-content {
  background-color: transparent !important;
  background: transparent !important;
}

.dark-theme .contract-archive-page .kpi-card:hover .kpi-card-content {
  background-color: transparent !important;
  background: transparent !important;
}
</style>
