<template>
  <div class="flex-1 space-y-6 p-6 sla-expiring-page">
    <div class="flex items-center justify-between">
      <div>
        <h2 class="text-3xl font-bold tracking-tight">Expired & Expiring SLAs</h2>
        <p class="text-muted-foreground">
          SLAs that have expired or are approaching expiration and require renewal or review
        </p>
      </div>
      <div class="flex items-center gap-2">
        <span class="badge-priority-high">
          {{ expiringSLAs.filter(sla => sla.daysUntilExpiry <= 7).length }} CRITICAL
        </span>
        <span class="badge-priority-medium">
          {{ expiringSLAs.filter(sla => sla.daysUntilExpiry <= 30 && sla.daysUntilExpiry > 7).length }} UPCOMING
        </span>
        <span v-if="expiringSLAs.filter(sla => sla.notified).length > 0" class="badge-approved">
          {{ expiringSLAs.filter(sla => sla.notified).length }} NOTIFIED
        </span>
      </div>
    </div>

    <!-- Summary Cards -->
    <div class="kpi-cards-grid">
      <div class="kpi-card">
        <div class="kpi-card-content">
          <div class="kpi-card-icon-wrapper kpi-card-icon-red">
            <AlertTriangle />
          </div>
          <div class="kpi-card-text">
            <p class="kpi-card-title">Expired SLAs</p>
            <p class="kpi-card-value">{{ expiringSLAs.filter(sla => sla.status === 'EXPIRED' || sla.daysUntilExpiry < 0).length }}</p>
            <p class="kpi-card-subheading">Immediate renewal required</p>
          </div>
        </div>
      </div>
      
      <div class="kpi-card">
        <div class="kpi-card-content">
          <div class="kpi-card-icon-wrapper kpi-card-icon-orange">
            <AlertTriangle />
          </div>
          <div class="kpi-card-text">
            <p class="kpi-card-title">Expiring Soon (≤7 days)</p>
            <p class="kpi-card-value">{{ expiringSLAs.filter(sla => sla.daysUntilExpiry <= 7 && sla.daysUntilExpiry >= 0).length }}</p>
            <p class="kpi-card-subheading">Critical attention required</p>
          </div>
        </div>
      </div>

      <div class="kpi-card">
        <div class="kpi-card-content">
          <div class="kpi-card-icon-wrapper kpi-card-icon-yellow">
            <Calendar />
          </div>
          <div class="kpi-card-text">
            <p class="kpi-card-title">Expiring This Month</p>
            <p class="kpi-card-value">{{ expiringSLAs.filter(sla => sla.daysUntilExpiry <= 30 && sla.daysUntilExpiry > 7).length }}</p>
            <p class="kpi-card-subheading">Plan renewal actions</p>
          </div>
        </div>
      </div>

      <div class="kpi-card">
        <div class="kpi-card-content">
          <div class="kpi-card-icon-wrapper kpi-card-icon-blue">
            <Clock />
          </div>
          <div class="kpi-card-text">
            <p class="kpi-card-title">Manual Renewal Required</p>
            <p class="kpi-card-value">{{ expiringSLAs.filter(sla => !sla.autoRenewal).length }}</p>
            <p class="kpi-card-subheading">Manual intervention needed</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Filters -->
    <Card>
      <CardHeader>
        <CardTitle class="flex items-center gap-2">
          <Filter class="h-5 w-5" />
          Filters
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div class="flex gap-4 items-center">
          <div class="flex-1">
            <!-- Component-level styling from main.css -->
            <div class="search-container">
              <div class="search-input-wrapper">
                <Search class="search-icon" />
                <input
                  type="text"
                  class="search-input search-input--medium search-input--default"
                  placeholder="Search expiring SLAs..."
                  v-model="searchTerm"
                />
              </div>
            </div>
          </div>
          <SingleSelectDropdown
            v-model="criticalityFilter"
            :options="criticalityFilterOptions"
            placeholder="Criticality"
            height="2.5rem"
            width="180px"
          />
          <SingleSelectDropdown
            v-model="renewalFilter"
            :options="renewalFilterOptions"
            placeholder="Renewal Type"
            height="2.5rem"
            width="180px"
          />
        </div>
      </CardContent>
    </Card>

    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center p-8">
      <div class="text-center">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
        <p class="mt-2 text-sm text-muted-foreground">Loading expiring SLAs...</p>
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

    <!-- Expiring SLAs Table -->
    <Card v-else>
      <CardHeader>
        <CardTitle>Expired & Expiring SLAs</CardTitle>
        <CardDescription>
          SLAs that have expired or are approaching expiration and require renewal or review
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div class="overflow-x-hidden">
          <Table class="table-fixed w-full">
            <TableHeader>
              <TableRow>
                <TableHead class="w-[80px]">SLA ID</TableHead>
                <TableHead class="w-[200px]">SLA Name</TableHead>
                <TableHead class="w-[150px]">Vendor</TableHead>
                <TableHead class="w-[120px]">Expiry Date</TableHead>
                <TableHead class="w-[140px]">Days Until Expiry</TableHead>
                <TableHead class="w-[110px]">Criticality</TableHead>
                <TableHead class="w-[120px]">Auto-Renewal</TableHead>
                <TableHead class="w-[140px]">Renewal Status</TableHead>
                <TableHead class="w-[140px]">Notification Status</TableHead>
                <TableHead class="w-[120px]">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              <TableRow v-for="sla in filteredSLAs" :key="sla.id">
                <TableCell class="font-mono text-sm">{{ sla.id }}</TableCell>
                <TableCell class="font-medium break-words">{{ sla.name }}</TableCell>
                <TableCell class="break-words">{{ sla.vendor }}</TableCell>
              <TableCell>{{ sla.currentExpiry }}</TableCell>
              <TableCell>
                <div class="flex items-center gap-2">
                  <AlertTriangle v-if="sla.status === 'EXPIRED' || sla.daysUntilExpiry < 0" class="h-4 w-4 text-red-600" />
                  <AlertTriangle v-else-if="sla.daysUntilExpiry <= 7" class="h-4 w-4 text-orange-600" />
                  <Clock v-else-if="sla.daysUntilExpiry <= 30" class="h-4 w-4 text-yellow-600" />
                  <Calendar v-else class="h-4 w-4 text-green-600" />
                  <span :class="getExpiryUrgency(sla.daysUntilExpiry, sla.status)">
                    {{ sla.daysUntilExpiry < 0 ? 'Expired' : sla.daysUntilExpiry + ' days' }}
                  </span>
                </div>
              </TableCell>
              <TableCell>
                <span :class="getCriticalityBadgeClass(sla.criticality)">
                  {{ formatText(sla.criticality) }}
                </span>
              </TableCell>
              <TableCell>
                <span :class="getAutoRenewalBadgeClass(sla.autoRenewal)">
                  {{ sla.autoRenewal ? 'YES' : 'NO' }}
                </span>
              </TableCell>
              <TableCell>
                <span :class="getRenewalStatusBadgeClass(sla.renewalStatus)">
                  {{ formatRenewalStatusText(sla.renewalStatus) }}
                </span>
              </TableCell>
              <TableCell>
                <span :class="getNotificationBadgeClass(sla.notified)">
                  {{ sla.notified ? 'NOTIFIED' : 'PENDING' }}
                </span>
              </TableCell>
              <TableCell>
                <div class="flex items-center gap-2">
                  <Button 
                    :variant="sla.notified ? 'secondary' : (sla.status === 'EXPIRED' || sla.daysUntilExpiry < 0 ? 'destructive' : 'default')" 
                    size="sm" 
                    @click="handleRenewSLA(sla)"
                    :disabled="sla.notified"
                  >
                    <RefreshCw class="h-4 w-4" />
                    {{ sla.notified ? 'Notified' : (sla.status === 'EXPIRED' || sla.daysUntilExpiry < 0 ? 'Renew Now' : 'Renew') }}
                  </Button>
                  <Button 
                    v-if="sla.notified"
                    variant="outline" 
                    size="sm" 
                    @click="clearNotification(sla)"
                    class="flex items-center gap-1"
                  >
                    <X class="h-3 w-3" />
                    Clear
                  </Button>
                </div>
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
        </div>
      </CardContent>
    </Card>
  </div>

  <!-- Popup Modal -->
  <PopupModal />
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { AlertTriangle, Search, Filter, RefreshCw, Calendar, Clock, X } from 'lucide-vue-next'
import apiService from '@/services/api'
import PopupModal from '@/popup/PopupModal.vue'
import '@/assets/components/dropdown.css'
import SingleSelectDropdown from '@/assets/components/SingleSelectDropdown.vue'
import { PopupService } from '@/popup/popupService'
import { useNotifications } from '@/composables/useNotifications'
import loggingService from '@/services/loggingService'
import '@/assets/components/main.css'
import '@/assets/components/main.css'

const router = useRouter()
const { showSLASuccess, showSLAError, showSLAWarning, showInfo } = useNotifications()

const searchTerm = ref("")
const criticalityFilter = ref("all")
const renewalFilter = ref("all")

// Dropdown options
const criticalityFilterOptions = [
  { value: 'all', label: 'All Criticality' },
  { value: 'critical', label: 'Critical' },
  { value: 'high', label: 'High' },
  { value: 'medium', label: 'Medium' },
  { value: 'low', label: 'Low' }
]

const renewalFilterOptions = [
  { value: 'all', label: 'All Types' },
  { value: 'auto', label: 'Auto-Renewal' },
  { value: 'manual', label: 'Manual Renewal' }
]

const loading = ref(false)
const error = ref(null)

// API data
const expiringSLAs = ref([])

// Load data from API
const loadData = async () => {
  loading.value = true
  error.value = null
  
  try {
    // Load SLAs from backend
    const slasData = await apiService.getSLAs()
    
    // Filter SLAs that are expiring (within 90 days) or already expired
    const today = new Date()
    const ninetyDaysFromNow = new Date(today.getTime() + (90 * 24 * 60 * 60 * 1000))
    
    // Get notified SLAs from localStorage
    const notifiedSLAs = JSON.parse(localStorage.getItem('notifiedSLAs') || '[]')
    
    expiringSLAs.value = slasData.filter(sla => {
      const expiryDate = new Date(sla.expiry_date)
      const daysUntilExpiry = getDaysUntilExpiry(sla.expiry_date)
      
      // Include SLAs that are:
      // 1. Expired (status = 'EXPIRED' or daysUntilExpiry < 0)
      // 2. Expiring within 90 days (status = 'ACTIVE' and daysUntilExpiry <= 90)
      return (sla.status === 'EXPIRED' || daysUntilExpiry < 0) || 
             (sla.status === 'ACTIVE' && daysUntilExpiry <= 90)
    }).map(sla => ({
      id: sla.sla_id,
      name: sla.sla_name,
      vendor: getVendorName(sla),
      product: sla.business_service_impacted || 'Service',
      type: sla.sla_type,
      currentExpiry: sla.expiry_date,
      daysUntilExpiry: getDaysUntilExpiry(sla.expiry_date),
      status: sla.status,
      autoRenewal: determineAutoRenewal(sla),
      renewalStatus: getRenewalStatus(sla),
      criticality: getCriticalityLevel(sla),
      lastReview: sla.effective_date,
      notified: notifiedSLAs.includes(sla.sla_id),
      notifiedAt: notifiedSLAs.includes(sla.sla_id) ? new Date().toISOString() : null
    }))
    
    console.log('Loaded expiring/expired SLAs:', expiringSLAs.value.length)
    console.log('Notified SLAs from localStorage:', notifiedSLAs)
    console.log('SLAs with notified status:', expiringSLAs.value.filter(sla => sla.notified))
    
  } catch (err) {
    error.value = err.message
    console.error('Error loading expiring SLAs:', err)
    PopupService.error('Error loading expiring SLAs. Please try again later.', 'Loading Error')
  } finally {
    loading.value = false
  }
}

// Load data on component mount
onMounted(async () => {
  await loggingService.logPageView('SLA', 'Expiring SLAs')
  await loadData()
})

// Helper functions based on vendor_slas table data
const getDaysUntilExpiry = (expiryDate) => {
  const today = new Date()
  const expiry = new Date(expiryDate)
  const diff = Math.ceil((expiry.getTime() - today.getTime()) / (1000 * 60 * 60 * 24))
  return diff
}

// Helper function to get vendor name (handles both nested objects and ID-based relationships)
const getVendorName = (sla) => {
  // Check if SLA has nested vendor object
  if (sla.vendor && typeof sla.vendor === 'object') {
    return sla.vendor.company_name || 'Unknown Vendor'
  }
  
  // Fallback to looking up by vendor_id (if vendors array is available)
  if (sla.vendor_id) {
    // This would require loading vendors separately, for now return a placeholder
    return 'Vendor ID: ' + sla.vendor_id
  }
  
  return 'Unknown Vendor'
}

const determineAutoRenewal = (sla) => {
  // Determine auto-renewal based on SLA characteristics
  // In a real implementation, this would be a field in the database
  // For now, we'll use business logic based on SLA type and contract terms
  if (sla.sla_type === 'AVAILABILITY' && sla.business_service_impacted?.toLowerCase().includes('critical')) {
    return true // Critical services often have auto-renewal
  }
  if (sla.contract?.contract_type === 'MASTER_AGREEMENT') {
    return true // Master agreements often have auto-renewal
  }
  return false // Default to manual renewal
}

const getRenewalStatus = (sla) => {
  const days = getDaysUntilExpiry(sla.expiry_date)
  const autoRenewal = determineAutoRenewal(sla)
  
  // Handle expired SLAs
  if (sla.status === 'EXPIRED' || days < 0) {
    if (autoRenewal) return 'Expired - Auto-Renewal Failed'
    return 'Expired - Manual Renewal Required'
  }
  
  // Handle expiring SLAs
  if (autoRenewal && days <= 30) return 'Auto-Renewal Scheduled'
  if (days <= 7) return 'Critical - Renewal Required'
  if (days <= 30) return 'In Progress'
  return 'Under Review'
}

const getCriticalityLevel = (sla) => {
  const days = getDaysUntilExpiry(sla.expiry_date)
  const businessService = sla.business_service_impacted?.toLowerCase() || ''
  
  // Handle expired SLAs - always critical
  if (sla.status === 'EXPIRED' || days < 0) {
    return 'Critical'
  }
  
  // Determine criticality based on business impact and time remaining
  if (days <= 7) return 'Critical'
  if (days <= 30) {
    // High criticality for critical business services
    if (businessService.includes('critical') || businessService.includes('core') || 
        businessService.includes('payment') || businessService.includes('security')) {
      return 'High'
    }
    return 'High'
  }
  if (days <= 60) return 'Medium'
  return 'Low'
}


const filteredSLAs = computed(() => {
  return expiringSLAs.value.filter(sla => {
    const matchesSearch = sla.name.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
                         sla.vendor.toLowerCase().includes(searchTerm.value.toLowerCase())
    const matchesCriticality = criticalityFilter.value === "all" || sla.criticality.toLowerCase() === criticalityFilter.value
    const matchesRenewal = renewalFilter.value === "all" || 
                          (renewalFilter.value === "auto" && sla.autoRenewal) ||
                          (renewalFilter.value === "manual" && !sla.autoRenewal)
    
    return matchesSearch && matchesCriticality && matchesRenewal
  })
})

const getExpiryUrgency = (days, status) => {
  if (status === 'EXPIRED' || days < 0) return "text-red-600 font-bold"
  if (days <= 7) return "text-red-600 font-bold"
  if (days <= 30) return "text-yellow-600 font-medium"
  return "text-green-600"
}

const formatText = (text) => {
  if (!text) return 'UNKNOWN'
  return String(text).toUpperCase()
}

const formatRenewalStatusText = (status) => {
  if (!status) return 'UNKNOWN'
  return String(status).toUpperCase()
}

const getCriticalityBadgeClass = (criticality) => {
  if (!criticality) return 'badge-draft'
  
  const criticalityLower = String(criticality).toLowerCase()
  
  if (criticalityLower === 'critical') {
    return 'badge-priority-high' // Red
  } else if (criticalityLower === 'high') {
    return 'badge-priority-high' // Red
  } else if (criticalityLower === 'medium') {
    return 'badge-priority-medium' // Orange
  } else if (criticalityLower === 'low') {
    return 'badge-priority-low' // Blue
  }
  
  return 'badge-draft' // Default gray
}

const getAutoRenewalBadgeClass = (autoRenewal) => {
  if (autoRenewal) {
    return 'badge-approved' // Green
  }
  return 'badge-draft' // Gray
}

const getRenewalStatusBadgeClass = (status) => {
  if (!status) return 'badge-draft'
  
  const statusLower = String(status).toLowerCase()
  
  if (statusLower.includes('expired')) {
    return 'badge-expired' // Gray
  } else if (statusLower.includes('critical')) {
    return 'badge-priority-high' // Red
  } else if (statusLower.includes('auto-renewal')) {
    return 'badge-approved' // Green
  } else if (statusLower.includes('in progress')) {
    return 'badge-in-review' // Orange
  } else if (statusLower.includes('under review')) {
    return 'badge-in-review' // Orange
  }
  
  return 'badge-draft' // Default gray
}

const getNotificationBadgeClass = (notified) => {
  if (notified) {
    return 'badge-approved' // Green
  }
  return 'badge-draft' // Gray
}

// Handler functions
const handleRenewSLA = async (sla) => {
  console.log('Renewing SLA:', sla)
  
  try {
    // Show info notification about renewal process
    await showInfo('SLA Renewal Initiated', `Starting renewal process for SLA "${sla.name}"`, {
      sla_id: sla.id,
      sla_name: sla.name,
      action: 'renewal_initiated'
    })
    
    // Mark SLA as notified in localStorage for persistence
    const notifiedSLAs = JSON.parse(localStorage.getItem('notifiedSLAs') || '[]')
    if (!notifiedSLAs.includes(sla.id)) {
      notifiedSLAs.push(sla.id)
      localStorage.setItem('notifiedSLAs', JSON.stringify(notifiedSLAs))
    }
    
    // Mark SLA as notified in local state
    const slaIndex = expiringSLAs.value.findIndex(s => s.id === sla.id)
    if (slaIndex !== -1) {
      expiringSLAs.value[slaIndex].notified = true
      expiringSLAs.value[slaIndex].notifiedAt = new Date().toISOString()
    }
    
    // Navigate to SLA renewal page with SLA data
    router.push({
      path: '/slas/renew',
      query: {
        slaId: sla.id,
        slaName: sla.name,
        vendor: sla.vendor,
        currentExpiry: sla.currentExpiry,
        daysUntilExpiry: sla.daysUntilExpiry,
        status: sla.status,
        businessService: sla.product
      }
    })
  } catch (error) {
    console.error('Error initiating SLA renewal:', error)
    await showSLAError('renewal_initiation_failed', error.message, {
      sla_id: sla.id,
      sla_name: sla.name
    })
  }
}

const clearNotification = async (sla) => {
  try {
    // Show info notification about clearing notification
    await showInfo('SLA Notification Cleared', `Cleared notification for SLA "${sla.name}"`, {
      sla_id: sla.id,
      sla_name: sla.name,
      action: 'notification_cleared'
    })
    
    // Remove from localStorage
    const notifiedSLAs = JSON.parse(localStorage.getItem('notifiedSLAs') || '[]')
    const updatedNotifiedSLAs = notifiedSLAs.filter(id => id !== sla.id)
    localStorage.setItem('notifiedSLAs', JSON.stringify(updatedNotifiedSLAs))
    
    // Update local state
    const slaIndex = expiringSLAs.value.findIndex(s => s.id === sla.id)
    if (slaIndex !== -1) {
      expiringSLAs.value[slaIndex].notified = false
      expiringSLAs.value[slaIndex].notifiedAt = null
    }
  } catch (error) {
    console.error('Error clearing notification:', error)
    await showSLAError('notification_clear_failed', error.message, {
      sla_id: sla.id,
      sla_name: sla.name
    })
  }
}
</script>

<style scoped>
@import '@/assets/components/main.css';
@import '@/assets/components/badge.css';

/* Prevent horizontal scrolling */
.sla-expiring-page {
  overflow-x: hidden;
  max-width: 100vw;
}

/* Ensure table fits within container */
.sla-expiring-page .overflow-x-hidden {
  overflow-x: hidden;
  max-width: 100%;
}

.sla-expiring-page table {
  table-layout: fixed;
  width: 100%;
}

.sla-expiring-page table td,
.sla-expiring-page table th {
  word-wrap: break-word;
  overflow-wrap: break-word;
  white-space: normal;
  padding: 0.75rem;
  vertical-align: top;
}

/* Allow table rows to expand vertically */
.sla-expiring-page table tbody tr {
  height: auto;
}

.sla-expiring-page table tbody td {
  height: auto;
  min-height: 3rem;
}

/* Ensure search input doesn't overflow */
.sla-expiring-page .search-container {
  width: 100%;
  max-width: 100%;
}

.sla-expiring-page .search-input-wrapper {
  width: 100%;
  max-width: 100%;
}

.sla-expiring-page .search-input {
  width: 100%;
  max-width: 100%;
}

/* Ensure table cells with long text wrap properly */
.sla-expiring-page .font-medium,
.sla-expiring-page .break-words {
  word-wrap: break-word;
  overflow-wrap: break-word;
  white-space: normal;
  line-height: 1.5;
}

/* Allow text to wrap to multiple lines */
.sla-expiring-page table td p,
.sla-expiring-page table td span {
  word-wrap: break-word;
  overflow-wrap: break-word;
  white-space: normal;
  max-width: 100%;
}
</style>
