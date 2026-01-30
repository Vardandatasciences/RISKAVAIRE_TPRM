<template>
  <div class="lifecycle-tracker-container" style="min-height: 100vh; background: #ffffff; padding: 1.5rem;">
    <!-- Header -->
    <div class="flex items-center justify-between" style="margin-bottom: 1.5rem;">
      <div>
        <h1 class="text-2xl font-bold text-gray-900" style="font-size: 1.875rem; font-weight: 600; margin: 0; color: #111827;">Vendor Lifecycle Tracker</h1>
        <p class="text-gray-600 mt-1" style="color: #6b7280; margin: 0.25rem 0 0 0; font-size: 0.875rem;">Track vendor progress through onboarding stages with detailed lifecycle tracking</p>
      </div>
    </div>

    <!-- Vendor Selection Section -->
    <div class="vendor-selection-section" style="width: 100%; margin-bottom: 1.5rem;">
      <div class="bg-white p-4 rounded-lg border border-gray-200" style="background: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px; padding: 1rem;">
        <div class="flex items-center justify-between" style="display: flex; align-items: center; justify-content: space-between;">
          <div class="flex items-center space-x-4" style="display: flex; align-items: center; gap: 1rem;">
            <div class="flex items-center space-x-2" style="display: flex; align-items: center; gap: 0.5rem;">
              <label class="text-sm font-medium text-gray-700" style="font-weight: 500; color: #111827; font-size: 0.875rem;">Vendor:</label>
              <SingleSelectDropdown
                v-model="selectedVendorId"
                :options="vendorOptions"
                placeholder="Select a vendor..."
                :disabled="loading"
                width="300px"
                height="2.5rem"
                @update:model-value="onVendorSelect"
              />
            </div>
          </div>
          <div class="flex items-center space-x-3" style="display: flex; align-items: center; gap: 0.75rem;">
            <button @click="refreshData" class="button button--refresh" :disabled="loading">
              <RefreshCw class="h-4 w-4" :class="{ 'animate-spin': loading }" />
              {{ loading ? 'Loading...' : 'Refresh' }}
            </button>
            <button 
              @click="exportTimeline" 
              :disabled="loading || !selectedVendor"
              class="button button--export"
            >
              {{ loading ? 'Loading...' : 'Export' }}
            </button>
          </div>
        </div>
        <div class="vendor-summary" v-if="selectedVendor" style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #e5e7eb;">
          <div class="summary-item">
            <span class="summary-label">STATUS:</span>
            <span class="summary-badge" :class="getStatusBadgeClass(selectedVendor.status)">
              {{ getStatusDisplay(selectedVendor.status) }}
            </span>
          </div>
          <div class="summary-item">
            <span class="summary-label">RISK LEVEL:</span>
            <span class="summary-badge" :class="getRiskLevelBadgeClass(selectedVendor.risk_level)">
              {{ selectedVendor.risk_level || 'N/A' }}
            </span>
          </div>
          <div class="summary-item">
            <span class="summary-label">PROGRESS:</span>
            <span class="summary-value">
              {{ selectedVendor.completed_stages || 0 }}/{{ selectedVendor.total_stages || 0 }} stages ({{ selectedVendor.progress_percentage || 0 }}%)
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Error Message -->
    <div v-if="error" class="error-message">
      <div class="card">
        <div class="card-content">
          <div class="error-content">
            <svg class="error-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            <div>
              <h4>Error Loading Data</h4>
              <p>{{ error }}</p>
              <button @click="loadInitialData" class="btn btn-outline">Retry</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading && !error" class="loading-state">
      <div class="card">
        <div class="card-content">
          <div class="loading-content">
            <div class="spinner"></div>
            <p>{{ selectedVendorId ? 'Loading vendor lifecycle data...' : 'Loading vendors list...' }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content: Vendor Lifecycle Timeline -->
    <div v-if="selectedVendor && vendorTimeline.length > 0" class="vendor-timeline-section">
      <div class="card">
        <div class="card-header">
          <div class="timeline-header">
            <div class="timeline-title">
              <h3 class="card-title">{{ selectedVendor.company_name }} - Lifecycle Timeline</h3>
              <p class="card-subtitle">Stage-wise progression through vendor onboarding process</p>
            </div>
            <div class="timeline-progress">
              <div class="progress-summary">              
                <div class="progress-bar-wrapper">
                  <div class="progress-bar-full">
                    <div 
                      class="progress-bar-fill" 
                      :style="{ width: (selectedVendor.progress_percentage || 0) + '%' }"
                      :class="getProgressBarClass(selectedVendor.progress_percentage || 0)"
                    ></div>
                  </div>
                  <span class="progress-percentage">{{ selectedVendor.progress_percentage || 0 }}%</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="card-content">
          <div class="timeline-container">
            <div v-for="(stage, index) in vendorTimeline" :key="stage.tracker_id || index" class="timeline-item" :class="{ 'timeline-item--current': stage.status === 'in_progress', 'timeline-item--completed': stage.status === 'completed' }">
              <!-- Timeline Dot -->
              <div class="timeline-dot" :class="getTimelineDotClass(stage.status)">
                <div class="timeline-dot-inner">
                  <svg v-if="stage.status === 'completed'" class="timeline-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"/>
                  </svg>
                  <svg v-else-if="stage.status === 'in_progress'" class="timeline-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                  <div v-else class="timeline-step-number">{{ stage.stage_order || index + 1 }}</div>
                </div>
              </div>
              
              <!-- Timeline Content -->
              <div class="timeline-content">
                <div class="timeline-header">
                  <h4 class="timeline-title">{{ stage.stage_name }}</h4>
                  <div class="timeline-meta">
                    <span class="timeline-status" :class="getStatusClass(stage.status)">
                      {{ formatStatusText(stage.status) }}
                    </span>
                    <span class="timeline-code">{{ stage.stage_code }}</span>
                  </div>
                </div>
                
                <p class="timeline-description" v-if="stage.stage_description">
                  {{ stage.stage_description }}
                </p>
                
                <div class="timeline-details">
                  <div class="timeline-dates">
                    <div class="date-item" v-if="stage.started_at">
                      <svg class="date-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                      </svg>
                      <span class="date-label">STARTED</span>
                      <span class="date-value">{{ formatDate(stage.started_at) }}</span>
                    </div>
                    
                    <div class="date-item" v-if="stage.ended_at">
                      <svg class="date-icon date-icon-completed" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                      </svg>
                      <span class="date-label">COMPLETED</span>
                      <span class="date-value">{{ formatDate(stage.ended_at) }}</span>
                    </div>
                    
                    <div class="date-item" v-if="stage.started_at && stage.ended_at">
                      <svg class="date-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                      </svg>
                      <span class="date-label">DURATION</span>
                      <span class="date-value">{{ stage.duration?.display || formatDuration(stage.started_at, stage.ended_at) }}</span>
                    </div>
                  </div>
                  
                  <div class="timeline-flags" v-if="stage.approval_required || stage.max_duration_days">
                    <button class="flag flag-approval" v-if="stage.approval_required">
                      Approval Required
                    </button>
                    <button class="flag flag-max-days" v-if="stage.max_duration_days">
                      Max: {{ stage.max_duration_days }} days
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- No Vendor Selected State -->
    <div v-if="!selectedVendorId && !loading" class="no-selection-state">
      <div class="card">
        <div class="card-content">
          <div class="no-selection-content">
            <svg class="selection-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
            </svg>
            <h3>Select a Vendor</h3>
            <p>Choose a vendor from the dropdown above to view their detailed lifecycle tracking and stage progression.</p>
            <div class="selection-stats" v-if="vendorsList.length > 0">
              <div class="stat-item">
                <span class="stat-number">{{ vendorsList.length }}</span>
                <span class="stat-label">Total Vendors</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- No Timeline Data State -->
    <div v-if="selectedVendorId && vendorTimeline.length === 0 && !loading" class="no-timeline-state">
      <div class="card">
        <div class="card-content">
          <div class="no-timeline-content">
            <svg class="timeline-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"/>
            </svg>
            <h3>No Lifecycle Data Available</h3>
            <p>No lifecycle tracking data found for {{ selectedVendor?.company_name || 'this vendor' }}. Lifecycle tracking may not have been initialized yet.</p>
            <button @click="refreshData" class="button button--refresh">
              <RefreshCw class="h-4 w-4" />
              Refresh Data
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Analytics Section -->
    <div v-if="selectedVendor && vendorTimeline.length > 0" class="analytics-section">
      <div class="card">
        <div class="card-header">
          <h3 class="card-title" style="border-bottom: none !important; text-decoration: none !important;">Lifecycle Stage Analytics</h3>
        </div>
        <div class="card-content">
          <div class="kpi-cards-grid">
            <div class="kpi-card">
              <div class="kpi-card-content">
                <div class="kpi-card-icon-wrapper kpi-card-icon-green">
                  <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                </div>
                <div class="kpi-card-text">
                  <p class="kpi-card-title">COMPLETED</p>
                  <p class="kpi-card-value">{{ getCompletedStagesCount() }}</p>
                  <p class="kpi-card-subheading">Stages completed</p>
                </div>
              </div>
            </div>
            <div class="kpi-card">
              <div class="kpi-card-content">
                <div class="kpi-card-icon-wrapper kpi-card-icon-blue">
                  <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                </div>
                <div class="kpi-card-text">
                  <p class="kpi-card-title">IN PROGRESS</p>
                  <p class="kpi-card-value">{{ getInProgressStagesCount() }}</p>
                  <p class="kpi-card-subheading">Stages in progress</p>
                </div>
              </div>
            </div>
            <div class="kpi-card">
              <div class="kpi-card-content">
                <div class="kpi-card-icon-wrapper kpi-card-icon-gray">
                  <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                </div>
                <div class="kpi-card-text">
                  <p class="kpi-card-title">PENDING</p>
                  <p class="kpi-card-value">{{ getPendingStagesCount() }}</p>
                  <p class="kpi-card-subheading">Stages pending</p>
                </div>
              </div>
            </div>
            <div class="kpi-card">
              <div class="kpi-card-content">
                <div class="kpi-card-icon-wrapper kpi-card-icon-orange">
                  <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
                  </svg>
                </div>
                <div class="kpi-card-text">
                  <p class="kpi-card-title">OVERALL PROGRESS</p>
                  <p class="kpi-card-value">{{ selectedVendor.progress_percentage || 0 }}%</p>
                  <p class="kpi-card-subheading">Completion rate</p>
                </div>
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
import apiClient from '@/config/axios.js'
import PopupModal from '@/popup/PopupModal.vue'
import { PopupService } from '@/popup/popupService'
import { useNotifications } from '@/composables/useNotifications'
import notificationService from '@/services/notificationService'
import '@/assets/components/main.css'
import '@/assets/components/badge.css'
import { RefreshCw } from 'lucide-vue-next'
// Import dropdown styles
import '@/assets/components/dropdown.css'
// Import custom dropdown component
import SingleSelectDropdown from '@/assets/components/SingleSelectDropdown.vue'
const { showSuccess, showError, showWarning, showInfo } = useNotifications()

// Component state
const loading = ref(false)
const error = ref(null)

// Vendor selection
const selectedVendorId = ref('')
const vendorsList = ref([])

// Vendor options for dropdown
const vendorOptions = computed(() => {
  return [
    { value: '', label: 'Select a vendor...' },
    ...vendorsList.value.map(vendor => ({
      value: vendor.vendor_id,
      label: `${vendor.company_name} (${vendor.vendor_code || 'No Code'})`
    }))
  ]
})

// Vendor data
const selectedVendor = ref(null)
const vendorTimeline = ref([])
const analyticsData = ref(null)

// API configuration
const API_BASE_URL = 'http://localhost:8000/api/v1'

// Get headers with auth token
const getHeaders = () => {
  const token = localStorage.getItem('access_token') || localStorage.getItem('token')
  const headers = {
    'Content-Type': 'application/json'
  }
  
  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }
  
  return headers
}

// Load initial data (vendors list and analytics)
const loadInitialData = async () => {
  loading.value = true
  error.value = null
  
  try {
    // Load vendors list and analytics in parallel
    const [vendorsResponse, analyticsResponse] = await Promise.all([
      apiClient.get(`${API_BASE_URL}/vendor-lifecycle/vendors-list/`),
      apiClient.get(`${API_BASE_URL}/vendor-lifecycle/analytics/`)
    ])
    
    vendorsList.value = vendorsResponse.data.vendors || []
    analyticsData.value = analyticsResponse.data
    
    console.log('Loaded vendors:', vendorsList.value.length)
    console.log('Analytics data:', analyticsData.value)
    
  } catch (err) {
    console.error('Error loading initial data:', err)
    error.value = err.response?.data?.error || 'Failed to load data'
  } finally {
    loading.value = false
  }
}

// Load vendor lifecycle timeline
const loadVendorTimeline = async (vendorId) => {
  if (!vendorId) {
    selectedVendor.value = null
    vendorTimeline.value = []
    return
  }
  
  loading.value = true
  error.value = null
  
  try {
    const response = await apiClient.get(`${API_BASE_URL}/vendor-lifecycle/vendor-timeline/${vendorId}/`)
    
    selectedVendor.value = response.data.vendor
    vendorTimeline.value = response.data.timeline || []
    
    console.log('Loaded vendor timeline:', vendorTimeline.value.length, 'stages')
    console.log('Vendor data:', selectedVendor.value)
    
  } catch (err) {
    console.error('Error loading vendor timeline:', err)
    error.value = err.response?.data?.error || 'Failed to load vendor timeline'
    selectedVendor.value = null
    vendorTimeline.value = []
  } finally {
    loading.value = false
  }
}

// Handle vendor selection
const onVendorSelect = async () => {
  await loadVendorTimeline(selectedVendorId.value)
}

// Refresh all data
const refreshData = async () => {
  await loadInitialData()
  if (selectedVendorId.value) {
    await loadVendorTimeline(selectedVendorId.value)
  }
}

// Export timeline data
const exportTimeline = async () => {
  if (!selectedVendor.value || vendorTimeline.value.length === 0) {
    PopupService.warning('No timeline data to export', 'No Data')
    return
  }
  
  try {
    // Create CSV content
    const csvContent = [
      'Stage Name,Stage Code,Status,Started At,Ended At,Duration (Days),Approval Required',
      ...vendorTimeline.value.map(stage => 
        `"${stage.stage_name}","${stage.stage_code}","${stage.status}","${stage.started_at || ''}","${stage.ended_at || ''}","${stage.duration?.days || ''}","${stage.approval_required ? 'Yes' : 'No'}"`
      )
    ].join('\n')
    
    // Download CSV
    const blob = new Blob([csvContent], { type: 'text/csv' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${selectedVendor.value.company_name}-lifecycle-timeline-${new Date().toISOString().split('T')[0]}.csv`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    window.URL.revokeObjectURL(url)
  } catch (err) {
    console.error('Error exporting timeline:', err)
    PopupService.error('Failed to export timeline data', 'Export Failed')
  }
}

// Load data on component mount
onMounted(async () => {
  await loadInitialData()
  
  // Check for vendor ID in query parameters
  const urlParams = new URLSearchParams(window.location.search)
  const vendorId = urlParams.get('vendorId')
  const fromRegistration = urlParams.get('fromRegistration')
  
  if (vendorId) {
    console.log('Vendor ID found in query parameters:', vendorId)
    console.log('From registration:', fromRegistration)
    
    // Set the selected vendor ID
    selectedVendorId.value = vendorId
    
    // Load the vendor timeline
    await loadVendorTimeline(vendorId)
    
    // Log that user came from registration (no notification needed)
    if (fromRegistration === 'true') {
      console.log('User navigated from vendor registration')
    }
  }
})

/* Timeline dot classes */
const getTimelineDotClass = (status) => {
  switch (status) {
    case 'completed': return 'timeline-dot--completed'
    case 'in_progress': return 'timeline-dot--in-progress'
    case 'pending': return 'timeline-dot--pending'
    case 'failed': return 'timeline-dot--failed'
    default: return 'timeline-dot--default'
  }
}

/* Progress bar color classes */
const getProgressBarClass = (percentage) => {
  if (percentage >= 80) return 'progress-bar--high'
  if (percentage >= 50) return 'progress-bar--medium'
  if (percentage >= 20) return 'progress-bar--low'
  return 'progress-bar--minimal'
}

/* Status badge classes - using badge.css */
const getStatusClass = (status) => {
  const normalizedStatus = status?.toLowerCase() || ''
  switch (normalizedStatus) {
    case 'completed':
    case 'approved':
    case 'active':
    case 'cleared':
      return 'badge-approved'
    case 'in_progress':
      return 'badge-in-review'
    case 'pending':
      return 'badge-draft'
    case 'rejected':
    case 'failed':
    default:
      return 'badge-draft'
  }
}

/* Risk level classes */
const getRiskLevelClass = (riskLevel) => {
  switch (riskLevel?.toLowerCase()) {
    case 'low': return 'risk-low'
    case 'medium': return 'risk-medium'
    case 'high': return 'risk-high'
    case 'critical': return 'risk-critical'
    default: return 'risk-unknown'
  }
}

/* Format date for display */
const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  try {
    const date = new Date(dateString)
    const month = date.toLocaleDateString('en-US', { month: 'short' })
    const day = date.getDate()
    const year = date.getFullYear()
    const time = date.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      hour12: true
    })
    return `${month} ${day}, ${year}, ${time}`
  } catch (e) {
    return 'Invalid Date'
  }
}

/* Format duration */
const formatDuration = (startDate, endDate) => {
  if (!startDate || !endDate) return 'N/A'
  try {
    const start = new Date(startDate)
    const end = new Date(endDate)
    const diff = end - start
    const days = Math.floor(diff / (1000 * 60 * 60 * 24))
    const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
    return `${days} days, ${hours} hours`
  } catch (e) {
    return 'N/A'
  }
}

/* Get status display text */
const getStatusDisplay = (status) => {
  switch (status?.toLowerCase()) {
    case 'cleared':
    case 'approved':
    case 'active':
      return 'Cleared'
    case 'in_progress':
      return 'In Progress'
    case 'pending':
      return 'Pending'
    default:
      return status || 'Unknown'
  }
}

/* Format status text for timeline */
const formatStatusText = (status) => {
  const normalizedStatus = status?.toLowerCase() || ''
  switch (normalizedStatus) {
    case 'completed':
    case 'approved':
    case 'active':
    case 'cleared':
      return 'Approved'
    case 'in_progress':
      return 'In Review'
    case 'pending':
      return 'Draft'
    case 'rejected':
      return 'Rejected'
    case 'failed':
      return 'Failed'
    default:
      return status?.replace('_', ' ').toUpperCase() || 'Unknown'
  }
}

/* Get status badge class - using badge.css */
const getStatusBadgeClass = (status) => {
  const normalizedStatus = status?.toLowerCase() || ''
  switch (normalizedStatus) {
    case 'cleared':
    case 'approved':
    case 'active':
    case 'completed':
      return 'badge-approved'
    case 'in_progress':
      return 'badge-in-review'
    case 'pending':
      return 'badge-draft'
    default:
      return 'badge-draft'
  }
}

/* Get risk level badge class */
const getRiskLevelBadgeClass = (riskLevel) => {
  switch (riskLevel?.toLowerCase()) {
    case 'low':
      return 'badge-low-risk'
    case 'medium':
      return 'badge-medium-risk'
    case 'high':
      return 'badge-high-risk'
    case 'critical':
      return 'badge-critical'
    default:
      return ''
  }
}

/* Get analytics counts */
const getCompletedStagesCount = () => {
  return vendorTimeline.value.filter(s => s.status === 'completed').length
}

const getInProgressStagesCount = () => {
  return vendorTimeline.value.filter(s => s.status === 'in_progress').length
}

const getPendingStagesCount = () => {
  return vendorTimeline.value.filter(s => s.status === 'pending').length
}
</script>

<style>
@import './VendorLifecycleTracker.css';

/* Fallback styles in case CSS variables are not defined */
:root {
  --card: #ffffff;
  --border: #e5e7eb;
  --background: #ffffff;
  --foreground: #0f172a;
  --muted-foreground: #64748b;
  --muted: #f8fafc;
  --primary: #bfdbfe;
  --primary-foreground: #1d4ed8;
  --success: #bbf7d0;
  --warning: #fde68a;
  --destructive: #fca5a5;
}

/* Ensure basic visibility */
.lifecycle-tracker-container {
  min-height: 100vh;
  background: var(--background);
}

.card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 1.5rem;
}

.card-header {
  margin-bottom: 1rem;
}

.card-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--foreground);
  margin: 0 0 0.5rem 0;
}

/* Card content styles are handled by the imported CSS file */

.btn {
  display: inline-flex;
  align-items: center;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  text-decoration: none;
  border: 1px solid transparent;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary {
  background: var(--primary);
  color: var(--primary-foreground);
  border-color: var(--primary);
}

.btn-primary:hover:not(:disabled) {
  background: #93c5fd;
  border-color: #93c5fd;
}

.btn-outline {
  background: transparent;
  color: var(--foreground);
  border-color: var(--border);
}

.btn-outline:hover:not(:disabled) {
  background: var(--muted);
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.mr-2 {
  margin-right: 0.5rem;
}

.mr-3 {
  margin-right: 0.75rem;
}

.h-4 {
  height: 1rem;
}

.w-4 {
  width: 1rem;
}
</style>