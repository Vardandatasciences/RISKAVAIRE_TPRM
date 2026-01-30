<template>
  <div class="min-h-screen bg-background">
    <!-- Standalone routes (no layout) -->
    <RouterView v-if="isStandaloneRoute" />
    
    <!-- Routes with layout -->
    <AppLayout v-else>
      <RouterView />
    </AppLayout>
    
    <!-- Global Popup Modal -->
    <PopupModal />
  </div>
</template>

<script setup>
import { RouterView, useRoute, useRouter } from 'vue-router'
import AppLayout from './components/layout/AppLayout.vue'
import PopupModal from './popup/PopupModal.vue'
import { computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useTheme } from './assets/components/useTheme.js'
import { useColorBlindness } from './assets/components/useColorBlindness.js'

const route = useRoute()
const router = useRouter()
const store = useStore()

// Initialize theme on app load
const { theme } = useTheme()

// Initialize color blindness on app load
const { colorBlindness } = useColorBlindness()

// Define standalone routes that should not have layout
const standaloneRoutes = [
  'VendorPortal',
  'VendorPortalSubmit', 
  'VendorPortalOpen',
  'TestVendorPortal',
  'VendorPortalDirect',
  'AwardResponse',
  'Login',
  'OtpVerification'  // Auth pages should be standalone
]

const isStandaloneRoute = computed(() => {
  return standaloneRoutes.includes(route.name)
})

onMounted(() => {
  console.log('=== TPRM App Mounted ===')
  console.log('Environment:', import.meta.env.MODE)
  console.log('API Base URL:', import.meta.env.VITE_API_BASE_URL)
  
  // Initialize theme (this ensures theme is applied on app load)
  // The useTheme composable already loads from localStorage, but we call it here to ensure it's active
  useTheme()
  
  // Initialize color blindness (this ensures color blindness is applied on app load)
  // The useColorBlindness composable already loads from localStorage, but we call it here to ensure it's active
  useColorBlindness()
  
  // Listen for GRC authentication from parent window (when embedded in iframe)
  const handleGrcAuth = (event) => {
    // Accept messages from parent window or same origin
    if (event.data && event.data.type === 'GRC_AUTH_SYNC') {
      console.log('[TPRM] Received GRC authentication from parent window')
      const { token, refreshToken, user, isAuthenticated } = event.data
      
      if (token) {
        localStorage.setItem('session_token', token)
        localStorage.setItem('access_token', token)
        if (refreshToken) {
          localStorage.setItem('refresh_token', refreshToken)
        }
      }
      
      if (user) {
        // Ensure user has id or userid for permissions service
        let processedUser = user
        if (!processedUser.id && !processedUser.userid) {
          // Try to extract id from nested structure
          if (processedUser.user && (processedUser.user.id || processedUser.user.userid)) {
            processedUser.id = processedUser.user.id || processedUser.user.userid
          } else if (processedUser.user_id) {
            processedUser.id = processedUser.user_id
          } else if (processedUser.userid) {
            processedUser.id = processedUser.userid
          }
        }
        
        localStorage.setItem('current_user', JSON.stringify(processedUser))
        localStorage.setItem('user', JSON.stringify(processedUser)) // Also store as 'user' for compatibility
      }
      
      if (isAuthenticated) {
        localStorage.setItem('isAuthenticated', 'true')
        localStorage.setItem('is_logged_in', 'true')
      }
      
      // Commit directly to store for immediate effect
      if (user && token) {
        store.commit('auth/SET_AUTH', { user: user, token: token })
        console.log('[TPRM] GRC authentication committed to store:', {
          username: user.username || user.email || 'Unknown',
          hasId: !!(user.id || user.userid),
          userId: user.id || user.userid
        })
      } else {
        // Re-initialize auth state
        store.dispatch('auth/initializeAuth')
      }
      console.log('[TPRM] GRC authentication synced successfully')
    }
  }
  
  // Request auth from parent if in iframe
  const isInIframe = window.self !== window.top
  if (isInIframe) {
    console.log('[TPRM] Running in iframe - requesting auth from parent window')
    window.addEventListener('message', handleGrcAuth)
    
    // Handle navigation messages from parent window
    const handleNavigation = (event) => {
      // Accept messages from parent window
      if (event.data && event.data.type === 'NAVIGATE_TO_ROUTE') {
        const targetPath = event.data.path
        if (targetPath && targetPath !== route.path) {
          console.log('[TPRM] Received navigation request from parent:', targetPath)
          // Use router to navigate without reloading
          router.push(targetPath).catch(err => {
            // Ignore navigation duplicates
            if (err.name !== 'NavigationDuplicated') {
              console.error('[TPRM] Navigation error:', err)
            }
          })
        }
      }
      
      // Handle route request from parent
      if (event.data && event.data.type === 'GET_CURRENT_ROUTE') {
        console.log('[TPRM] Sending current route to parent:', route.path)
        if (window.parent) {
          window.parent.postMessage({ 
            type: 'CURRENT_ROUTE', 
            path: route.path 
          }, '*')
        }
      }
    }
    
    // Add navigation message listener
    window.addEventListener('message', handleNavigation)
    
    // Send ready message to parent to confirm iframe loaded
    if (window.parent) {
      window.parent.postMessage({ type: 'TPRM_IFRAME_READY' }, '*')
      console.log('[TPRM] ✅ Sent iframe ready message to parent')
      
      // Request auth from parent
      window.parent.postMessage({ type: 'TPRM_AUTH_REQUEST' }, '*')
    }
    
    // Also check for existing GRC auth in localStorage (shared storage)
    const grcToken = localStorage.getItem('access_token') || localStorage.getItem('session_token')
    const grcUser = localStorage.getItem('user') || localStorage.getItem('current_user')
    if (grcToken && grcUser) {
      console.log('[TPRM] Found existing GRC authentication in localStorage')
      if (!localStorage.getItem('session_token')) {
        localStorage.setItem('session_token', grcToken)
      }
      if (!localStorage.getItem('current_user')) {
        try {
          const parsedUser = typeof grcUser === 'string' ? JSON.parse(grcUser) : grcUser
          localStorage.setItem('current_user', JSON.stringify(parsedUser))
        } catch (e) {
          localStorage.setItem('current_user', grcUser)
        }
      }
    }
  }
  
  // Initialize authentication state from localStorage
  store.dispatch('auth/initializeAuth')
  console.log('Auth initialized')
})
</script>

<style>
/* Global styles for standalone vendor portal */
.vendor-portal-standalone {
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
  right: 0 !important;
  bottom: 0 !important;
  width: 100vw !important;
  height: 100vh !important;
  z-index: 99999 !important;
  overflow-y: auto !important;
  overflow-x: hidden !important;
  background-color: #f9fafb !important;
  margin: 0 !important;
  padding: 0 !important;
}

/* Hide any external layout elements when on standalone routes */
body.standalone-route aside,
body.standalone-route .sidebar,
body.standalone-route .app-sidebar,
body.standalone-route header,
body.standalone-route .header,
body.standalone-route .app-header,
body.standalone-route nav:not(.vendor-portal nav),
body.standalone-route .navigation:not(.vendor-portal .navigation),
body.standalone-route .app-navigation:not(.vendor-portal .app-navigation),
body.standalone-route .app-layout:not(.vendor-portal .app-layout),
body.standalone-route .main-content:not(.vendor-portal .main-content) {
  display: none !important;
  visibility: hidden !important;
}

/* Ensure body and html are clean for standalone routes */
body.standalone-route {
  margin: 0 !important;
  padding: 0 !important;
  overflow-y: auto !important;
  overflow-x: hidden !important;
}

html.standalone-route {
  margin: 0 !important;
  padding: 0 !important;
}
</style>
