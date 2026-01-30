<template>
  <div class="tprm-wrapper">
    <div v-if="!hasBaseUrl" class="tprm-wrapper__message">
      <p>
        <strong>VUE_APP_TPRM_BASE_URL</strong> is not configured. Set it in your
        <code>.env</code> file to embed the TPRM application.
      </p>
    </div>
    <div v-else-if="connectionError" class="tprm-wrapper__message tprm-wrapper__error">
      <div class="error-icon">⚠️</div>
      <h3>TPRM Server Connection Error</h3>
      <p>
        Unable to connect to the TPRM server at <code>{{ BASE_URL }}</code>
      </p>
      <div v-if="isDevelopment" class="error-instructions">
        <p><strong>To fix this issue:</strong></p>
        <ol>
          <li>Open a new terminal window</li>
          <li>Navigate to the TPRM frontend directory:
            <code>cd grc_frontend/tprm_frontend</code>
          </li>
          <li>Start the TPRM development server:
            <code>npm run dev</code>
          </li>
          <li>Wait for the server to start (usually runs on <code>http://localhost:3000</code>)</li>
          <li>Refresh this page</li>
        </ol>
      </div>
      <div v-else class="error-instructions">
        <p><strong>This appears to be a production environment.</strong></p>
        <p>Please contact your system administrator if this issue persists.</p>
      </div>
    </div>
    <div v-else class="tprm-wrapper__frame">
      <iframe
        ref="tprmIframe"
        :src="iframeSrc"
        :key="iframeKey"
        title="TPRM Module"
        frameborder="0"
        referrerpolicy="no-referrer"
        sandbox="allow-same-origin allow-scripts allow-forms allow-popups allow-modals allow-downloads allow-popups-to-escape-sandbox"
        @load="onIframeLoad"
        @error="onIframeError"
      />
    </div>
  </div>
</template>

<script>
import { computed, ref, watch, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

// Get TPRM base URL from env or use fallback based on current location
const getTprmBaseUrl = () => {
  // Debug logging to see what's happening
  const debugInfo = {
    hasEnvVar: !!process.env.VUE_APP_TPRM_BASE_URL,
    envVarValue: process.env.VUE_APP_TPRM_BASE_URL,
    nodeEnv: process.env.NODE_ENV,
    hostname: typeof window !== 'undefined' ? window.location?.hostname : 'unknown',
    href: typeof window !== 'undefined' ? window.location?.href : 'unknown'
  }
  
  // Check if we're on production domain FIRST
  const isProductionDomain = typeof window !== 'undefined' && window.location && 
    (window.location.hostname.includes('vardaands.com') || 
     window.location.hostname.includes('grc-tprm') ||
     window.location.href.includes('vardaands.com'))
  
  // First, check Vue CLI-style environment variable (highest priority)
  // BUT: Ignore localhost values if we're on production domain
  if (process.env.VUE_APP_TPRM_BASE_URL) {
    const envUrl = process.env.VUE_APP_TPRM_BASE_URL
    
    // CRITICAL: If env var is localhost but we're on production domain, IGNORE IT
    if (isProductionDomain && (envUrl.includes('localhost') || envUrl.includes('127.0.0.1'))) {
      console.warn('[TprmWrapper] ⚠️ VUE_APP_TPRM_BASE_URL is set to localhost but running on production domain!')
      console.warn('[TprmWrapper] Ignoring env var and using production URL instead')
      console.warn('[TprmWrapper] Fix: Remove or update VUE_APP_TPRM_BASE_URL in your .env file')
      // Fall through to use production URL
    } else {
      console.log('[TprmWrapper] Using VUE_APP_TPRM_BASE_URL:', envUrl, debugInfo)
      return envUrl
    }
  }

  // CRITICAL: TPRM should be served from the same origin as GRC at /tprm subdirectory
  // This prevents CORS issues and ensures proper routing
  if (typeof window !== 'undefined' && window.location) {
    const origin = window.location.origin
    const hostname = window.location.hostname
    
    // Production: use same origin with /tprm prefix
    if (hostname.includes('vardaands.com') || hostname.includes('grc-tprm')) {
      const tprmBaseUrl = `${origin}/tprm`
      console.log('[TprmWrapper] Production domain detected, using same origin with /tprm:', tprmBaseUrl, debugInfo)
      return tprmBaseUrl
    }
    
    // Development: use localhost:3000 (TPRM dev server)
    if ((hostname === 'localhost' || hostname === '127.0.0.1') && 
        process.env.NODE_ENV === 'development') {
      console.log('[TprmWrapper] Development mode on localhost, using localhost:3000', debugInfo)
      return `http://${hostname}:3000`
    }
    
    // Any other domain: use same origin with /tprm prefix
    const tprmBaseUrl = `${origin}/tprm`
    console.log('[TprmWrapper] Using same origin with /tprm prefix:', tprmBaseUrl, debugInfo)
    return tprmBaseUrl
  }

  // Fallback: use same origin with /tprm
  if (typeof window !== 'undefined' && window.location) {
    return `${window.location.origin}/tprm`
  }
  
  console.log('[TprmWrapper] Using default fallback /tprm', debugInfo)
  return '/tprm'
}

// Don't call at module level - call in setup() for runtime evaluation
// const BASE_URL = getTprmBaseUrl() // REMOVED - will be computed in setup()

export default {
  name: 'TprmWrapper',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const tprmIframe = ref(null)
    const connectionError = ref(false)
    const isDevelopment = ref(process.env.NODE_ENV === 'development')
    
    // Call at runtime, not module load time
    const BASE_URL = getTprmBaseUrl()

    const normalizedPath = computed(() => {
      const param = route.params.tprmPath

      let pathValue = ''
      if (Array.isArray(param)) {
        pathValue = param.join('/')
      } else if (typeof param === 'string') {
        pathValue = param
      }

      // If no path value, default to '/' (home page)
      // But ensure it's a valid path for the TPRM app
      const cleanPath = pathValue ? `/${pathValue}` : '/'
      
      // Remove any leading/trailing slashes and ensure single leading slash
      let normalized = cleanPath.replace(/^\/+|\/+$/g, '')
      normalized = normalized ? `/${normalized}` : '/'
      
      const query = route.query
      const queryString = new URLSearchParams(query).toString()

      const finalPath = queryString ? `${normalized}?${queryString}` : normalized
      
      // Debug logging
      console.log('[TprmWrapper] Normalized path:', {
        routePath: route.path,
        param,
        pathValue,
        cleanPath,
        normalized,
        finalPath
      })
      
      return finalPath
    })

    // Track the last path we navigated to, to prevent duplicate navigations
    const lastNavigatedPath = ref(null)
    
    // Track if iframe has been loaded at least once
    const iframeLoaded = ref(false)
    
    // Store the path that was used when iframe first loaded
    // This helps us know if we need to reload the iframe for a different route
    const initialPath = ref(normalizedPath.value)
    
    const iframeSrc = computed(() => {
      if (!BASE_URL) return ''
      const base = BASE_URL.endsWith('/') ? BASE_URL.slice(0, -1) : BASE_URL
      // Always use the current normalized path for the iframe src
      // This ensures the iframe loads with the correct route initially
      // After it loads, we'll navigate via postMessage for subsequent route changes
      return `${base}${normalizedPath.value}`
    })
    
    // Use a key that changes when route changes before iframe loads
    // This ensures the iframe loads with the correct route
    // After iframe loads, we navigate via postMessage instead of reloading
    const iframeKey = computed(() => {
      // If iframe hasn't loaded yet, include the path in the key so it loads with correct route
      // If iframe has loaded, keep key stable to prevent unnecessary reloads
      if (!iframeLoaded.value) {
        return BASE_URL ? `${BASE_URL}-${normalizedPath.value}` : `default-${normalizedPath.value}`
      }
      // After iframe loads, keep key stable (only change if base URL changes)
      return BASE_URL ? BASE_URL : 'default'
    })

    // Get auth data from GRC localStorage
    const getAuthData = () => {
      const token = localStorage.getItem('access_token') || 
                    localStorage.getItem('session_token') || 
                    localStorage.getItem('token')
      const user = localStorage.getItem('user') || localStorage.getItem('current_user')
      const refreshToken = localStorage.getItem('refresh_token')
      
      return {
        type: 'GRC_AUTH_SYNC',
        token,
        refreshToken,
        user: user ? JSON.parse(user) : null,
        isAuthenticated: localStorage.getItem('isAuthenticated') === 'true' || 
                         localStorage.getItem('is_logged_in') === 'true'
      }
    }

    // Send auth data to TPRM iframe
    const sendAuthToIframe = () => {
      if (tprmIframe.value && tprmIframe.value.contentWindow) {
        const authData = getAuthData()
        console.log('[TprmWrapper] Sending auth data to TPRM iframe:', { 
          hasToken: !!authData.token, 
          hasUser: !!authData.user,
          isAuthenticated: authData.isAuthenticated 
        })
        tprmIframe.value.contentWindow.postMessage(authData, '*')
      }
    }

    const onIframeLoad = () => {
      console.log('[TprmWrapper] ✅ TPRM iframe load event fired - iframe loaded successfully!')
      console.log('[TprmWrapper] Iframe src:', iframeSrc.value)
      console.log('[TprmWrapper] Current route path:', route.path)
      console.log('[TprmWrapper] Normalized path:', normalizedPath.value)
      
      // Clear any connection errors - iframe loaded successfully
      connectionError.value = false
      
      // Mark iframe as loaded - this allows navigation via postMessage for subsequent route changes
      iframeLoaded.value = true
      // Store the current path as the initial path
      initialPath.value = normalizedPath.value
      lastNavigatedPath.value = normalizedPath.value
      
      // Small delay to ensure iframe is ready to receive messages
      setTimeout(() => {
        sendAuthToIframe()
        
        // The iframe should already be at the correct route from the URL in the src
        // The TPRM router will read it from window.location.pathname
        // No need to navigate again - it's already at the right route
        
        // Request current route from iframe to confirm it's at the right place
        if (tprmIframe.value && tprmIframe.value.contentWindow) {
          tprmIframe.value.contentWindow.postMessage({ type: 'GET_CURRENT_ROUTE' }, '*')
        }
        
        // Retry auth after 1 second in case first attempt failed
        setTimeout(sendAuthToIframe, 1000)
      }, 100)
    }
    
    // Watch for route changes and navigate iframe without reloading
    // CRITICAL: Only navigate via postMessage if iframe is already loaded
    // This prevents reloading the iframe on every route change
    watch(() => normalizedPath.value, (newPath, oldPath) => {
      // Only navigate if:
      // 1. Path actually changed
      // 2. Iframe is loaded (not initial load)
      // 3. Path is different from last navigated path
      // 4. Iframe ref exists
      if (iframeLoaded.value && 
          newPath !== oldPath && 
          tprmIframe.value && 
          tprmIframe.value.contentWindow && 
          newPath !== lastNavigatedPath.value) {
        console.log('[TprmWrapper] Route changed, navigating iframe via postMessage (no reload):', {
          oldPath,
          newPath,
          lastNavigated: lastNavigatedPath.value
        })
        tprmIframe.value.contentWindow.postMessage({ 
          type: 'NAVIGATE_TO_ROUTE', 
          path: newPath 
        }, '*')
        lastNavigatedPath.value = newPath
        // Update initialPath to reflect the new route
        initialPath.value = newPath
      } else if (!iframeLoaded.value) {
        // If iframe hasn't loaded yet, update initialPath so it loads with the correct route
        console.log('[TprmWrapper] Route changed before iframe loaded, updating initial path:', newPath)
        initialPath.value = newPath
      }
    })
    
    // Handle iframe errors
    // NOTE: The @error event may not fire reliably for cross-origin iframes
    // We rely more on the @load event and timeout checks
    const onIframeError = (error) => {
      console.error('[TprmWrapper] ❌ Iframe error event fired:', error)
      console.error('[TprmWrapper] Failed to load TPRM from:', iframeSrc.value)
      console.error('[TprmWrapper] Check that VUE_APP_TPRM_BASE_URL is configured correctly')
      
      // Only set connection error if we're sure it failed
      // The @error event is more reliable than trying to access iframe content
      connectionError.value = true
      
      // In development, try to detect if server is running
      if (isDevelopment.value && BASE_URL.includes('localhost')) {
        console.warn('[TprmWrapper] Development mode detected. Make sure TPRM dev server is running:')
        console.warn('[TprmWrapper] Run: cd grc_frontend/tprm_frontend && npm run dev')
        console.warn('[TprmWrapper] Server should be running on http://localhost:3000')
      }
    }
    
    // Check if iframe loaded successfully after a timeout
    // NOTE: We can't access iframe content due to cross-origin restrictions,
    // so we rely on the @load event and messages from the iframe
    const checkIframeLoad = () => {
      // Set a longer timeout (10 seconds) to account for slow connections
      setTimeout(() => {
        // Only show error if iframe hasn't loaded AND we haven't received any messages
        // The @load event should fire when iframe loads, even with cross-origin restrictions
        if (tprmIframe.value && !iframeLoaded.value) {
          // Check if iframe src is still about:blank (means it never started loading)
          // But we can't check this due to CORS, so we'll rely on the load event
          // If load event didn't fire after 10 seconds, it's likely a connection issue
          console.warn('[TprmWrapper] Iframe load timeout - iframe may not have loaded')
          console.warn('[TprmWrapper] This could be due to:')
          console.warn('[TprmWrapper] 1. Server not running')
          console.warn('[TprmWrapper] 2. Network issues')
          console.warn('[TprmWrapper] 3. CORS blocking (check browser console)')
          // Don't set connectionError here - let the @error event handle it
          // The @load event should fire even with CORS, so if it didn't, there's a real issue
        }
      }, 10000) // Increased to 10 seconds
    }

    // Listen for messages from TPRM iframe (auth requests and navigation)
    const handleMessage = (event) => {
      // Verify origin if BASE_URL is configured
      if (BASE_URL) {
        const baseOrigin = new URL(BASE_URL).origin
        if (event.origin !== baseOrigin && event.origin !== window.location.origin) {
          return
        }
      }

      if (event.data && event.data.type === 'TPRM_AUTH_REQUEST') {
        console.log('[TprmWrapper] Received auth request from TPRM')
        // Clear connection error if we receive messages from iframe (means it loaded)
        connectionError.value = false
        iframeLoaded.value = true
        sendAuthToIframe()
      }
      
      // Handle iframe ready message (confirms iframe loaded successfully)
      if (event.data && event.data.type === 'TPRM_IFRAME_READY') {
        console.log('[TprmWrapper] ✅ Received iframe ready message from TPRM')
        connectionError.value = false
        iframeLoaded.value = true
      }
      
      // Handle redirect request from TPRM iframe (when authentication is required)
      if (event.data && event.data.type === 'TPRM_REDIRECT_TO_LOGIN') {
        console.log('[TprmWrapper] Received redirect to login request from TPRM iframe')
        // Redirect parent window to GRC login
        window.location.href = '/login'
      }
      
      // Helper function to normalize TPRM path and convert to parent route
      const normalizeTprmPath = (tprmPath) => {
        if (!tprmPath) return '/tprm'
        
        // Remove /tprm/ prefix if present (defensive - shouldn't happen but prevents loops)
        let normalized = tprmPath.replace(/^\/tprm\/?/, '/')
        
        // Ensure it starts with /
        if (!normalized.startsWith('/')) {
          normalized = '/' + normalized
        }
        
        // Convert to parent route format
        return normalized === '/' ? '/tprm' : `/tprm${normalized}`
      }
      
      // Handle navigation sync from TPRM iframe
      if (event.data && event.data.type === 'TPRM_NAVIGATION') {
        const tprmPath = event.data.path || ''
        const newPath = normalizeTprmPath(tprmPath)
        console.log('[TprmWrapper] Received navigation from TPRM iframe:', tprmPath, '-> Updating parent route to:', newPath)
        
        // Update parent router using replace to avoid adding to history stack
        // This prevents navigation loops and multiple page loads
        // Only update if the path is actually different
        if (route.path !== newPath && !route.path.startsWith(newPath + '/')) {
          router.replace(newPath).catch(err => {
            // Ignore navigation errors (e.g., if already on that route)
            if (err.name !== 'NavigationDuplicated' && !err.message?.includes('already being navigated')) {
              console.warn('[TprmWrapper] Navigation error:', err)
            }
          })
        }
      }
      
      // Handle route request from iframe (when iframe loads)
      if (event.data && event.data.type === 'CURRENT_ROUTE') {
        const tprmPath = event.data.path || ''
        const newPath = normalizeTprmPath(tprmPath)
        console.log('[TprmWrapper] Received current route from TPRM iframe:', tprmPath, '-> Syncing parent route to:', newPath)
        
        // Only update if we're not already on the correct route
        // Use replace to avoid adding to history stack
        // Check if current path matches or is a sub-path of the target
        if (route.path !== newPath && !route.path.startsWith(newPath + '/')) {
          router.replace(newPath).catch(err => {
            // Ignore navigation duplicates and already-matched routes
            if (err.name !== 'NavigationDuplicated' && !err.message?.includes('already being navigated')) {
              console.warn('[TprmWrapper] Route sync error:', err)
            }
          })
        }
      }
    }

    // Set up message listener and log configuration on mount
    onMounted(() => {
      window.addEventListener('message', handleMessage)
      console.log('[TprmWrapper] ========== DEBUG INFO ==========')
      console.log('[TprmWrapper] BASE_URL:', BASE_URL)
      console.log('[TprmWrapper] NODE_ENV:', process.env.NODE_ENV)
      console.log('[TprmWrapper] VUE_APP_TPRM_BASE_URL:', process.env.VUE_APP_TPRM_BASE_URL)
      console.log('[TprmWrapper] window.location.hostname:', window.location?.hostname)
      console.log('[TprmWrapper] window.location.href:', window.location?.href)
      console.log('[TprmWrapper] Current route:', route.path)
      console.log('[TprmWrapper] Iframe will load:', iframeSrc.value)
      console.log('[TprmWrapper] =================================')
      if (!BASE_URL) {
        console.warn('[TprmWrapper] WARNING: VUE_APP_TPRM_BASE_URL is not configured!')
        console.warn('[TprmWrapper] TPRM pages will not load. Set VUE_APP_TPRM_BASE_URL in .env file')
      }
      // Only warn about localhost in production, not in development
      if (BASE_URL.includes('localhost') && process.env.NODE_ENV === 'production') {
        console.error('[TprmWrapper] ⚠️⚠️⚠️ ERROR: Using localhost URL in production!')
        console.error('[TprmWrapper] This will cause CORS errors. Check environment variables.')
      } else if (BASE_URL.includes('localhost') && process.env.NODE_ENV === 'development') {
        console.log('[TprmWrapper] ✓ Using localhost URL in development mode (expected)')
        console.log('[TprmWrapper] Make sure TPRM dev server is running: cd grc_frontend/tprm_frontend && npm run dev')
      }
      
      // Check iframe load status after mount
      checkIframeLoad()
    })

    onUnmounted(() => {
      window.removeEventListener('message', handleMessage)
    })

    return {
      tprmIframe,
      iframeSrc,
      iframeKey,
      BASE_URL,
      hasBaseUrl: computed(() => Boolean(BASE_URL)),
      connectionError,
      isDevelopment,
      onIframeLoad,
      onIframeError
    }
  }
}
</script>

<style scoped>
.tprm-wrapper {
  width: 100%;
  height: calc(100vh - 80px);
  display: flex;
  flex-direction: column;
  background: #f5f6fb;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid #e3e7f0;
}

.tprm-wrapper__frame {
  flex: 1;
  position: relative;
}

.tprm-wrapper__frame iframe {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  border: 0;
  background: white;
}

.tprm-wrapper__message {
  padding: 32px;
  text-align: center;
  color: #0f172a;
}

.tprm-wrapper__message code {
  background: #e2e8f0;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
}

.tprm-wrapper__error {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 48px 32px;
  text-align: center;
}

.tprm-wrapper__error .error-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.tprm-wrapper__error h3 {
  margin: 0 0 16px 0;
  color: #dc2626;
  font-size: 24px;
  font-weight: 600;
}

.tprm-wrapper__error p {
  margin: 8px 0;
  color: #64748b;
  font-size: 16px;
}

.tprm-wrapper__error .error-instructions {
  margin-top: 24px;
  padding: 24px;
  background: #f8fafc;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  text-align: left;
  max-width: 600px;
}

.tprm-wrapper__error .error-instructions p {
  margin: 8px 0;
  color: #334155;
}

.tprm-wrapper__error .error-instructions ol {
  margin: 16px 0;
  padding-left: 24px;
}

.tprm-wrapper__error .error-instructions li {
  margin: 12px 0;
  color: #475569;
  line-height: 1.6;
}

.tprm-wrapper__error .error-instructions code {
  background: #e2e8f0;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
  color: #1e293b;
}
</style>

