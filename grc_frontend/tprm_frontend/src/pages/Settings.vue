<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Settings</h1>
        <p class="text-gray-600 mt-2">Manage your application preferences and accessibility options</p>
      </div>

      <!-- Settings Sections -->
      <div class="space-y-6">
        <!-- Accessibility Section -->
        <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div class="flex items-center gap-3 mb-6">
            <div class="p-2 bg-blue-100 rounded-lg">
              <Accessibility class="h-6 w-6 text-blue-600" />
            </div>
            <div>
              <h2 class="text-xl font-semibold text-gray-900">Accessibility</h2>
              <p class="text-sm text-gray-600">Customize font size and other accessibility features</p>
            </div>
          </div>

          <!-- Font Size Control -->
          <div class="border-t border-gray-200 pt-6">
            <div class="flex items-center justify-between mb-4">
              <div>
                <h3 class="text-lg font-medium text-gray-900 mb-1">Font Size</h3>
                <p class="text-sm text-gray-600">Adjust the font size to make text easier to read</p>
              </div>
            </div>
            
            <!-- Font Scroller -->
            <div class="flex items-center justify-start">
              <FontScroller />
            </div>
            
            <p class="text-xs text-gray-500 mt-4">
              Changes to font size will apply across all pages and will be saved automatically.
            </p>
          </div>

          <!-- Theme Control -->
          <div class="border-t border-gray-200 pt-6 mt-6">
            <div class="flex items-center justify-between mb-4">
              <div>
                <h3 class="text-lg font-medium text-gray-900 mb-1">Theme</h3>
                <p class="text-sm text-gray-600">Choose between light and dark theme</p>
              </div>
            </div>
            
            <!-- Theme Toggle -->
            <div class="flex items-center justify-start">
              <ThemeToggle />
            </div>
            
            <p class="text-xs text-gray-500 mt-4">
              Changes to theme will apply across all pages and will be saved automatically.
            </p>
          </div>

          <!-- Color Blindness Control -->
          <div class="border-t border-gray-200 pt-6 mt-6">
            <div class="flex items-center justify-between mb-4">
              <div>
                <h3 class="text-lg font-medium text-gray-900 mb-1">Color Blindness</h3>
                <p class="text-sm text-gray-600">Select a color blindness mode for better accessibility</p>
              </div>
            </div>
            
            <!-- Color Blindness Toggle -->
            <div class="flex items-center justify-start">
              <ColorBlindnessToggle />
            </div>
            
            <p class="text-xs text-gray-500 mt-4">
              Changes to color blindness mode will apply across all pages and will be saved automatically.
            </p>
          </div>
        </div>

        <!-- Additional Settings Sections (Placeholder) -->
        <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div class="flex items-center gap-3 mb-6">
            <div class="p-2 bg-purple-100 rounded-lg">
              <User class="h-6 w-6 text-purple-600" />
            </div>
            <div>
              <h2 class="text-xl font-semibold text-gray-900">Profile Settings</h2>
              <p class="text-sm text-gray-600">Manage your profile and account preferences</p>
            </div>
          </div>
          <p class="text-gray-500 text-sm">Profile settings coming soon...</p>
        </div>

        <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div class="flex items-center gap-3 mb-6">
            <div class="p-2 bg-green-100 rounded-lg">
              <Bell class="h-6 w-6 text-green-600" />
            </div>
            <div>
              <h2 class="text-xl font-semibold text-gray-900">Notification Preferences</h2>
              <p class="text-sm text-gray-600">Configure how you receive notifications</p>
            </div>
          </div>
          <p class="text-gray-500 text-sm">Notification preferences coming soon...</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Accessibility, User, Bell } from 'lucide-vue-next'
import FontScroller from '@/assets/components/FontScroller.vue'
import ThemeToggle from '@/assets/components/ThemeToggle.vue'
import ColorBlindnessToggle from '@/assets/components/ColorBlindnessToggle.vue'
</script>

<style scoped>
/* Settings page specific styles */
</style>

