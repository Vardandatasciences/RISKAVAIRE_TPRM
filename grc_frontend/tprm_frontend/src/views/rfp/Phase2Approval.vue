<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
      <div>
        <h1 class="text-3xl font-bold tracking-tight">RFP Management</h1>
        <p class="text-muted-foreground">
          View and manage RFPs created by users.
        </p>
      </div>
    </div>


    <!-- User Filter Section -->
      <Card class="phase-card">
        <CardHeader>
        <CardTitle>Filter RFPs by Creator</CardTitle>
        <CardDescription>Select a user to view their created RFPs</CardDescription>
        </CardHeader>
        <CardContent>
        <div class="flex items-center gap-4">
          <div class="flex-1">
            <label class="block text-sm font-medium text-gray-700 mb-2">Select Creator:</label>
            <SingleSelectDropdown
              v-model="selectedUserId"
              :options="userOptions"
              placeholder="All Users"
              width="18rem"
              height="2.3rem"
              @update:model-value="onUserChange"
            />
          </div>
            <div class="flex items-center gap-2">
            <button 
              @click="fetchRFPs" 
              :disabled="loading"
              type="button"
              class="button button--refresh"
            >
              <RefreshCw class="h-4 w-4" :class="{ 'animate-spin': loading }" />
              {{ loading ? 'Loading...' : 'Refresh' }}
            </button>
            </div>
            </div>
        <div v-if="selectedUserId" class="mt-3 p-3 bg-primary/5 rounded-lg">
          <span class="text-sm text-primary font-medium">
            Showing RFPs created by: <strong>{{ getSelectedUserName() }}</strong>
            <span class="text-muted-foreground ml-2">({{ filteredRFPs.length }} RFPs)</span>
          </span>
          </div>
        </CardContent>
      </Card>

    <!-- RFP Table -->
      <Card class="phase-card">
        <CardHeader>
        <CardTitle>RFPs</CardTitle>
        <CardDescription>List of all RFPs</CardDescription>
        </CardHeader>
        <CardContent>
        <!-- Loading State -->
        <div v-if="loading" class="text-center py-12">
          <RefreshCw class="h-8 w-8 text-primary animate-spin mx-auto mb-4" />
          <p class="text-muted-foreground">Loading RFPs...</p>
                </div>

        <!-- Empty State -->
        <div v-else-if="filteredRFPs.length === 0" class="text-center py-12">
          <FileText class="h-12 w-12 text-muted-foreground mx-auto mb-4" />
          <h3 class="text-lg font-medium text-gray-900 mb-2">No RFPs Found</h3>
          <p class="text-muted-foreground">
            {{ selectedUserId ? 'This user has not created any RFPs yet.' : 'No RFPs available. Please select a user to view their RFPs.' }}
          </p>
                  </div>

        <!-- RFP Table -->
        <div v-else class="overflow-x-hidden">
          <table class="w-full border-collapse table-fixed">
            <thead>
              <tr class="border-b border-gray-200">
                <th class="text-left py-3 px-4 font-medium text-gray-900 w-32">RFP Number</th>
                <th class="text-left py-3 px-4 font-medium text-gray-900 w-1/4">Title</th>
                <th class="text-left py-3 px-4 font-medium text-gray-900 w-32">Type</th>
                <th class="text-left py-3 px-4 font-medium text-gray-900 w-28">Budget</th>
                <th class="text-left py-3 px-4 font-medium text-gray-900 w-24">Status</th>
                <th class="text-left py-3 px-4 font-medium text-gray-900 w-28">Created</th>
                <th class="text-left py-3 px-4 font-medium text-gray-900 w-28">Deadline</th>
                <th class="text-left py-3 px-4 font-medium text-gray-900 w-24">Creator</th>
                <th class="text-left py-3 px-4 font-medium text-gray-900 w-32">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr 
                v-for="rfp in filteredRFPs" 
                :key="rfp.rfp_id"
                class="border-b border-gray-100 hover:bg-gray-50 transition-colors"
              >
                <td class="py-3 px-4">
                  <span class="font-mono text-sm text-gray-600 break-words">{{ rfp.rfp_number }}</span>
                </td>
                <td class="py-3 px-4">
                    <div class="min-w-0">
                    <div class="font-medium text-gray-900 break-words">{{ rfp.rfp_title }}</div>
                    <div class="text-sm text-gray-500 mt-1 line-clamp-2 break-words">
                      {{ rfp.description }}
                    </div>
                  </div>
                </td>
                <td class="py-3 px-4">
                  <div class="break-words min-w-0">
                    <Badge v-if="rfp.rfp_type" variant="outline" class="text-xs inline-block max-w-full break-words">{{ rfp.rfp_type }}</Badge>
                  <span v-else class="text-sm text-gray-400">N/A</span>
                  </div>
                </td>
                <td class="py-3 px-4">
                  <span class="font-medium text-sm whitespace-nowrap">{{ formatCurrency(rfp.estimated_value) }}</span>
                </td>
                <td class="py-3 px-4">
                  <component :is="getStatusBadgeComponent(rfp.status)" />
                </td>
                <td class="py-3 px-4">
                  <span class="text-sm text-gray-600 whitespace-nowrap">{{ formatDate(rfp.created_at) }}</span>
                </td>
                <td class="py-3 px-4">
                  <span class="text-sm text-gray-600 whitespace-nowrap">{{ formatDate(rfp.submission_deadline) }}</span>
                </td>
                <td class="py-3 px-4">
                  <span class="text-sm text-gray-600 break-words">{{ getCreatorName(rfp.created_by) }}</span>
                </td>
                <td class="py-3 px-4">
                  <div class="flex items-center gap-2">
                    <Button 
                      v-if="rfp.status === 'APPROVED'"
                      @click="proceedToVendorSelection(rfp)"
                      size="sm"
                      class="px-3 py-1.5 text-xs font-medium bg-blue-600 hover:bg-blue-700 text-white rounded-md transition-colors whitespace-nowrap"
                    >
                      Vendor Selection
                    </Button>
                    <span v-else class="text-xs text-gray-400 break-words">
                      {{ getActionText(rfp.status) }}
                    </span>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
          </div>
        </CardContent>
      </Card>
    </div>
</template>

<script setup lang="ts">
import { ref, h, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useNotifications } from '@/composables/useNotifications'
import loggingService from '@/services/loggingService'
import { 
  FileText, 
  RefreshCw
} from 'lucide-vue-next'
import { rfpUseToast } from '@/composables/rfpUseToast.js'
import { API_CONFIG, API_ENDPOINTS, buildApiUrl, apiCall } from '@/config/api.js'
import Card from '@/components_rfp/ui/Card.vue'
import CardContent from '@/components_rfp/ui/CardContent.vue'
// Import dropdown styles
import '@/assets/components/dropdown.css'
// Import custom dropdown component
import SingleSelectDropdown from '@/assets/components/SingleSelectDropdown.vue'
import CardDescription from '@/components_rfp/ui/CardDescription.vue'
import CardHeader from '@/components_rfp/ui/CardHeader.vue'
import CardTitle from '@/components_rfp/ui/CardTitle.vue'
import Button from '@/components_rfp/ui/Button.vue'
import Badge from '@/components_rfp/ui/Badge.vue'
import '@/assets/components/badge.css'
import '@/assets/components/rfp_darktheme.css' // Import RFP dark theme styles
import '@/assets/components/main.css' // Import global refresh button styles

const { success, error } = rfpUseToast()
const router = useRouter()

// Reactive data for RFP management
const { showSuccess, showError, showWarning, showInfo } = useNotifications()

const rfps = ref([])
const users = ref([])
const selectedUserId = ref('')
const loading = ref(false)

// User options for dropdown
const userOptions = computed(() => {
  return [
    { value: '', label: 'All Users' },
    ...users.value.map(user => ({
      value: user.id,
      label: `${user.first_name} ${user.last_name} (${user.username})`
    }))
  ]
})

// Computed properties
const filteredRFPs = computed(() => {
  if (!selectedUserId.value) {
    return rfps.value
  }
  return rfps.value.filter(rfp => rfp.created_by === parseInt(selectedUserId.value))
})

// Methods for RFP management
const fetchUsers = async () => {
  try {
    const url = buildApiUrl(API_ENDPOINTS.RFP_APPROVAL.USERS)
    const data = await apiCall(url)
    users.value = data
  } catch (err) {
    console.error('Error fetching users:', err)
    error('Error', 'Failed to fetch users from database')
    users.value = []
  }
}

const fetchRFPs = async () => {
  loading.value = true
  try {
    // Use the correct API endpoint for RFPs
    const url = `${API_CONFIG.BASE_URL}/v1/rfps/`
    const data = await apiCall(url)
    rfps.value = data.results || data // Handle pagination if present
  } catch (err) {
    console.error('Error fetching RFPs:', err)
    error('Error', 'Failed to fetch RFPs from database')
    rfps.value = []
  } finally {
    loading.value = false
  }
}

const onUserChange = () => {
  // Filtering is handled by computed property
}

const getSelectedUserName = () => {
  const user = users.value.find(u => u.id === parseInt(selectedUserId.value))
  return user ? `${user.first_name} ${user.last_name}` : 'Unknown User'
}

const getCreatorName = (userId: number) => {
  const user = users.value.find(u => u.id === userId)
  return user ? `${user.first_name} ${user.last_name}` : `User ${userId}`
}

const formatCurrency = (amount: number) => {
  if (!amount) return 'N/A'
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(amount)
}

const formatDate = (dateString: string) => {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

// Get badge class for status
const getStatusBadgeClass = (status: string) => {
  const normalizedStatus = status?.toUpperCase() || ''
  switch (normalizedStatus) {
    case 'DRAFT': return 'badge-draft'
    case 'IN_REVIEW':
    case 'EVALUATION': return 'badge-in-review'
    case 'APPROVED':
    case 'AWARDED': return 'badge-approved'
    default: return 'badge-draft'
  }
}

// Format status text for display
const formatStatusText = (status: string) => {
  const normalizedStatus = status?.toUpperCase() || ''
  switch (normalizedStatus) {
    case 'DRAFT': return 'Draft'
    case 'IN_REVIEW': return 'In Review'
    case 'APPROVED': return 'Approved'
    case 'PUBLISHED': return 'Published'
    case 'SUBMISSION_OPEN': return 'Submission Open'
    case 'EVALUATION': return 'In Review'
    case 'AWARDED': return 'Approved'
    case 'CANCELLED': return 'Cancelled'
    case 'ARCHIVED': return 'Archived'
    default: return status || 'Draft'
  }
}

const getStatusBadgeComponent = (status: string) => {
  // Use badge.css classes for draft, in review, and approved
  const badgeClass = getStatusBadgeClass(status)
  const statusText = formatStatusText(status)
  
  // Return a span element with the badge class for plain text styling
  return h('span', { class: badgeClass }, statusText)
}

const proceedToVendorSelection = (rfp: any) => {
  // Store the selected RFP data for the vendor selection page
  localStorage.setItem('selectedRFP', JSON.stringify(rfp))
  
    // Navigate to Phase 3 Vendor Selection
    window.location.href = '/rfp-vendor-selection'
  
  success('Proceeding to Vendor Selection', `RFP ${rfp.rfp_number} is ready for vendor selection.`)
}

const getActionText = (status: string) => {
  const actionTexts = {
    'DRAFT': 'Awaiting submission',
    'IN_REVIEW': 'Under review',
    'PUBLISHED': 'Published',
    'SUBMISSION_OPEN': 'Accepting submissions',
    'EVALUATION': 'Under evaluation',
    'AWARDED': 'Awarded',
    'CANCELLED': 'Cancelled',
    'ARCHIVED': 'Archived'
  }
  return actionTexts[status] || 'No action available'
}

// Initialize data on component mount
onMounted(async () => {
  await loggingService.logPageView('RFP', 'Phase 2 - RFP Approval')
  await fetchUsers()
  fetchRFPs()
})
</script>

<style scoped>
.phase-card {
  @apply bg-white border border-border rounded-lg shadow-sm;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>

<style>
/* Global styles for Phase2Approval.vue to preserve colors in color blindness modes */

/* Preserve primary colors */
html:not(.dark-theme)[data-colorblind="protanopia"] .bg-primary\/5,
html:not(.dark-theme)[data-colorblind="deuteranopia"] .bg-primary\/5,
html:not(.dark-theme)[data-colorblind="tritanopia"] .bg-primary\/5 {
  background-color: rgba(59, 130, 246, 0.05) !important;
}

html:not(.dark-theme)[data-colorblind="protanopia"] .text-primary,
html:not(.dark-theme)[data-colorblind="deuteranopia"] .text-primary,
html:not(.dark-theme)[data-colorblind="tritanopia"] .text-primary {
  color: #3b82f6 !important;
}

/* Preserve blue button colors */
html:not(.dark-theme)[data-colorblind="protanopia"] .bg-blue-600,
html:not(.dark-theme)[data-colorblind="deuteranopia"] .bg-blue-600,
html:not(.dark-theme)[data-colorblind="tritanopia"] .bg-blue-600 {
  background-color: #2563eb !important;
}

html:not(.dark-theme)[data-colorblind="protanopia"] .hover\:bg-blue-700:hover,
html:not(.dark-theme)[data-colorblind="deuteranopia"] .hover\:bg-blue-700:hover,
html:not(.dark-theme)[data-colorblind="tritanopia"] .hover\:bg-blue-700:hover {
  background-color: #1d4ed8 !important;
}

html:not(.dark-theme)[data-colorblind="protanopia"] .text-white,
html:not(.dark-theme)[data-colorblind="deuteranopia"] .text-white,
html:not(.dark-theme)[data-colorblind="tritanopia"] .text-white {
  color: #ffffff !important;
}

/* Preserve gray colors */
html:not(.dark-theme)[data-colorblind="protanopia"] .text-gray-700,
html:not(.dark-theme)[data-colorblind="deuteranopia"] .text-gray-700,
html:not(.dark-theme)[data-colorblind="tritanopia"] .text-gray-700 {
  color: #374151 !important;
}

html:not(.dark-theme)[data-colorblind="protanopia"] .text-gray-900,
html:not(.dark-theme)[data-colorblind="deuteranopia"] .text-gray-900,
html:not(.dark-theme)[data-colorblind="tritanopia"] .text-gray-900 {
  color: #111827 !important;
}

html:not(.dark-theme)[data-colorblind="protanopia"] .text-gray-600,
html:not(.dark-theme)[data-colorblind="deuteranopia"] .text-gray-600,
html:not(.dark-theme)[data-colorblind="tritanopia"] .text-gray-600 {
  color: #4b5563 !important;
}

html:not(.dark-theme)[data-colorblind="protanopia"] .text-gray-500,
html:not(.dark-theme)[data-colorblind="deuteranopia"] .text-gray-500,
html:not(.dark-theme)[data-colorblind="tritanopia"] .text-gray-500 {
  color: #6b7280 !important;
}

html:not(.dark-theme)[data-colorblind="protanopia"] .text-gray-400,
html:not(.dark-theme)[data-colorblind="deuteranopia"] .text-gray-400,
html:not(.dark-theme)[data-colorblind="tritanopia"] .text-gray-400 {
  color: #9ca3af !important;
}

html:not(.dark-theme)[data-colorblind="protanopia"] .border-gray-200,
html:not(.dark-theme)[data-colorblind="deuteranopia"] .border-gray-200,
html:not(.dark-theme)[data-colorblind="tritanopia"] .border-gray-200 {
  border-color: #e5e7eb !important;
}

html:not(.dark-theme)[data-colorblind="protanopia"] .border-gray-100,
html:not(.dark-theme)[data-colorblind="deuteranopia"] .border-gray-100,
html:not(.dark-theme)[data-colorblind="tritanopia"] .border-gray-100 {
  border-color: #f3f4f6 !important;
}

/* Preserve background colors */
html:not(.dark-theme)[data-colorblind="protanopia"] .bg-white,
html:not(.dark-theme)[data-colorblind="deuteranopia"] .bg-white,
html:not(.dark-theme)[data-colorblind="tritanopia"] .bg-white {
  background-color: #ffffff !important;
}

html:not(.dark-theme)[data-colorblind="protanopia"] .hover\:bg-gray-50:hover,
html:not(.dark-theme)[data-colorblind="deuteranopia"] .hover\:bg-gray-50:hover,
html:not(.dark-theme)[data-colorblind="tritanopia"] .hover\:bg-gray-50:hover {
  background-color: #f9fafb !important;
}

/* Preserve muted foreground colors */
html:not(.dark-theme)[data-colorblind="protanopia"] .text-muted-foreground,
html:not(.dark-theme)[data-colorblind="deuteranopia"] .text-muted-foreground,
html:not(.dark-theme)[data-colorblind="tritanopia"] .text-muted-foreground {
  color: #6b7280 !important;
}
</style>

<style>
/* Prevent horizontal scrolling and ensure table fits */
.overflow-x-hidden {
  overflow-x: hidden;
}

/* Ensure table cells wrap properly */
table.table-fixed {
  table-layout: fixed;
  width: 100%;
}

table.table-fixed td,
table.table-fixed th {
  word-wrap: break-word;
  overflow-wrap: break-word;
}

/* Ensure button text doesn't overflow */
button {
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Allow Type column to wrap into multiple lines */
table.table-fixed td .break-words {
  word-wrap: break-word;
  overflow-wrap: break-word;
  word-break: break-word;
  white-space: normal;
  line-height: 1.4;
}

/* Ensure Badge component wraps properly */
table.table-fixed td .inline-block {
  display: inline-block;
  max-width: 100%;
  white-space: normal;
  word-wrap: break-word;
  overflow-wrap: break-word;
}
</style>
