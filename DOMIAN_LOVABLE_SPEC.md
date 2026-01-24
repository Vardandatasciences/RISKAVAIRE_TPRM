# Domain Management Page - Lovable Spec

## 🎯 Overview
**Route**: `/domain-management` (or as configured)  
**Purpose**: Organize frameworks by domain via drag-and-drop

## 📐 Layout
- Sidebar: 240px left
- Main: margin-left 240px, margin-top 80px, padding 24px
- Height: calc(100vh - 80px), overflow-y auto

---

## 📋 NO FORM FIELDS

This page has **no inputs, dropdowns, or text fields**. It is display-only + drag-drop + buttons.

---

## 🏗️ Page Structure

### 1. Header
```html
<div class="header">
  <h1><i class="fas fa-sitemap"></i> Domain Management</h1>
  <p class="subtitle">Organize frameworks by domain. Drag and drop frameworks to assign them to domains.</p>
</div>
```

### 2. Loading State
```html
<div class="loading-container">
  <div class="spinner"></div>
  <p>Loading domains and frameworks...</p>
</div>
```

### 3. Error State
```html
<div class="error-container">
  <div class="error-message">
    <i class="fas fa-exclamation-circle"></i>
    <p>{{ error }}</p>
    <button class="retry-btn">Retry</button>
  </div>
</div>
```

### 4. Main Content (2-column grid)

#### Domain Card (repeat per domain)
```html
<div class="domain-section domain-card" @drop @dragover @dragleave>
  <div class="domain-header">
    <h2>
      <i class="fas fa-folder"></i>
      {{ domain.domain_name }}
      <span class="framework-count">({{ domain.frameworks.length }})</span>
    </h2>
  </div>
  
  <div class="frameworks-list">
    <div class="framework-item" draggable="true" @dragstart @dragend>
      <i class="fas fa-grip-vertical drag-handle"></i>
      <div class="framework-info">
        <h3>{{ framework.framework_name }}</h3>
        <div class="framework-meta">
          <span class="version">v{{ framework.current_version }}</span>
          <span class="status" :class="statusClass">{{ framework.status }}</span>
        </div>
      </div>
      <button class="remove-btn" @click="removeFramework">
        <i class="fas fa-times"></i>
      </button>
    </div>
    
    <div v-if="domain.frameworks.length === 0" class="empty-state">
      <i class="fas fa-inbox"></i>
      <p>No frameworks assigned. Drag frameworks here to assign them to this domain.</p>
    </div>
  </div>
</div>
```

#### Unlinked Frameworks Card
```html
<div class="domain-section domain-card unlinked-section">
  <div class="domain-header">
    <h2>
      <i class="fas fa-folder-open"></i>
      Unlinked Frameworks
      <span class="framework-count">({{ unlinkedFrameworks.length }})</span>
    </h2>
  </div>
  
  <div class="frameworks-list">
    <!-- Same framework-item structure, NO remove button -->
    <div class="empty-state" v-if="unlinkedFrameworks.length === 0">
      <i class="fas fa-check-circle"></i>
      <p>All frameworks are assigned to domains.</p>
    </div>
  </div>
</div>
```

### 5. Toast
```html
<div :class="['toast', toast.type]">
  <i class="fas fa-check-circle"></i> <!-- or fa-exclamation-circle for error -->
  <span>{{ toast.message }}</span>
</div>
```

---

## 📊 Displayed Data (Not Editable)

| Level | Field | Display |
|-------|-------|---------|
| **Domain** | domain_id | key (not shown) |
| | domain_name | h2 header |
| | frameworks.length | badge in (n) |
| **Framework** | framework_id | key (not shown) |
| | framework_name | h3 |
| | current_version | `v{{ x }}` badge |
| | status | badge with status class |

**Status classes**: `status-active` (green), `status-review` (yellow), `status-draft` (orange), `status-default` (gray)

---

## 🎨 Key CSS Classes

```css
.domains-container {
  padding: 24px;
  margin-left: 240px;
  margin-top: 80px;
  width: calc(100% - 240px);
  height: calc(100vh - 80px);
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: #cbd5e0 #f7fafc;
}

.header h1 {
  font-size: 28px;
  font-weight: 600;
  color: #1a1a1a;
  display: flex;
  align-items: center;
  gap: 12px;
}
.header h1 i { color: #003399; }
.subtitle { color: #666; font-size: 14px; margin: 0; }

.spinner {
  width: 40px; height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #003399;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.retry-btn {
  padding: 10px 24px;
  background: #003399;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}
.retry-btn:hover { background: #002266; }

.domains-content {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 24px;
}

.domain-section {
  background: white;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  padding: 20px;
  min-height: 200px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: all 0.3s;
}
.domain-section:hover {
  border-color: #003399;
  box-shadow: 0 4px 12px rgba(0,51,153,0.15);
}
.domain-section.drag-over {
  border-color: #003399;
  background: #f0f4ff;
  box-shadow: 0 6px 16px rgba(0,51,153,0.2);
}

.unlinked-section {
  border-color: #ff9800;
  background: #fff8f0;
}
.unlinked-section:hover { border-color: #f57c00; }

.domain-header {
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 2px solid #f0f0f0;
}
.domain-header h2 {
  font-size: 22px;
  font-weight: 600;
  color: #1a1a1a;
  display: flex;
  align-items: center;
  gap: 12px;
}
.domain-header h2 i { color: #003399; }
.unlinked-section .domain-header h2 i { color: #ff9800; }
.framework-count { font-size: 14px; color: #666; margin-left: 8px; }

.frameworks-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  min-height: 100px;
  flex: 1;
  overflow-y: auto;
  max-height: calc(100vh - 400px);
  scrollbar-width: thin;
}

.framework-item {
  background: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 16px;
  cursor: grab;
  transition: all 0.2s;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  user-select: none;
  display: flex;
  align-items: center;
  gap: 12px;
}
.framework-item:active { cursor: grabbing; }
.framework-item:hover {
  background: #f0f4ff;
  border-color: #003399;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,51,153,0.15);
}
.framework-item.dragging {
  opacity: 0.5;
  border-color: #003399;
  background: #e8f0fe;
}

.drag-handle { color: #999; cursor: grab; font-size: 16px; }
.framework-info { flex: 1; min-width: 0; overflow: hidden; }
.framework-info h3 {
  font-size: 16px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 8px 0;
}
.framework-meta { display: flex; gap: 12px; align-items: center; }
.version {
  font-size: 12px;
  color: #666;
  background: #e0e0e0;
  padding: 2px 8px;
  border-radius: 4px;
}
.status { font-size: 12px; padding: 2px 8px; border-radius: 4px; font-weight: 500; }
.status-active { background: #c8e6c9; color: #2e7d32; }
.status-review { background: #fff9c4; color: #f57f17; }
.status-draft { background: #ffccbc; color: #d84315; }
.status-default { background: #e0e0e0; color: #616161; }

.remove-btn {
  background: transparent;
  border: none;
  color: #d32f2f;
  cursor: pointer;
  padding: 6px;
  border-radius: 4px;
}
.remove-btn:hover { background: #ffebee; color: #b71c1c; }

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #999;
}
.empty-state i { font-size: 48px; margin-bottom: 12px; opacity: 0.5; }
.empty-state p { margin: 0; font-size: 14px; }

.toast {
  position: fixed;
  bottom: 24px;
  right: 24px;
  padding: 16px 24px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  display: flex;
  align-items: center;
  gap: 12px;
  z-index: 1000;
  animation: slideIn 0.3s ease;
}
.toast.success { background: #4caf50; color: white; }
.toast.error { background: #f44336; color: white; }

@keyframes slideIn {
  from { transform: translateX(100%); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
}

@media (max-width: 1400px) {
  .domains-content { grid-template-columns: 1fr; }
}
@media (max-width: 768px) {
  .domains-container {
    margin-left: 0; width: 100%;
    margin-top: 60px;
    height: calc(100vh - 60px);
  }
}
```

---

## 📊 Component Summary

| Component | Type | Interactive |
|-----------|------|-------------|
| **Header** | Title + subtitle | None |
| **Loading** | Spinner + text | None |
| **Error** | Message + Retry button | Retry click |
| **Domain cards** | Drop zones | Drag-over highlight |
| **Framework items** | Draggable | Drag, Remove (in domains only) |
| **Empty states** | Icon + message | None |
| **Toast** | Success/Error notification | Auto-dismiss 3s |

---

## 🎬 Key Features

1. ✅ 2-column grid (1 col on &lt;1400px)
2. ✅ Drag-and-drop frameworks between domains and Unlinked
3. ✅ `.drag-over` on drop zones (blue border, light blue bg)
4. ✅ `.dragging` on item being dragged (opacity 0.5, blue tint)
5. ✅ Remove button only on frameworks inside domains (not Unlinked)
6. ✅ Status badges: Active (green), Review (yellow), Draft (orange), Default (gray)
7. ✅ Version badge: `vX.X`
8. ✅ Custom scrollbars (container + frameworks-list)
9. ✅ Toast: success (green), error (red), slide-in from right
10. ✅ Responsive: single column, reduced padding/margins on mobile

**No form fields. Display + drag-drop + Retry/Remove/Toast only.**

**This is the complete, concise spec for Lovable to build Domain Management page.** 🚀
