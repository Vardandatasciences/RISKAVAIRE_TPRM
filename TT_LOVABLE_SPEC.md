# Tailoring & Templating Page - Lovable Spec

## 🎯 Overview
**Route**: `/policy/tailoring-templating`  
**Purpose**: Customize internal frameworks and policies

## 📐 Layout
- Sidebar: 280px left
- Main: margin-left 280px, padding 30px

## 🎨 Header Section

### Data Type Legend (Display Only)
```html
<div class="data-type-legend">
  <div class="legend-item personal">👤 Personal</div>
  <div class="legend-item confidential">🛡️ Confidential</div>
  <div class="legend-item regular">📄 Regular</div>
</div>
```

### Info Cards (3 cards)
```html
<div class="info-cards">
  <div class="info-card">
    <i class="fas fa-cogs"></i>
    <h3>Framework Tailoring</h3>
    <p>Adapt internal frameworks...</p>
  </div>
  <!-- 2 more cards -->
</div>
```

---

## 🔄 Toggle Tabs (Framework / Policy)

```html
<div class="toggle-group">
  <button class="toggle active">Framework</button>
  <button class="toggle">Policy</button>
</div>
```

**Style**: Transparent bg, blue bottom border on active (#3d5afe), 3px height

---

## 📝 FRAMEWORK TAB

### Selection Dropdown
```html
<CustomDropdown label="Framework" with-search />
<i class="info-icon">🛈</i>
<div class="tooltip">Only internal frameworks can be tailored</div>
```

### Framework Form (7 Fields)

| # | Field | Type | Required | Data Type Toggle | Auto-Gen | Notes |
|---|-------|------|----------|------------------|----------|-------|
| 1 | Framework Name | Text Input | ✅ | ✅ | | |
| 2 | Description | Textarea (3 rows) | ✅ | ✅ | | |
| 3 | Identifier | Text Input | ✅ | ✅ | ✅ | Readonly |
| 4 | Category | Text Input | ✅ | ✅ | | |
| 5 | Internal/External | Select | ✅ | ✅ | | Internal, External |
| 6 | Start Date | Date | ✅ | ✅ | | |
| 7 | End Date | Date | | ✅ | | |
| 8 | Upload Document | File | | ✅ | | Optional |
| 9 | Reviewer | Select (Users) | ✅ | ✅ | | Dropdown from users |

**Submit Button**: "Submit Framework" (blue #3d5afe, center)

---

## 📄 POLICY TAB

### Selection Dropdowns
```html
<CustomDropdown label="Framework" with-search />
<CustomDropdown label="Policy" with-search />
```

### Policy Tabs (Dynamic)
```html
<div class="policy-tabs-row">
  <button class="policy-tab active">Policy 1</button>
  <button class="policy-tab">Policy 2</button>
  <button class="add-policy-tab">+ Add Policy</button>
</div>
```

### Policy Form (15 Fields)

| # | Field | Type | Required | Data Type Toggle | Options/Notes |
|---|-------|------|----------|------------------|---------------|
| 1 | Policy Name | Text Input | ✅ | ✅ | |
| 2 | Identifier | Text Input | ✅ | ✅ | Auto-gen readonly |
| 3 | Description | Textarea (3 rows) | ✅ | ✅ | |
| 4 | Policy Type | Multi-Select Dropdown | ✅ | ✅ | Search + Create New |
| 5 | Policy Category | Multi-Select Dropdown | ✅ | ✅ | Search + Create New |
| 6 | Policy Sub Category | Multi-Select Dropdown | ✅ | ✅ | Search + Create New |
| 7 | Scope | Text Input | ✅ | ✅ | |
| 8 | Department | Searchable Input | ✅ | ✅ | Datalist dropdown |
| 9 | Objective | Textarea (3 rows) | ✅ | ✅ | |
| 10 | Coverage Rate (%) | Number Input | ✅ | ✅ | 0-100, step 0.01 |
| 11 | Applicability | Textarea (3 rows) | ✅ | ✅ | |
| 12 | Reviewer | Select (Users) | ✅ | ✅ | |
| 13 | Control | Textarea (4 rows) | ✅ | ✅ | |
| 14 | Start Date | Date | ✅ | ✅ | |
| 15 | End Date | Date | | ✅ | |
| 16 | Upload Document | File | | ✅ | Optional |

**Exclude Policy Button**: Top right, red border (#f44336), transparent bg

---

### Subpolicy Tabs (Nested, Dynamic)
```html
<div class="subpolicy-tabs-row">
  <button class="subpolicy-tab active">Subpolicy 1</button>
  <button class="subpolicy-tab">Subpolicy 2</button>
  <button class="add-subpolicy-tab">+ Add Sub Policy</button>
</div>
```

### Subpolicy Form (7 Fields)

| # | Field | Type | Required | Data Type Toggle | Notes |
|---|-------|------|----------|------------------|-------|
| 1 | Sub Policy Name | Text Input | ✅ | ✅ | |
| 2 | Identifier | Text Input | ✅ | ✅ | Auto-gen readonly |
| 3 | Description | Textarea (3 rows) | ✅ | ✅ | |
| 4 | Control | Textarea (4 rows) | ✅ | ✅ | |
| 5 | Start Date | Date | ✅ | ✅ | |
| 6 | End Date | Date | | ✅ | |
| 7 | Upload Document | File | | ✅ | Optional |

**Exclude Subpolicy Button**: Top right, red border, smaller size

---

### Universal Submit Button
```html
<div class="universal-submit-wrapper">
  <button class="universal-submit-btn">Submit</button>
</div>
```

**Style**: Blue #3d5afe, 100px width, left aligned, margin-top 40px

---

## 🎨 Data Type Circle Toggle

Every field has 3 colored circles for classification:

```html
<div class="data-type-circle-toggle">
  <div class="circle personal-circle"></div>
  <div class="circle confidential-circle"></div>
  <div class="circle regular-circle active"></div>
</div>
```

**Colors**:
- Personal: #E53E3E (red)
- Confidential: #DD6B20 (orange)
- Regular: #48BB78 (green)

**Active State**: Border 2px solid, inner dot visible

---

## 🔽 Custom Multi-Select Dropdowns

### Policy Type / Category / Sub Category

```html
<div class="policy-type-dropdown">
  <div class="selected-policy-type">
    <div class="policy-type-content">
      <span class="policy-type-value">Selected Item</span>
    </div>
    <i class="dropdown-arrow">▼</i>
  </div>
  <div class="policy-type-options">
    <div class="search-input-container">
      <input type="text" placeholder="Search..." />
    </div>
    <div class="policy-type-option">Option 1</div>
    <div class="policy-type-option create-new-option">
      <i class="fas fa-plus"></i> Create New
    </div>
  </div>
</div>
```

**Style**:
- Border left: 3px solid #805AD5 (purple)
- Search icon before content (FontAwesome)
- Max height: 180px
- Scrollbar: 4px width
- Create new: Green bg #f0fff4

---

## 🎨 Key CSS Classes

```css
/* Container */
.TT-container {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.08);
  padding: 30px 24px;
}

/* Toggle Group */
.TT-toggle-group { display: flex; gap: 0; margin-bottom: 20px; }
.TT-toggle {
  background: transparent;
  border: none;
  color: #555;
  padding: 12px 32px;
  position: relative;
  font-weight: 600;
}
.TT-toggle::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 3px;
  background: transparent;
}
.TT-toggle.TT-active::after { background: #3d5afe; }

/* Form Inputs */
.TT-input, .TT-textarea {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #bfcfff;
  border-radius: 8px;
  background: white;
}
.TT-input:focus, .TT-textarea:focus {
  border-color: #3d5afe;
  box-shadow: 0 0 0 2px rgba(61,90,254,0.08);
}
.TT-textarea { height: 140px; resize: vertical; }

/* Policy Tabs */
.TT-policy-tabs-row {
  background: white;
  border-bottom: 1px solid #eaedf3;
  padding: 0 32px;
  display: flex;
}
.TT-policy-tab {
  background: transparent;
  border: none;
  color: #555;
  padding: 16px 24px;
  position: relative;
}
.TT-policy-tab::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 3px;
  background: transparent;
}
.TT-policy-tab-active::after { background: #3d5afe; }

/* Subpolicy Tabs (same but smaller) */
.TT-subpolicy-tab { padding: 14px 20px; font-size: 0.9rem; }

/* Buttons */
.TT-submit, .TT-universal-submit-btn {
  background: #3d5afe;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 10px 32px;
  font-weight: 600;
  cursor: pointer;
}
.TT-submit:hover { background: #2a3a5e; }

.TT-exclude-policy-btn, .TT-exclude-subpolicy-btn {
  position: absolute;
  top: 18px;
  right: 18px;
  background: transparent;
  color: #f44336;
  border: 1px solid #f44336;
  border-radius: 6px;
  padding: 6px 18px;
}

/* Data Type Circles */
.policy-data-type-circle-toggle {
  display: flex;
  gap: 6px;
  position: absolute;
  right: 0;
  top: 0;
}
.policy-circle-option {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  cursor: pointer;
  border: 2px solid transparent;
  transition: all 0.2s;
}
.personal-circle { background: #E53E3E; }
.confidential-circle { background: #DD6B20; }
.regular-circle { background: #48BB78; }
.policy-circle-option.active {
  border-color: currentColor;
  transform: scale(1.1);
}
.policy-circle-option.active .policy-circle-inner {
  width: 6px;
  height: 6px;
  background: white;
  border-radius: 50%;
  margin: 3px auto;
}

/* Multi-Select Dropdown */
.selected-policy-type {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 12px;
  border: 1px solid #e2e8f0;
  border-left: 3px solid #805AD5;
  border-radius: 6px;
  cursor: pointer;
}
.selected-policy-type::before {
  content: '\f002';
  font-family: 'Font Awesome 5 Free';
  position: absolute;
  left: 10px;
  color: #805AD5;
}
.policy-type-options {
  position: absolute;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  max-height: 180px;
  overflow-y: auto;
  z-index: 1000;
}
.create-new-option {
  background: #f0fff4;
  border-left: 3px solid #48bb78;
}
```

---

## 📊 Field Summary

| Section | Fields | Required | Data Type Toggles |
|---------|--------|----------|-------------------|
| **Framework** | 9 | 7 | All 9 |
| **Policy** | 16 per policy | 14 | All 16 |
| **Subpolicy** | 7 per subpolicy | 5 | All 7 |

**Total**: Dynamic based on tabs (can be 50+ fields for multiple policies)

---

## 🎬 Key Features

1. ✅ 2-tab system (Framework / Policy)
2. ✅ Dynamic policy & subpolicy tabs
3. ✅ Data type classification on every field (3 circles)
4. ✅ Auto-generated identifiers (readonly)
5. ✅ Multi-select dropdowns with search + create new
6. ✅ Searchable user dropdown (reviewer)
7. ✅ Datalist for departments
8. ✅ File upload on framework/policy/subpolicy
9. ✅ Exclude buttons for policies/subpolicies
10. ✅ Form validation with error messages
11. ✅ Hover underline on tabs (rgba blue)
12. ✅ Info tooltip for framework selection

**This is the complete, concise spec for Lovable to build TT page.** 🚀
