import { ref } from 'vue'

// Theme options
const THEME_OPTIONS = {
  LIGHT: 'light',
  DARK: 'dark'
}

const THEME_LABELS = {
  [THEME_OPTIONS.LIGHT]: 'Light',
  [THEME_OPTIONS.DARK]: 'Dark'
}

const STORAGE_KEY = 'app_theme'

// Global theme state (default to LIGHT)
const theme = ref(THEME_OPTIONS.LIGHT)

// Load theme from localStorage on initialization
const loadTheme = () => {
  if (typeof window === 'undefined') return
  
  const saved = localStorage.getItem(STORAGE_KEY)
  if (saved && (saved === THEME_OPTIONS.LIGHT || saved === THEME_OPTIONS.DARK)) {
    theme.value = saved
  } else {
    theme.value = THEME_OPTIONS.LIGHT
  }
  applyTheme()
}

// Apply theme to document
const applyTheme = () => {
  if (typeof document === 'undefined') return
  
  const html = document.documentElement
  const body = document.body
  
  if (theme.value === THEME_OPTIONS.DARK) {
    html.classList.add('dark-theme')
    body.classList.add('dark-theme')
  } else {
    html.classList.remove('dark-theme')
    body.classList.remove('dark-theme')
  }
}

// Save theme to localStorage
const saveTheme = () => {
  if (typeof window === 'undefined') return
  localStorage.setItem(STORAGE_KEY, theme.value)
}

// Set theme
const setTheme = (newTheme) => {
  if (newTheme !== THEME_OPTIONS.LIGHT && newTheme !== THEME_OPTIONS.DARK) {
    return
  }
  theme.value = newTheme
  applyTheme()
  saveTheme()
}

// Toggle between light and dark
const toggleTheme = () => {
  setTheme(theme.value === THEME_OPTIONS.LIGHT ? THEME_OPTIONS.DARK : THEME_OPTIONS.LIGHT)
}

// Initialize on module load
if (typeof window !== 'undefined') {
  loadTheme()
}

export const useTheme = () => {
  return {
    theme,
    setTheme,
    toggleTheme,
    THEME_OPTIONS,
    THEME_LABELS,
    isDark: () => theme.value === THEME_OPTIONS.DARK,
    isLight: () => theme.value === THEME_OPTIONS.LIGHT
  }
}

