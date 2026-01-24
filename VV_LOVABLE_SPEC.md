# Policy Versioning Page - Lovable Spec

## 🎯 Overview
**Route**: `/policy/versioning`  
**Purpose**: Create and manage versions of frameworks and policies

## 📐 Layout
- Sidebar: 280px left
- Main: margin-left 280px, padding-top 30px

## 🎨 Header Section

### Title & Description
```html
<h2>Policy Versioning</h2>
<p>Create and manage versions of your frameworks and policies...</p>
```

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
<div class="vv-info-cards">
  <div class="vv-info-card">
    <i class="fas fa-code-branch"></i>
    <h3>Version Control</h3>
    <p>Track changes to frameworks...</p>
  </div>
  <!-- 2 more cards: Change Management, Compliance Tracking -->
</div>
```

**Style**: White cards, blue circular icon bg (#ebf4ff), hover lift effect

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
| 7 | End Date | Date | ✅ | ✅ | | Required (not optional) |
| 8 | Reviewer | Select (Users) | ✅ | ✅ | | Dropdown from users |

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
<div class="policy-tabs">
  <button class="policy-tab active">Policy 1</button>
  <button class="policy-tab">Policy 2</button>
  <button class="add-policy-tab">+ Add Policy</button>
</div>
```

**Style**: Blue bg on active, rounded top corners, dashed border on add button

### Policy Form (13 Fields)

| # | Field | Type | Required | Data Type Toggle | Options/Notes |
|---|-------|------|----------|------------------|---------------|
| 1 | Policy Name | Text Input | ✅ | ✅ | |
| 2 | Identifier | Text Input | ✅ | ✅ | Readonly for internal |
| 3 | Description | Textarea (3 rows) | ✅ | ✅ | |
| 4 | Policy Type | Multi-Select Dropdown | ✅ | ✅ | Search + Create New |
| 5 | Policy Category | Multi-Select Dropdown | ✅ | ✅ | Search + Create New |
| 6 | Policy Sub Category | Multi-Select Dropdown | ✅ | ✅ | Search + Create New |
| 7 | Scope | Text Input | ✅ | ✅ | |
| 8 | Department | Searchable Input | ✅ | ✅ | Datalist dropdown |
| 9 | Objective | Textarea (3 rows) | ✅ | ✅ | |
| 10 | Coverage Rate (%) | Number Input | ✅ | ✅ | 0-100, step 0.01 |
| 11 | Applicability | Text Input | ✅ | ✅ | |
| 12 | Start Date | Date | ✅ | ✅ | |
| 13 | End Date | Date | ✅ | ✅ | Required |
| 14 | Reviewer | Select (Users) | ✅ | ✅ | Searchable dropdown |

**Exclude Policy Button**: Top right, red border, white bg

---

### Subpolicy Tabs (Nested, Dynamic)
```html
<div class="subpolicy-tabs">
  <button class="subpolicy-tab active">Subpolicy 1</button>
  <button class="subpolicy-tab">Subpolicy 2</button>
  <button class="add-subpolicy-tab">+ Add Sub Policy</button>
</div>
```

### Subpolicy Form (4 Fields)

| # | Field | Type | Required | Data Type Toggle | Notes |
|---|-------|------|----------|------------------|-------|
| 1 | Sub Policy Name | Text Input | ✅ | ✅ | |
| 2 | Identifier | Text Input | ✅ | ✅ | Readonly for internal |
| 3 | Control | Textarea (3 rows) | ✅ | ✅ | |
| 4 | Description | Textarea (3 rows) | ✅ | ✅ | |

**Exclude Subpolicy Button**: Top right, red border, smaller

---

### Version Type Selection
```html
<div class="version-type-selection">
  <label>
    <input type="radio" value="minor" />
    Minor Version (e.g., 1.1)
  </label>
  <label>
    <input type="radio" value="major" />
    Major Version (e.g., 2.0)
  </label>
</div>
```

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

Every field has 3 colored circles:

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

---

## 🎨 Key CSS Classes

```css
/* Container */
.VV-container {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.08);
  padding: 32px 24px;
}

/* Toggle Group */
.VV-toggle-group { display: flex; gap: 0; margin-bottom: 20px; }
.VV-toggle {
  background: transparent;
  border: none;
  color: #555;
  padding: 10px 30px;
  font-size: 1.1rem;
  position: relative;
}
.VV-toggle.VV-active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 3px;
  background: #3d5afe;
}

/* Info Cards */
.vv-info-cards { display: flex; gap: 20px; margin-bottom: 32px; }
.vv-info-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  padding: 24px;
  flex: 1;
  min-width: 300px;
  border: 1px solid #e2e8f0;
}
.vv-info-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.12);
}
.vv-info-card-icon {
  background: #ebf4ff;
  color: #3d5afe;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Form Inputs */
.VV-input, .VV-textarea {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #bfcfff;
  border-radius: 8px;
  background: white;
}
.VV-input:focus, .VV-textarea:focus {
  border-color: #3d5afe;
  box-shadow: 0 0 0 2px rgba(61,90,254,0.08);
}

/* Policy Tabs */
.VV-policy-tabs {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  scrollbar-width: thin;
}
.VV-policy-tab {
  background: #f5f7ff;
  border: 1px solid #bfcfff;
  color: #2a3a5e;
  padding: 10px 32px;
  border-radius: 8px 8px 0 0;
  cursor: pointer;
  flex-shrink: 0;
}
.VV-policy-tab-active {
  background: #3d5afe;
  color: white;
  border-bottom: 2px solid white;
}
.VV-add-policy-tab {
  background: #e3eaff;
  border: 1px dashed #3d5afe;
  color: #3d5afe;
  border-radius: 8px;
}
.VV-add-policy-tab:hover {
  background: #3d5afe;
  color: white;
}

/* Subpolicy Tabs (same but smaller) */
.VV-subpolicy-tab { padding: 7px 22px; font-size: 0.98rem; }

/* Buttons */
.VV-submit, .VV-universal-submit-btn {
  background: #3d5afe;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 10px 32px;
  font-weight: 600;
  cursor: pointer;
}
.VV-submit:hover { background: #2a3a5e; }

.VV-exclude-policy-btn, .VV-exclude-subpolicy-btn {
  position: absolute;
  top: 18px;
  right: 34px;
  background: white;
  color: red;
  border: 1px solid red;
  border-radius: 6px;
  padding: 6px 18px;
}

/* Multi-Select Dropdown */
.selected-policy-type, .selected-policy-category, .selected-policy-subcategory {
  border: 1px solid #bfcfff;
  border-radius: 8px;
  padding: 10px 12px;
  cursor: pointer;
  background: white;
}
.selected-policy-type:hover { border-color: #3d5afe; }
.policy-type-options, .policy-category-options, .policy-subcategory-options {
  position: absolute;
  background: white;
  border: 1px solid #bfcfff;
  border-radius: 8px;
  max-height: 200px;
  overflow-y: auto;
  z-index: 1000;
}
.policy-type-option:hover { background: #f8f9fa; }
.create-new-option {
  background: #e3f2fd;
  border-top: 2px solid #2196f3;
}
```

---

## 📊 Field Summary

| Section | Fields | Required | Data Type Toggles |
|---------|--------|----------|-------------------|
| **Framework** | 8 | 8 (all) | All 8 |
| **Policy** | 14 per policy | 14 (all) | All 14 |
| **Subpolicy** | 4 per subpolicy | 4 (all) | All 4 |
| **Version Type** | 2 radio buttons | 1 | No |

**Total**: Dynamic (can be 50+ fields for multiple policies/subpolicies)

---

## 🎬 Key Features

1. ✅ 2-tab system (Framework / Policy)
2. ✅ Dynamic policy & subpolicy tabs with scrollable horizontal tabs
3. ✅ Data type classification on every field (3 circles)
4. ✅ Auto-generated identifiers (readonly)
5. ✅ Multi-select dropdowns with search + create new
6. ✅ Searchable user dropdown (reviewer)
7. ✅ Datalist for departments
8. ✅ Version type radio selection (minor/major)
9. ✅ Exclude buttons for policies/subpolicies
10. ✅ Info cards with hover animation
11. ✅ All framework & policy dates are REQUIRED
12. ✅ Identifiers are readonly for internal frameworks

**This is the complete, concise spec for Lovable to build VV Versioning page.** 🚀
