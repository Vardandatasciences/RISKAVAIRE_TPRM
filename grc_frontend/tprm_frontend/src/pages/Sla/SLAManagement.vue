<template>
  <div class="space-y-6 sla-management-page">
    <!-- Page Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold tracking-tight">SLA Management</h1>
        <p class="text-muted-foreground">Manage service level agreements across vendors and contracts</p>
      </div>
      <div class="flex items-center gap-2">
        <RouterLink to="/slas/extract">
          <Button variant="outline">
            <FileText class="h-4 w-4 mr-2" />
            Extract from Document
          </Button>
        </RouterLink>
        <Button @click="handleCreateSLA" variant="ghost" class="button button--create">
          <Plus class="h-4 w-4 mr-2" />
          Create New SLA
        </Button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center p-8">
      <div class="text-center">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
        <p class="mt-2 text-sm text-muted-foreground">Loading data...</p>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-md p-4">
      <div class="flex">
        <div class="ml-3">
          <h3 class="text-sm font-medium text-red-800">Error loading data</h3>
          <div class="mt-2 text-sm text-red-700">
            <p>{{ error }}</p>
          </div>
          <div class="mt-4">
            <button @click="loadData" class="bg-red-100 px-3 py-2 rounded-md text-sm font-medium text-red-800 hover:bg-red-200">
              Try again
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Summary Cards -->
    <div v-else class="kpi-cards-grid">
      <div class="kpi-card">
        <div class="kpi-card-content">
          <div class="kpi-card-icon-wrapper kpi-card-icon-gray">
            <FileText />
          </div>
          <div class="kpi-card-text">
            <p class="kpi-card-title">Total SLAs</p>
            <p class="kpi-card-value">{{ dashboardStats.total_slas || allSLAs.length }}</p>
            <p class="kpi-card-subheading">Across all vendors and contracts</p>
          </div>
        </div>
      </div>
      <div class="kpi-card">
        <div class="kpi-card-content">
          <div class="kpi-card-icon-wrapper kpi-card-icon-green">
            <CheckCircle />
          </div>
          <div class="kpi-card-text">
            <p class="kpi-card-title">Active SLAs</p>
            <p class="kpi-card-value">{{ dashboardStats.active_slas || allSLAs.filter(s => s.status === 'ACTIVE').length }}</p>
            <p class="kpi-card-subheading">Currently active agreements</p>
          </div>
        </div>
      </div>
      <div class="kpi-card">
        <div class="kpi-card-content">
          <div class="kpi-card-icon-wrapper kpi-card-icon-blue">
            <Clock />
          </div>
          <div class="kpi-card-text">
            <p class="kpi-card-title">Pending SLAs</p>
            <p class="kpi-card-value">{{ dashboardStats.pending_slas || allSLAs.filter(s => s.status === 'PENDING').length }}</p>
            <p class="kpi-card-subheading">Awaiting activation</p>
          </div>
        </div>
      </div>
      <div class="kpi-card">
        <div class="kpi-card-content">
          <div class="kpi-card-icon-wrapper kpi-card-icon-orange">
            <AlertTriangle />
          </div>
          <div class="kpi-card-text">
            <p class="kpi-card-title">Expiring Soon</p>
            <p class="kpi-card-value">{{ dashboardStats.expiring_soon || allSLAs.filter(s => { const d = getDaysUntilExpiry(s.expiry_date); return d > 0 && d <= 30 }).length }}</p>
            <p class="kpi-card-subheading">Within 30 days</p>
          </div>
        </div>
      </div>
    </div>

    <div class="space-y-6">
      <!-- Simple Tab Navigation -->
      <div class="grid w-full grid-cols-3 border-b">
        <button 
          @click="activeTab = 'all'"
          :class="activeTab === 'all' ? 'border-b-2 border-blue-500 text-blue-600' : 'text-gray-500 hover:text-gray-700'"
          class="px-4 py-2 text-sm font-medium"
        >
          All SLAs
        </button>
        <button 
          @click="activeTab = 'vendors'"
          :class="activeTab === 'vendors' ? 'border-b-2 border-blue-500 text-blue-600' : 'text-gray-500 hover:text-gray-700'"
          class="px-4 py-2 text-sm font-medium"
        >
          Vendor View
        </button>
        <button 
          @click="activeTab = 'contracts'"
          :class="activeTab === 'contracts' ? 'border-b-2 border-blue-500 text-blue-600' : 'text-gray-500 hover:text-gray-700'"
          class="px-4 py-2 text-sm font-medium"
        >
          Contract View
        </button>
      </div>

      <div v-if="activeTab === 'all'" class="space-y-6">
        <!-- Filters -->
        <Card>
          <CardHeader>
            <CardTitle class="flex items-center gap-2">
              <Filter class="h-5 w-5" />
              Filters
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div class="space-y-4">
              <!-- Search Bar Row -->
              <div class="search-container">
                <div class="search-input-wrapper">
                  <Search class="search-icon" />
                  <input
                    type="text"
                    class="search-input search-input--medium search-input--default"
                    placeholder="Search SLAs..."
                    v-model="searchTerm"
                  />
                </div>
              </div>
              
              <!-- Dropdowns Row -->
              <div class="grid gap-4 grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 xl:grid-cols-6">
                <SingleSelectDropdown
                  v-model="vendorFilter"
                  :options="vendorFilterOptions"
                  placeholder="Vendor"
                  height="2.5rem"
                />
                <SingleSelectDropdown
                  v-model="contractFilter"
                  :options="contractFilterOptions"
                  placeholder="Contract"
                  height="2.5rem"
                />
                <SingleSelectDropdown
                  v-model="statusFilter"
                  :options="statusFilterOptions"
                  placeholder="Status"
                  height="2.5rem"
                />
                <SingleSelectDropdown
                  v-model="typeFilter"
                  :options="typeFilterOptions"
                  placeholder="Type"
                  height="2.5rem"
                />
                <div class="flex gap-2 col-span-1 sm:col-span-2 lg:col-span-2">
                  <Input type="date" v-model="dateRange.start" class="flex-1" />
                  <Input type="date" v-model="dateRange.end" class="flex-1" />
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <!-- SLA Table -->
        <Card>
          <CardHeader>
            <CardTitle>SLA List</CardTitle>
            <CardDescription>{{ filteredSLAs.length }} SLAs found</CardDescription>
          </CardHeader>
          <CardContent>
            <div class="overflow-x-hidden">
              <Table class="table-fixed w-full">
                <TableHeader>
                <TableRow>
                  <TableHead class="w-[200px]">SLA Name</TableHead>
                  <TableHead class="w-[150px]">Vendor</TableHead>
                  <TableHead class="w-[180px]">Contract/Product</TableHead>
                  <TableHead class="w-[120px]">Type</TableHead>
                  <TableHead class="w-[100px]">Status</TableHead>
                  <TableHead class="w-[100px]">Compliance</TableHead>
                  <TableHead class="w-[100px]">Priority</TableHead>
                  <TableHead class="w-[120px]">Effective Date</TableHead>
                  <TableHead class="w-[120px]">Expiry</TableHead>
                  <TableHead class="w-[100px]">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                <TableRow v-for="sla in filteredSLAs" :key="sla.sla_id">
                  <TableCell>
                    <div class="flex items-start gap-2 min-w-0">
                      <component :is="getTypeIcon(sla.sla_type)" class="h-4 w-4 text-muted-foreground flex-shrink-0 mt-0.5" />
                      <div class="min-w-0 flex-1">
                        <p class="font-medium break-words">{{ sla.sla_name }}</p>
                        <p class="text-xs text-muted-foreground">v{{ sla.document_versioning || '1.0' }}</p>
                      </div>
                    </div>
                  </TableCell>
                  <TableCell>
                    <div class="flex items-start gap-2 min-w-0">
                      <Building class="h-4 w-4 text-muted-foreground flex-shrink-0 mt-0.5" />
                      <span class="break-words">{{ getVendorName(sla) }}</span>
                    </div>
                  </TableCell>
                  <TableCell>
                    <div class="min-w-0">
                      <p class="text-sm font-medium break-words">{{ getContractName(sla) }}</p>
                      <p class="text-xs text-muted-foreground break-words">{{ sla.business_service_impacted }}</p>
                    </div>
                  </TableCell>
                  <TableCell><Badge variant="outline">{{ sla.sla_type }}</Badge></TableCell>
                  <TableCell>
                    <span :class="getStatusBadgeClass(sla.status)">
                      {{ formatStatusText(sla.status) }}
                    </span>
                  </TableCell>
                  <TableCell>
                    <span :class="getComplianceBadgeClass(sla.compliance_score || 0)">
                      {{ sla.compliance_score || 0 }}%
                    </span>
                  </TableCell>
                  <TableCell>
                    <span :class="getPriorityBadgeClass(sla.priority?.toLowerCase() || 'medium')">
                      {{ formatPriorityText(sla.priority || 'Medium') }}
                    </span>
                  </TableCell>
                  <TableCell>{{ sla.effective_date }}</TableCell>
                  <TableCell>
                    <div :class="'text-sm ' + getExpiryStatus(getDaysUntilExpiry(sla.expiry_date)).color">
                      {{ sla.expiry_date }}
                      <br />
                      <span class="text-xs">{{ getDaysUntilExpiry(sla.expiry_date) < 0 ? 'Expired' : getDaysUntilExpiry(sla.expiry_date) + ' days' }}</span>
                    </div>
                  </TableCell>
                  <TableCell>
                    <div class="flex items-center gap-2">
                      <button class="button button--view" @click="handleViewSLA(sla)">
                        View
                      </button>
                    </div>
                  </TableCell>
                </TableRow>
              </TableBody>
            </Table>
            </div>
          </CardContent>
        </Card>
      </div>

      <div v-if="activeTab === 'vendors'" class="space-y-6">
        <div v-if="loading" class="flex items-center justify-center p-8">
          <div class="text-center">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
            <p class="mt-2 text-sm text-muted-foreground">Loading vendor data...</p>
          </div>
        </div>
        <div v-else-if="vendorsWithContracts.length === 0" class="text-center p-8">
          <p class="text-muted-foreground">No vendor data available</p>
        </div>
        <div v-else class="grid gap-6">
          <Card v-for="v in vendorsWithContracts" :key="v.id">
            <CardHeader>
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-3">
                  <Building class="h-6 w-6 text-primary" />
                  <div>
                    <CardTitle>{{ v.name }}</CardTitle>
                    <CardDescription>{{ v.contracts.length }} contracts • {{ v.contracts.flatMap(c => c.slas).length }} SLAs</CardDescription>
                  </div>
                </div>
                <Button variant="outline" size="sm" @click="handleViewVendor(v)">View Details</Button>
              </div>
            </CardHeader>
            <CardContent>
              <div class="space-y-4">
                <div v-for="c in v.contracts" :key="c.id" class="border rounded-lg p-4">
                  <div class="flex items-center justify-between mb-3">
                    <h4 class="font-medium">{{ c.name }}</h4>
                    <Badge variant="outline">{{ c.slas.length }} SLAs</Badge>
                  </div>
                  <div class="grid gap-2">
                    <div v-for="s in c.slas" :key="s.id" class="flex items-center justify-between p-2 border rounded">
                      <div class="flex items-center gap-2">
                        <component :is="getTypeIcon(s.type)" class="h-4 w-4" />
                        <span class="text-sm font-medium">{{ s.name }}</span>
                      </div>
                      <div class="flex items-center gap-2">
                        <span :class="getStatusBadgeClass(s.status)">
                          {{ formatStatusText(s.status) }}
                        </span>
                        <span :class="getComplianceBadgeClass(s.compliance)">
                          {{ s.compliance }}%
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      <div v-if="activeTab === 'contracts'" class="space-y-6">
        <div v-if="loading" class="flex items-center justify-center p-8">
          <div class="text-center">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
            <p class="mt-2 text-sm text-muted-foreground">Loading contract data...</p>
          </div>
        </div>
        <div v-else-if="contractsWithSLAs.length === 0" class="text-center p-8">
          <p class="text-muted-foreground">No contract data available</p>
        </div>
        <div v-else class="grid gap-6">
          <Card v-for="c in contractsWithSLAs" :key="c.id">
            <CardHeader>
              <div class="flex items-center justify-between">
                <div>
                  <CardTitle>{{ c.name }}</CardTitle>
                  <CardDescription>{{ c.slas.length }} SLAs • {{ c.slas.filter(s => s.status === 'ACTIVE').length }} Active</CardDescription>
                </div>
                <div class="flex items-center gap-2">
                  <Badge variant="outline">{{ c.slas.length }} SLAs</Badge>
                  <Button variant="outline" size="sm" @click="handleAddSLAToContract(c)"><Plus class="h-4 w-4 mr-2" />Add SLA</Button>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <div class="overflow-x-hidden">
                <Table class="table-fixed w-full">
                  <TableHeader>
                    <TableRow>
                      <TableHead>SLA Name</TableHead>
                      <TableHead>Type</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead>Compliance</TableHead>
                      <TableHead>Expiry</TableHead>
                      <TableHead>Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    <TableRow v-for="s in c.slas" :key="s.id">
                      <TableCell>
                        <div class="flex items-start gap-2 min-w-0">
                          <component :is="getTypeIcon(s.type)" class="h-4 w-4 flex-shrink-0 mt-0.5" />
                          <div class="min-w-0 flex-1">
                            <p class="font-medium break-words">{{ s.name }}</p>
                            <p class="text-xs text-muted-foreground">v{{ s.version }}</p>
                          </div>
                        </div>
                      </TableCell>
                    <TableCell><Badge variant="outline">{{ s.type }}</Badge></TableCell>
                    <TableCell>
                      <span :class="getStatusBadgeClass(s.status)">
                        {{ formatStatusText(s.status) }}
                      </span>
                    </TableCell>
                    <TableCell>
                      <span :class="getComplianceBadgeClass(s.compliance)">
                        {{ s.compliance }}%
                      </span>
                    </TableCell>
                    <TableCell>
                      <div :class="'text-sm ' + getExpiryStatus(getDaysUntilExpiry(s.expiryDate)).color">
                        {{ s.expiryDate }}
                        <br />
                        <span class="text-xs">{{ getDaysUntilExpiry(s.expiryDate) < 0 ? 'Expired' : getDaysUntilExpiry(s.expiryDate) + ' days' }}</span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div class="flex items-center gap-2">
                        <button class="button button--view" @click="router.push(`/slas/${s.id}`)">
                          View
                        </button>
                        <RouterLink :to="`/slas/${s.id}/edit`"><Button variant="ghost" size="sm"><Edit class="h-4 w-4" /></Button></RouterLink>
                      </div>
                    </TableCell>
                  </TableRow>
                </TableBody>
              </Table>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  </div>

  <!-- Popup Modal -->
  <PopupModal />
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { 
  Plus, Download, Clock, Shield, Zap, Database, Users, CheckCircle, FileText, Building, Filter, Search, Eye, Edit, AlertTriangle, BarChart3
} from 'lucide-vue-next'
import apiService from '@/services/api'
import { useRouter } from 'vue-router'
import PopupModal from '@/popup/PopupModal.vue'
import '@/assets/components/main.css'
import '@/assets/components/dropdown.css'
import { PopupService } from '@/popup/popupService'
import { usePermissions } from '@/composables/usePermissions'
import loggingService from '@/services/loggingService'
import '@/assets/components/main.css'
import SingleSelectDropdown from '@/assets/components/SingleSelectDropdown.vue'

const router = useRouter()
const { withPermissionCheck } = usePermissions()
const activeTab = ref('all')
const searchTerm = ref('')
const vendorFilter = ref('all')
const contractFilter = ref('all')
const statusFilter = ref('all')
const typeFilter = ref('all')
const dateRange = ref({ start: '', end: '' })
const loading = ref(false)
const error = ref(null)

// API data
const vendors = ref([])
const contracts = ref([])
const slas = ref([])
const dashboardStats = ref({})

// Load data from API
const loadData = async () => {
  loading.value = true
  error.value = null
  
  try {
    // Load vendors
    const vendorsData = await withPermissionCheck(() => apiService.getVendors())
    vendors.value = Array.isArray(vendorsData) ? vendorsData : []
    
    // Load contracts
    const contractsData = await withPermissionCheck(() => apiService.getContracts())
    contracts.value = Array.isArray(contractsData) ? contractsData : []
    
    // Load SLAs with proper vendor and contract relationships
    const slasData = await withPermissionCheck(() => apiService.getSLAs())
    slas.value = Array.isArray(slasData) ? slasData : []
    
    // Debug: Log the structure of the first SLA to understand the data format
    if (slas.value.length > 0) {
      console.log('First SLA structure:', slas.value[0])
      console.log('Total SLAs loaded:', slas.value.length)
    }
    
    // Debug: Log vendor and contract data
    console.log('Vendors loaded:', vendors.value.length)
    console.log('Contracts loaded:', contracts.value.length)
    
    // Debug: Check vendor and contract view data
    console.log('Vendors with contracts:', vendorsWithContracts.value.length)
    console.log('Contracts with SLAs:', contractsWithSLAs.value.length)
    
    // Load dashboard stats
    try {
      const statsData = await apiService.getDashboardStats()
      dashboardStats.value = statsData || {}
    } catch (statsError) {
      console.warn('Dashboard stats not available:', statsError)
      dashboardStats.value = {}
    }
    
  } catch (err) {
    error.value = err.message
    console.error('Error loading data:', err)
    PopupService.error('Error loading SLA management data. Please try again later.', 'Loading Error')
  } finally {
    loading.value = false
  }
}

// Load data on component mount
onMounted(async () => {
  await loggingService.logPageView('SLA', 'SLA Management')
  await loadData()
})


const allContracts = computed(() => Array.isArray(contracts.value) ? contracts.value : [])

// Dropdown options
const vendorFilterOptions = computed(() => {
  return [
    { value: 'all', label: 'All Vendors' },
    ...vendors.value.map(v => ({
      value: v.company_name,
      label: v.company_name
    }))
  ]
})

const contractFilterOptions = computed(() => {
  return [
    { value: 'all', label: 'All Contracts' },
    ...allContracts.value.map(c => ({
      value: c.contract_name,
      label: c.contract_name
    }))
  ]
})

const statusFilterOptions = [
  { value: 'all', label: 'All Status' },
  { value: 'ACTIVE', label: 'Active' },
  { value: 'EXPIRED', label: 'Expired' },
  { value: 'PENDING', label: 'Pending' }
]

const typeFilterOptions = [
  { value: 'all', label: 'All Types' },
  { value: 'AVAILABILITY', label: 'Availability' },
  { value: 'RESPONSE_TIME', label: 'Response Time' },
  { value: 'RESOLUTION_TIME', label: 'Resolution Time' },
  { value: 'QUALITY', label: 'Quality' },
  { value: 'CUSTOM', label: 'Custom' }
]
const allSLAs = computed(() => Array.isArray(slas.value) ? slas.value : [])

// Helper functions to get vendor and contract names
// These functions handle both cases:
// 1. When API returns nested objects (vendor, contract)
// 2. When API returns only IDs (vendor_id, contract_id)
const getVendorName = (sla) => {
  // Check if SLA has nested vendor object
  if (sla.vendor && typeof sla.vendor === 'object') {
    return sla.vendor.company_name || 'Unknown Vendor'
  }
  
  // Fallback to looking up by vendor_id
  if (sla.vendor_id) {
    const vendor = vendors.value.find(v => v.vendor_id === sla.vendor_id)
    return vendor?.company_name || 'Unknown Vendor'
  }
  
  return 'Unknown Vendor'
}

const getContractName = (sla) => {
  // Check if SLA has nested contract object
  if (sla.contract && typeof sla.contract === 'object') {
    return sla.contract.contract_name || 'Unknown Contract'
  }
  
  // Fallback to looking up by contract_id
  if (sla.contract_id) {
    const contract = contracts.value.find(c => c.contract_id === sla.contract_id)
    return contract?.contract_name || 'Unknown Contract'
  }
  
  return 'Unknown Contract'
}

// Transform API data for vendor view
const vendorsWithContracts = computed(() => {
  if (!Array.isArray(vendors.value) || !Array.isArray(contracts.value) || !Array.isArray(slas.value)) {
    return []
  }
  
  return vendors.value.map(vendor => ({
    id: vendor.vendor_id,
    name: vendor.company_name,
    contracts: contracts.value
      .filter(contract => {
        // Find SLAs that belong to this vendor and contract
        return slas.value.some(sla => {
          // Handle both nested objects and ID-based relationships
          const slaVendorId = sla.vendor_id || (sla.vendor?.vendor_id)
          const slaContractId = sla.contract_id || (sla.contract?.contract_id)
          return slaVendorId === vendor.vendor_id && slaContractId === contract.contract_id
        })
      })
      .map(contract => ({
        id: contract.contract_id,
        name: contract.contract_name,
        slas: slas.value.filter(sla => {
          // Handle both nested objects and ID-based relationships
          const slaVendorId = sla.vendor_id || (sla.vendor?.vendor_id)
          const slaContractId = sla.contract_id || (sla.contract?.contract_id)
          return slaVendorId === vendor.vendor_id && slaContractId === contract.contract_id
        }).map(sla => ({
          id: sla.sla_id,
          name: sla.sla_name,
          type: sla.sla_type,
          status: sla.status,
          compliance: 0, // Will be calculated from actual compliance data
          version: sla.document_versioning || '1.0'
        }))
      }))
  })).filter(vendor => vendor.contracts.length > 0)
})

// Transform API data for contract view
const contractsWithSLAs = computed(() => {
  if (!Array.isArray(contracts.value) || !Array.isArray(slas.value)) {
    return []
  }
  
  return contracts.value.map(contract => ({
    id: contract.contract_id,
    name: contract.contract_name,
    slas: slas.value.filter(sla => {
      // Handle both nested objects and ID-based relationships
      const slaContractId = sla.contract_id || (sla.contract?.contract_id)
      return slaContractId === contract.contract_id
    }).map(sla => ({
      id: sla.sla_id,
      name: sla.sla_name,
      type: sla.sla_type,
      status: sla.status,
      compliance: 0, // Will be calculated from actual compliance data
      version: sla.document_versioning || '1.0',
      expiryDate: sla.expiry_date
    }))
  })).filter(contract => contract.slas.length > 0)
})

const filteredSLAs = computed(() => {
  return allSLAs.value.filter(sla => {
    // Get vendor and contract names using helper functions
    const vendorName = getVendorName(sla)
    const contractName = getContractName(sla)
    
    const matchesSearch = sla.sla_name?.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
      vendorName.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
      contractName.toLowerCase().includes(searchTerm.value.toLowerCase())
    const matchesVendor = vendorFilter.value === 'all' || vendorName === vendorFilter.value
    const matchesContract = contractFilter.value === 'all' || contractName === contractFilter.value
    const matchesStatus = statusFilter.value === 'all' || sla.status === statusFilter.value
    const matchesType = typeFilter.value === 'all' || sla.sla_type === typeFilter.value
    const matchesDate = !dateRange.value.start || !dateRange.value.end ||
      (sla.effective_date >= dateRange.value.start && sla.effective_date <= dateRange.value.end)
    return matchesSearch && matchesVendor && matchesContract && matchesStatus && matchesType && matchesDate
  })
})

function formatStatusText(status) {
  if (!status) return 'UNKNOWN'
  return String(status).toUpperCase()
}

function formatPriorityText(priority) {
  if (!priority) return 'MEDIUM'
  return String(priority).charAt(0).toUpperCase() + String(priority).slice(1).toLowerCase()
}

function getStatusBadgeClass(status) {
  if (!status) return 'badge-draft'
  
  const statusUpper = String(status).toUpperCase()
  
  // Map SLA statuses to badge classes
  if (statusUpper === 'ACTIVE') {
    return 'badge-approved' // Green
  } else if (statusUpper === 'EXPIRED') {
    return 'badge-expired' // Gray
  } else if (statusUpper === 'PENDING') {
    return 'badge-pending-assignment' // Orange
  }
  
  return 'badge-draft' // Default gray
}

function getComplianceBadgeClass(compliance) {
  // Map compliance scores to badge classes
  if (compliance >= 95) {
    return 'badge-approved' // Green for high compliance
  } else if (compliance >= 85) {
    return 'badge-priority-medium' // Orange/amber for medium compliance
  } else {
    return 'badge-priority-high' // Red for low compliance
  }
}

function getPriorityBadgeClass(priority) {
  if (!priority) return 'badge-priority-medium'
  
  const priorityLower = String(priority).toLowerCase()
  
  // Map priority levels to badge classes
  if (priorityLower === 'critical' || priorityLower === 'high') {
    return 'badge-priority-high' // Red
  } else if (priorityLower === 'medium') {
    return 'badge-priority-medium' // Orange
  } else if (priorityLower === 'low') {
    return 'badge-priority-low' // Blue
  }
  
  return 'badge-priority-medium' // Default medium
}

function getTypeIcon(type) {
  switch (type) {
    case 'AVAILABILITY': return CheckCircle
    case 'RESPONSE_TIME': return Clock
    case 'RESOLUTION_TIME': return Clock
    case 'QUALITY': return BarChart3
    case 'CUSTOM': return FileText
    default: return Database
  }
}

function getDaysUntilExpiry(expiryDate) {
  const today = new Date()
  const expiry = new Date(expiryDate)
  const diff = Math.ceil((expiry.getTime() - today.getTime()) / (1000 * 60 * 60 * 24))
  return diff
}

function getExpiryStatus(days) {
  if (days < 0) return { status: 'expired', color: 'text-red-600' }
  if (days <= 30) return { status: 'expiring soon', color: 'text-orange-600' }
  if (days <= 90) return { status: 'expiring', color: 'text-yellow-600' }
  return { status: 'active', color: 'text-green-600' }
}

// Handle Create SLA button click
const handleCreateSLA = () => {
  // Navigate to create SLA page
  router.push('/slas/create')
}

// Handle View SLA button click
const handleViewSLA = (sla) => {
  // Navigate to SLA detail page
  router.push(`/slas/${sla.sla_id}`)
}

// Handle Edit SLA button click
const handleEditSLA = (sla) => {
  // Navigate to SLA edit page
  router.push(`/slas/${sla.sla_id}/edit`)
}

// Handle View Vendor button click
const handleViewVendor = (vendor) => {
  // Navigate to vendor detail page or show vendor information
  console.log('Viewing vendor:', vendor)
  // You can implement navigation to vendor detail page here
  // router.push(`/vendors/${vendor.id}`)
}

// Handle Add SLA to Contract button click
const handleAddSLAToContract = (contract) => {
  // Navigate to create SLA page with contract pre-selected
  console.log('Adding SLA to contract:', contract)
  router.push(`/slas/create?contract_id=${contract.id}`)
}

</script>

<style scoped>
@import '@/assets/components/main.css';
@import '@/assets/components/badge.css';

/* Prevent horizontal scrolling */
.sla-management-page {
  overflow-x: hidden;
  max-width: 100vw;
}

/* Ensure table fits within container */
.sla-management-page .overflow-x-hidden {
  overflow-x: hidden;
  max-width: 100%;
}

.sla-management-page table {
  table-layout: fixed;
  width: 100%;
}

.sla-management-page table td,
.sla-management-page table th {
  word-wrap: break-word;
  overflow-wrap: break-word;
  white-space: normal;
  padding: 0.75rem;
  vertical-align: top;
}

/* Allow table rows to expand vertically */
.sla-management-page table tbody tr {
  height: auto;
}

.sla-management-page table tbody td {
  height: auto;
  min-height: 3rem;
}

/* Ensure search input doesn't overflow */
.sla-management-page .search-container {
  width: 100%;
  max-width: 100%;
}

.sla-management-page .search-input-wrapper {
  width: 100%;
  max-width: 100%;
}

.sla-management-page .search-input {
  width: 100%;
  max-width: 100%;
}

/* Ensure table cells with long text wrap properly */
.sla-management-page .font-medium,
.sla-management-page .break-words {
  word-wrap: break-word;
  overflow-wrap: break-word;
  white-space: normal;
  line-height: 1.5;
}

/* Allow text to wrap to multiple lines */
.sla-management-page table td p,
.sla-management-page table td span {
  word-wrap: break-word;
  overflow-wrap: break-word;
  white-space: normal;
  max-width: 100%;
}
</style>
