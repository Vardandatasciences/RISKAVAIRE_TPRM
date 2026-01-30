<template>
  <div class="space-y-6 vendor-contracts-page">
    <!-- Loading State -->
    <div v-if="isLoading" class="flex flex-col items-center justify-center py-20">
      <div class="relative">
        <div class="animate-spin rounded-full h-16 w-16 border-4 border-primary/20 border-t-primary"></div>
        <div class="absolute inset-0 flex items-center justify-center">
          <Building2 class="h-6 w-6 text-primary animate-pulse" />
        </div>
      </div>
       <h3 class="mt-6 text-xl font-semibold text-foreground">Loading Vendor Contracts</h3>
       <p class="mt-2 text-muted-foreground text-center max-w-md">
         Please wait while we fetch vendor contract information and statistics.
       </p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="flex flex-col items-center justify-center py-20">
      <div class="w-20 h-20 bg-red-50 dark:bg-red-900/20 rounded-full flex items-center justify-center mb-6">
        <FileText class="h-10 w-10 text-red-500" />
      </div>
       <h3 class="text-xl font-semibold text-foreground mb-2">Error Loading Vendor Contracts</h3>
       <p class="text-muted-foreground text-center max-w-md mb-6">
         {{ error }}
       </p>
       <Button @click="loadVendors" class="gap-2">
         <FileText class="w-4 h-4" />
         Try Again
       </Button>
    </div>

    <!-- Vendor Details View -->
    <div v-else-if="selectedVendor" class="space-y-6">
      <div class="flex items-center gap-4">
        <button type="button" class="button button--back" @click="handleBackToList">
          Back to Vendor Contracts
        </button>
        <div>
          <h1 class="text-3xl font-bold text-foreground">{{ selectedVendor.company_name }}</h1>
          <p class="text-muted-foreground">Vendor Contract Details & Associated Contracts</p>
        </div>
      </div>

      <!-- Vendor Information -->
      <Card>
        <CardHeader>
          <CardTitle class="flex items-center gap-3">
            <div class="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center">
              <Building2 class="w-6 h-6 text-primary" />
            </div>
            <div>
              <div class="text-xl font-bold">{{ selectedVendor.company_name }}</div>
              <div class="text-sm text-muted-foreground">{{ selectedVendor.vendor_code }}</div>
            </div>
            <span :class="getStatusBadgeClass(selectedVendor.status)">
              {{ formatStatusText(selectedVendor.status) }}
            </span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div class="space-y-3">
              <h3 class="font-medium text-foreground">Contact Information</h3>
              <div class="space-y-2">
                <div v-if="selectedVendor.primary_contact" class="flex items-center gap-2 text-sm">
                  <Mail class="w-4 h-4 text-muted-foreground" />
                  {{ selectedVendor.primary_contact.email }}
                </div>
                <div v-if="selectedVendor.primary_contact" class="flex items-center gap-2 text-sm">
                  <Phone class="w-4 h-4 text-muted-foreground" />
                  {{ selectedVendor.primary_contact.primary_phone }}
                </div>
                <div class="flex items-center gap-2 text-sm">
                  <MapPin class="w-4 h-4 text-muted-foreground" />
                  {{ selectedVendor.full_address }}
                </div>
              </div>
            </div>
            
            <div>
              <h3 class="font-medium text-foreground mb-2">Total Contracts</h3>
              <div class="text-2xl font-bold text-primary">{{ selectedVendor.contracts_count || 0 }}</div>
            </div>
            
            <div>
              <h3 class="font-medium text-foreground mb-2">Total Value</h3>
              <div class="text-2xl font-bold text-primary">${{ (selectedVendor.total_value || 0).toLocaleString() }}</div>
            </div>
            
            <div>
              <h3 class="font-medium text-foreground mb-2">Last Activity</h3>
              <div class="text-lg text-muted-foreground">
                {{ selectedVendor.last_activity ? new Date(selectedVendor.last_activity).toLocaleDateString() : 'No activity' }}
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      <!-- Contracts List -->
      <Card>
        <CardHeader>
          <CardTitle class="flex items-center gap-2">
            <FileText class="w-5 h-5" />
            Contracts
          </CardTitle>
          <CardDescription>All contracts associated with this vendor</CardDescription>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Contract Details</TableHead>
                <TableHead>Type</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Start Date</TableHead>
                <TableHead>End Date</TableHead>
                <TableHead>Value</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              <TableRow v-for="contract in selectedVendor.contracts" :key="contract.contract_id">
                <TableCell>
                  <div>
                    <div class="font-medium text-foreground">{{ contract.contract_title }}</div>
                    <div class="text-sm text-muted-foreground">{{ contract.contract_number }}</div>
                  </div>
                </TableCell>
                <TableCell>
                  <Badge variant="outline">{{ contract.contract_type }}</Badge>
                </TableCell>
                <TableCell>
                  <span :class="getStatusBadgeClass(contract.status)">
                    {{ formatStatusText(contract.status) }}
                  </span>
                </TableCell>
                <TableCell>{{ contract.start_date ? new Date(contract.start_date).toLocaleDateString() : 'N/A' }}</TableCell>
                <TableCell>{{ contract.end_date ? new Date(contract.end_date).toLocaleDateString() : 'N/A' }}</TableCell>
                <TableCell class="font-medium">${{ (contract.contract_value || 0).toLocaleString() }}</TableCell>
                <TableCell>
                  <Button 
                    variant="outline" 
                    size="sm"
                    @click="viewContract(contract.contract_id)"
                    class="gap-2"
                  >
                    <Eye class="w-4 h-4" />
                    View
                  </Button>
                </TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>

    <!-- Main Vendors List View -->
    <div v-else class="space-y-6">
      <div class="flex justify-between items-center">
        <div>
          <h1 class="text-3xl font-bold text-foreground">Vendor Contracts</h1>
          <p class="text-muted-foreground">Manage vendor relationships and their associated contracts</p>
        </div>
        <button type="button" class="button button--add">
          Add Vendor
        </button>
      </div>

      <!-- Stats Cards -->
      <div class="kpi-cards-grid">
        <div class="kpi-card">
          <div class="kpi-card-content">
            <div class="kpi-card-icon-wrapper kpi-card-icon-blue">
              <Building2 />
            </div>
            <div class="kpi-card-text">
              <h3 class="kpi-card-title">Total Vendors</h3>
              <div class="kpi-card-value">{{ vendorStats.total_vendors || 0 }}</div>
            </div>
          </div>
        </div>
        
        <div class="kpi-card">
          <div class="kpi-card-content">
            <div class="kpi-card-icon-wrapper kpi-card-icon-green">
              <CheckCircle />
            </div>
            <div class="kpi-card-text">
              <h3 class="kpi-card-title">Active Vendors</h3>
              <div class="kpi-card-value">{{ vendorStats.active_vendors || 0 }}</div>
            </div>
          </div>
        </div>

        <div class="kpi-card">
          <div class="kpi-card-content">
            <div class="kpi-card-icon-wrapper kpi-card-icon-purple">
              <FileText />
            </div>
            <div class="kpi-card-text">
              <h3 class="kpi-card-title">Total Contracts</h3>
              <div class="kpi-card-value">{{ vendorStats.total_contracts || 0 }}</div>
            </div>
          </div>
        </div>

        <div class="kpi-card">
          <div class="kpi-card-content">
            <div class="kpi-card-icon-wrapper kpi-card-icon-orange">
              <DollarSign />
            </div>
            <div class="kpi-card-text">
              <h3 class="kpi-card-title">Total Value</h3>
              <div class="kpi-card-value">${{ (vendorStats.total_value || 0).toLocaleString() }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Filters -->
      <Card>
        <CardHeader>
          <CardTitle>Search & Filter</CardTitle>
           <CardDescription>Find vendor contracts quickly</CardDescription>
        </CardHeader>
        <CardContent>
          <div class="flex gap-4">
            <!-- Page-level positioning with Tailwind -->
            <div class="flex-1">
              <!-- Component-level styling from main.css -->
              <div class="search-container">
                <div class="search-input-wrapper">
                  <Search class="search-icon" />
                  <input 
                    v-model="searchQuery" 
                    @input="handleSearch"
                    type="text"
                    placeholder="Search vendor contracts..." 
                    class="search-input search-input--medium search-input--default"
                  />
                </div>
              </div>
            </div>
            <SingleSelectDropdown
              v-model="statusFilter"
              :options="statusFilterOptions"
              placeholder="Status"
              height="2.5rem"
              width="180px"
              @update:model-value="handleSearch"
            />
          </div>
        </CardContent>
      </Card>

      <!-- Vendors Table -->
      <Card>
        <CardHeader>
           <CardTitle>Vendor Contracts Directory</CardTitle>
           <CardDescription>
             {{ isVendor ? 'Your vendor information and contracts' : 'Complete list of vendor contract partners' }}
           </CardDescription>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Vendor Details</TableHead>
                <TableHead>Contact</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Contracts</TableHead>
                <TableHead>Total Value</TableHead>
                <TableHead>Last Activity</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              <TableRow v-for="vendor in filteredVendors" :key="vendor.vendor_id">
                <TableCell>
                  <div class="flex items-center gap-3">
                    <div class="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center">
                      <Building2 class="w-5 h-5 text-primary" />
                    </div>
                    <div>
                      <div class="font-medium text-foreground">{{ vendor.company_name }}</div>
                      <div class="text-sm text-muted-foreground">{{ vendor.vendor_code }}</div>
                    </div>
                  </div>
                </TableCell>
                <TableCell>
                  <div class="space-y-1">
                    <div v-if="vendor.primary_contact" class="flex items-center gap-2 text-sm">
                      <Mail class="w-3 h-3 text-muted-foreground" />
                      {{ vendor.primary_contact.email }}
                    </div>
                    <div v-if="vendor.primary_contact" class="flex items-center gap-2 text-sm">
                      <Phone class="w-3 h-3 text-muted-foreground" />
                      {{ vendor.primary_contact.primary_phone }}
                    </div>
                    <div class="flex items-center gap-2 text-sm">
                      <MapPin class="w-3 h-3 text-muted-foreground" />
                      {{ vendor.full_address }}
                    </div>
                  </div>
                </TableCell>
                <TableCell>
                  <span :class="getStatusBadgeClass(vendor.status)">
                    {{ formatStatusText(vendor.status) }}
                  </span>
                </TableCell>
                <TableCell class="text-center">{{ vendor.contracts_count || 0 }}</TableCell>
                <TableCell>${{ (vendor.total_value || 0).toLocaleString() }}</TableCell>
                <TableCell>{{ vendor.last_activity ? new Date(vendor.last_activity).toLocaleDateString() : 'No activity' }}</TableCell>
                <TableCell>
                  <div class="flex gap-2">
                    <button 
                      type="button"
                      class="button button--view"
                      @click="loadVendorDetails(vendor.vendor_id)"
                    >
                      View
                    </button>
                  </div>
                </TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { 
  Card, CardContent, CardDescription, CardHeader, CardTitle,
  Badge, Button, Input,
  Table, TableBody, TableCell, TableHead, TableHeader, TableRow
} from '@/components/ui_contract'
import { 
  Search, Plus, Building2, Mail, Phone, MapPin, ArrowLeft, FileText, 
  CheckCircle, DollarSign, Eye, Edit, Trash2, Calendar, User, Shield
} from 'lucide-vue-next'
import vendorcontractsApi from '../../services/vendorcontractsApi'
import loggingService from '@/services/loggingService'
import '@/assets/components/main.css'
import '@/assets/components/main.css'
import '@/assets/components/main.css'
import '@/assets/components/dropdown.css'
import SingleSelectDropdown from '@/assets/components/SingleSelectDropdown.vue'

const store = useStore()
const router = useRouter()

// Get current user from store
const currentUser = computed(() => store.getters['auth/currentUser'])

// Check if user is a vendor
const isVendor = computed(() => {
  if (!currentUser.value) return false
  const role = currentUser.value.role || currentUser.value.user_role || ''
  return role.toLowerCase() === 'vendor'
})

// State
const selectedVendor = ref(null)
const searchQuery = ref('')
const statusFilter = ref('all')
const vendors = ref([])
const vendorStats = ref({
  total_vendors: 0,
  active_vendors: 0,
  total_contracts: 0,
  total_value: 0
})
const isLoading = ref(true)
const error = ref(null)

// Dropdown options
const statusFilterOptions = [
  { value: 'all', label: 'All Status' },
  { value: 'APPROVED', label: 'Approved' },
  { value: 'DRAFT', label: 'Draft' },
  { value: 'SUBMITTED', label: 'Submitted' },
  { value: 'IN_REVIEW', label: 'In Review' },
  { value: 'REJECTED', label: 'Rejected' },
  { value: 'SUSPENDED', label: 'Suspended' },
  { value: 'TERMINATED', label: 'Terminated' }
]

// Computed
const filteredVendors = computed(() => {
  return vendors.value.filter(vendor => {
    // Search filter
    if (searchQuery.value) {
      const query = searchQuery.value.toLowerCase()
      const matchesQuery = 
        vendor.company_name?.toLowerCase().includes(query) ||
        vendor.vendor_code?.toLowerCase().includes(query) ||
        vendor.legal_name?.toLowerCase().includes(query) ||
        vendor.description?.toLowerCase().includes(query)
      
      if (!matchesQuery) return false
    }

    // Status filter
    if (statusFilter.value !== 'all' && vendor.status !== statusFilter.value) {
      return false
    }

    return true
  })
})

// Methods
const loadVendors = async () => {
  try {
    isLoading.value = true
    error.value = null
    
    const response = await vendorcontractsApi.getVendors({
      search: searchQuery.value,
      status: statusFilter.value !== 'all' ? statusFilter.value : '',
      page_size: 100 // Load more vendors for better UX
    })
    
    if (response.success) {
      vendors.value = response.data || []
       console.log('Vendor contracts loaded:', vendors.value.length, 'vendor contracts')
      // Calculate stats from loaded vendors as fallback
      calculateStatsFromVendors()
    } else {
       error.value = response.message || 'Failed to load vendor contracts'
    }
  } catch (err) {
    console.error('Error loading vendor contracts:', err)
    error.value = 'Failed to load vendor contracts'
  } finally {
    isLoading.value = false
  }
}

const loadVendorStats = async () => {
  try {
    const response = await vendorcontractsApi.getVendorStats()
    if (response.success) {
      vendorStats.value = response.data
       console.log('Vendor contract stats loaded:', response.data)
    } else {
      console.error('Failed to load vendor contract stats:', response.message)
      // Calculate stats from vendor list as fallback
      calculateStatsFromVendors()
    }
  } catch (err) {
    console.error('Error loading vendor contract stats:', err)
    // Calculate stats from vendor list as fallback
    calculateStatsFromVendors()
  }
}

const calculateStatsFromVendors = () => {
  if (vendors.value.length > 0) {
    const totalVendors = vendors.value.length
    const activeVendors = vendors.value.filter(v => v.status === 'APPROVED').length
    const totalContracts = vendors.value.reduce((sum, v) => sum + (v.contracts_count || 0), 0)
    const totalValue = vendors.value.reduce((sum, v) => sum + (v.total_value || 0), 0)
    
    vendorStats.value = {
      total_vendors: totalVendors,
      active_vendors: activeVendors,
      total_contracts: totalContracts,
      total_value: totalValue
    }
     console.log('Calculated stats from vendor contracts:', vendorStats.value)
  }
}

const loadVendorDetails = async (vendorId) => {
  try {
    const response = await vendorcontractsApi.getVendor(vendorId)
    if (response.success) {
      selectedVendor.value = response.data
    } else {
       error.value = response.message || 'Failed to load vendor contract details'
    }
  } catch (err) {
    console.error('Error loading vendor contract details:', err)
    error.value = 'Failed to load vendor contract details'
  }
}

const handleVendorSelect = (vendor) => {
  selectedVendor.value = vendor
}

const handleBackToList = () => {
  selectedVendor.value = null
}

const viewContract = (contractId) => {
  if (contractId) {
    router.push({
      path: `/contracts/${contractId}`,
      query: { returnTo: 'vendor-contracts' }
    })
  }
}

// Watch for search changes
const handleSearch = () => {
  loadVendors()
}

// Watch for changes in vendors to recalculate stats
watch(vendors, () => {
  calculateStatsFromVendors()
}, { deep: true })

// Badge helper functions
const getStatusBadgeClass = (status) => {
  if (!status) return ''
  
  const statusUpper = String(status).toUpperCase()
  
  // Map to badge.css classes
  if (statusUpper === 'APPROVED' || statusUpper === 'ACTIVE') {
    return 'badge-approved'
  }
  if (statusUpper === 'DRAFT') {
    return 'badge-draft'
  }
  if (statusUpper === 'IN_REVIEW' || statusUpper === 'SUBMITTED' || 
      statusUpper === 'UNDER_REVIEW' || statusUpper === 'PENDING') {
    return 'badge-in-review'
  }
  
  // For other statuses, return empty string (no special styling)
  return ''
}

const formatStatusText = (status) => {
  if (!status) return 'N/A'
  
  // Convert underscores to spaces and title case
  return String(status)
    .replace(/_/g, ' ')
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(' ')
}

// Lifecycle
onMounted(async () => {
  await loggingService.logPageView('Contract', 'Vendor Contracts')
  await Promise.all([
    loadVendors(),
    loadVendorStats()
  ])
})
</script>

<style scoped>
@import '@/assets/components/main.css';
@import '@/assets/components/badge.css';
@import '@/assets/components/contract_darktheme.css';
</style>

<style>
/* Force Building icons to remain blue even with color blindness enabled */
/* This style is not scoped to ensure it overrides color blindness CSS */
html:not(.dark-theme)[data-colorblind="protanopia"] .vendor-contracts-page svg.text-primary,
html:not(.dark-theme)[data-colorblind="deuteranopia"] .vendor-contracts-page svg.text-primary,
html:not(.dark-theme)[data-colorblind="tritanopia"] .vendor-contracts-page svg.text-primary,
html:not(.dark-theme)[data-colorblind="protanopia"] .vendor-contracts-page .text-primary svg,
html:not(.dark-theme)[data-colorblind="deuteranopia"] .vendor-contracts-page .text-primary svg,
html:not(.dark-theme)[data-colorblind="tritanopia"] .vendor-contracts-page .text-primary svg,
html:not(.dark-theme)[data-colorblind="protanopia"] .vendor-contracts-page [class*="text-primary"] svg,
html:not(.dark-theme)[data-colorblind="deuteranopia"] .vendor-contracts-page [class*="text-primary"] svg,
html:not(.dark-theme)[data-colorblind="tritanopia"] .vendor-contracts-page [class*="text-primary"] svg,
/* Override main.css color blindness rules for KPI card blue icons - Must be more specific than main.css */
html:not(.dark-theme)[data-colorblind="protanopia"] .vendor-contracts-page .kpi-card-icon-blue svg,
html:not(.dark-theme)[data-colorblind="deuteranopia"] .vendor-contracts-page .kpi-card-icon-blue svg,
html:not(.dark-theme)[data-colorblind="tritanopia"] .vendor-contracts-page .kpi-card-icon-blue svg,
html:not(.dark-theme)[data-colorblind="protanopia"] .vendor-contracts-page .kpi-card-icon-wrapper.kpi-card-icon-blue svg,
html:not(.dark-theme)[data-colorblind="deuteranopia"] .vendor-contracts-page .kpi-card-icon-wrapper.kpi-card-icon-blue svg,
html:not(.dark-theme)[data-colorblind="tritanopia"] .vendor-contracts-page .kpi-card-icon-wrapper.kpi-card-icon-blue svg,
html:not(.dark-theme)[data-colorblind="protanopia"] .vendor-contracts-page .kpi-card-icon-blue .kpi-card-icon-wrapper svg,
html:not(.dark-theme)[data-colorblind="deuteranopia"] .vendor-contracts-page .kpi-card-icon-blue .kpi-card-icon-wrapper svg,
html:not(.dark-theme)[data-colorblind="tritanopia"] .vendor-contracts-page .kpi-card-icon-blue .kpi-card-icon-wrapper svg,
/* Even more specific - target the exact structure */
html:not(.dark-theme)[data-colorblind="protanopia"] .vendor-contracts-page .kpi-card .kpi-card-content .kpi-card-icon-wrapper.kpi-card-icon-blue svg,
html:not(.dark-theme)[data-colorblind="deuteranopia"] .vendor-contracts-page .kpi-card .kpi-card-content .kpi-card-icon-wrapper.kpi-card-icon-blue svg,
html:not(.dark-theme)[data-colorblind="tritanopia"] .vendor-contracts-page .kpi-card .kpi-card-content .kpi-card-icon-wrapper.kpi-card-icon-blue svg,
html:not(.dark-theme)[data-colorblind="protanopia"] .vendor-contracts-page [class*="bg-primary/10"] svg,
html:not(.dark-theme)[data-colorblind="deuteranopia"] .vendor-contracts-page [class*="bg-primary/10"] svg,
html:not(.dark-theme)[data-colorblind="tritanopia"] .vendor-contracts-page [class*="bg-primary/10"] svg {
  color: #3b82f6 !important;
  fill: none !important;
  stroke: #3b82f6 !important;
  stroke-width: 2 !important;
}

html:not(.dark-theme)[data-colorblind="protanopia"] .vendor-contracts-page .kpi-card-icon-blue,
html:not(.dark-theme)[data-colorblind="deuteranopia"] .vendor-contracts-page .kpi-card-icon-blue,
html:not(.dark-theme)[data-colorblind="tritanopia"] .vendor-contracts-page .kpi-card-icon-blue,
html:not(.dark-theme)[data-colorblind="protanopia"] .vendor-contracts-page .kpi-card-icon-wrapper.kpi-card-icon-blue,
html:not(.dark-theme)[data-colorblind="deuteranopia"] .vendor-contracts-page .kpi-card-icon-wrapper.kpi-card-icon-blue,
html:not(.dark-theme)[data-colorblind="tritanopia"] .vendor-contracts-page .kpi-card-icon-wrapper.kpi-card-icon-blue {
  background-color: #dbeafe !important;
}

html:not(.dark-theme)[data-colorblind="protanopia"] .vendor-contracts-page [class*="bg-primary/10"],
html:not(.dark-theme)[data-colorblind="deuteranopia"] .vendor-contracts-page [class*="bg-primary/10"],
html:not(.dark-theme)[data-colorblind="tritanopia"] .vendor-contracts-page [class*="bg-primary/10"] {
  background-color: rgba(59, 130, 246, 0.1) !important;
}

/* Specifically target Building2 icons in KPI cards - catch all cases with maximum specificity */
html:not(.dark-theme)[data-colorblind="protanopia"] .vendor-contracts-page .kpi-card-icon-wrapper svg[data-lucide="building2"],
html:not(.dark-theme)[data-colorblind="deuteranopia"] .vendor-contracts-page .kpi-card-icon-wrapper svg[data-lucide="building2"],
html:not(.dark-theme)[data-colorblind="tritanopia"] .vendor-contracts-page .kpi-card-icon-wrapper svg[data-lucide="building2"],
html:not(.dark-theme)[data-colorblind="protanopia"] .vendor-contracts-page .kpi-card-icon-wrapper.kpi-card-icon-blue svg,
html:not(.dark-theme)[data-colorblind="deuteranopia"] .vendor-contracts-page .kpi-card-icon-wrapper.kpi-card-icon-blue svg,
html:not(.dark-theme)[data-colorblind="tritanopia"] .vendor-contracts-page .kpi-card-icon-wrapper.kpi-card-icon-blue svg,
/* Target ALL svg elements inside kpi-card-icon-blue wrapper - most aggressive */
html:not(.dark-theme)[data-colorblind="protanopia"] .vendor-contracts-page .kpi-card .kpi-card-icon-wrapper.kpi-card-icon-blue svg,
html:not(.dark-theme)[data-colorblind="deuteranopia"] .vendor-contracts-page .kpi-card .kpi-card-icon-wrapper.kpi-card-icon-blue svg,
html:not(.dark-theme)[data-colorblind="tritanopia"] .vendor-contracts-page .kpi-card .kpi-card-icon-wrapper.kpi-card-icon-blue svg {
  color: #3b82f6 !important;
  fill: none !important;
  stroke: #3b82f6 !important;
  stroke-width: 2 !important;
}

/* Remove hover effects from KPI cards */
.vendor-contracts-page .kpi-card:hover,
.vendor-contracts-page .kpi-card:hover .kpi-card-content,
.vendor-contracts-page .kpi-card-content:hover {
  background-color: #ffffff !important;
  background: #ffffff !important;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1) !important;
  transform: none !important;
  transition: none !important;
}
</style>