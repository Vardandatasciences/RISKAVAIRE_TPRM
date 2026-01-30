<template>
  <div class="dashboard">
    <div class="row">
      <div class="col-24">
        <h1 class="dashboard-title">Approval System Dashboard</h1>
        <p class="dashboard-subtitle">Manage workflows, requests, and approvals</p>
      </div>
    </div>

    <!-- Statistics Cards Grid -->
    <div class="kpi-cards-grid" style="margin-bottom: 40px;">
      <!-- Total Requests Card -->
      <div class="kpi-card" :class="{ 'loading': loading }">
        <div class="kpi-card-content">
          <div class="kpi-card-icon-wrapper kpi-card-icon-blue">
            <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
            </svg>
          </div>
          <div class="kpi-card-text">
            <p class="kpi-card-title">TOTAL REQUESTS</p>
            <p class="kpi-card-value">
              <span v-if="!loading">{{ stats.total_requests || 0 }}</span>
              <span v-else class="loading-skeleton" style="display: inline-block; width: 60px; height: 28px; background: linear-gradient(90deg, #f1f5f9 25%, #e2e8f0 50%, #f1f5f9 75%); background-size: 200% 100%; animation: loading 1.5s infinite; border-radius: 4px;"></span>
            </p>
            <p class="kpi-card-subheading">All requests</p>
          </div>
        </div>
      </div>

      <!-- Pending Requests Card -->
      <div class="kpi-card" :class="{ 'loading': loading }">
        <div class="kpi-card-content">
          <div class="kpi-card-icon-wrapper kpi-card-icon-red">
            <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <div class="kpi-card-text">
            <p class="kpi-card-title">PENDING REQUESTS</p>
            <p class="kpi-card-value">
              <span v-if="!loading">{{ stats.pending_requests || 0 }}</span>
              <span v-else class="loading-skeleton" style="display: inline-block; width: 60px; height: 28px; background: linear-gradient(90deg, #f1f5f9 25%, #e2e8f0 50%, #f1f5f9 75%); background-size: 200% 100%; animation: loading 1.5s infinite; border-radius: 4px;"></span>
            </p>
            <p class="kpi-card-subheading">Awaiting action</p>
          </div>
        </div>
      </div>

      <!-- In Progress Card -->
      <div class="kpi-card" :class="{ 'loading': loading }">
        <div class="kpi-card-content">
          <div class="kpi-card-icon-wrapper kpi-card-icon-green">
            <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
            </svg>
          </div>
          <div class="kpi-card-text">
            <p class="kpi-card-title">IN PROGRESS</p>
            <p class="kpi-card-value">
              <span v-if="!loading">{{ stats.in_progress_requests || 0 }}</span>
              <span v-else class="loading-skeleton" style="display: inline-block; width: 60px; height: 28px; background: linear-gradient(90deg, #f1f5f9 25%, #e2e8f0 50%, #f1f5f9 75%); background-size: 200% 100%; animation: loading 1.5s infinite; border-radius: 4px;"></span>
            </p>
            <p class="kpi-card-subheading">Currently processing</p>
          </div>
        </div>
      </div>

      <!-- Approved Card -->
      <div class="kpi-card" :class="{ 'loading': loading }">
        <div class="kpi-card-content">
          <div class="kpi-card-icon-wrapper kpi-card-icon-purple">
            <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <div class="kpi-card-text">
            <p class="kpi-card-title">APPROVED</p>
            <p class="kpi-card-value">
              <span v-if="!loading">{{ stats.approved_requests || 0 }}</span>
              <span v-else class="loading-skeleton" style="display: inline-block; width: 60px; height: 28px; background: linear-gradient(90deg, #f1f5f9 25%, #e2e8f0 50%, #f1f5f9 75%); background-size: 200% 100%; animation: loading 1.5s infinite; border-radius: 4px;"></span>
            </p>
            <p class="kpi-card-subheading">Successfully approved</p>
          </div>
        </div>
      </div>

      <!-- Rejected Card -->
      <div class="kpi-card" :class="{ 'loading': loading }">
        <div class="kpi-card-content">
          <div class="kpi-card-icon-wrapper kpi-card-icon-orange">
            <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <div class="kpi-card-text">
            <p class="kpi-card-title">REJECTED</p>
            <p class="kpi-card-value">
              <span v-if="!loading">{{ stats.rejected_requests || 0 }}</span>
              <span v-else class="loading-skeleton" style="display: inline-block; width: 60px; height: 28px; background: linear-gradient(90deg, #f1f5f9 25%, #e2e8f0 50%, #f1f5f9 75%); background-size: 200% 100%; animation: loading 1.5s infinite; border-radius: 4px;"></span>
            </p>
            <p class="kpi-card-subheading">Rejected requests</p>
          </div>
        </div>
      </div>

      <!-- My Tasks Card -->
      <div class="kpi-card" :class="{ 'loading': loading }">
        <div class="kpi-card-content">
          <div class="kpi-card-icon-wrapper kpi-card-icon-blue">
            <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"/>
            </svg>
          </div>
          <div class="kpi-card-text">
            <p class="kpi-card-title">MY TASKS</p>
            <p class="kpi-card-value">
              <span v-if="!loading">{{ myTasksCount }}</span>
              <span v-else class="loading-skeleton" style="display: inline-block; width: 60px; height: 28px; background: linear-gradient(90deg, #f1f5f9 25%, #e2e8f0 50%, #f1f5f9 75%); background-size: 200% 100%; animation: loading 1.5s infinite; border-radius: 4px;"></span>
            </p>
            <p class="kpi-card-subheading">Pending tasks</p>
          </div>
        </div>
      </div>

      <!-- Recent Requests Card -->
      <div class="kpi-card" :class="{ 'loading': loading }">
        <div class="kpi-card-content">
          <div class="kpi-card-icon-wrapper kpi-card-icon-gray">
            <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <div class="kpi-card-text">
            <p class="kpi-card-title">RECENT REQUESTS</p>
            <p class="kpi-card-value">
              <span v-if="!loading">{{ recentRequestsCount }}</span>
              <span v-else class="loading-skeleton" style="display: inline-block; width: 60px; height: 28px; background: linear-gradient(90deg, #f1f5f9 25%, #e2e8f0 50%, #f1f5f9 75%); background-size: 200% 100%; animation: loading 1.5s infinite; border-radius: 4px;"></span>
            </p>
            <p class="kpi-card-subheading">Latest requests</p>
          </div>
        </div>
      </div>
    </div>


    <!-- Recent Activity -->
    <div class="row activity-row">
      <div class="col-12">
        <div class="activity-card">
          <div class="card-header">
            <div class="card-header-with-dropdown">
              <h3>Recent Requests</h3>
              <SingleSelectDropdown
                v-model="selectedRequestUser"
                :options="userDropdownOptions"
                placeholder="Select User"
                height="2rem"
                @update:model-value="loadUserRequests"
              />
            </div>
          </div>
          
          <div class="content-container">
            <div v-if="!hasRecentRequests" class="no-data">
              <div class="empty-state">No recent requests</div>
            </div>
            
            <div v-if="hasRecentRequests" class="request-list">
              <div 
                v-for="request in recentRequests" 
                :key="request.approval_id"
                class="request-item"
                @click="viewRequest(request.approval_id)"
              >
                <div class="request-header">
                  <span class="request-title">{{ request.request_title }}</span>
                  <div class="request-tags">
                    <span :class="getStatusBadgeClass(request.overall_status)">
                      {{ formatStatusText(request.overall_status) }}
                    </span>
                    <span class="tag" :class="getWorkflowTypeColor(request.workflow_type)">
                      {{ formatWorkflowType(request.workflow_type) }}
                    </span>
                  </div>
                </div>
                <div class="request-meta">
                  <span class="workflow-name">{{ request.workflow_name }}</span>
                  <span class="request-date">{{ formatDate(request.created_at) }}</span>
                </div>
                <div class="request-details">
                  <span class="requester">By: {{ request.requester_id }}</span>
                  <span class="priority" :class="getPriorityClass(request.priority)">
                    {{ request.priority || 'MEDIUM' }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-12">
        <div class="activity-card">
          <div class="card-header">
            <div class="card-header-with-dropdown">
              <h3>My Tasks</h3>
              <select 
                v-model="selectedTaskUser" 
                @change="loadUserTasks"
                class="user-select"
              >
                <option value="">Select User</option>
                <option
                  v-for="user in users"
                  :key="user.UserId"
                  :value="user.UserId"
                >
                  {{ user.UserName }}
                </option>
              </select>
            </div>
          </div>
          
          <div class="content-container">
            <div v-if="!hasMyTasks" class="no-data">
              <div class="empty-state">No pending tasks</div>
            </div>
            
            <div v-if="hasMyTasks" class="task-list">
              <div 
                v-for="task in myTasks" 
                :key="task.stage_id"
                class="task-item"
                @click="viewRequest(task.approval_id)"
              >
                <div class="task-header">
                  <span class="task-name">{{ task.stage_name }}</span>
                  <div class="task-tags">
                    <span :class="getStatusBadgeClass(task.stage_status)">
                      {{ formatStatusText(task.stage_status) }}
                    </span>
                    <span class="tag" :class="getWorkflowTypeColor(task.workflow_type)">
                      {{ formatWorkflowType(task.workflow_type) }}
                    </span>
                  </div>
                </div>
                <div class="task-meta">
                  <span class="request-title">{{ task.request_title }}</span>
                  <span class="deadline">{{ formatDate(task.deadline_date) }}</span>
                </div>
                <div class="task-details">
                  <span class="workflow-name">{{ task.workflow_name }}</span>
                  <span v-show="isDeadlineNear(task.deadline_date)" class="deadline-warning">
                    ⚠️ Due Soon
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/utils/api'
import dayjs from 'dayjs'
import loggingService from '@/services/loggingService'
// Import dropdown styles
import '@/assets/components/dropdown.css'
// Import custom dropdown component
import SingleSelectDropdown from '@/assets/components/SingleSelectDropdown.vue'

export default {
  name: 'VendorApprovalDashboard',
  setup() {
    const router = useRouter()
    const stats = ref({})
    const recentRequests = ref([])
    const myTasks = ref([])
    const loading = ref(false)
    const lastUpdated = ref(null)
    const users = ref([])
    const selectedRequestUser = ref('')
    const selectedTaskUser = ref('')

    // User options for dropdown
    const userDropdownOptions = computed(() => {
      return [
        { value: '', label: 'Select User' },
        ...users.value.map(user => ({
          value: user.UserId,
          label: user.UserName
        }))
      ]
    })

    // Computed properties to avoid template complexity
    const myTasksCount = computed(() => {
      return myTasks.value ? myTasks.value.length : 0
    })

    const recentRequestsCount = computed(() => {
      return recentRequests.value ? recentRequests.value.length : 0
    })

    const hasRecentRequests = computed(() => {
      return recentRequests.value && recentRequests.value.length > 0
    })

    const hasMyTasks = computed(() => {
      return myTasks.value && myTasks.value.length > 0
    })

    const loadUsers = async () => {
      try {
        console.log('Loading users...')
        const usersResponse = await api.get('/api/v1/vendor-approval/users/')
        console.log('Users response:', usersResponse.data)
        users.value = usersResponse.data
        
        // Set default selected users
        if (users.value.length > 0) {
          selectedRequestUser.value = users.value[0].UserId
          selectedTaskUser.value = users.value[0].UserId
        }
      } catch (error) {
        console.error('Error loading users:', error)
        users.value = []
      }
    }

    const loadUserRequests = async () => {
      if (!selectedRequestUser.value) return
      
      try {
        console.log('Loading requests for user:', selectedRequestUser.value)
        const response = await api.get(`/api/v1/vendor-approval/dashboard/user-requests/${selectedRequestUser.value}/`)
        console.log('User requests response:', response.data)
        recentRequests.value = response.data
      } catch (error) {
        console.error('Error loading user requests:', error)
        recentRequests.value = []
      }
    }

    const loadUserTasks = async () => {
      if (!selectedTaskUser.value) return
      
      try {
        console.log('Loading tasks for user:', selectedTaskUser.value)
        const response = await api.get(`/api/v1/vendor-approval/dashboard/user-tasks/${selectedTaskUser.value}/`)
        console.log('User tasks response:', response.data)
        myTasks.value = response.data
      } catch (error) {
        console.error('Error loading user tasks:', error)
        myTasks.value = []
      }
    }

    const loadDashboardData = async () => {
      try {
        loading.value = true
        console.log('Loading dashboard data...')
        
        // Load statistics
        console.log('Fetching stats...')
        const statsResponse = await api.get('/api/v1/vendor-approval/dashboard/stats/')
        console.log('Stats response:', statsResponse.data)
        stats.value = statsResponse.data

        // Load recent requests from database
        console.log('Fetching recent requests...')
        const recentResponse = await api.get('/api/v1/vendor-approval/dashboard/recent-requests/')
        console.log('Recent requests response:', recentResponse.data)
        recentRequests.value = recentResponse.data

        // Load my tasks from database (using current user ID)
        const currentUserId = localStorage.getItem('currentUserId') || 'admin'
        console.log('Fetching tasks for user:', currentUserId)
        const tasksResponse = await api.get(`/api/v1/vendor-approval/dashboard/user-tasks/${currentUserId}/`)
        console.log('Tasks response:', tasksResponse.data)
        myTasks.value = tasksResponse.data

        console.log('Dashboard data loaded successfully!')
        
        // Update last updated timestamp
        lastUpdated.value = new Date().toLocaleTimeString()

      } catch (error) {
        console.error('Error loading dashboard data:', error)
        console.error('Error details:', error.response?.data || error.message)
        // Set empty arrays on error
        recentRequests.value = []
        myTasks.value = []
      } finally {
        loading.value = false
      }
    }

    const viewRequest = (approvalId) => {
      router.push(`/review/${approvalId}`)
    }


    const getStatusBadgeClass = (status) => {
      if (!status) return ''
      
      const statusUpper = String(status).toUpperCase()
      
      // Map to badge.css classes
      if (statusUpper === 'APPROVED') {
        return 'badge-approved'
      }
      if (statusUpper === 'DRAFT') {
        return 'badge-draft'
      }
      if (statusUpper === 'IN_PROGRESS' || statusUpper === 'PENDING') {
        return 'badge-in-review'
      }
      
      // For other statuses (REJECTED, etc.), return empty string (no special styling)
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

    const getWorkflowTypeColor = (type) => {
      const colors = {
        'MULTI_LEVEL': 'primary',
        'MULTI_PERSON': 'success'
      }
      return colors[type] || 'info'
    }

    const formatWorkflowType = (type) => {
      if (!type) return 'Unknown'
      const typeStr = String(type).toUpperCase()
      if (typeStr === 'MULTI_LEVEL') return 'Tiered Approval'
      if (typeStr === 'MULTI_PERSON') return 'Team Approval'
      return type
    }

    const getPriorityClass = (priority) => {
      if (!priority) return 'priority-medium'
      return `priority-${priority.toLowerCase()}`
    }

    const formatDate = (date) => {
      if (!date) return 'Not set'
      return dayjs(date).format('MMM DD, YYYY')
    }

    const isDeadlineNear = (deadlineDate) => {
      if (!deadlineDate) return false
      const deadline = dayjs(deadlineDate)
      const now = dayjs()
      const daysUntilDeadline = deadline.diff(now, 'day')
      return daysUntilDeadline <= 3 && daysUntilDeadline >= 0
    }

    onMounted(async () => {
      await loggingService.logPageView('Vendor', 'Vendor Approval Dashboard (Alt)')
      await loadUsers()
      await loadDashboardData()
    })

    return {
      stats,
      recentRequests,
      myTasks,
      loading,
      lastUpdated,
      users,
      selectedRequestUser,
      selectedTaskUser,
      myTasksCount,
      recentRequestsCount,
      hasRecentRequests,
      hasMyTasks,
      loadDashboardData,
      loadUsers,
      loadUserRequests,
      loadUserTasks,
      viewRequest,
      getStatusBadgeClass,
      formatStatusText,
      getWorkflowTypeColor,
      formatWorkflowType,
      getPriorityClass,
      formatDate,
      isDeadlineNear
    }
  }
}
</script>

<style scoped>
@import '@/assets/components/main.css';
@import '@/assets/components/badge.css';
/* Import KPI Cards from main.css */
@import '@/assets/components/main.css';
@import '@/assets/components/vendor_darktheme.css';

/* Dashboard Container */
.dashboard {
  max-width: 1400px;
  margin: 0 auto;
  padding: 16px 24px 32px 24px;
  min-height: 100vh;
}

.dashboard-title {
  margin: 0 0 12px 0;
  color: #1e293b;
  font-size: 32px;
  font-weight: 700;
  letter-spacing: -0.025em;
  line-height: 1.2;
}

.dashboard-subtitle {
  margin: 0 0 40px 0;
  color: #64748b;
  font-size: 18px;
  font-weight: 400;
  line-height: 1.5;
}

/* Grid System */
.row {
  display: flex;
  flex-wrap: wrap;
  margin: 0 -12px;
  gap: 0;
}

.col-24 {
  flex: 0 0 100%;
  max-width: 100%;
  padding: 0 12px;
}

.col-12 {
  flex: 0 0 50%;
  max-width: 50%;
  padding: 0 12px;
}

.col-6 {
  flex: 0 0 25%;
  max-width: 25%;
  padding: 0 12px;
}

/* Statistics Grid - Now using kpi-cards-grid from main.css */

/* Buttons */
.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.btn:hover::before {
  left: 100%;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
}

.btn-primary {
  background: linear-gradient(135deg, #bfdbfe 0%, #a5b4fc 100%);
  color: #1e3a8a;
  box-shadow: 0 4px 14px 0 rgba(148, 163, 184, 0.3);
}

.btn-primary:hover:not(:disabled) {
  background: linear-gradient(135deg, #cbd5f5 0%, #c7d2fe 100%);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px 0 rgba(148, 163, 184, 0.35);
}

.btn-success {
  background-color: #bbf7d0;
  color: #166534;
}

.btn-success:hover:not(:disabled) {
  background-color: #a7f3ce;
}

.btn-warning {
  background-color: #fde68a;
  color: #b45309;
}

.btn-warning:hover:not(:disabled) {
  background-color: #fcd34d;
}

.btn-info {
  background-color: #e2e8f0;
  color: #475569;
}

.btn-info:hover:not(:disabled) {
  background-color: #cbd5f5;
}

.btn-small {
  padding: 6px 12px;
  font-size: 12px;
}

.btn-large {
  padding: 12px 24px;
  font-size: 16px;
}


/* Activity Cards */
.activity-row {
  margin-bottom: 40px;
}


.activity-card {
  border-radius: 20px;
  background: #ffffff;
  border: 1px solid rgba(226, 232, 240, 0.8);
  box-shadow: 0 14px 32px -16px rgba(148, 163, 184, 0.5);
  height: 520px;
  display: flex;
  flex-direction: column;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.activity-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 28px 46px -24px rgba(148, 163, 184, 0.6);
}

.card-header-with-dropdown {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 24px 0 24px;
  margin-top: 4px;
}

.card-header-with-dropdown h3 {
  margin: 0;
  color: #1e293b;
  font-size: 20px;
  font-weight: 700;
  letter-spacing: -0.025em;
}

.user-select {
  padding: 10px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 500;
  background-color: #fff;
  min-width: 200px;
  transition: all 0.3s ease;
  color: #475569;
}

.user-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.content-container {
  flex: 1;
  padding: 24px;
  overflow: hidden;
}

.no-data {
  padding: 40px 20px;
  text-align: center;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.empty-state {
  color: #909399;
  font-size: 14px;
}

.request-list,
.task-list {
  height: 100%;
  overflow-y: auto;
}

.request-item,
.task-item {
  padding: 20px;
  border: 1px solid #f1f5f9;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border-radius: 12px;
  margin-bottom: 12px;
  background: #ffffff;
  position: relative;
  overflow: hidden;
}

.request-item:hover,
.task-item:hover {
  background-color: #f1f5f9;
  border-color: #cbd5e1;
  transform: translateX(4px);
  box-shadow: 0 4px 12px rgba(148, 163, 184, 0.25);
}

.request-item:last-child,
.task-item:last-child {
  border-bottom: none;
  margin-bottom: 0;
}

.request-header,
.task-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;
}

.request-title,
.task-name {
  font-weight: 700;
  color: #1e293b;
  flex: 1;
  margin-right: 10px;
  font-size: 15px;
  line-height: 1.4;
}

.request-tags,
.task-tags {
  display: flex;
  gap: 5px;
  flex-shrink: 0;
}

.tag {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.tag.info {
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  color: #475569;
  border: 1px solid #cbd5e1;
}

.tag.warning {
  background: linear-gradient(135deg, #fdf4ff 0%, #fde68a 100%);
  color: #b45309;
  border: 1px solid #fcd34d;
}

.tag.primary {
  background: linear-gradient(135deg, #eef2ff 0%, #dbeafe 100%);
  color: #4338ca;
  border: 1px solid #c7d2fe;
}

.tag.success {
  background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
  color: #15803d;
  border: 1px solid #86efac;
}

.tag.danger {
  background: linear-gradient(135deg, #fee2e2 0%, #fbcfe8 100%);
  color: #b91c1c;
  border: 1px solid #fda4af;
}

.request-meta,
.task-meta {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
  font-size: 14px;
  color: #666;
}

.request-details,
.task-details {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  color: #999;
}

.priority-high {
  color: #f87171;
  font-weight: 600;
}

.priority-medium {
  color: #fbbf24;
  font-weight: 600;
}

.priority-low {
  color: #34d399;
  font-weight: 600;
}

.deadline-warning {
  color: #f59e0b;
  font-weight: 600;
}


/* Responsive Design */
@media (max-width: 1400px) {
  .dashboard {
    padding: 28px 20px;
  }
  
}

@media (max-width: 1024px) {
  .dashboard {
    padding: 24px 16px;
  }
  
  .col-6 {
    flex: 0 0 50%;
    max-width: 50%;
  }
}

@media (max-width: 768px) {
  .dashboard {
    padding: 20px 12px;
  }
  
  .dashboard-title {
    font-size: 28px;
  }
  
  .dashboard-subtitle {
    font-size: 16px;
  }
  
  .col-6 {
    flex: 0 0 100%;
    max-width: 100%;
    margin-bottom: 16px;
  }
  
  .col-12 {
    flex: 0 0 100%;
    max-width: 100%;
    margin-bottom: 24px;
  }
  
  .card-header-with-dropdown {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }
  
  .user-select {
    width: 100% !important;
    min-width: auto;
  }
  
  .activity-card {
    height: 480px;
  }
  
  .request-item,
  .task-item {
    padding: 16px;
  }
}

@media (max-width: 480px) {
  .dashboard {
    padding: 16px 8px;
  }
  
  .dashboard-title {
    font-size: 24px;
  }
  
  .dashboard-subtitle {
    font-size: 14px;
    margin-bottom: 24px;
  }
  
}

/* Loading States and Animations */
.loading-skeleton {
  width: 60px;
  height: 28px;
  background: linear-gradient(90deg, #f1f5f9 25%, #e2e8f0 50%, #f1f5f9 75%);
  background-size: 200% 100%;
  animation: loading 1.5s infinite;
  border-radius: 4px;
}

.kpi-card.loading {
  pointer-events: none;
  opacity: 0.7;
}

@keyframes loading {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

/* Fade in animation for content */
.kpi-card {
  animation: fadeInUp 0.6s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Staggered animation for KPI cards */
.kpi-card:nth-child(1) { animation-delay: 0.1s; }
.kpi-card:nth-child(2) { animation-delay: 0.2s; }
.kpi-card:nth-child(3) { animation-delay: 0.3s; }
.kpi-card:nth-child(4) { animation-delay: 0.4s; }
.kpi-card:nth-child(5) { animation-delay: 0.5s; }
.kpi-card:nth-child(6) { animation-delay: 0.6s; }
.kpi-card:nth-child(7) { animation-delay: 0.7s; }
.kpi-card:nth-child(8) { animation-delay: 0.8s; }

.activity-card {
  animation: fadeInUp 0.8s ease-out;
}

.activity-card:nth-child(1) { animation-delay: 0.2s; }
.activity-card:nth-child(2) { animation-delay: 0.4s; }
</style>

<style>
/* Reduce dropdown border radius */
.card-header-with-dropdown .dropdown__button {
  border-radius: 0.25vh !important;
}

.card-header-with-dropdown .dropdown__menu {
  border-radius: 0.25vh !important;
}
</style>