<template>
  <div class="contract-approval-container contract-approval-page">
    <!-- Header Section -->
    <div class="approval-header">
      <div class="header-content">
        <div class="header-top-row">
          <div class="header-text">
            <h1 class="page-title">Contract Approval Assignment</h1>
          </div>
          <div class="header-button-right">
            <button 
              @click="toggleFormView" 
              class="button button--create gap-2"
              v-if="!showCreateForm"
            >
              <svg class="btn-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
              </svg>
              Create Assignment
            </button>
          </div>
        </div>
        <div class="header-bottom-row">
          <p class="page-subtitle">Streamline contract approval workflows and manage assignments efficiently</p>
          <div class="header-actions">
            <div class="status-badge">
              <svg class="badge-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
              </svg>
              Workflow Management
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- PENDING CONTRACTS TABLE -->
    <div v-if="!showCreateForm" class="space-y-6">
      <!-- Filters -->
      <div class="filters-card">
        <div class="filters-header">
          <div class="filters-title">
            <svg class="filters-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.414A1 1 0 013 6.707V4z"/>
            </svg>
            <h3>Advanced Filters</h3>
          </div>
          <div class="filters-count">
            <span class="count-badge">{{ pendingContracts.length }} contracts</span>
          </div>
        </div>
        <div class="filters-content">
          <div class="filters-grid">
            <div class="filter-group">
              <label class="filter-label">
                <svg class="label-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
                </svg>
                Search Contracts
              </label>
              <!-- Component-level styling from main.css -->
              <div class="search-container">
                <div class="search-input-wrapper">
                  <Search class="search-icon" />
              <input 
                v-model="filters.search" 
                type="text" 
                    class="search-input search-input--large search-input--default"
                placeholder="Search by title, number, or vendor..."
                @input="fetchPendingContracts"
                    style="min-width: 220px;"
              />
                </div>
              </div>
            </div>
            <div class="filter-group">
              <label class="filter-label">
                <svg class="label-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
                </svg>
                Contract Type
              </label>
              <SingleSelectDropdown
                v-model="filters.contract_type"
                :options="contractTypeOptions"
                placeholder="All Types"
                height="2.5rem"
                @update:model-value="fetchPendingContracts"
              />
            </div>
            <div class="filter-group">
              <label class="filter-label">
                <svg class="label-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                </svg>
                Contract Kind
              </label>
              <SingleSelectDropdown
                v-model="filters.contract_kind"
                :options="contractKindOptions"
                placeholder="All Kinds"
                height="2.5rem"
                @update:model-value="fetchPendingContracts"
              />
            </div>
            <div class="filter-group">
              <label class="filter-label">
                <svg class="label-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
                </svg>
                Vendor
              </label>
              <SingleSelectDropdown
                v-model="filters.vendor_id"
                :options="vendorOptions"
                placeholder="All Vendors"
                height="2.5rem"
                @update:model-value="fetchPendingContracts"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- Pending Contracts Table -->
      <div class="contracts-card">
        <div class="contracts-header">
          <div class="contracts-title">
            <svg class="contracts-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
            </svg>
            <div>
              <h3>Contracts Pending Assignment</h3>
              <p class="contracts-subtitle">Contracts awaiting approval workflow assignment</p>
            </div>
          </div>
          <div class="contracts-stats">
            <div class="stat-item">
              <span class="stat-number">{{ pendingContracts.length }}</span>
              <span class="stat-label">Pending</span>
            </div>
            <div class="stat-item">
              <span class="stat-number">{{ approvals.length }}</span>
              <span class="stat-label">Assigned</span>
            </div>
          </div>
        </div>
        <div class="contracts-content">
          <div v-if="isLoadingContracts" class="loading-state">
            <div class="loading-spinner"></div>
            <p class="loading-text">Loading contracts...</p>
          </div>
          <div v-else-if="pendingContracts.length === 0" class="empty-state">
            <svg class="empty-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
            </svg>
            <h4>No Contracts Pending</h4>
            <p>All contracts have been assigned for approval or are in progress.</p>
          </div>
          <div v-else class="contracts-table-container">
            <table class="contracts-table">
              <thead>
                <tr>
                  <th class="col-id">ID</th>
                  <th class="col-title">Contract Details</th>
                  <th class="col-type">Type</th>
                  <th class="col-kind">Kind</th>
                  <th class="col-vendor">Vendor</th>
                  <th class="col-value">Value</th>
                  <th class="col-date">Created</th>
                  <th class="col-status">Status</th>
                  <th class="col-actions">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="contract in pendingContracts" :key="contract.contract_id" class="contract-row">
                  <td class="col-id">
                    <span class="contract-id">#{{ contract.contract_id }}</span>
                  </td>
                  <td class="col-title">
                    <div class="contract-info">
                      <h4 class="contract-name">{{ contract.contract_title }}</h4>
                      <p class="contract-number">{{ contract.contract_number }}</p>
                    </div>
                  </td>
                  <td class="col-type">
                    <span class="type-badge">{{ contract.contract_type }}</span>
                  </td>
                  <td class="col-kind">
                    <span class="kind-badge" :class="getKindClass(contract.contract_kind)">
                      {{ contract.contract_kind }}
                    </span>
                  </td>
                  <td class="col-vendor">
                    <div class="vendor-info">
                      <span class="vendor-name">{{ contract.vendor?.company_name || 'N/A' }}</span>
                    </div>
                  </td>
                  <td class="col-value">
                    <span class="value-amount">{{ formatCurrency(contract.contract_value) }}</span>
                  </td>
                  <td class="col-date">
                    <span class="date-text">{{ formatDate(contract.created_at) }}</span>
                  </td>
                  <td class="col-status">
                    <span :class="getStatusBadgeClass(contract.status)">
                      {{ formatStatusText(contract.status) }}
                    </span>
                  </td>
                  <td class="col-actions">
                    <div class="action-buttons">
                      <button 
                        @click="assignApproval(contract)" 
                        class="button button--assign"
                        title="Assign Approval"
                      >
                        Assign
                      </button>
                      <button 
                        @click="viewContract(contract)" 
                        class="button button--view"
                        title="View Details"
                      >
                        View
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Existing Approvals Table -->
      <div class="approvals-card" v-if="approvals.length > 0">
        <div class="approvals-header">
          <div class="approvals-title">
            <svg class="approvals-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"/>
            </svg>
            <div>
              <h3>Existing Approval Assignments</h3>
              <p class="approvals-subtitle">Active and completed approval workflows</p>
            </div>
          </div>
          <div class="approvals-count">
            <span class="count-badge">{{ approvals.length }} assignments</span>
          </div>
        </div>
        <div class="approvals-content">
          <div class="approvals-table-container">
            <table class="approvals-table">
              <thead>
                <tr>
                  <th class="col-id">ID</th>
                  <th class="col-workflow">Workflow</th>
                  <th class="col-type">Type</th>
                  <th class="col-contract">Contract</th>
                  <th class="col-assigner">Assigner</th>
                  <th class="col-assignee">Assignee</th>
                  <th class="col-status">Status</th>
                  <th class="col-dates">Timeline</th>
                  <th class="col-actions">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="approval in approvals" :key="approval.approval_id" class="approval-row">
                  <td class="col-id">
                    <span class="approval-id">#{{ approval.approval_id }}</span>
                  </td>
                  <td class="col-workflow">
                    <div class="workflow-info">
                      <span class="workflow-name">{{ approval.workflow_name }}</span>
                    </div>
                  </td>
                  <td class="col-type">
                    <span class="type-badge type-creation">{{ approval.object_type }}</span>
                  </td>
                  <td class="col-contract">
                    <div v-if="approval.contract_details" class="contract-details">
                      <div class="contract-title">{{ approval.contract_details.title }}</div>
                      <div class="contract-number">{{ approval.contract_details.number }}</div>
                    </div>
                    <div v-else class="contract-id">{{ approval.object_id }}</div>
                  </td>
                  <td class="col-assigner">
                    <div class="user-info">
                      <span class="user-name">{{ approval.assigner_name }}</span>
                    </div>
                  </td>
                  <td class="col-assignee">
                    <div class="user-info">
                      <span class="user-name">{{ approval.assignee_name }}</span>
                    </div>
                  </td>
                  <td class="col-status">
                    <span :class="getApprovalStatusBadgeClass(approval.status)">
                      {{ formatStatusText(approval.status) }}
                    </span>
                  </td>
                  <td class="col-dates">
                    <div class="date-info">
                      <div class="date-item">
                        <span class="date-label">Assigned</span>
                        <span class="date-value">{{ formatDate(approval.assigned_date) }}</span>
                      </div>
                      <div class="date-item">
                        <span class="date-label">Due</span>
                        <span class="date-value">{{ formatDate(approval.due_date) }}</span>
                      </div>
                    </div>
                  </td>
                  <td class="col-actions">
                    <div class="action-buttons">
                      <button class="button button--view" title="View Details">
                        View
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- CREATE ASSIGNMENT FORM -->
    <div v-if="showCreateForm" class="space-y-6">
        <div class="card">
          <div class="card-header">
            <div class="flex items-center justify-between">
              <h3 class="card-title flex items-center gap-2">
                <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
                </svg>
                Create New Approval Assignment
              </h3>
              <button type="button" @click="toggleFormView" class="button button--back">
                Back to List
              </button>
            </div>
          </div>
          <div class="card-content space-y-6">
            <!-- Selected Contract Information -->
            <div v-if="selectedContract" class="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h4 class="text-lg font-semibold text-blue-900 mb-2">Selected Contract</h4>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <p class="text-sm text-blue-700"><strong>Title:</strong> {{ selectedContract.contract_title }}</p>
                  <p class="text-sm text-blue-700"><strong>Number:</strong> {{ selectedContract.contract_number }}</p>
                  <p class="text-sm text-blue-700"><strong>Type:</strong> {{ selectedContract.contract_type }}</p>
                </div>
                <div>
                  <p class="text-sm text-blue-700"><strong>Vendor:</strong> {{ selectedContract.vendor?.company_name || 'N/A' }}</p>
                  <p class="text-sm text-blue-700"><strong>Value:</strong> {{ formatCurrency(selectedContract.contract_value) }}</p>
                  <p class="text-sm text-blue-700"><strong>Status:</strong> {{ selectedContract.status.replace('_', ' ') }}</p>
                </div>
              </div>
            </div>
            <form @submit.prevent="createAssignment" class="global-form-container">
              <div class="global-form-box">
                <!-- Workflow Information -->
                <div class="global-form-section">
                  <h4 class="global-form-section-title">Workflow Information</h4>
                  <div class="global-form-row">
                    <div class="global-form-group">
                      <label for="workflowName" class="global-form-label">Workflow Name <span class="global-form-label-required">*</span></label>
                      <input 
                        v-model="form.workflow_name" 
                        type="text" 
                        id="workflowName" 
                        class="global-form-input" 
                        required 
                        placeholder="Enter workflow name"
                      />
                    </div>
                    <div class="global-form-group">
                      <label for="objectType" class="global-form-label">Object Type <span class="global-form-label-required">*</span></label>
                      <select v-model="form.object_type" id="objectType" class="global-form-select" required :disabled="selectedContract" @change="onObjectTypeChange">
                        <option value="">Select object type</option>
                        <option value="CONTRACT_CREATION">Contract Creation</option>
                        <option value="CONTRACT_AMENDMENT">Contract Amendment</option>
                        <option value="SUBCONTRACT_CREATION">Subcontract Creation</option>
                        <option value="CONTRACT_RENEWAL">Contract Renewal</option>
                      </select>
                      <p v-if="selectedContract" class="global-form-helper-text">
                        Object type is automatically set based on the selected contract kind: {{ selectedContract.contract_kind }}
                      </p>
                    </div>
                    <div class="global-form-group">
                      <label for="contractId" class="global-form-label">Contract <span class="global-form-label-required">*</span></label>
                      <select v-model="form.object_id" id="contractId" class="global-form-select" required @change="onContractChange">
                        <option value="">Select contract</option>
                        <option v-for="contract in contracts" :key="contract.contract_id" :value="contract.contract_id">
                          {{ contract.contract_title }} ({{ contract.contract_number }}) - {{ contract.contract_type }} [{{ contract.contract_kind }}]
                        </option>
                      </select>
                    </div>
                  </div>
                </div>

                <!-- Assignment Details -->
                <div class="global-form-section">
                  <h4 class="global-form-section-title">Assignment Details</h4>
                  <div class="global-form-row">
                    <div class="global-form-group">
                      <label for="assignerId" class="global-form-label">Assigner <span class="global-form-label-required">*</span></label>
                      <select v-model="form.assigner_id" id="assignerId" class="global-form-select" required @change="onAssignerChange" :disabled="isLoadingUsers">
                        <option value="">{{ isLoadingUsers ? 'Loading users...' : 'Select assigner' }}</option>
                        <option v-for="user in users" :key="user.user_id" :value="user.user_id">
                          {{ user.display_name }}
                        </option>
                      </select>
                    </div>
                    <div class="global-form-group">
                      <label for="assigneeId" class="global-form-label">Assignee <span class="global-form-label-required">*</span></label>
                      <select v-model="form.assignee_id" id="assigneeId" class="global-form-select" required @change="onAssigneeChange" :disabled="isLoadingUsers">
                        <option value="">{{ isLoadingUsers ? 'Loading users...' : 'Select assignee' }}</option>
                        <option v-for="user in users" :key="user.user_id" :value="user.user_id">
                          {{ user.display_name }}
                        </option>
                      </select>
                    </div>
                  </div>
                </div>

                <!-- Timeline -->
                <div class="global-form-section">
                  <h4 class="global-form-section-title">Timeline</h4>
                  <div class="global-form-row">
                    <div class="global-form-group">
                      <label for="dueDate" class="global-form-label">Due Date <span class="global-form-label-required">*</span></label>
                      <input 
                        v-model="form.due_date" 
                        type="datetime-local" 
                        id="dueDate" 
                        class="global-form-input" 
                        required
                      />
                    </div>
                  </div>
                </div>
              </div>

              <!-- Action Buttons -->
              <div class="flex gap-4 pt-4">
                <button type="button" @click="resetForm" class="btn btn--outline">
                  <svg class="h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
                  </svg>
                  Reset Form
                </button>
                <button type="submit" class="button button--create gap-2" :disabled="isSubmitting">
                  <svg class="h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
                  </svg>
                  {{ isSubmitting ? 'Creating...' : 'Create Assignment' }}
                </button>
              </div>
            </form>
          </div>
        </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import './ContractApprovalAssignment.css'
import '@/assets/components/badge.css'
import '@/assets/components/form.css'
import '@/assets/components/contract_darktheme.css'
import { ref, onMounted, watch, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useStore } from 'vuex'
import { Search } from 'lucide-vue-next'
import contractApprovalApi from '../../services/contractApprovalApi.js'
import contractsApi from '../../services/contractsApi.js'
import loggingService from '@/services/loggingService'
import { PopupService } from '@/popup/popupService'
import '@/assets/components/main.css'
import '@/assets/components/dropdown.css'
import SingleSelectDropdown from '@/assets/components/SingleSelectDropdown.vue'

const route = useRoute()
const store = useStore()

// Get current user from store
const currentUser = computed(() => store.getters['auth/currentUser'] || store.state.auth?.currentUser)

// Reactive data
const isSubmitting = ref(false)
const users = ref([])
const isLoadingUsers = ref(false)
const approvals = ref([])
const isLoadingApprovals = ref(false)
const showCreateForm = ref(false)
const pendingContracts = ref([])
const isLoadingContracts = ref(false)
const vendors = ref([])
const selectedContract = ref(null)

// Filters
const filters = ref({
  search: '',
  contract_type: '',
  contract_kind: '',
  vendor_id: '',
  status: '',
  object_type: '',
  assignee_id: '',
  is_overdue: false
})

// Form data
const form = ref({
  workflow_id: null, // Will be auto-generated as integer based on workflow_name
  workflow_name: '',
  assigner_id: '',
  assignee_id: '', // User can select from dropdown
  object_type: '', // Will be updated based on selected contract
  object_id: '',
  due_date: '',
  comment_text: ''
})

// Additional data
const contracts = ref([])

// Dropdown options for SingleSelectDropdown
const contractTypeOptions = [
  { value: '', label: 'All Types' },
  { value: 'SERVICE', label: 'Service' },
  { value: 'SUPPLY', label: 'Supply' },
  { value: 'CONSULTING', label: 'Consulting' },
  { value: 'MAINTENANCE', label: 'Maintenance' }
]

const contractKindOptions = [
  { value: '', label: 'All Kinds' },
  { value: 'MAIN', label: 'Main' },
  { value: 'AMENDMENT', label: 'Amendment' },
  { value: 'SUBCONTRACT', label: 'Subcontract' },
  { value: 'RENEWAL', label: 'Renewal' }
]

const vendorOptions = computed(() => {
  return [
    { value: '', label: 'All Vendors' },
    ...vendors.value.map(vendor => ({
      value: vendor.vendor_id,
      label: vendor.company_name
    }))
  ]
})

// Watch form changes for debugging
watch(form, (newForm) => {
  console.log('Form data changed:', newForm)
}, { deep: true })

// Methods
const fetchUsers = async () => {
  isLoadingUsers.value = true
  try {
    console.log('Fetching approval users (with ApproveContract permission) from contracts API')
    // Use the new endpoint that filters users by ApproveContract permission
    const response = await contractsApi.getApprovalUsers()
    
    console.log('API response data:', response)
    
    if (response.success && response.data) {
      users.value = response.data
      console.log('Successfully fetched approval users:', response.data.length, 'records')
      
      // Set assigner_id to current logged-in user if they have permission
      if (currentUser.value) {
        const currentUserId = currentUser.value.userid || currentUser.value.user_id
        if (currentUserId) {
          // Check if current user is in the filtered list
          const currentUserInList = users.value.find(u => u.user_id == currentUserId)
          if (currentUserInList) {
          form.value.assigner_id = currentUserId.toString()
          console.log('Set assigner_id to current user:', currentUserId)
          } else {
            console.log('Current user does not have ApproveContract permission, not setting as assigner')
          }
        }
      }
    } else {
      console.error('API returned no approval users data')
      users.value = []
    }
  } catch (error) {
    console.error('Error fetching approval users:', error)
    users.value = []
    
    // Check if we're in iframe mode (embedded in GRC)
    const isInIframe = window.self !== window.top
    
    // Only show error popup if not a permission error or if not in iframe mode
    if (!isInIframe && error.response?.status !== 403) {
      PopupService.warning('Failed to load users with approval permissions. Please try again or contact your administrator.', 'Loading Error')
    } else if (error.response?.status === 403) {
      console.warn('[ContractApprovalAssignment] Permission denied for users - showing empty state')
    }
  } finally {
    isLoadingUsers.value = false
  }
}

const fetchPendingContracts = async () => {
  isLoadingContracts.value = true
  try {
    console.log('Fetching contracts pending assignment')
    const response = await contractsApi.getContracts({ status: 'PENDING_ASSIGNMENT' })
    
    console.log('API response data:', response)
    
    if (response.success && response.data) {
      // Filter contracts to only show MAIN and AMENDMENT contract kinds
      let filteredContracts = response.data.filter(contract => 
        contract.contract_kind === 'MAIN' || contract.contract_kind === 'AMENDMENT'
      )
      
      // Apply additional filters if specified
      if (filters.value.contract_kind) {
        filteredContracts = filteredContracts.filter(contract => 
          contract.contract_kind === filters.value.contract_kind
        )
      }
      
      if (filters.value.contract_type) {
        filteredContracts = filteredContracts.filter(contract => 
          contract.contract_type === filters.value.contract_type
        )
      }
      
      if (filters.value.vendor_id) {
        filteredContracts = filteredContracts.filter(contract => 
          contract.vendor_id == filters.value.vendor_id
        )
      }
      
      if (filters.value.search) {
        const searchTerm = filters.value.search.toLowerCase()
        filteredContracts = filteredContracts.filter(contract => 
          contract.contract_title.toLowerCase().includes(searchTerm) ||
          contract.contract_number.toLowerCase().includes(searchTerm) ||
          (contract.vendor?.company_name && contract.vendor.company_name.toLowerCase().includes(searchTerm))
        )
      }
      
      pendingContracts.value = filteredContracts
      console.log('Successfully fetched pending contracts:', filteredContracts.length, 'records (filtered for MAIN and AMENDMENT)')
    } else {
      console.error('API returned no pending contracts data')
      pendingContracts.value = []
    }
  } catch (error) {
    console.error('Error fetching pending contracts:', error)
    pendingContracts.value = []
    
    // Check if we're in iframe mode (embedded in GRC)
    const isInIframe = window.self !== window.top
    
    // Only log permission errors, don't show popups in iframe mode
    if (error.response?.status === 403) {
      console.warn('[ContractApprovalAssignment] Permission denied for pending contracts - showing empty state')
    } else if (!isInIframe) {
      console.warn('[ContractApprovalAssignment] Error fetching pending contracts:', error.message)
    }
  } finally {
    isLoadingContracts.value = false
  }
}

const fetchVendors = async () => {
  try {
    console.log('Fetching vendors for approval assignment')
    const response = await contractsApi.getVendors()
    
    console.log('API response data:', response)
    
    if (response.success && response.data) {
      vendors.value = response.data
      console.log('Successfully fetched vendors:', response.data.length, 'records')
    } else {
      console.error('API returned no vendors data')
      vendors.value = []
    }
  } catch (error) {
    console.error('Error fetching vendors:', error)
    vendors.value = []
    
    // Check if we're in iframe mode (embedded in GRC)
    const isInIframe = window.self !== window.top
    
    // Only log permission errors, don't show popups in iframe mode
    if (error.response?.status === 403) {
      console.warn('[ContractApprovalAssignment] Permission denied for vendors - showing empty state')
    } else if (!isInIframe) {
      console.warn('[ContractApprovalAssignment] Error fetching vendors:', error.message)
    }
  }
}

const fetchAllContracts = async () => {
  try {
    console.log('Fetching all contracts for dropdown')
    const response = await contractsApi.getContracts({})
    
    console.log('API response data:', response)
    
    if (response.success && response.data) {
      // Filter contracts to only show MAIN and AMENDMENT contract kinds
      const filteredContracts = response.data.filter(contract => 
        contract.contract_kind === 'MAIN' || contract.contract_kind === 'AMENDMENT'
      )
      contracts.value = filteredContracts
      console.log('Successfully fetched contracts:', filteredContracts.length, 'records (filtered for MAIN and AMENDMENT)')
  } else {
      console.error('API returned no contracts data')
      contracts.value = []
    }
  } catch (error) {
    console.error('Error fetching contracts:', error)
    contracts.value = []
    
    // Check if we're in iframe mode (embedded in GRC)
    const isInIframe = window.self !== window.top
    
    // Only log permission errors, don't show popups in iframe mode
    if (error.response?.status === 403) {
      console.warn('[ContractApprovalAssignment] Permission denied for contracts - showing empty state')
    } else if (!isInIframe) {
      console.warn('[ContractApprovalAssignment] Error fetching contracts:', error.message)
    }
  }
}

const assignApproval = (contract) => {
  selectedContract.value = contract
  form.value.object_id = contract.contract_id
  
  // Object type will be selected by user
  // Assignee will be selected by user from dropdown
  
  // Add the selected contract to the contracts list if not already present
  const existingContract = contracts.value.find(c => c.contract_id === contract.contract_id)
  if (!existingContract) {
    contracts.value.unshift(contract) // Add to the beginning of the list
  }
  
  showCreateForm.value = true
}

const viewContract = (contract) => {
  // Navigate to contract detail page
  window.open(`/contracts/${contract.contract_id}`, '_blank')
}

const formatCurrency = (value) => {
  if (!value) return 'N/A'
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
  }).format(value)
}

const onAssignerChange = () => {
  // Names are now auto-populated by backend
  console.log('Assigner changed:', form.value.assigner_id)
}

const onAssigneeChange = () => {
  // Names are now auto-populated by backend
  console.log('Assignee changed:', form.value.assignee_id)
}

const onObjectTypeChange = () => {
  // Warn user if they try to change object type when a contract is selected
  if (selectedContract.value) {
    console.warn('Object type should be automatically set based on contract kind. Current contract kind:', selectedContract.value.contract_kind)
  }
}

const onContractChange = () => {
  const contract = contracts.value.find(c => c.contract_id == form.value.object_id)
  if (contract) {
    selectedContract.value = contract
    
    // Set object_type based on contract_kind
    if (contract.contract_kind === 'AMENDMENT') {
      form.value.object_type = 'CONTRACT_CREATION' // AMENDMENT contracts are still treated as contract creation
    } else if (contract.contract_kind === 'SUBCONTRACT') {
      form.value.object_type = 'SUBCONTRACT_CREATION'
    } else {
      form.value.object_type = 'CONTRACT_CREATION'
    }
    
    console.log('Selected contract:', contract)
  } else {
    selectedContract.value = null
  }
}

const createAssignment = async () => {
  isSubmitting.value = true
  
  try {
    console.log('Creating contract approval assignment:', form.value)
    console.log('Selected contract:', selectedContract.value)
    
    // Ensure object_type is correct based on selected contract
    if (selectedContract.value) {
      if (selectedContract.value.contract_kind === 'AMENDMENT') {
        form.value.object_type = 'CONTRACT_CREATION'
      } else if (selectedContract.value.contract_kind === 'SUBCONTRACT') {
        form.value.object_type = 'SUBCONTRACT_CREATION'
      } else {
        form.value.object_type = 'CONTRACT_CREATION'
      }
      console.log('Updated object_type based on contract kind:', form.value.object_type)
    }
    
    // Ensure object_id is a number, not a string
    // Generate a workflow_id if not provided (backend requires an integer)
    const workflowId = form.value.workflow_id || 
      (form.value.workflow_name ? 
        Math.abs(form.value.workflow_name.split('').reduce((a, b) => { a = ((a << 5) - a) + b.charCodeAt(0); return a & a }, 0)) : 
        Math.floor(Math.random() * 1000000) + 1)
    
    const formData = {
      ...form.value,
      workflow_id: parseInt(workflowId),
      object_id: parseInt(form.value.object_id),
      assigner_id: parseInt(form.value.assigner_id),
      assignee_id: parseInt(form.value.assignee_id)
    }
    
    console.log('Final form data being sent to API:', formData)
    
    // Call the API to create the approval assignment
    const response = await contractApprovalApi.createApproval(formData)
    
    console.log('Assignment created successfully:', response)
    
    // Reset form and go back to list view
    resetForm()
    showCreateForm.value = false
    selectedContract.value = null
    
    // Refresh the pending contracts and approvals lists
    await fetchPendingContracts()
    await fetchApprovals()
    
    PopupService.success(`Contract approval assignment created successfully! Approval ID: ${response.data.approval_id}. The contract status has been updated to UNDER_REVIEW. The assigned user can now see this approval in their "My Approvals" page.`, 'Assignment Created')
  } catch (error) {
    console.error('Error creating assignment:', error)
    
    // Handle different types of errors
    let errorMessage = 'Error creating assignment. Please try again.'
    if (error.message) {
      errorMessage = error.message
    } else if (error.response?.data?.message) {
      errorMessage = error.response.data.message
    } else if (error.response?.data?.error) {
      errorMessage = error.response.data.error
    }
    
    PopupService.error(errorMessage, 'Error')
  } finally {
    isSubmitting.value = false
  }
}

const resetForm = () => {
  // Get current user ID for assigner
  const currentUserId = currentUser.value?.userid || currentUser.value?.user_id
  
  form.value = {
    workflow_id: null, // Will be auto-generated as integer based on workflow_name
    workflow_name: '',
    assigner_id: currentUserId ? currentUserId.toString() : '', // Set to current logged-in user
    assignee_id: '', // User can select from dropdown
    object_type: '', // Will be updated based on selected contract
    object_id: '',
    due_date: '',
    comment_text: ''
  }
  selectedContract.value = null
}

const fetchApprovals = async () => {
  isLoadingApprovals.value = true
  try {
    console.log('Fetching contract approvals with filters:', filters.value)
    const response = await contractApprovalApi.getApprovals(filters.value)
    
    console.log('API response:', response)
    
    if (response.success && response.data) {
      approvals.value = response.data
      console.log('Successfully fetched approvals:', response.data.length, 'records')
    } else {
      console.error('API returned no approvals data')
      approvals.value = []
    }
  } catch (error) {
    console.error('Error fetching approvals:', error)
    approvals.value = []
    
    // Check if we're in iframe mode (embedded in GRC)
    const isInIframe = window.self !== window.top
    
    // Only show error popup if not a permission error or if not in iframe mode
    // In iframe mode, GRC handles permissions, so we just show empty state
    if (!isInIframe && error.response?.status !== 403) {
      const errorMessage = error.message || error.response?.data?.message || 'Failed to load approvals'
      PopupService.warning(`${errorMessage}. Please check your connection and try again.`, 'Loading Failed')
    } else if (error.response?.status === 403) {
      console.warn('[ContractApprovalAssignment] Permission denied for approvals - showing empty state')
    }
  } finally {
    isLoadingApprovals.value = false
  }
}

const toggleFormView = () => {
  showCreateForm.value = !showCreateForm.value
  if (!showCreateForm.value) {
    resetForm()
  }
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  } catch (error) {
    return 'Invalid Date'
  }
}

const formatStatusText = (status) => {
  if (!status) return 'UNKNOWN'
  
  // Convert underscores to spaces and uppercase
  return String(status)
    .replace(/_/g, ' ')
    .toUpperCase()
}

const getStatusBadgeClass = (status) => {
  if (!status) return 'badge-draft'
  
  const statusUpper = String(status).toUpperCase()
  
  // Map contract statuses to badge classes
  if (statusUpper === 'PENDING_ASSIGNMENT') {
    return 'badge-pending-assignment'
  } else if (statusUpper === 'APPROVED' || statusUpper === 'ACTIVE') {
    return 'badge-approved'
  } else if (statusUpper.includes('REVIEW') || statusUpper.includes('PENDING')) {
    return 'badge-in-review'
  } else if (statusUpper === 'DRAFT') {
    return 'badge-draft'
  }
  
  return 'badge-draft'
}

const getApprovalStatusBadgeClass = (status) => {
  if (!status) return 'badge-draft'
  
  const statusUpper = String(status).toUpperCase()
  
  // Map approval statuses to badge classes
  if (statusUpper === 'APPROVED' || statusUpper === 'COMMENTED') {
    return 'badge-approved' // Green for approved/commented
  } else if (statusUpper === 'ASSIGNED' || statusUpper === 'IN_PROGRESS') {
    return 'badge-in-review' // Orange for in progress
  } else if (statusUpper === 'SKIPPED' || statusUpper === 'EXPIRED' || statusUpper === 'CANCELLED') {
    return 'badge-draft' // Gray for inactive
  }
  
  return 'badge-draft'
}

const getKindClass = (kind) => {
  const kindClasses = {
    'MAIN': 'kind-main',
    'AMENDMENT': 'kind-amendment',
    'SUBCONTRACT': 'kind-subcontract',
    'RENEWAL': 'kind-renewal'
  }
  return kindClasses[kind] || 'kind-default'
}


// Initialize form with default due date and fetch users
onMounted(async () => {
  await loggingService.logPageView('Contract', 'Contract Approval Assignment')
  const tomorrow = new Date()
  tomorrow.setDate(tomorrow.getDate() + 1)
  
  form.value.due_date = tomorrow.toISOString().slice(0, 16)
  
  // Set assigner_id to current logged-in user if available
  if (currentUser.value) {
    const currentUserId = currentUser.value.userid || currentUser.value.user_id
    if (currentUserId) {
      form.value.assigner_id = currentUserId.toString()
      console.log('Set assigner_id to current user on mount:', currentUserId)
    }
  }
  
  // Fetch all data first
  await fetchUsers()
  await fetchVendors()
  await fetchAllContracts()
  await fetchPendingContracts()
  await fetchApprovals()
  
  // Check for URL parameters and auto-fill form (if any parameters, show form directly)
  const contractId = route.query.contractId
  const objectType = route.query.objectType
  
  if (contractId || objectType) {
    showCreateForm.value = true
    
    if (contractId) {
      // Handle both string and array types from route.query
      const contractIdValue = Array.isArray(contractId) ? contractId[0] : contractId
      form.value.object_id = contractIdValue
      // Find and set the selected contract
      const contract = contracts.value.find(c => c.contract_id == contractIdValue)
      if (contract) {
        selectedContract.value = contract
        
        // Set object_type based on contract_kind
        if (contract.contract_kind === 'AMENDMENT') {
          form.value.object_type = 'CONTRACT_CREATION' // AMENDMENT contracts are still treated as contract creation
        } else if (contract.contract_kind === 'SUBCONTRACT') {
          form.value.object_type = 'SUBCONTRACT_CREATION'
        } else {
          form.value.object_type = 'CONTRACT_CREATION'
        }
      }
      console.log('Auto-filled object_id from URL parameter:', contractId)
    }
    
    if (objectType) {
      // Handle both string and array types from route.query
      const objectTypeValue = Array.isArray(objectType) ? objectType[0] : objectType
      const contractIdValue = Array.isArray(contractId) ? contractId[0] : contractId
      // Only set object_type if no contract was found above
      if (!contractId || !contracts.value.find(c => c.contract_id == contractIdValue)) {
        form.value.object_type = objectTypeValue
        console.log('Auto-filled object_type from URL parameter:', objectType)
      }
    }
  }
})
</script>
