# Color Blindness Support - RFP Module Guide

## Overview

The RFP module now has **comprehensive color-blindness support** for all visual elements including status badges, progress bars, workflow indicators, evaluation scores, and more.

## Automatic Coverage

### ✅ All RFP Pages Supported

All RFP module pages automatically support color-blindness modes:

1. **Dashboard** (`Dashboard.vue`) - KPI cards, RFP status indicators
2. **Phase 1: Creation** (`Phase1Creation.vue`) - Form validation, status badges
3. **Phase 2: Approval** (`Phase2Approval.vue`) - Approval status indicators
4. **Phase 3: Vendor Selection** (`Phase3VendorSelection.vue`) - Match scores, vendor badges
5. **Phase 4: URL Generation** (`Phase4URLGeneration.vue`) - Status indicators
6. **Phase 6: Evaluation** (`Phase6Evaluation.vue`) - Evaluation scores, ratings
7. **Phase 7: Comparison** (`Phase7Comparison.vue`) - Comparison highlights, best/worst indicators
8. **Phase 8: Consensus** (`Phase8ConsensusAndAward.vue`) - Consensus indicators
9. **Phase 9: Award** (`Phase9Award.vue`) - Award status, winner indicators
10. **RFP List** (`RFPList.vue`) - Status badges, filters
11. **Vendor Portal** (`VendorPortal.vue`) - Submission status, vendor badges
12. **KPIs** (`KPIs.vue`) - Data visualization, trend indicators
13. **Split Screen Evaluator** (`SplitScreenEvaluator.vue`) - Evaluation interface
14. **Draft Manager** (`DraftManager.vue`) - Draft status indicators
15. **Award Response** (`AwardResponse.vue`) - Response status

## RFP-Specific Color-Blind Classes

### Status Badges

All status badges automatically adapt:

```vue
<!-- Automatically color-blind friendly -->
<span :class="getStatusBadgeClass(status)">
  {{ status }}
</span>
```

**Supported Status Classes:**
- `.badge-approved` / `.status-approved` → Green (Success)
- `.badge-in-review` / `.status-in-review` → Orange (Warning)
- `.badge-draft` / `.status-draft` → Gray (Neutral)
- `.badge-active` / `.status-active` → Green (Success)
- `.badge-rejected` / `.status-rejected` → Red (Error)
- `.badge-pending` / `.status-pending` → Orange (Warning)

### Workflow Progress Indicators

```vue
<!-- Progress steps automatically styled -->
<div class="progress-step completed">✓</div>
<div class="progress-step active">→</div>
<div class="progress-step pending">○</div>
```

**Classes:**
- `.progress-step.completed` → Primary blue
- `.progress-step.active` → Primary blue
- `.progress-step.pending` → Neutral gray
- `.progress-line.completed` → Primary blue

### Evaluation Scores

```vue
<!-- Score badges automatically styled -->
<span class="eval-score-excellent">95/100</span>
<span class="eval-score-good">85/100</span>
<span class="eval-score-fair">70/100</span>
<span class="eval-score-poor">45/100</span>
```

**Classes:**
- `.eval-score-excellent` → Green (Success)
- `.eval-score-good` → Blue (Primary)
- `.eval-score-fair` → Orange (Warning)
- `.eval-score-poor` → Red (Error)

### Match Scores

```vue
<!-- Vendor match scores -->
<span class="match-score-high">90%+</span>
<span class="match-score-medium">70-89%</span>
<span class="match-score-low">&lt;70%</span>
```

**Classes:**
- `.match-score-high` → Green light background, green text
- `.match-score-medium` → Orange light background, orange text
- `.match-score-low` → Red light background, red text

### Award Status

```vue
<!-- Award winner indicators -->
<div class="award-winner">🏆 Winner</div>
<div class="award-runner-up">Runner-up</div>
<div class="award-not-selected">Not Selected</div>
```

**Classes:**
- `.award-winner` → Green border and background
- `.award-runner-up` → Blue border and background
- `.award-not-selected` → Gray border and background

### KPI Cards

```vue
<!-- KPI indicators -->
<div class="kpi-card success">
  <span class="kpi-increase">↑ 15%</span>
</div>
<div class="kpi-card error">
  <span class="kpi-decrease">↓ 8%</span>
</div>
```

**Classes:**
- `.kpi-card.success` / `.kpi-increase` → Green
- `.kpi-card.error` / `.kpi-decrease` → Red
- `.kpi-card.warning` → Orange
- `.kpi-card.info` → Blue

### Comparison View

```vue
<!-- Comparison highlights -->
<tr class="comparison-best">Best Option</tr>
<tr class="comparison-average">Average</tr>
<tr class="comparison-worst">Worst Option</tr>
```

**Classes:**
- `.comparison-best` → Green background, green left border
- `.comparison-average` → Orange background, orange left border
- `.comparison-worst` → Red background, red left border

### Milestone Timeline

```vue
<!-- Timeline milestones -->
<div class="milestone-completed">✓ RFP Created</div>
<div class="milestone-current">→ Vendor Selection</div>
<div class="milestone-upcoming">○ Evaluation</div>
```

**Classes:**
- `.milestone-completed` → Green background, white text
- `.milestone-current` → Blue background, white text
- `.milestone-upcoming` → Gray background, gray border

### Action Buttons

```vue
<!-- Action buttons -->
<button class="action-approve">Approve</button>
<button class="action-reject">Reject</button>
<button class="action-review">Review</button>
```

**Classes:**
- `.action-approve` / `.action-accept` → Green background
- `.action-reject` / `.action-decline` → Red background
- `.action-review` / `.action-pending` → Orange background

## Tailwind Utility Classes

All Tailwind color utilities automatically adapt when color-blindness mode is active:

### Background Colors

```vue
<!-- All these automatically adapt -->
<div class="bg-green-50">Light green background</div>
<div class="bg-blue-100">Light blue background</div>
<div class="bg-red-50">Light red background</div>
<div class="bg-yellow-100">Light yellow background</div>
```

**Supported:**
- `bg-green-50`, `bg-green-100`, `bg-green-200`
- `bg-blue-50`, `bg-blue-100`, `bg-blue-200`
- `bg-red-50`, `bg-red-100`, `bg-red-200`
- `bg-yellow-50`, `bg-yellow-100`, `bg-yellow-200`

### Text Colors

```vue
<!-- All these automatically adapt -->
<span class="text-green-600">Success text</span>
<span class="text-blue-700">Primary text</span>
<span class="text-red-600">Error text</span>
<span class="text-yellow-600">Warning text</span>
```

**Supported:**
- `text-green-600`, `text-green-700`, `text-green-800`, `text-green-900`
- `text-blue-600`, `text-blue-700`, `text-blue-800`, `text-blue-900`
- `text-red-600`, `text-red-700`, `text-red-800`, `text-red-900`
- `text-yellow-600`, `text-yellow-700`, `text-yellow-800`, `text-yellow-900`

### Border Colors

```vue
<!-- All these automatically adapt -->
<div class="border-green-300">Green border</div>
<div class="border-blue-300">Blue border</div>
<div class="border-red-300">Red border</div>
```

**Supported:**
- `border-green-200`, `border-green-300`, `border-green-400`
- `border-blue-200`, `border-blue-300`, `border-blue-400`
- `border-red-200`, `border-red-300`, `border-red-400`
- `border-yellow-200`, `border-yellow-300`, `border-yellow-400`

### Gradient Backgrounds

```vue
<!-- Gradients automatically adapt -->
<button class="bg-gradient-to-r from-blue-600 to-blue-700">
  Primary Button
</button>
<button class="bg-gradient-to-r from-green-600 to-green-700">
  Success Button
</button>
```

**Supported:**
- `from-blue-*`, `to-blue-*` → Adapts to color-blind primary
- `from-green-*`, `to-green-*` → Adapts to color-blind success
- `from-red-*`, `to-red-*` → Adapts to color-blind error
- `from-yellow-*`, `to-yellow-*` → Adapts to color-blind warning

### Focus States

```vue
<!-- Focus rings automatically adapt -->
<input class="focus:ring-blue-500" />
<input class="focus:ring-green-500" />
<input class="focus:ring-red-500" />
```

**Supported:**
- `focus:ring-blue-500`, `focus:ring-blue-600`
- `focus:ring-green-500`, `focus:ring-green-600`
- `focus:ring-red-500`, `focus:ring-red-600`
- `focus:ring-yellow-500`, `focus:ring-yellow-600`

## Semantic Color Classes

RFP module uses semantic color classes that automatically adapt:

```vue
<!-- Semantic classes -->
<div class="bg-primary text-primary-foreground">Primary</div>
<div class="bg-success text-success">Success</div>
<div class="bg-warning text-warning-foreground">Warning</div>
<div class="bg-destructive text-destructive-foreground">Error</div>
<div class="bg-muted text-muted-foreground">Muted</div>
```

**All supported semantic classes:**
- `.bg-primary`, `.text-primary`, `.border-primary`
- `.bg-secondary`, `.text-secondary`
- `.bg-success`, `.text-success`
- `.bg-warning`, `.text-warning`, `.text-warning-foreground`
- `.bg-destructive`, `.text-destructive`, `.text-destructive-foreground`
- `.bg-info`, `.text-info`
- `.bg-muted`, `.text-muted`, `.text-muted-foreground`
- `.text-primary-foreground`, `.text-secondary-foreground`

## Usage Examples

### Example 1: Status Badge in Dashboard

```vue
<template>
  <div class="rfp-card">
    <span :class="getStatusColor(rfp.status)">
      {{ formatStatusText(rfp.status) }}
    </span>
  </div>
</template>

<script setup>
const getStatusColor = (status) => {
  switch (status.toLowerCase()) {
    case 'approved':
    case 'awarded':
      return 'badge-approved'
    case 'in_review':
    case 'evaluation':
      return 'badge-in-review'
    case 'rejected':
      return 'badge-rejected'
    default:
      return 'badge-draft'
  }
}
</script>
```

### Example 2: Progress Indicator

```vue
<template>
  <div class="workflow-progress">
    <div
      v-for="(phase, index) in phases"
      :key="index"
      :class="getPhaseClass(phase)"
    >
      {{ phase.name }}
    </div>
  </div>
</template>

<script setup>
const getPhaseClass = (phase) => {
  if (phase.completed) return 'progress-step completed'
  if (phase.active) return 'progress-step active'
  return 'progress-step pending'
}
</script>
```

### Example 3: Evaluation Score Badge

```vue
<template>
  <div class="evaluation-scores">
    <span :class="getScoreClass(score)">
      {{ score }}/100
    </span>
  </div>
</template>

<script setup>
const getScoreClass = (score) => {
  if (score >= 90) return 'eval-score-excellent'
  if (score >= 75) return 'eval-score-good'
  if (score >= 60) return 'eval-score-fair'
  return 'eval-score-poor'
}
</script>
```

### Example 4: KPI Card with Trend

```vue
<template>
  <div class="kpi-card">
    <h4>Total RFPs</h4>
    <div class="kpi-value">{{ totalRFPs }}</div>
    <div :class="trendClass">
      {{ trend }}% from last month
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps(['totalRFPs', 'trend'])

const trendClass = computed(() => {
  return props.trend > 0 ? 'kpi-increase' : 'kpi-decrease'
})
</script>
```

### Example 5: Vendor Match Score

```vue
<template>
  <div class="vendor-card">
    <span :class="getMatchScoreClass(matchScore)">
      {{ matchScore }}% Match
    </span>
  </div>
</template>

<script setup>
const getMatchScoreClass = (score) => {
  if (score >= 90) return 'match-score-high'
  if (score >= 70) return 'match-score-medium'
  return 'match-score-low'
}
</script>
```

## Testing Color-Blindness in RFP Module

### Manual Testing Steps

1. **Navigate to Settings**
   - Go to Settings → Accessibility → Color Blindness

2. **Test Each Mode**
   - Enable Protanopia mode
   - Navigate through all RFP phases
   - Verify status badges, progress bars, and indicators are distinguishable
   - Repeat for Deuteranopia and Tritanopia modes

3. **Test Specific Elements**
   - **Dashboard**: KPI cards, status badges
   - **Vendor Selection**: Match scores, vendor badges
   - **Evaluation**: Score badges, ratings
   - **Comparison**: Best/worst indicators
   - **Award**: Winner badges, award status

### Visual Verification Checklist

✅ **Status Badges**: Different statuses should be clearly distinguishable
✅ **Progress Bars**: Completed vs pending states should be clear
✅ **Evaluation Scores**: High/medium/low scores should be distinguishable
✅ **Match Scores**: Different score ranges should be clearly differentiated
✅ **KPI Trends**: Increase vs decrease indicators should be clear
✅ **Action Buttons**: Approve/reject/review actions should be distinguishable
✅ **Award Status**: Winner/runner-up/not-selected should be clear
✅ **Timeline Milestones**: Completed/current/upcoming should be distinguishable

## Color Mode Differences

### Protanopia Mode (Red-Blindness)
- **Success**: Green `#16a34a`
- **Error**: Red `#dc2626`
- **Warning**: Orange `#f97316`
- **Primary**: Blue `#2563eb`

### Deuteranopia Mode (Green-Blindness)
- **Success**: Teal `#0f766e` (instead of green for better distinction)
- **Error**: Red `#dc2626`
- **Warning**: Orange `#f97316`
- **Primary**: Blue `#2563eb`

### Tritanopia Mode (Blue-Yellow Blindness)
- **Success**: Green `#16a34a`
- **Error**: Red `#dc2626`
- **Warning**: Orange `#f97316`
- **Primary**: Purple `#7c3aed` (instead of blue)

## Best Practices for RFP Development

### ✅ DO

1. **Use Semantic Classes**: Always use `.badge-approved`, `.eval-score-good`, etc.
2. **Use Tailwind Utilities**: Leverage `bg-green-50`, `text-blue-600`, etc.
3. **Test All Modes**: Test with Protanopia, Deuteranopia, and Tritanopia
4. **Add Icons**: Use icons alongside colors for important states
5. **Provide Context**: Add text labels in addition to color coding

### ❌ DON'T

1. **Don't Hard-code Colors**: Avoid `style="color: #16a34a"`
2. **Don't Rely Only on Color**: Add icons or text labels
3. **Don't Use Custom Colors**: Use the provided color-blind variables
4. **Don't Skip Testing**: Always test with color-blindness modes enabled

## Troubleshooting

### Issue: Colors not changing in RFP module

**Solution**: Ensure `colourblindness-components.css` is imported in `main.js`:
```javascript
import './assets/components/colourblindness-components.css'
```

### Issue: Custom RFP classes not affected

**Solution**: Use the provided class names (`.badge-approved`, `.eval-score-good`, etc.) or Tailwind utilities (`bg-green-50`, `text-blue-600`, etc.)

### Issue: Gradients not adapting

**Solution**: Use Tailwind gradient classes (`from-blue-600`, `to-blue-700`) which are automatically adapted

## Support

For any issues or questions about color-blindness support in the RFP module:
1. Check this documentation
2. Review `COLOURBLINDNESS_USAGE.md` for general guidelines
3. Verify CSS files are imported correctly
4. Test with browser dev tools

---

**Note**: All RFP module pages automatically support color-blindness modes. No additional configuration needed!
