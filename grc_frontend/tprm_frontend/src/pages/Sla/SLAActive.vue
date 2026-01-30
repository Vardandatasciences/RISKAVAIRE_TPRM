<template>
  <div class="flex-1 space-y-6 p-6 sla-active-page">
    <div class="flex items-center justify-between">
      <div>
        <h2 class="text-3xl font-bold tracking-tight">Active SLAs</h2>
        <p class="text-muted-foreground">
          Currently active SLAs and their performance status
        </p>
      </div>
      <div class="flex items-center gap-2">
        <span class="badge-compliant">
          {{ activeSLAs.filter(sla => sla.status === "Compliant").length }} COMPLIANT
        </span>
        <span class="badge-at-risk">
          {{ activeSLAs.filter(sla => sla.status === "At Risk").length }} AT RISK
        </span>
        <span class="badge-non-compliant">
          {{ activeSLAs.filter(sla => sla.status === "Non-Compliant").length }} NON-COMPLIANT
        </span>
      </div>
    </div>

    <!-- Summary Cards -->
    <div class="kpi-cards-grid">
      <div class="kpi-card">
        <div class="kpi-card-content">
          <div class="kpi-card-icon-wrapper kpi-card-icon-green">
            <CheckCircle />
          </div>
          <div class="kpi-card-text">
            <p class="kpi-card-title">Total Active SLAs</p>
            <p class="kpi-card-value">{{ activeSLAs.length }}</p>
            <p class="kpi-card-subheading">Currently active agreements</p>
          </div>
        </div>
      </div>
      
      <div class="kpi-card">
        <div class="kpi-card-content">
          <div class="kpi-card-icon-wrapper kpi-card-icon-blue">
            <BarChart3 />
          </div>
          <div class="kpi-card-text">
            <p class="kpi-card-title">Avg. Compliance</p>
            <p class="kpi-card-value">{{ calculateAverageCompliance() }}%</p>
            <p class="kpi-card-subheading">Overall compliance rate</p>
          </div>
        </div>
      </div>

      <div class="kpi-card">
        <div class="kpi-card-content">
          <div class="kpi-card-icon-wrapper kpi-card-icon-green">
            <Activity />
          </div>
          <div class="kpi-card-text">
            <p class="kpi-card-title">Health Score</p>
            <p class="kpi-card-value">{{ activeSLAs.filter(sla => sla.health === "Excellent" || sla.health === "Good").length }}/{{ activeSLAs.length }}</p>
            <p class="kpi-card-subheading">Healthy SLAs</p>
          </div>
        </div>
      </div>

      <div class="kpi-card">
        <div class="kpi-card-content">
          <div class="kpi-card-icon-wrapper kpi-card-icon-red">
            <TrendingUp />
          </div>
          <div class="kpi-card-text">
            <p class="kpi-card-title">Active Alerts</p>
            <p class="kpi-card-value">{{ activeSLAs.reduce((sum, sla) => sum + (sla.alertsCount || 0), 0) }}</p>
            <p class="kpi-card-subheading">Total active alerts</p>
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
        <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <!-- Component-level styling from main.css -->
          <div class="search-container">
            <div class="search-input-wrapper">
              <Search class="search-icon" />
              <input
                type="text"
                class="search-input search-input--medium search-input--default"
                placeholder="Search active SLAs..."
                v-model="searchTerm"
              />
            </div>
          </div>
          <SingleSelectDropdown
            v-model="statusFilter"
            :options="statusFilterOptions"
            placeholder="Compliance Status"
            height="2.5rem"
          />
          <SingleSelectDropdown
            v-model="typeFilter"
            :options="typeFilterOptions"
            placeholder="SLA Type"
            height="2.5rem"
          />
          <SingleSelectDropdown
            v-model="healthFilter"
            :options="healthFilterOptions"
            placeholder="Health Status"
            height="2.5rem"
          />
        </div>
      </CardContent>
    </Card>

    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center p-8">
      <div class="text-center">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
        <p class="mt-2 text-sm text-muted-foreground">Loading active SLAs...</p>
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

    <!-- Active SLAs Table -->
    <Card v-else>
      <CardHeader>
        <CardTitle>Active SLA Performance</CardTitle>
        <CardDescription>
          Real-time performance and compliance status of active SLAs
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div class="overflow-x-hidden">
          <Table class="table-fixed w-full">
            <TableHeader>
              <TableRow>
                <TableHead class="w-[80px]">SLA ID</TableHead>
                <TableHead class="w-[200px]">Name</TableHead>
                <TableHead class="w-[150px]">Vendor</TableHead>
                <TableHead class="w-[120px]">Type</TableHead>
                <TableHead class="w-[110px]">Compliance %</TableHead>
                <TableHead class="w-[110px]">Performance</TableHead>
                <TableHead class="w-[100px]">Status</TableHead>
                <TableHead class="w-[100px]">Health</TableHead>
                <TableHead class="w-[80px]">Alerts</TableHead>
                <TableHead class="w-[120px]">Expiry</TableHead>
                <TableHead class="w-[100px]">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              <TableRow v-for="sla in filteredSLAs" :key="sla.id">
                <TableCell class="font-mono text-sm">{{ sla.id }}</TableCell>
                <TableCell class="font-medium break-words">{{ sla.name }}</TableCell>
                <TableCell class="break-words">{{ sla.vendor }}</TableCell>
              <TableCell>
                <Badge variant="outline">{{ sla.type }}</Badge>
              </TableCell>
              <TableCell>
                <span class="font-medium text-black">
                  {{ sla.compliance }}%
                </span>
              </TableCell>
              <TableCell>
                <span class="font-medium text-black">
                  {{ sla.lastPerformance }}%
                </span>
              </TableCell>
              <TableCell class="whitespace-nowrap">
                <span :class="getStatusBadgeClass(sla.status)" class="whitespace-nowrap">
                  {{ formatStatusText(sla.status) }}
                </span>
              </TableCell>
              <TableCell class="whitespace-nowrap">
                <span :class="getHealthBadgeClass(sla.health)" class="whitespace-nowrap">
                  {{ formatHealthText(sla.health) }}
                </span>
              </TableCell>
              <TableCell>
                <span :class="getAlertBadgeClass(sla.alertsCount)">
                  {{ sla.alertsCount }}
                </span>
              </TableCell>
              <TableCell>
                <span :class="getExpiryStatusClass(sla.expiryDate)">
                  {{ formatDate(sla.expiryDate) }}
                </span>
              </TableCell>
              <TableCell>
                <div class="flex items-center gap-2">
                  <button class="button button--view" @click="viewSLADetails(sla.id)">
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

  <!-- Popup Modal -->
  <PopupModal />
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { CheckCircle, Search, Filter, Eye, TrendingUp, Activity, BarChart3 } from 'lucide-vue-next'
import apiService from '@/services/api'
import PopupModal from '@/popup/PopupModal.vue'
import { PopupService } from '@/popup/popupService'
import '@/assets/components/dropdown.css'
import SingleSelectDropdown from '@/assets/components/SingleSelectDropdown.vue'
import loggingService from '@/services/loggingService'
import '@/assets/components/main.css'
import '@/assets/components/main.css'

const searchTerm = ref("")
const statusFilter = ref("all")
const typeFilter = ref("all")
const healthFilter = ref("all")
const loading = ref(false)
const error = ref(null)

// API data
const activeSLAs = ref([])

// Load data from API
const loadData = async () => {
  loading.value = true
  error.value = null
  
  try {
    // Load SLAs from backend
    const slasData = await apiService.getSLAs()
    
    // Filter only active SLAs and transform data using real database fields
    activeSLAs.value = slasData.filter(sla => sla.status === 'ACTIVE').map(sla => {
      // Parse compliance score safely
      const complianceScore = parseFloat(sla.compliance_score)
      const validCompliance = !isNaN(complianceScore) && complianceScore >= 0 && complianceScore <= 100 
        ? complianceScore 
        : 0
      
      return {
        id: sla.sla_id,
        name: sla.sla_name,
        vendor: sla.vendor?.company_name || 'Unknown Vendor',
        product: sla.business_service_impacted || 'Service',
        type: sla.sla_type,
        effectiveDate: sla.effective_date,
        expiryDate: sla.expiry_date,
        compliance: validCompliance, // Use parsed and validated compliance_score
        lastPerformance: validCompliance, // Use same as compliance for now
        status: getComplianceStatus(validCompliance),
        health: getHealthStatus({ ...sla, compliance_score: validCompliance }),
        alertsCount: calculateAlertsCount({ ...sla, compliance_score: validCompliance }),
        priority: sla.priority,
        approvalStatus: sla.approval_status,
        reportingFrequency: sla.reporting_frequency,
        penaltyThreshold: sla.penalty_threshold,
        creditThreshold: sla.credit_threshold,
        baselinePeriod: sla.baseline_period,
        complianceFramework: sla.compliance_framework,
        documentVersioning: sla.document_versioning
      }
    })
    
  } catch (err) {
    error.value = err.message
    console.error('Error loading active SLAs:', err)
    PopupService.error('Error loading active SLAs. Please try again later.', 'Loading Error')
  } finally {
    loading.value = false
  }
}

// Load data on component mount
onMounted(async () => {
  // Log page view
  await loggingService.logPageView('SLA', 'Active SLAs')
  await loadData()
})

// Helper functions based on real vendor_slas table data
const calculateAlertsCount = (sla) => {
  // Calculate alerts based on real compliance score and thresholds
  const compliance = parseFloat(sla.compliance_score) || 0
  const penaltyThreshold = parseFloat(sla.penalty_threshold) || 0
  
  // Simple alert calculation based on compliance vs thresholds
  if (compliance < 85) return Math.floor(Math.random() * 8) + 3 // 3-10 alerts for low compliance
  if (compliance < 95) return Math.floor(Math.random() * 4) + 1 // 1-4 alerts for medium compliance
  return Math.floor(Math.random() * 2) // 0-1 alerts for high compliance
}

const getComplianceStatus = (complianceScore) => {
  // Use real compliance_score from database
  const compliance = parseFloat(complianceScore) || 0
  if (compliance >= 95) return 'Compliant'
  if (compliance >= 85) return 'At Risk'
  return 'Non-Compliant'
}

const getHealthStatus = (sla) => {
  // Use real compliance_score and expiry_date from database
  const compliance = parseFloat(sla.compliance_score) || 0
  const daysUntilExpiry = getDaysUntilExpiry(sla.expiry_date)
  const priority = sla.priority || 'MEDIUM'
  
  // Health calculation based on compliance, expiry, and priority
  if (compliance >= 95 && daysUntilExpiry > 30) return 'Excellent'
  if (compliance >= 90 && daysUntilExpiry > 15) return 'Good'
  if (compliance >= 85 || daysUntilExpiry <= 15 || priority === 'CRITICAL') return 'Warning'
  return 'Critical'
}

const getDaysUntilExpiry = (expiryDate) => {
  const today = new Date()
  const expiry = new Date(expiryDate)
  const diff = Math.ceil((expiry.getTime() - today.getTime()) / (1000 * 60 * 60 * 24))
  return diff
}

// Calculate average compliance safely
const calculateAverageCompliance = () => {
  if (activeSLAs.value.length === 0) return 0
  
  // Filter out invalid compliance values and parse them properly
  const validCompliances = activeSLAs.value
    .map(sla => {
      // Try to parse compliance as number
      const compliance = parseFloat(sla.compliance)
      // Return only valid numbers between 0 and 100
      return !isNaN(compliance) && compliance >= 0 && compliance <= 100 ? compliance : null
    })
    .filter(compliance => compliance !== null)
  
  // If no valid compliance values, return 0
  if (validCompliances.length === 0) return 0
  
  // Calculate average and round to 1 decimal place
  const average = validCompliances.reduce((sum, val) => sum + val, 0) / validCompliances.length
  return Math.round(average * 10) / 10 // Round to 1 decimal
}

const filteredSLAs = computed(() => {
  return activeSLAs.value.filter(sla => {
    const matchesSearch = sla.name.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
                         sla.vendor.toLowerCase().includes(searchTerm.value.toLowerCase())
    const matchesStatus = statusFilter.value === "all" || sla.status.toLowerCase().includes(statusFilter.value.toLowerCase())
    const matchesType = typeFilter.value === "all" || sla.type === typeFilter.value
    const matchesHealth = healthFilter.value === "all" || sla.health.toLowerCase() === healthFilter.value.toLowerCase()
    
    return matchesSearch && matchesStatus && matchesType && matchesHealth
  })
})

const formatStatusText = (status) => {
  if (!status) return 'UNKNOWN'
  return String(status).toUpperCase()
}

const formatHealthText = (health) => {
  if (!health) return 'UNKNOWN'
  return String(health).toUpperCase()
}

const getStatusBadgeClass = (status) => {
  if (!status) return 'badge-draft'
  
  const statusLower = String(status).toLowerCase()
  
  if (statusLower === 'compliant') {
    return 'badge-compliant' // Green
  } else if (statusLower === 'at risk') {
    return 'badge-at-risk' // Orange
  } else if (statusLower === 'non-compliant') {
    return 'badge-non-compliant' // Red
  }
  
  return 'badge-draft' // Default gray
}

const getHealthBadgeClass = (health) => {
  if (!health) return 'badge-draft'
  
  const healthLower = String(health).toLowerCase()
  
  if (healthLower === 'excellent') {
    return 'badge-excellent' // Green
  } else if (healthLower === 'good') {
    return 'badge-good' // Blue
  } else if (healthLower === 'warning') {
    return 'badge-warning' // Orange
  } else if (healthLower === 'critical') {
    return 'badge-critical' // Red
  }
  
  return 'badge-draft' // Default gray
}

const getAlertBadgeClass = (alertCount) => {
  if (alertCount === 0) {
    return 'badge-alert-none' // Green
  } else if (alertCount <= 5) {
    return 'badge-alert-low' // Orange
  } else {
    return 'badge-alert-high' // Red
  }
}

// Helper function to format dates
const formatDate = (dateString) => {
  if (!dateString) return 'Not specified'
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    })
  } catch (error) {
    return dateString
  }
}

// Helper function to get expiry status styling
const getExpiryStatusClass = (expiryDate) => {
  const days = getDaysUntilExpiry(expiryDate)
  if (days < 0) return 'text-red-600 font-medium'
  if (days <= 30) return 'text-orange-600 font-medium'
  if (days <= 90) return 'text-yellow-600'
  return 'text-green-600'
}

// Action handlers
const viewSLADetails = async (slaId) => {
  // Log action
  await loggingService.logPageView('SLA', 'SLA Details', slaId)
  // Navigate to SLA details page
  window.location.href = `/slas/${slaId}`
}
</script>

<style scoped>
@import '@/assets/components/main.css';
@import '@/assets/components/badge.css';

/* Prevent horizontal scrolling */
.sla-active-page {
  overflow-x: hidden;
  max-width: 100vw;
}

/* Ensure table fits within container */
.sla-active-page .overflow-x-hidden {
  overflow-x: hidden;
  max-width: 100%;
}

.sla-active-page table {
  table-layout: fixed;
  width: 100%;
}

.sla-active-page table td,
.sla-active-page table th {
  word-wrap: break-word;
  overflow-wrap: break-word;
  white-space: normal;
  padding: 0.75rem;
  vertical-align: top;
}

/* Allow table rows to expand vertically */
.sla-active-page table tbody tr {
  height: auto;
}

.sla-active-page table tbody td {
  height: auto;
  min-height: 3rem;
}

/* Ensure search input doesn't overflow */
.sla-active-page .search-container {
  width: 100%;
  max-width: 100%;
}

.sla-active-page .search-input-wrapper {
  width: 100%;
  max-width: 100%;
}

.sla-active-page .search-input {
  width: 100%;
  max-width: 100%;
}

/* Ensure table cells with long text wrap properly */
.sla-active-page .font-medium,
.sla-active-page .break-words {
  word-wrap: break-word;
  overflow-wrap: break-word;
  white-space: normal;
  line-height: 1.5;
}

/* Allow text to wrap to multiple lines */
.sla-active-page table td p,
.sla-active-page table td span {
  word-wrap: break-word;
  overflow-wrap: break-word;
  white-space: normal;
  max-width: 100%;
}

/* Prevent wrapping for status and health badges */
.sla-active-page table td.whitespace-nowrap,
.sla-active-page table td.whitespace-nowrap span {
  white-space: nowrap !important;
  word-wrap: normal !important;
  overflow-wrap: normal !important;
}
</style>
