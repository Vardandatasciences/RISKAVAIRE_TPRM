<template>
  <div class="colorblind-toggle-container">
    <div class="colorblind-toggle-wrapper">
      <span class="colorblind-toggle-label">Mode</span>
      <div class="colorblind-toggle-buttons">
        <button
          @click="setOff"
          :class="['colorblind-button', { 'colorblind-button-active': isOff() }]"
          :title="'Off - No color blindness filter'"
        >
          <span class="colorblind-button-text">Off</span>
        </button>
        <button
          @click="setProtanopia"
          :class="['colorblind-button', { 'colorblind-button-active': isProtanopia() }]"
          :title="'Protanopia - Red-blindness'"
        >
          <span class="colorblind-button-text">Protanopia</span>
        </button>
        <button
          @click="setDeuteranopia"
          :class="['colorblind-button', { 'colorblind-button-active': isDeuteranopia() }]"
          :title="'Deuteranopia - Green-blindness'"
        >
          <span class="colorblind-button-text">Deuteranopia</span>
        </button>
        <button
          @click="setTritanopia"
          :class="['colorblind-button', { 'colorblind-button-active': isTritanopia() }]"
          :title="'Tritanopia - Blue-yellow blindness'"
        >
          <span class="colorblind-button-text">Tritanopia</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useColorBlindness } from './useColorBlindness.js'
import './colourblindness.css'

const { 
  colorBlindness, 
  setColorBlindness, 
  COLORBLIND_OPTIONS,
  isOff,
  isProtanopia,
  isDeuteranopia,
  isTritanopia
} = useColorBlindness()

const setOff = () => {
  setColorBlindness(COLORBLIND_OPTIONS.OFF)
}

const setProtanopia = () => {
  setColorBlindness(COLORBLIND_OPTIONS.PROTANOPIA)
}

const setDeuteranopia = () => {
  setColorBlindness(COLORBLIND_OPTIONS.DEUTERANOPIA)
}

const setTritanopia = () => {
  setColorBlindness(COLORBLIND_OPTIONS.TRITANOPIA)
}
</script>

<style scoped>
.colorblind-toggle-container {
  display: inline-flex;
  align-items: center;
  user-select: none;
}

.colorblind-toggle-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;
}

.colorblind-toggle-label {
  font-size: 12px;
  font-weight: 500;
  color: #6b7280;
  white-space: nowrap;
}

.colorblind-toggle-buttons {
  display: flex;
  gap: 8px;
  background: #f3f4f6;
  border-radius: 8px;
  padding: 4px;
  flex-wrap: wrap;
}

.colorblind-button {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border: none;
  border-radius: 6px;
  background: transparent;
  color: #6b7280;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.colorblind-button:hover {
  background: rgba(0, 0, 0, 0.05);
  color: #374151;
}

.colorblind-button-active {
  background: #ffffff;
  color: #111827;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.colorblind-button-text {
  white-space: nowrap;
}

/* Dark theme styles for the toggle itself */
:global(.dark-theme) .colorblind-toggle-label {
  color: #9ca3af;
}

:global(.dark-theme) .colorblind-toggle-buttons {
  background: #374151;
}

:global(.dark-theme) .colorblind-button {
  color: #9ca3af;
}

:global(.dark-theme) .colorblind-button:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #e5e7eb;
}

:global(.dark-theme) .colorblind-button-active {
  background: #1f2937;
  color: #ffffff;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}
</style>
