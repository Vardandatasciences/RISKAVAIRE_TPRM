<template>
  <div class="dropdown" ref="dropdownRef" :style="{ width: width, display: width !== 'auto' ? 'block' : 'inline-block' }">
    <!-- Dropdown Trigger -->
    <button
      @click="toggleDropdown"
      class="dropdown__button"
      :class="{ 'dropdown__button--open': isOpen }"
      :disabled="disabled"
      type="button"
      :style="{ height: height }"
    >
      <div class="text-content">
        <span class="dropdown-value">{{ displayText || placeholder }}</span>
      </div>
      <ChevronDown 
        class="h-4 w-4 transition-transform duration-200" 
        :class="{ 'rotate-180': isOpen }"
      />
    </button>

    <!-- Dropdown Content -->
    <div
      v-if="isOpen"
      class="dropdown__menu"
    >
      <!-- Individual Options -->
      <div 
        v-for="option in options" 
        :key="option.value"
        class="dropdown__item"
        :class="{ 'dropdown__item--selected': modelValue === option.value }"
        @click="selectOption(option.value)"
      >
        <div class="dropdown__item-text">
          {{ option.label || option }}
        </div>
        <div v-if="modelValue === option.value" class="dropdown__item-check">
          <Check class="dropdown__check-icon" />
        </div>
      </div>
      
      <!-- No Results -->
      <div v-if="options.length === 0" class="dropdown__no-results">
        No options available
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { ChevronDown, Check } from 'lucide-vue-next'
import '@/assets/components/dropdown.css'

interface Option {
  value: string | number
  label?: string
}

interface Props {
  modelValue?: string | number
  options: (Option | string)[]
  placeholder?: string
  disabled?: boolean
  width?: string
  height?: string
}

const props = withDefaults(defineProps<Props>(), {
  placeholder: 'Select an option...',
  disabled: false,
  width: 'auto',
  height: '50px'
})

const emit = defineEmits<{
  'update:modelValue': [value: string | number]
}>()

const isOpen = ref(false)
const dropdownRef = ref<HTMLElement | null>(null)

const displayText = computed(() => {
  if (props.modelValue === '' || props.modelValue === null || props.modelValue === undefined) return ''
  
  const option = props.options.find(opt => {
    const value = typeof opt === 'string' ? opt : opt.value
    return value === props.modelValue
  })
  
  if (!option) return ''
  return typeof option === 'string' ? option : (option.label || String(option.value))
})

const toggleDropdown = () => {
  if (props.disabled) return
  isOpen.value = !isOpen.value
}

const selectOption = (value: string | number) => {
  emit('update:modelValue', value)
  isOpen.value = false
}

const handleClickOutside = (event: MouseEvent) => {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target as Node)) {
    isOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

