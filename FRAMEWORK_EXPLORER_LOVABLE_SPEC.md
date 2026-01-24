# Framework Explorer Page - Lovable Spec

## 🎯 Overview
**Route**: `/policy/framework-explorer`  
**Purpose**: Explore frameworks, versions, policies, and subpolicies in hierarchical view

## 📐 Layout
- Sidebar: 280px left
- Main: Full width with responsive padding

---

## 📊 Top Section

### Summary Cards (2 cards)
```html
<div class="summary-cards">
  <div class="summary-card active">
    <div class="summary-label">ACTIVE FRAMEWORKS</div>
    <div class="summary-value">15</div>
  </div>
  <div class="summary-card">
    <div class="summary-label">INACTIVE FRAMEWORKS</div>
    <div class="summary-value">3</div>
  </div>
</div>
```

**Style**: White cards, blue gradient on hover, click to filter

---

## 🎛️ Controls Row

### Export Section
```html
<div class="export-controls">
  <select class="export-dropdown">
    <option value="">Select format</option>
    <option value="xlsx">Excel (.xlsx)</option>
    <option value="pdf">PDF (.pdf)</option>
    <option value="csv">CSV (.csv)</option>
    <option value="json">JSON (.json)</option>
    <option value="xml">XML (.xml)</option>
    <option value="txt">Text (.txt)</option>
  </select>
  <button class="export-btn">
    <i class="fas fa-download"></i> Export
  </button>
</div>
```

### Dropdowns (3 filters)
```html
<CustomDropdown label="Framework" with-search />
<CustomDropdown label="Internal/External" />
<CustomDropdown label="Entity" />
```

### View Toggle (2 buttons)
```html
<div class="tab-controls">
  <button class="tab-btn active">Framework</button>
  <button class="tab-btn">Policy</button>
</div>
```

---

## 📋 FRAMEWORK VIEW (List)

### Table Header
```html
<div class="framework-list-header">
  <div class="list-header-item">Framework</div>
  <div class="list-header-item">Category</div>
  <div class="list-header-item">Type</div>
  <div class="list-header-item">Description</div>
  <div class="list-header-item">Status</div>
  <div class="list-header-item">Actions</div>
</div>
```

### Framework Row (Expandable)
```html
<div class="framework-list-item">
  <div class="list-item-content">
    <!-- Grid: 2fr 1.2fr 1fr 2.5fr 1.2fr 1.2fr -->
    <div class="framework-name-cell">
      <div class="framework-title">PCI DSS</div>
      <div class="framework-id">ID: 123</div>
    </div>
    <div class="framework-category-cell">
      <span class="category-text">Security</span>
    </div>
    <div class="framework-type-cell">
      <span class="type-text">Internal</span>
    </div>
    <div class="framework-description-cell">
      <p class="description-text">Description...</p>
    </div>
    <div class="framework-status-cell">
      <!-- Toggle Switch -->
      <label class="switch">
        <input type="checkbox" checked />
        <span class="slider"></span>
      </label>
      <span class="switch-label active">Active</span>
    </div>
    <div class="framework-actions-cell">
      <button class="action-btn details-btn">Details</button>
      <i class="fas fa-chevron-down expand-arrow"></i>
    </div>
  </div>
</div>
```

---

### Expanded: Framework Versions
```html
<div class="framework-expandable-row">
  <div class="expandable-header">
    <h4>Framework Versions</h4>
    <div class="hierarchy-breadcrumb">
      <span class="hierarchy-item active">PCI DSS</span>
    </div>
  </div>
  
  <div class="versions-list">
    <div class="version-item">
      <div class="version-header">
        <div class="version-main-info">
          <span class="version-name">Version 3.2.1</span>
        </div>
        <div class="version-info">
          <span class="version-status approved">Approved</span>
          <i class="fas fa-chevron-down"></i>
        </div>
      </div>
      
      <!-- Expanded: Policies List -->
      <div class="version-policies">
        <div class="policy-list-header">
          <div class="list-header-item">Policy</div>
          <div class="list-header-item">Category</div>
          <div class="list-header-item">Type</div>
          <div class="list-header-item">Description</div>
          <div class="list-header-item">Status</div>
          <div class="list-header-item">Actions</div>
        </div>
        
        <div class="policy-list-item">
          <div class="list-item-content">
            <div class="policy-name-cell">
              <div class="policy-title">Access Control</div>
              <div class="policy-id">ID: 456</div>
            </div>
            <div class="policy-category-cell">
              <span class="category-text">Security</span>
            </div>
            <div class="policy-type-cell">
              <span class="type-text">External</span>
            </div>
            <div class="policy-description-cell">
              <p class="description-text">Description...</p>
            </div>
            <div class="policy-status-cell">
              <label class="switch">
                <input type="checkbox" />
                <span class="slider"></span>
              </label>
              <span class="switch-label">Active</span>
            </div>
            <div class="policy-actions-cell">
              <button class="acknowledge-btn-list">Acknowledge</button>
              <button class="view-reports-btn-list">View Reports</button>
              <button class="action-btn details-btn">Details</button>
              <i class="fas fa-chevron-down"></i>
            </div>
          </div>
        </div>
        
        <!-- Expanded: Policy Versions -->
        <div class="inline-policy-versions-container">
          <div class="inline-policy-version-item">
            <div class="inline-policy-version-header">
              <span class="version-label">Version 2.0</span>
              <span class="version-status">Active</span>
              <i class="fas fa-chevron-down"></i>
            </div>
            
            <!-- Expanded: Subpolicies -->
            <div class="inline-subpolicies-container">
              <div class="inline-subpolicy-item">
                <span class="subpolicy-name">Password Requirements</span>
                <span class="subpolicy-id">ID: 789</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
```

---

## 🎴 POLICY VIEW (Cards)

```html
<div class="framework-cards-grid">
  <div class="framework-card">
    <div class="framework-card-header">
      <div class="framework-card-icon">
        <i class="fas fa-shield-alt"></i>
      </div>
      <div class="framework-card-status">
        <label class="switch">
          <input type="checkbox" checked />
          <span class="slider"></span>
        </label>
      </div>
    </div>
    
    <div class="framework-card-content">
      <h3 class="framework-card-title">PCI DSS</h3>
      <p class="framework-card-id">ID: 123</p>
      <div class="framework-card-badges">
        <span class="badge category-badge">Security</span>
        <span class="badge type-badge internal">Internal</span>
      </div>
      <p class="framework-card-description">Description...</p>
      
      <div class="framework-card-footer">
        <div class="card-stats">
          <span>12 Policies</span>
        </div>
        <button class="card-details-btn">Details</button>
      </div>
    </div>
  </div>
</div>
```

**Style**: Grid layout, min-width 320px, hover lift effect

---

## 📄 Framework Details Modal

```html
<div class="framework-details-view">
  <div class="details-header">
    <button class="policy-dashboard-back-btn">
      <i class="fas fa-arrow-left"></i>
    </button>
    <h2>Framework Details</h2>
  </div>
  
  <div class="details-content">
    <div class="detail-row">
      <span class="detail-label">Framework Name</span>
      <span class="detail-value">PCI DSS</span>
    </div>
    <!-- 12 detail rows total -->
  </div>
</div>
```

**12 Detail Fields**:
1. Framework Name
2. Description
3. Category
4. Version
5. Status
6. Active/Inactive
7. Identifier
8. Effective Date
9. Start Date
10. End Date
11. Created By
12. Created Date
13. Documentation (link)

---

## 🎨 Key CSS Classes

```css
/* Summary Cards */
.summary-cards { display: flex; gap: 20px; margin-bottom: 24px; }
.summary-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(79,108,255,0.08);
  cursor: pointer;
  transition: all 0.3s;
}
.summary-card:hover { transform: translateY(-4px); }
.summary-label { font-size: 0.75rem; font-weight: 700; color: #64748b; }
.summary-value { font-size: 2rem; font-weight: 700; color: #2c3e50; }

/* List Table */
.framework-list-header {
  display: grid;
  grid-template-columns: 2fr 1.2fr 1fr 2.5fr 1.2fr 1.2fr;
  gap: 20px;
  padding: 16px 24px;
  background: #f8fafc;
  font-weight: 700;
  font-size: 0.8rem;
  color: #64748b;
}

.framework-list-item {
  background: white;
  border-radius: 12px;
  margin-bottom: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  transition: all 0.2s;
}
.framework-list-item:hover { box-shadow: 0 4px 16px rgba(79,108,255,0.12); }

.list-item-content {
  display: grid;
  grid-template-columns: 2fr 1.2fr 1fr 2.5fr 1.2fr 1.2fr;
  gap: 20px;
  padding: 20px 24px;
  align-items: center;
}

/* Toggle Switch */
.switch {
  position: relative;
  width: 44px;
  height: 24px;
}
.switch input { display: none; }
.slider {
  position: absolute;
  cursor: pointer;
  top: 0; left: 0; right: 0; bottom: 0;
  background: #cbd5e1;
  border-radius: 24px;
  transition: 0.3s;
}
.slider:before {
  content: "";
  position: absolute;
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 3px;
  background: white;
  border-radius: 50%;
  transition: 0.3s;
}
input:checked + .slider { background: #22c55e; }
input:checked + .slider:before { transform: translateX(20px); }

/* Expandable Sections */
.framework-expandable-row {
  background: #f8fafc;
  border-left: 4px solid #4f6cff;
  padding: 24px;
  margin: 8px 0 12px 0;
  border-radius: 0 8px 8px 0;
}

.expandable-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.hierarchy-breadcrumb { display: flex; gap: 8px; }
.hierarchy-item {
  padding: 4px 12px;
  background: #e0e7ff;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 600;
  color: #4f6cff;
}

.version-item {
  background: white;
  border-radius: 8px;
  margin-bottom: 12px;
  overflow: hidden;
}

.version-header {
  display: flex;
  justify-content: space-between;
  padding: 16px 20px;
  cursor: pointer;
  background: #f1f5f9;
}

.version-status {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
}
.version-status.approved { background: #d1fae5; color: #059669; }
.version-status.rejected { background: #fee2e2; color: #dc2626; }

/* Cards View */
.framework-cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 24px;
}

.framework-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(79,108,255,0.08);
  border: 1px solid #e8edfa;
  cursor: pointer;
  transition: all 0.3s;
}
.framework-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 32px rgba(79,108,255,0.16);
}

.framework-card-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 16px;
}

.framework-card-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #e8edfa 0%, #d0d9f7 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #4f6cff;
  font-size: 1.5rem;
}

.framework-card-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 8px;
}

.framework-card-badges {
  display: flex;
  gap: 8px;
  margin: 12px 0;
}

.badge {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
}

.category-badge {
  background: linear-gradient(135deg, #e8edfa 0%, #d0d9f7 100%);
  color: #4f6cff;
  border: 1px solid #c7d0f0;
}

.type-badge.internal {
  background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
  color: #059669;
  border: 1px solid #6ee7b7;
}

/* Buttons */
.action-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 8px;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  background: linear-gradient(135deg, #f0f4ff 0%, #e0e7ff 100%);
  color: #4f6cff;
  border: 1px solid #c7d0f0;
  transition: all 0.2s;
}
.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(79,108,255,0.2);
}

.export-btn {
  background: #4f6cff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
}
```

---

## 📊 Component Summary

| Component | Purpose | Interactive |
|-----------|---------|-------------|
| **Summary Cards** | Show active/inactive count | Click to filter |
| **Export Controls** | Export framework data | 6 format options |
| **Filter Dropdowns** | Filter frameworks | 3 dropdowns |
| **View Toggle** | Switch list/card view | 2 buttons |
| **List View** | Hierarchical table | 4-level expansion |
| **Card View** | Framework cards | Grid layout |
| **Details Modal** | Show full details | 13 fields |
| **Toggle Switch** | Active/Inactive status | Per item |

---

## 🎬 Key Features

1. ✅ 2 summary cards (active/inactive frameworks)
2. ✅ 6 export formats (Excel, PDF, CSV, JSON, XML, TXT)
3. ✅ 3 filter dropdowns (Framework, Type, Entity)
4. ✅ 2 view modes (List/Card toggle)
5. ✅ 4-level hierarchical expansion (Framework → Version → Policy → Subpolicy)
6. ✅ Toggle switches for status on every item
7. ✅ Action buttons (Details, Acknowledge, View Reports)
8. ✅ Breadcrumb navigation in expanded rows
9. ✅ Version status badges (Approved, Rejected, etc.)
10. ✅ Card view with hover animations
11. ✅ Details modal with 13 framework fields
12. ✅ Responsive grid layouts

**This is the complete, concise spec for Lovable to build Framework Explorer page.** 🚀
