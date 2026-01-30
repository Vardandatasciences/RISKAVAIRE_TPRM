import authService from '@/services/authService'
import permissionsService from '@/services/permissionsService'
 
const authModule = {
  namespaced: true,
 
  state: {
    currentUser: null,
    isAuthenticated: false,
    sessionToken: null,
    loading: false,
    error: null,
    otpUser: null, // Store user info during OTP flow
    requiresOtp: false
  },
 
  getters: {
    currentUser: state => state.currentUser,
    isAuthenticated: state => state.isAuthenticated,
    sessionToken: state => state.sessionToken,
    isLoading: state => state.loading,
    hasError: state => !!state.error,
    error: state => state.error,
    otpUser: state => state.otpUser,
    requiresOtp: state => state.requiresOtp
  },
 
  mutations: {
    SET_AUTH(state, { user, token }) {
      state.currentUser = user
      state.sessionToken = token
      state.isAuthenticated = true
      state.requiresOtp = false
      state.otpUser = null
      if (token) {
        localStorage.setItem('session_token', token)
        localStorage.setItem('current_user', JSON.stringify(user))
      }
      // Clear permission cache on login to force fresh permission checks
      console.log('[Auth] Clearing permission cache on login')
      permissionsService.clearCache()
    },
   
    SET_OTP_REQUIRED(state, { user, requiresOtp }) {
      state.otpUser = user
      state.requiresOtp = requiresOtp
      state.isAuthenticated = false
    },
   
    CLEAR_AUTH(state) {
      state.currentUser = null
      state.sessionToken = null
      state.isAuthenticated = false
      state.otpUser = null
      state.requiresOtp = false
      localStorage.removeItem('session_token')
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('current_user')
      // Clear permission cache on logout
      console.log('[Auth] Clearing permission cache on logout')
      permissionsService.clearCache()
    },
   
    SET_LOADING(state, loading) {
      state.loading = loading
    },
   
    SET_ERROR(state, error) {
      state.error = error
    },
   
    CLEAR_ERROR(state) {
      state.error = null
    },
   
    SET_USER(state, user) {
      state.currentUser = user
      if (user) {
        localStorage.setItem('current_user', JSON.stringify(user))
      }
    }
  },
 
  actions: {
    /**
     * Step 1: Login with username and password
     * This will trigger OTP to be sent
     */
    async login({ commit }, { username, password }) {
      try {
        commit('SET_LOADING', true)
        commit('CLEAR_ERROR')
       
        console.log('Auth module: Attempting login for user:', username)
       
        const result = await authService.login(username, password)
       
        if (result.success) {
          if (result.requiresOtp) {
            // OTP required, store user info for OTP verification
            commit('SET_OTP_REQUIRED', {
              user: result.user,
              requiresOtp: true
            })
            console.log('Auth module: OTP required, check your email')
            return {
              success: true,
              requiresOtp: true,
              message: result.message,
              user: result.user
            }
          } else {
            // Direct login without OTP (shouldn't happen with MFA)
            commit('SET_AUTH', {
              user: result.user,
              token: result.data.session_token
            })
            return {
              success: true,
              requiresOtp: false,
              user: result.user
            }
          }
        } else {
          commit('SET_ERROR', result.error)
          return {
            success: false,
            error: result.error
          }
        }
      } catch (error) {
        console.error('Auth module: Login error:', error)
        const errorMessage = error.message || 'An unexpected error occurred during login'
        commit('SET_ERROR', errorMessage)
        return {
          success: false,
          error: errorMessage
        }
      } finally {
        commit('SET_LOADING', false)
      }
    },
   
    /**
     * Step 2: Verify OTP code
     */
    async verifyOtp({ commit, state }, otp) {
      try {
        commit('SET_LOADING', true)
        commit('CLEAR_ERROR')
       
        if (!state.otpUser) {
          const error = 'No user found for OTP verification. Please login again.'
          commit('SET_ERROR', error)
          return { success: false, error }
        }
       
        console.log('Auth module: Verifying OTP for user:', state.otpUser.username)
       
        const result = await authService.verifyOtp(state.otpUser.username, otp)
       
        if (result.success) {
          commit('SET_AUTH', {
            user: result.user,
            token: result.token
          })
          console.log('Auth module: OTP verification successful')
          return {
            success: true,
            user: result.user
          }
        } else {
          commit('SET_ERROR', result.error)
          return {
            success: false,
            error: result.error
          }
        }
      } catch (error) {
        console.error('Auth module: OTP verification error:', error)
        const errorMessage = error.message || 'OTP verification failed'
        commit('SET_ERROR', errorMessage)
        return {
          success: false,
          error: errorMessage
        }
      } finally {
        commit('SET_LOADING', false)
      }
    },
   
    /**
     * Resend OTP code
     */
    async resendOtp({ commit, state }) {
      try {
        commit('SET_LOADING', true)
        commit('CLEAR_ERROR')
       
        if (!state.otpUser) {
          const error = 'No user found for OTP resend. Please login again.'
          commit('SET_ERROR', error)
          return { success: false, error }
        }
       
        console.log('Auth module: Resending OTP for user:', state.otpUser.username)
       
        const result = await authService.resendOtp(state.otpUser.username)
       
        if (result.success) {
          return {
            success: true,
            message: result.message
          }
        } else {
          commit('SET_ERROR', result.error)
          return {
            success: false,
            error: result.error
          }
        }
      } catch (error) {
        console.error('Auth module: Resend OTP error:', error)
        const errorMessage = error.message || 'Failed to resend OTP'
        commit('SET_ERROR', errorMessage)
        return {
          success: false,
          error: errorMessage
        }
      } finally {
        commit('SET_LOADING', false)
      }
    },
   
    /**
     * Validate current session
     */
    async validateSession({ commit }) {
      try {
        commit('SET_LOADING', true)
        commit('CLEAR_ERROR')
       
        // Check if we have a token
        if (!authService.isAuthenticated()) {
          commit('CLEAR_AUTH')
          return { success: false, error: 'No authentication found' }
        }
       
        console.log('Auth module: Validating session')
       
        const result = await authService.validateSession()
       
        if (result.success) {
          const token = authService.getSessionToken()
          commit('SET_AUTH', {
            user: result.user,
            token: token
          })
          console.log('Auth module: Session validation successful')
          return {
            success: true,
            user: result.user
          }
        } else {
          commit('CLEAR_AUTH')
          return {
            success: false,
            error: result.error
          }
        }
      } catch (error) {
        console.error('Auth module: Session validation error:', error)
        commit('CLEAR_AUTH')
        return {
          success: false,
          error: error.message || 'Session validation failed'
        }
      } finally {
        commit('SET_LOADING', false)
      }
    },
   
    /**
     * Logout user
     */
    async logoutUser({ commit }) {
      try {
        commit('SET_LOADING', true)
       
        console.log('Auth module: Logging out user')
       
        const result = await authService.logout()
       
        console.log('Auth module: Logout service result:', result)
       
        // Always clear auth state from Vuex
        commit('CLEAR_AUTH')
       
        if (result.success) {
          console.log('Auth module: ✅ Logout successful - session token cleared from database')
          return { success: true, message: result.message }
        } else {
          console.log('Auth module: ⚠️ Logout API failed but local state cleared')
          return { success: false, error: result.error }
        }
      } catch (error) {
        console.error('Auth module: ❌ Logout error:', error)
        // Still clear auth even if API call fails
        commit('CLEAR_AUTH')
        return { success: false, error: error.message }
      } finally {
        commit('SET_LOADING', false)
      }
    },
   
    /**
     * Initialize auth state from localStorage
     * Also checks for GRC authentication when in iframe
     */
    initializeAuth({ commit }) {
      try {
        // First try TPRM's own auth
        let user = authService.getCurrentUser()
        let token = authService.getSessionToken()
       
        // If not found and in iframe, check for GRC auth
        if ((!user || !token) && window.self !== window.top) {
          console.log('[Auth] In iframe - checking for GRC authentication')
          
          // Check for GRC tokens
          const grcToken = localStorage.getItem('access_token') || 
                          localStorage.getItem('session_token') || 
                          localStorage.getItem('token')
          
          // Check for GRC user (try multiple keys)
          let grcUser = null
          const userKeys = ['current_user', 'user', 'currentUser']
          for (const key of userKeys) {
            const userStr = localStorage.getItem(key)
            if (userStr) {
              try {
                grcUser = typeof userStr === 'string' ? JSON.parse(userStr) : userStr
                if (grcUser && (grcUser.id || grcUser.userid || grcUser.username)) {
                  break
                }
              } catch (e) {
                console.warn(`[Auth] Could not parse user from ${key}:`, e)
              }
            }
          }
          
          if (grcToken && grcUser) {
            console.log('[Auth] Found GRC authentication, syncing to TPRM')
            // Sync GRC auth to TPRM keys
            if (!localStorage.getItem('session_token')) {
              localStorage.setItem('session_token', grcToken)
            }
            if (!localStorage.getItem('current_user')) {
              localStorage.setItem('current_user', JSON.stringify(grcUser))
            }
            user = grcUser
            token = grcToken
          }
        }
       
        if (user && token) {
          // Ensure user has id or userid for permissions service
          if (!user.id && !user.userid) {
            console.warn('[Auth] User object missing id/userid, attempting to extract from user object:', user)
            // Try to find id in nested structure
            if (user.user && (user.user.id || user.user.userid)) {
              user.id = user.user.id || user.user.userid
            } else if (user.user_id) {
              user.id = user.user_id
            } else if (user.userid) {
              user.id = user.userid
            }
          }
          
          commit('SET_AUTH', { user, token })
          console.log('Auth module: Initialized with stored user:', user.username || user.email || 'Unknown', {
            hasId: !!(user.id || user.userid),
            userId: user.id || user.userid
          })
        } else {
          commit('CLEAR_AUTH')
          console.log('Auth module: No stored authentication found')
        }
      } catch (error) {
        console.error('Auth module: Initialize error:', error)
        commit('CLEAR_AUTH')
      }
    },
   
    /**
     * Clear error message
     */
    clearError({ commit }) {
      commit('CLEAR_ERROR')
    }
  }
}
 
export default authModule