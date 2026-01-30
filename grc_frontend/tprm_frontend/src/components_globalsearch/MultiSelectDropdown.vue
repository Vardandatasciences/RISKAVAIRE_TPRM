<template>
  <div class="dropdown w-full min-w-full" ref="dropdownRef">
    <!-- Dropdown Trigger -->
    <button
      @click="toggleDropdown"
      class="dropdown__button min-w-full h-auto py-2 px-3"
      :class="{ 'dropdown__button--open': isOpen }"
    >
      <div class="text-content">
        <span class="dropdown-value">{{ displayText }}</span>
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
      <!-- Select All Option -->
      <div 
        class="dropdown__item"
        @click="toggleSelectAll"
      >
        <div class="dropdown__item-text">
          <input
            type="checkbox"
            :checked="allSelected"
            :indeterminate="someSelected && !allSelected"
            class="mr-2"
            @click.stop
          />
          <span class="font-medium">
            {{ allSelected ? 'Deselect All' : 'Select All' }}
          </span>
        </div>
      </div>
      
      <div class="h-px bg-border my-1"></div>
      
      <!-- Individual Options -->
      <div 
        v-for="option in options" 
        :key="option.value"
        class="dropdown__item"
        :class="{ 'dropdown__item--selected': modelValue.includes(option.value) }"
        @click="toggleOption(option.value)"
      >
        <div class="dropdown__item-text">
          <input
            type="checkbox"
            :checked="modelValue.includes(option.value)"
            class="mr-2"
            @click.stop
          />
          <span>{{ option.label }}</span>
        </div>
        <div v-if="modelValue.includes(option.value)" class="dropdown__item-check">
          <svg class="dropdown__check-icon" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
          </svg>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { ChevronDown } from 'lucide-vue-next'
import '@/assets/components/dropdown.css'

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  },
  options: {
    type: Array,
    default: () => []
  },
  placeholder: {
    type: String,
    default: 'Select options...'
  },
  selectedCount: {
    type: Number,
    default: 0
  }
})

const emit = defineEmits(['update:modelValue'])

const isOpen = ref(false)
const dropdownRef = ref(null)

// Computed properties
const displayText = computed(() => {
  if (props.modelValue.length === 0) {
    return props.placeholder
  } else if (props.modelValue.length === 1) {
    const option = props.options.find(opt => opt.value === props.modelValue[0])
    return option ? option.label : 'Unknown'
  } else {
    return `${props.modelValue.length} selected`
  }
})

const allSelected = computed(() => {
  return props.options.length > 0 && props.modelValue.length === props.options.length
})

const someSelected = computed(() => {
  return props.modelValue.length > 0 && props.modelValue.length < props.options.length
})

// Methods
const toggleDropdown = () => {
  isOpen.value = !isOpen.value
}

const closeDropdown = () => {
  isOpen.value = false
}

const toggleOption = (value) => {
  const newValue = [...props.modelValue]
  const index = newValue.indexOf(value)
  
  if (index > -1) {
    newValue.splice(index, 1)
  } else {
    newValue.push(value)
  }
  
  emit('update:modelValue', newValue)
}

const toggleSelectAll = () => {
  if (allSelected.value) {
    emit('update:modelValue', [])
  } else {
    emit('update:modelValue', props.options.map(option => option.value))
  }
}

// Click outside handler
const handleClickOutside = (event) => {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
    closeDropdown()
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
/* Custom checkbox styling */
input[type="checkbox"] {
  accent-color: rgb(var(--primary));
  cursor: pointer;
}

/* Indeterminate checkbox styling */
input[type="checkbox"]:indeterminate {
  background-color: rgb(var(--primary));
  border-color: rgb(var(--primary));
}
</style>
