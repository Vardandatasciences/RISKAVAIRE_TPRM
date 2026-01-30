const stripTrailingSlash = (value) => value.replace(/\/+$/, '')

const resolveEnvOrigin = () => {
  const envCandidates = [
    import.meta.env?.VITE_API_ORIGIN,
    import.meta.env?.VITE_API_BASE_URL,
    import.meta.env?.VITE_API_URL,
    import.meta.env?.VITE_BACKEND_URL,
    import.meta.env?.VUE_APP_API_BASE_URL,
    import.meta.env?.VUE_APP_API_URL
  ].filter(Boolean)

  if (envCandidates.length > 0) {
    return stripTrailingSlash(envCandidates[0])
  }

  if (typeof window !== 'undefined' && window.location) {
    const { protocol, hostname, port } = window.location
    const devPorts = new Set(['3000', '4173', '4174', '5173', '5174'])
    let backendPort = port

    if (!backendPort || devPorts.has(backendPort)) {
      backendPort = '8000'
    }

    const portSegment = backendPort ? `:${backendPort}` : ''
    return `${protocol}//${hostname}${portSegment}`
  }

  return 'http://localhost:8000'
}

const ensureLeadingSlash = (path) => (path.startsWith('/') ? path : `/${path}`)

const API_ORIGIN = stripTrailingSlash(resolveEnvOrigin())
const API_BASE_URL = `${API_ORIGIN}/api`
const API_V1_BASE_URL = `${API_BASE_URL}/v1`

export const getApiOrigin = () => API_ORIGIN
export const getApiBaseUrl = () => API_BASE_URL
export const getApiV1BaseUrl = () => API_V1_BASE_URL

export const getApiUrl = (path = '') => `${API_BASE_URL}${ensureLeadingSlash(path)}`
export const getApiV1Url = (path = '') => `${API_V1_BASE_URL}${ensureLeadingSlash(path)}`

