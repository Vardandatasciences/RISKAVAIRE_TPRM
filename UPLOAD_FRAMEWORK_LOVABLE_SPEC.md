# AI Policy Upload Framework - Lovable Spec

## 🎯 Overview
**Route**: `/create-policy/upload-framework`  
**Purpose**: Upload framework documents (PDF/DOC/XLS) → AI extracts → Edit → Save

## 📐 Layout
- Sidebar: 280px left (shared component)
- Main: margin-left 260px, padding 20px

## 🔢 6-Step Workflow with Progress Bar

```html
<div class="step-indicator">
  <!-- 6 steps with circles, labels, connecting lines -->
  Step 1: Upload Document
  Step 2: Processing  
  Step 3: Content Selection
  Step 4: Generate Compliances
  Step 5: Overview
  Step 6: Edit Policy Details
</div>
```

**Styles**: Horizontal step indicator, active=blue circle+text, completed=checkmark, connecting lines between

---

## 📝 STEP 1: Upload Document

### Upload Zone (Drag & Drop)
```html
<div class="upload-area drag-over">
  <h3>Drag & Drop framework file</h3>
  <p>or click to browse</p>
  <small>PDF, DOC, DOCX, TXT, XLS, XLSX</small>
</div>
```
**Style**: Dashed border #007bff, padding 40px, center text, hover=solid border

### File Preview Card
```html
<div class="file-preview">
  <i class="fas fa-file"></i>
  <h4>filename.pdf</h4>
  <p>2.5 MB</p>
  <button class="remove-btn">×</button>
  <button class="upload-btn">Upload Framework</button>
</div>
```

### OR Divider + Default Data Button
```html
<div class="or-divider">
  <div class="divider-line"></div>
  <span>OR</span>
</div>
<button class="load-default-btn">Load PCI DSS 2 Data</button>
```

---

## ⚙️ STEP 2: Processing Animation

### Animated Processing Section
```html
<div class="processing-section">
  <!-- Document icon with animated waves -->
  <div class="document-processing-visual">
    <i class="fas fa-file-pdf"></i>
    <div class="processing-waves">
      <div class="wave wave-1"></div>
      <div class="wave wave-2"></div>
      <div class="wave wave-3"></div>
    </div>
  </div>
  
  <h3>Processing Framework Document</h3>
  <p>Extracting document sections...</p>
  
  <!-- 6 Processing Stages with dots -->
  <div class="processing-stages">
    <div class="stage active">Document Analysis</div>
    <div class="stage">Text Extraction</div>
    <div class="stage">Structure Processing</div>
    <div class="stage">Content Mapping</div>
    <div class="stage">Hierarchy Building</div>
    <div class="stage">Finalizing</div>
  </div>
  
  <!-- Progress Bar -->
  <div class="progress-bar">
    <div class="progress-fill" style="width: 45%"></div>
    <div class="progress-glow"></div>
  </div>
  <div class="progress-percentage">45%</div>
</div>
```

**Animations**: Waves pulse outward, dots fade in/out, progress fills left-to-right

---

## ✅ STEP 3: Content Selection (Checkbox Tree)

### Search + View Mode + Filter
```html
<div class="search-box">
  <input type="text" placeholder="Search sections..." />
</div>
<select class="view-mode-select">
  <option>Collapsed View</option>
  <option>Expanded View</option>
</select>
<select class="filter-type-select">
  <option>All Types</option>
  <option>Policies Only</option>
  <option>Compliance Only</option>
</select>
```

### Hierarchical Checkbox Tree
```html
<div class="content-selection-tree">
  <!-- Section Level -->
  <div class="section-item">
    <input type="checkbox" /> Section Title
    <!-- Subsection Level (indent 20px) -->
    <div class="subsection-item">
      <input type="checkbox" /> Subsection Title
      <!-- Subpolicy Level (indent 40px) -->
      <div class="subpolicy-item">
        <input type="checkbox" /> Subpolicy Title
      </div>
    </div>
  </div>
</div>

<button class="proceed-btn">Proceed with Selected Content</button>
```

**Style**: Nested indentation 20px per level, blue checkboxes, expand/collapse icons

---

## 🤖 STEP 4: AI Compliance Generation

### Processing Status
```html
<div class="compliance-generation-section">
  <div class="ai-icon-animation">🤖</div>
  <h3>AI Compliance Generation</h3>
  <p class="ai-processing-status">Analyzing policies...</p>
  
  <!-- Progress with glowing effect -->
  <div class="progress-bar">
    <div class="progress-fill glow"></div>
  </div>
  <p>65% Complete</p>
</div>
```

---

## 📊 STEP 5: Overview (Statistics)

### Stats Cards
```html
<div class="overview-section">
  <h3>Framework Overview</h3>
  
  <div class="stats-grid">
    <div class="stat-card">
      <i class="fas fa-folder"></i>
      <h4>12</h4>
      <p>Sections</p>
    </div>
    <div class="stat-card">
      <i class="fas fa-file"></i>
      <h4>45</h4>
      <p>Policies</p>
    </div>
    <div class="stat-card">
      <i class="fas fa-list"></i>
      <h4>128</h4>
      <p>Subpolicies</p>
    </div>
    <div class="stat-card">
      <i class="fas fa-check"></i>
      <h4>89</h4>
      <p>Compliances</p>
    </div>
  </div>
  
  <button class="proceed-btn">Proceed to Edit</button>
  <button class="upload-another-btn">Upload Another</button>
</div>
```

**Style**: 4 cards grid, white bg, blue icons, box-shadow, hover lift

---

## ✏️ STEP 6: Edit Policy Details (Vertical Forms)

### Framework Form (7 fields)
```html
<div class="framework-level">
  <h3>Framework Details</h3>
  <label>Framework Name *</label>
  <input type="text" required />
  
  <label>Version</label>
  <input type="text" />
  
  <label>Description</label>
  <textarea rows="3"></textarea>
  
  <label>Category</label>
  <input type="text" />
  
  <label>Identifier</label>
  <input type="text" />
  
  <label>Status</label>
  <select>
    <option>Under Review</option>
    <option>Approved</option>
  </select>
  
  <label>Reviewer</label>
  <input type="text" />
</div>
```

### Policy Form (7 fields per policy)
```html
<div class="policy-level">
  <h4>Policy: [Title]</h4>
  <label>Policy Title *</label>
  <input type="text" />
  
  <label>Description</label>
  <textarea rows="3"></textarea>
  
  <label>Policy Type</label>
  <input type="text" />
  
  <label>Category</label>
  <input type="text" />
  
  <label>Subcategory</label>
  <input type="text" />
  
  <label>Scope</label>
  <textarea rows="2"></textarea>
  
  <label>Objective</label>
  <textarea rows="2"></textarea>
</div>
```

### Subpolicy Form (6 fields per subpolicy)
```html
<div class="subpolicy-level">
  <h5>Subpolicy: [Title]</h5>
  <label>Subpolicy Title *</label>
  <input type="text" />
  
  <label>Description</label>
  <textarea rows="3"></textarea>
  
  <label>Requirements</label>
  <textarea rows="2"></textarea>
  
  <label>Testing Procedures</label>
  <textarea rows="2"></textarea>
  
  <label>Guidance</label>
  <textarea rows="2"></textarea>
  
  <label>Reference</label>
  <input type="text" />
</div>
```

### Compliance Form (4 fields per compliance)
```html
<div class="compliance-level">
  <h6>Compliance: [Number]</h6>
  <label>Compliance Number</label>
  <input type="text" />
  
  <label>Title</label>
  <input type="text" />
  
  <label>Description</label>
  <textarea rows="2"></textarea>
  
  <label>Testing Procedure</label>
  <textarea rows="2"></textarea>
</div>
```

### Save Button
```html
<button class="save-framework-btn">
  <i class="fas fa-save"></i>
  Save Framework
</button>
```

---

## 🎨 Key CSS Classes

```css
/* Layout */
.upload-framework-container { margin-left: 260px; padding: 20px; }

/* Step Indicator */
.step-indicator { display: flex; align-items: center; gap: 10px; }
.step-item { display: flex; flex-direction: column; align-items: center; }
.step-number { width: 40px; height: 40px; border-radius: 50%; 
  border: 2px solid #ddd; display: flex; align-items: center; 
  justify-content: center; background: white; }
.step-item.active .step-number { background: #007bff; color: white; 
  border-color: #007bff; }
.step-item.completed .step-number { background: #28a745; }
.step-divider { width: 60px; height: 2px; background: #ddd; }
.step-label { font-size: 12px; margin-top: 8px; }

/* Upload Area */
.upload-area { border: 2px dashed #007bff; border-radius: 8px; 
  padding: 60px; text-align: center; cursor: pointer; 
  transition: all 0.3s; }
.upload-area:hover, .upload-area.drag-over { 
  border-style: solid; background: #f0f8ff; }

/* Processing Animation */
.processing-waves { position: relative; }
.wave { width: 100px; height: 100px; border-radius: 50%; 
  border: 2px solid #007bff; position: absolute; 
  animation: wave-pulse 2s infinite; opacity: 0; }
.wave-1 { animation-delay: 0s; }
.wave-2 { animation-delay: 0.7s; }
.wave-3 { animation-delay: 1.4s; }

@keyframes wave-pulse {
  0% { transform: scale(0.5); opacity: 0.8; }
  100% { transform: scale(2); opacity: 0; }
}

/* Progress Bar */
.progress-bar { width: 100%; height: 8px; background: #e9ecef; 
  border-radius: 4px; overflow: hidden; position: relative; }
.progress-fill { height: 100%; background: linear-gradient(90deg, 
  #007bff, #00bcd4); transition: width 0.3s; }
.progress-glow { position: absolute; width: 100px; height: 100%; 
  background: rgba(255,255,255,0.3); animation: glow-move 2s infinite; }

@keyframes glow-move {
  0% { left: -100px; }
  100% { left: 100%; }
}

/* Stats Cards */
.stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); 
  gap: 20px; }
.stat-card { background: white; padding: 30px; border-radius: 8px; 
  text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1); 
  transition: transform 0.2s; }
.stat-card:hover { transform: translateY(-5px); }
.stat-card i { font-size: 40px; color: #007bff; }
.stat-card h4 { font-size: 36px; margin: 10px 0; color: #333; }

/* Forms */
.v-form-row { margin-bottom: 15px; }
.v-form-row label { display: block; margin-bottom: 5px; 
  font-weight: 500; color: #333; font-size: 14px; }
.v-form-row input, .v-form-row textarea, .v-form-row select { 
  width: 100%; padding: 10px; border: 1px solid #ddd; 
  border-radius: 4px; font-size: 14px; }

/* Level Sections */
.framework-level { background: #f8f9fa; border-left: 4px solid #007bff; 
  padding: 20px; margin-bottom: 20px; }
.policy-level { background: #fff; border-left: 4px solid #28a745; 
  padding: 20px; margin: 10px 0 10px 20px; }
.subpolicy-level { background: #fff; border-left: 4px solid #ffc107; 
  padding: 15px; margin: 10px 0 10px 40px; }
.compliance-level { background: #fff; border-left: 4px solid #dc3545; 
  padding: 15px; margin: 10px 0 10px 60px; }

/* Buttons */
.upload-btn, .proceed-btn, .save-framework-btn { 
  background: #007bff; color: white; padding: 12px 24px; 
  border: none; border-radius: 6px; font-size: 14px; cursor: pointer; 
  transition: background 0.2s; }
.upload-btn:hover { background: #0056b3; }
.load-default-btn { background: #28a745; color: white; }
.upload-another-btn { background: #6c757d; color: white; }
.remove-btn { background: none; border: none; color: #dc3545; 
  font-size: 20px; cursor: pointer; }
```

---

## 📋 Field Summary

| Level | Fields | Required |
|-------|--------|----------|
| Framework | 7 | Name, Status |
| Policy | 7 | Title |
| Subpolicy | 6 | Title |
| Compliance | 4 | Number, Title |

**Total**: Dynamic based on uploaded document (can be 100+ fields)

---

## 🎬 Key Features

1. ✅ 6-step wizard with progress tracking
2. ✅ Drag-drop file upload with preview
3. ✅ Animated processing with real-time status
4. ✅ Hierarchical checkbox tree (3 levels)
5. ✅ AI compliance generation
6. ✅ Statistics overview with cards
7. ✅ Vertical forms for editing all extracted data
8. ✅ Color-coded hierarchy (blue→green→yellow→red)
9. ✅ Search + filter + view mode controls
10. ✅ Back navigation + Save framework

**This is the complete, concise specification for Lovable to build the AI Policy Upload page.** 🚀
