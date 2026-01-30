# RFP Color-Blindness - Quick Reference

## 🎨 Automatically Supported Classes

### Status Badges
```vue
.badge-approved        → Green (Success)
.badge-in-review       → Orange (Warning)
.badge-draft           → Gray (Neutral)
.badge-rejected        → Red (Error)
.badge-pending         → Orange (Warning)
.badge-active          → Green (Success)
```

### Evaluation Scores
```vue
.eval-score-excellent  → Green
.eval-score-good       → Blue
.eval-score-fair       → Orange
.eval-score-poor       → Red
```

### Match Scores
```vue
.match-score-high      → Green light bg, green text
.match-score-medium    → Orange light bg, orange text
.match-score-low       → Red light bg, red text
```

### Progress Indicators
```vue
.progress-step.completed  → Blue
.progress-step.active     → Blue
.progress-step.pending    → Gray
```

### Award Status
```vue
.award-winner          → Green border & bg
.award-runner-up       → Blue border & bg
.award-not-selected    → Gray border & bg
```

### KPI Cards
```vue
.kpi-increase          → Green
.kpi-decrease          → Red
.kpi-card.warning      → Orange
.kpi-card.info         → Blue
```

### Comparison View
```vue
.comparison-best       → Green bg, left border
.comparison-average    → Orange bg, left border
.comparison-worst      → Red bg, left border
```

### Timeline Milestones
```vue
.milestone-completed   → Green bg
.milestone-current     → Blue bg
.milestone-upcoming    → Gray bg
```

### Action Buttons
```vue
.action-approve        → Green bg
.action-reject         → Red bg
.action-review         → Orange bg
```

## 🎯 Tailwind Classes (Auto-Adapted)

### Backgrounds
```vue
bg-green-50, bg-green-100, bg-green-200
bg-blue-50, bg-blue-100, bg-blue-200
bg-red-50, bg-red-100, bg-red-200
bg-yellow-50, bg-yellow-100, bg-yellow-200
```

### Text
```vue
text-green-600, text-green-700, text-green-800
text-blue-600, text-blue-700, text-blue-800
text-red-600, text-red-700, text-red-800
text-yellow-600, text-yellow-700, text-yellow-800
```

### Borders
```vue
border-green-300, border-blue-300, border-red-300, border-yellow-300
```

### Gradients
```vue
from-blue-600 to-blue-700
from-green-600 to-green-700
from-red-600 to-red-700
from-yellow-600 to-yellow-700
```

### Focus Rings
```vue
focus:ring-blue-500
focus:ring-green-500
focus:ring-red-500
focus:ring-yellow-500
```

## 💡 Semantic Classes
```vue
.bg-primary            → Primary color
.bg-success            → Success color
.bg-warning            → Warning color
.bg-destructive        → Error color
.bg-info               → Info color
.bg-muted              → Muted color

.text-primary          → Primary text
.text-success          → Success text
.text-warning          → Warning text
.text-destructive      → Error text
.text-info             → Info text
.text-muted-foreground → Muted text
```

## 📊 Score Ranges

### Evaluation Scores
- Excellent: 90-100 → `.eval-score-excellent` (Green)
- Good: 75-89 → `.eval-score-good` (Blue)
- Fair: 60-74 → `.eval-score-fair` (Orange)
- Poor: 0-59 → `.eval-score-poor` (Red)

### Match Scores
- High: 90%+ → `.match-score-high` (Green)
- Medium: 70-89% → `.match-score-medium` (Orange)
- Low: <70% → `.match-score-low` (Red)

### KPI Trends
- Positive: `.kpi-increase` (Green)
- Negative: `.kpi-decrease` (Red)

## 🔧 Usage Template

```vue
<template>
  <div class="rfp-component">
    <!-- Status Badge -->
    <span :class="getStatusClass(status)">
      {{ status }}
    </span>
    
    <!-- Score Badge -->
    <span :class="getScoreClass(score)">
      {{ score }}/100
    </span>
    
    <!-- Progress Step -->
    <div :class="getProgressClass(step)">
      {{ step.name }}
    </div>
  </div>
</template>

<script setup>
const getStatusClass = (status) => {
  const map = {
    approved: 'badge-approved',
    in_review: 'badge-in-review',
    draft: 'badge-draft',
    rejected: 'badge-rejected'
  }
  return map[status.toLowerCase()] || 'badge-draft'
}

const getScoreClass = (score) => {
  if (score >= 90) return 'eval-score-excellent'
  if (score >= 75) return 'eval-score-good'
  if (score >= 60) return 'eval-score-fair'
  return 'eval-score-poor'
}

const getProgressClass = (step) => {
  if (step.completed) return 'progress-step completed'
  if (step.active) return 'progress-step active'
  return 'progress-step pending'
}
</script>
```

## ⚙️ Enable Color-Blindness

**User Path**: Settings → Accessibility → Color Blindness

**Options**:
- Off (default)
- Protanopia (red-blindness)
- Deuteranopia (green-blindness)
- Tritanopia (blue-yellow blindness)

## ✅ Coverage

**All 15 RFP pages** automatically support color-blindness:
- ✅ Dashboard
- ✅ Phase 1: Creation
- ✅ Phase 2: Approval
- ✅ Phase 3: Vendor Selection
- ✅ Phase 4: URL Generation
- ✅ Phase 6: Evaluation
- ✅ Phase 7: Comparison
- ✅ Phase 8: Consensus
- ✅ Phase 9: Award
- ✅ RFP List
- ✅ Vendor Portal
- ✅ KPIs
- ✅ Split Screen Evaluator
- ✅ Draft Manager
- ✅ Award Response

## 🎨 Color Modes

### Protanopia (Red-Blindness)
- Success: Green #16a34a
- Primary: Blue #2563eb
- Warning: Orange #f97316
- Error: Red #dc2626

### Deuteranopia (Green-Blindness)
- Success: Teal #0f766e (different from normal green)
- Primary: Blue #2563eb
- Warning: Orange #f97316
- Error: Red #dc2626

### Tritanopia (Blue-Yellow Blindness)
- Success: Green #16a34a
- Primary: Purple #7c3aed (different from normal blue)
- Warning: Orange #f97316
- Error: Red #dc2626

---

**No configuration needed** - Everything works automatically when color-blindness mode is enabled in Settings!
