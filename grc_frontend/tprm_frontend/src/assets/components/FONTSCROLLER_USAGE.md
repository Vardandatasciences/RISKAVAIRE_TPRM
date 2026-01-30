# Font Scroller Component - Usage Guide

## Overview
The Font Scroller component allows users to adjust the font size throughout the application by scrolling, similar to adjusting brightness on mobile devices.

## Features
- **Draggable Scroll Bar**: Click and drag the handle to adjust font size
- **Wheel Scrolling**: Scroll on the scroll bar to adjust font size
- **Global Wheel Scrolling** (Optional): Use Ctrl + Mouse Wheel anywhere on the page
- **Persistent Storage**: Font size preference is saved to localStorage
- **Visual Feedback**: Shows current font size percentage

## Installation

### 1. Import the component in your App component

```vue
<template>
  <div>
    <!-- Your app content -->
    <RouterView />
    
    <!-- Add Font Scroller -->
    <FontScroller />
  </div>
</template>

<script setup>
import FontScroller from './assets/components/FontScroller.vue'
</script>
```

### 2. Import the CSS (if not already imported)

The component imports its own CSS, but you may want to ensure the global font size styles are applied:

```javascript
// In your main.js or main entry file
import './assets/components/fontscroller.css'
```

## Usage Examples

### Basic Usage
```vue
<template>
  <FontScroller />
</template>

<script setup>
import FontScroller from '@/assets/components/FontScroller.vue'
</script>
```

### With Global Wheel Scrolling
Enable Ctrl + Mouse Wheel to adjust font size anywhere on the page:

```vue
<template>
  <FontScroller :enable-global-wheel="true" />
</template>

<script setup>
import FontScroller from '@/assets/components/FontScroller.vue'
</script>
```

### Using the Composable Directly
You can also use the `useFontSize` composable directly in your components:

```vue
<script setup>
import { useFontSize } from '@/assets/components/useFontSize.js'

const { fontSize, increaseFontSize, decreaseFontSize, resetFontSize } = useFontSize()
</script>

<template>
  <div>
    <p>Current font size: {{ fontSize }}%</p>
    <button @click="increaseFontSize">Increase</button>
    <button @click="decreaseFontSize">Decrease</button>
    <button @click="resetFontSize">Reset</button>
  </div>
</template>
```

## How It Works

1. The component adjusts the root `font-size` CSS property on the `<html>` element
2. All elements using `rem` units will scale proportionally
3. Font size is stored in localStorage and persists across page reloads
4. Default range: 50% to 200% (adjustable in `useFontSize.js`)

## Customization

### Adjust Font Size Range
Edit `src/assets/components/useFontSize.js`:

```javascript
const MIN_FONT_SIZE = 50  // Minimum 50%
const MAX_FONT_SIZE = 200 // Maximum 200%
const FONT_SIZE_STEP = 2  // Step size for adjustments
```

### Adjust Scroll Bar Position
Edit the CSS in `fontscroller.css`:

```css
.font-scroller-container {
  right: 20px;  /* Distance from right edge */
  top: 50%;     /* Vertical position */
}
```

## Notes

- The component uses `rem` units for scaling. Ensure your application uses `rem` or `em` units for best results
- Font size preference is saved to localStorage with key `app_font_size`
- The component is fixed positioned and appears on all pages where it's included

