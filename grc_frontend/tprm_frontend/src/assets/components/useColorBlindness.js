import { ref } from 'vue'

// Color blindness options
const COLORBLIND_OPTIONS = {
  OFF: 'off',
  PROTANOPIA: 'protanopia',
  DEUTERANOPIA: 'deuteranopia',
  TRITANOPIA: 'tritanopia'
}

const COLORBLIND_LABELS = {
  [COLORBLIND_OPTIONS.OFF]: 'Off',
  [COLORBLIND_OPTIONS.PROTANOPIA]: 'Protanopia',
  [COLORBLIND_OPTIONS.DEUTERANOPIA]: 'Deuteranopia',
  [COLORBLIND_OPTIONS.TRITANOPIA]: 'Tritanopia'
}

const STORAGE_KEY = 'app_colorblind'

// Global color blindness state (default to OFF)
const colorBlindness = ref(COLORBLIND_OPTIONS.OFF)

// Load color blindness setting from localStorage on initialization
const loadColorBlindness = () => {
  if (typeof window === 'undefined') return
  
  const saved = localStorage.getItem(STORAGE_KEY)
  if (saved && Object.values(COLORBLIND_OPTIONS).includes(saved)) {
    colorBlindness.value = saved
  } else {
    colorBlindness.value = COLORBLIND_OPTIONS.OFF
  }
  applyColorBlindness()
}

// Apply color blindness setting to document
const applyColorBlindness = () => {
  if (typeof document === 'undefined') return
  
  const html = document.documentElement
  const body = document.body
  
  // Remove all color blindness attributes first
  html.removeAttribute('data-colorblind')
  body.removeAttribute('data-colorblind')
  
  // Apply the selected mode (only if not OFF)
  if (colorBlindness.value !== COLORBLIND_OPTIONS.OFF) {
    html.setAttribute('data-colorblind', colorBlindness.value)
    body.setAttribute('data-colorblind', colorBlindness.value)
  }
}

// Save color blindness setting to localStorage
const saveColorBlindness = () => {
  if (typeof window === 'undefined') return
  localStorage.setItem(STORAGE_KEY, colorBlindness.value)
}

// Set color blindness mode
const setColorBlindness = (mode) => {
  if (!Object.values(COLORBLIND_OPTIONS).includes(mode)) {
    return
  }
  colorBlindness.value = mode
  applyColorBlindness()
  saveColorBlindness()
}

// Initialize on module load
if (typeof window !== 'undefined') {
  loadColorBlindness()
}

export const useColorBlindness = () => {
  return {
    colorBlindness,
    setColorBlindness,
    COLORBLIND_OPTIONS,
    COLORBLIND_LABELS,
    isOff: () => colorBlindness.value === COLORBLIND_OPTIONS.OFF,
    isProtanopia: () => colorBlindness.value === COLORBLIND_OPTIONS.PROTANOPIA,
    isDeuteranopia: () => colorBlindness.value === COLORBLIND_OPTIONS.DEUTERANOPIA,
    isTritanopia: () => colorBlindness.value === COLORBLIND_OPTIONS.TRITANOPIA
  }
}
