<template>
  <div class="theme-toggle-container">
    <div class="theme-toggle-wrapper">
      <span class="theme-toggle-label">Theme</span>
      <div class="theme-toggle-buttons">
        <button
          @click="setLightTheme"
          :class="['theme-button', { 'theme-button-active': !isDark }]"
          :title="'Light Theme'"
        >
          <Sun class="theme-icon" />
          <span class="theme-button-text">Light</span>
        </button>
        <button
          @click="setDarkTheme"
          :class="['theme-button', { 'theme-button-active': isDark }]"
          :title="'Dark Theme'"
        >
          <Moon class="theme-icon" />
          <span class="theme-button-text">Dark</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Sun, Moon } from 'lucide-vue-next'
import { useTheme } from './useTheme.js'
import './darktheme.css'

const { theme, setTheme, isDark } = useTheme()

const setLightTheme = () => {
  setTheme('light')
}

const setDarkTheme = () => {
  setTheme('dark')
}
</script>

<style scoped>
.theme-toggle-container {
  display: inline-flex;
  align-items: center;
  user-select: none;
}

.theme-toggle-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;
}

.theme-toggle-label {
  font-size: 12px;
  font-weight: 500;
  color: #6b7280;
  white-space: nowrap;
}

.theme-toggle-buttons {
  display: flex;
  gap: 8px;
  background: #f3f4f6;
  border-radius: 8px;
  padding: 4px;
}

.theme-button {
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
}

.theme-button:hover {
  background: rgba(0, 0, 0, 0.05);
  color: #374151;
}

.theme-button-active {
  background: #ffffff;
  color: #111827;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.theme-icon {
  width: 16px;
  height: 16px;
}

.theme-button-text {
  white-space: nowrap;
}

/* Dark theme styles for the toggle itself */
:global(.dark-theme) .theme-toggle-label {
  color: #9ca3af;
}

:global(.dark-theme) .theme-toggle-buttons {
  background: #374151;
}

:global(.dark-theme) .theme-button {
  color: #9ca3af;
}

:global(.dark-theme) .theme-button:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #e5e7eb;
}

:global(.dark-theme) .theme-button-active {
  background: #1f2937;
  color: #ffffff;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}
</style>

