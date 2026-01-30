# Color Blindness Support - Usage Guide

## Overview

The color blindness support system provides accessible color palettes for users with different types of color vision deficiencies. It supports three main types of color blindness:

- **Protanopia**: Red-blindness (most common)
- **Deuteranopia**: Green-blindness
- **Tritanopia**: Blue-yellow blindness

## Quick Start

### 1. Settings Integration

Users can enable color blindness modes from the **Settings** page under **Accessibility**:

```
Settings → Accessibility → Color Blindness → Select Mode
```

Available options:
- Off (default)
- Protanopia
- Deuteranopia
- Tritanopia

### 2. How It Works

When a color-blindness mode is selected:
1. A `data-colorblind` attribute is set on the `<html>` and `<body>` elements
2. CSS variables are automatically defined for that mode
3. All components using color-blindness variables are updated instantly
4. The selection is saved to `localStorage` and persists across sessions

## CSS Variables Reference

### Primary Colors
```css
var(--cb-primary)              /* Primary blue/purple color */
var(--cb-primary-hover)        /* Hover state for primary */
var(--cb-primary-light)        /* Light background variant */
var(--cb-primary-shadow)       /* Box shadow color */
var(--cb-primary-shadow-hover) /* Hover shadow color */
var(--cb-primary-shadow-focus) /* Focus ring color */
var(--cb-primary-border)       /* Border color */
```

### Success Colors (Green/Teal)
```css
var(--cb-success)              /* Success/approved state */
var(--cb-success-hover)        /* Hover state */
var(--cb-success-light)        /* Light background */
var(--cb-success-border)       /* Border color */
var(--cb-success-shadow)       /* Box shadow */
var(--cb-success-shadow-hover) /* Hover shadow */
```

### Error Colors (Red)
```css
var(--cb-error)                /* Error/danger state */
var(--cb-error-hover)          /* Hover state */
var(--cb-error-light)          /* Light background */
var(--cb-error-border)         /* Border color */
var(--cb-error-shadow)         /* Box shadow */
var(--cb-error-shadow-hover)   /* Hover shadow */
var(--cb-error-shadow-focus)   /* Focus ring */
```

### Warning Colors (Orange)
```css
var(--cb-warning)              /* Warning state */
var(--cb-warning-hover)        /* Hover state */
var(--cb-warning-light)        /* Light background */
var(--cb-warning-shadow)       /* Box shadow */
```

### Accent Colors
```css
var(--cb-accent-cyan)          /* Cyan accent */
var(--cb-accent-cyan-hover)    /* Cyan hover */
var(--cb-accent-cyan-shadow)   /* Cyan shadow */

var(--cb-accent-purple)        /* Purple accent */
var(--cb-accent-purple-hover)  /* Purple hover */
var(--cb-accent-purple-light)  /* Purple light bg */
var(--cb-accent-purple-shadow) /* Purple shadow */

var(--cb-accent-teal)          /* Teal accent */
var(--cb-accent-teal-hover)    /* Teal hover */
var(--cb-accent-teal-shadow)   /* Teal shadow */
```

### Neutral Colors
```css
var(--cb-neutral-bg)              /* White background */
var(--cb-neutral-border)          /* Border color */
var(--cb-neutral-border-light)    /* Light border */
var(--cb-neutral-border-hover)    /* Border hover */
var(--cb-neutral-text)            /* Primary text */
var(--cb-neutral-text-secondary)  /* Secondary text */
var(--cb-neutral-text-tertiary)   /* Tertiary text */
var(--cb-neutral-text-dark)       /* Dark text */
var(--cb-neutral-gray)            /* Gray background */
var(--cb-neutral-gray-hover)      /* Gray hover */
var(--cb-neutral-gray-text)       /* Gray text */
var(--cb-neutral-gray-text-hover) /* Gray text hover */
var(--cb-neutral-gray-border)     /* Gray border */
var(--cb-neutral-gray-border-hover)/* Gray border hover */
var(--cb-neutral-inactive)        /* Inactive state */
var(--cb-neutral-hover)           /* Hover background */
var(--cb-neutral-select-hover)    /* Select hover */
var(--cb-neutral-breadcrumb)      /* Breadcrumb bg */
```

### Text Colors
```css
var(--cb-text-primary)         /* Primary text color */
var(--cb-text-secondary)       /* Secondary text */
var(--cb-text-tertiary)        /* Tertiary text */
var(--cb-text-white)           /* White text */
```

## Automatic Component Support

The following components automatically adapt when color-blindness mode is enabled:

### ✅ Badges & Status Indicators
- `.badge-approved`, `.status-approved`
- `.badge-rejected`, `.status-rejected`
- `.badge-pending`, `.status-pending`
- `.badge-in-review`, `.status-in-review`
- `.badge-active`, `.status-active`
- All priority indicators

### ✅ Buttons
- `.btn-primary`, `.btn-success`, `.btn-danger`, `.btn-warning`
- Tailwind classes: `bg-blue-*`, `bg-green-*`, `bg-red-*`, `bg-orange-*`
- Hover and focus states included

### ✅ Forms & Inputs
- Input focus states (blue border + focus ring)
- Error states (red border)
- Success states (green border)
- Error and success messages

### ✅ Alerts & Notifications
- `.alert-success`, `.alert-error`, `.alert-warning`, `.alert-info`
- Tailwind alert backgrounds: `bg-green-50`, `bg-red-50`, etc.

### ✅ Links & Text Colors
- Primary links (blue)
- Success text (green)
- Error text (red)
- Warning text (orange/amber)
- Tailwind text classes: `text-blue-*`, `text-green-*`, etc.

### ✅ Borders
- Primary, success, error, warning borders
- Tailwind border classes automatically adapted

### ✅ Tables
- Row hover states
- Border colors

### ✅ Progress Bars
- Primary, success, error, warning progress indicators

### ✅ Checkboxes & Radio Buttons
- Checked states
- Focus rings

### ✅ Switches & Toggles
- Active states

### ✅ Charts & Data Visualization
- `.chart-primary`, `.chart-success`, `.chart-error`
- Accent colors for multi-series charts

## Usage in Components

### Example 1: Custom Button

```vue
<template>
  <button class="custom-button">
    Click Me
  </button>
</template>

<style scoped>
.custom-button {
  /* Use color-blindness variables */
  background-color: var(--cb-primary);
  border: 2px solid var(--cb-primary-border);
  color: var(--cb-text-white);
}

.custom-button:hover {
  background-color: var(--cb-primary-hover);
  box-shadow: 0 4px 8px var(--cb-primary-shadow-hover);
}

.custom-button:focus {
  outline: none;
  box-shadow: 0 0 0 3px var(--cb-primary-shadow-focus);
}
</style>
```

### Example 2: Status Badge

```vue
<template>
  <span :class="getStatusClass()">
    {{ status }}
  </span>
</template>

<script setup>
const props = defineProps(['status'])

const getStatusClass = () => {
  // These classes are automatically styled by color-blindness system
  const statusMap = {
    'approved': 'badge-approved',
    'rejected': 'badge-rejected',
    'pending': 'badge-pending',
    'in_review': 'badge-in-review'
  }
  return statusMap[props.status] || 'badge-draft'
}
</script>
```

### Example 3: Form with Validation

```vue
<template>
  <div class="form-group">
    <input 
      v-model="email"
      :class="{'error': hasError}"
      class="global-form-input"
    />
    <span v-if="hasError" class="error-message">
      Invalid email address
    </span>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const email = ref('')
const hasError = computed(() => {
  return email.value && !email.value.includes('@')
})
</script>

<style scoped>
/* These styles are automatically color-blind friendly */
.global-form-input:focus {
  /* Automatically gets --cb-primary border and focus ring */
}

.global-form-input.error {
  /* Automatically gets --cb-error border */
}

.error-message {
  /* Automatically gets --cb-error text color */
}
</style>
```

### Example 4: Alert/Notification

```vue
<template>
  <div :class="`alert-${type}`" class="alert">
    <slot></slot>
  </div>
</template>

<script setup>
defineProps({
  type: {
    type: String,
    default: 'info',
    validator: (value) => ['success', 'error', 'warning', 'info'].includes(value)
  }
})
</script>

<style scoped>
/* All alert types automatically get color-blind friendly styling */
.alert {
  padding: 1rem;
  border-radius: 0.5rem;
  border-width: 1px;
}

/* alert-success, alert-error, alert-warning, alert-info classes
   are automatically styled with color-blind friendly colors */
</style>
```

## Best Practices

### ✅ DO

1. **Use CSS Variables**: Always use `var(--cb-*)` variables for colors
2. **Use Semantic Class Names**: Use `.badge-success`, `.btn-primary`, etc.
3. **Test All Modes**: Test your UI with all three color-blindness modes
4. **Provide Multiple Cues**: Use icons, labels, and patterns in addition to color
5. **Maintain Contrast**: Ensure sufficient contrast for accessibility

### ❌ DON'T

1. **Don't Hard-code Colors**: Avoid `color: #16a34a`
2. **Don't Rely Only on Color**: Add icons or text labels for important states
3. **Don't Override Important Styles**: Avoid `!important` that conflicts with color-blind styles
4. **Don't Skip Testing**: Test with actual color-blindness modes enabled

## Testing

### Manual Testing

1. Go to **Settings → Accessibility → Color Blindness**
2. Select each mode (Protanopia, Deuteranopia, Tritanopia)
3. Navigate through your application
4. Verify all status indicators, buttons, and alerts are distinguishable

### Automated Testing

```javascript
// Example test
describe('Color Blindness Support', () => {
  it('should apply protanopia mode', () => {
    const { useColorBlindness } = require('@/assets/components/useColorBlindness.js')
    const { setColorBlindness, COLORBLIND_OPTIONS } = useColorBlindness()
    
    setColorBlindness(COLORBLIND_OPTIONS.PROTANOPIA)
    
    expect(document.documentElement.getAttribute('data-colorblind')).toBe('protanopia')
  })
})
```

## Color Palette Reference

### Protanopia Mode
- **Primary**: #2563eb (Blue)
- **Success**: #16a34a (Green)
- **Error**: #dc2626 (Red)
- **Warning**: #f97316 (Orange)

### Deuteranopia Mode
- **Primary**: #2563eb (Blue)
- **Success**: #0f766e (Teal - better distinction than green)
- **Error**: #dc2626 (Red)
- **Warning**: #f97316 (Orange)

### Tritanopia Mode
- **Primary**: #7c3aed (Purple - instead of blue)
- **Success**: #16a34a (Green)
- **Error**: #dc2626 (Red)
- **Warning**: #f97316 (Orange)

## Troubleshooting

### Issue: Colors not changing

**Solution**: Ensure the CSS files are imported in `main.js`:
```javascript
import './assets/components/colourblindness.css'
import './assets/components/colourblindness-components.css'
```

### Issue: Colors revert on page reload

**Solution**: Make sure `useColorBlindness()` is initialized in `App.vue`:
```javascript
import { useColorBlindness } from './assets/components/useColorBlindness.js'
const { colorBlindness } = useColorBlindness()
```

### Issue: Dark mode conflicts

**Solution**: The system automatically excludes dark mode. Color-blindness only applies to light theme.

### Issue: Custom components not affected

**Solution**: Use the provided CSS variables in your component styles:
```css
.my-custom-button {
  background-color: var(--cb-primary);
}
```

## API Reference

### useColorBlindness()

Returns an object with:

```javascript
{
  colorBlindness,              // ref<string> - Current mode
  setColorBlindness,           // (mode: string) => void
  COLORBLIND_OPTIONS,          // Object with mode constants
  isOff,                       // () => boolean
  isProtanopia,                // () => boolean
  isDeuteranopia,              // () => boolean
  isTritanopia                 // () => boolean
}
```

### COLORBLIND_OPTIONS

```javascript
{
  OFF: 'off',
  PROTANOPIA: 'protanopia',
  DEUTERANOPIA: 'deuteranopia',
  TRITANOPIA: 'tritanopia'
}
```

### setColorBlindness(mode)

Sets the color-blindness mode and persists to localStorage.

```javascript
import { useColorBlindness } from '@/assets/components/useColorBlindness.js'

const { setColorBlindness, COLORBLIND_OPTIONS } = useColorBlindness()

// Enable protanopia mode
setColorBlindness(COLORBLIND_OPTIONS.PROTANOPIA)

// Disable (return to normal)
setColorBlindness(COLORBLIND_OPTIONS.OFF)
```

## Support

For issues or questions:
1. Check this documentation
2. Review the CSS variable reference
3. Test with browser dev tools
4. Check console for errors

---

**Note**: Color-blindness support is automatically enabled for all existing components. New components should use the CSS variables to maintain consistency.
