# Upload Framework - Complete Field List

## 🎯 Overview
**Page**: `UploadFramework.vue`  
**Path**: `/create-policy/upload-framework`

---

## 📋 FIELD INVENTORY BY STEP

### **STEP 1: Upload Document**
| Field | Type | v-model | Notes |
|-------|------|---------|-------|
| File Input | File | `selectedFile` | PDF, DOC, DOCX, TXT, XLS, XLSX |

**UI State**:
- `isDragOver` - drag & drop state
- `isUploading` - upload progress state
- `isLoadingDefault` - loading PCI DSS data state

---

### **STEP 2: Processing**
**No editable fields - Display only**

**Status Fields**:
- `processingStatus.progress` - 0-100%
- `processingStatus.message` - current status text
- `processingStatus.currentSection` - section being processed
- `uploadedFileName` - name of file being processed

---

### **STEP 3: Content Selection**

#### **Search & Filters**
| Field | Type | v-model | Options |
|-------|------|---------|---------|
| Search | Text Input | `searchQuery` | Filter sections/policies |
| View Mode | Select | `viewMode` | `collapsed`, `expanded` |
| Filter Type | Select | `filterType` | `all`, `policies`, `compliance` |

#### **Hierarchical Checkboxes**
| Level | Field | v-model | Notes |
|-------|-------|---------|-------|
| Section | Checkbox | `section.selected` | Top level |
| Subsection | Checkbox | `subsection.selected` | 2nd level (indent 20px) |
| Subpolicy | Checkbox | `subpolicy.selected` | 3rd level (indent 40px) |

---

### **STEP 4: AI Compliance Generation**
**No editable fields - Display only**

**Status Fields**:
- `complianceGenerationMessage` - AI generation status
- `complianceGenerationProgress` - 0-100%
- `complianceStats.total_subpolicies`
- `complianceStats.processed_subpolicies`
- `complianceStats.total_compliances`

---

### **STEP 5: Overview Statistics**
**No editable fields - Display only**

**Stats Display**:
- `overviewStats.total_sections`
- `overviewStats.total_policies`
- `overviewStats.total_subpolicies`
- `overviewStats.total_compliances`

---

### **STEP 6: Edit Policy Details**

## 📝 **A. FRAMEWORK FORM (7 Fields)**

| # | Field Label | v-model | Type | Required | Notes |
|---|-------------|---------|------|----------|-------|
| 1 | Framework Name | `frameworkForm.FrameworkName` | Text Input | ✅ | |
| 2 | Version | `frameworkForm.CurrentVersion` | Text Input | | Default: '1.0' |
| 3 | Description | `frameworkForm.FrameworkDescription` | Textarea (3 rows) | | |
| 4 | Category | `frameworkForm.Category` | Text Input | | |
| 5 | Identifier | `frameworkForm.Identifier` | Text Input | | |
| 6 | Status | `frameworkForm.Status` | Select | | Options: Under Review, Approved, Rejected |
| 7 | Reviewer | `frameworkForm.Reviewer` | Text Input | | |

**Additional Framework Fields** (in data model but not shown in basic form):
- `StartDate` - Date
- `EndDate` - Date
- `EffectiveDate` - Date
- `CreatedByName` - Default: 'Admin'

---

## 📄 **B. POLICY FORM (7 Fields per Policy)**

| # | Field Label | v-model | Type | Required | Notes |
|---|-------------|---------|------|----------|-------|
| 1 | Policy Title | `policy.policy_title` | Text Input | ✅ | |
| 2 | Description | `policy.policy_description` | Textarea (3 rows) | | |
| 3 | Policy Type | `policy.policy_type` | Text Input | | |
| 4 | Category | `policy.policy_category` | Text Input | | |
| 5 | Subcategory | `policy.policy_subcategory` | Text Input | | |
| 6 | Scope | `policy.scope` | Textarea (2 rows) | | |
| 7 | Objective | `policy.objective` | Textarea (2 rows) | | |

**Additional Policy Fields** (in data model):
- `policy_id` - Auto-generated badge display

---

## 📑 **C. SUBPOLICY FORM (3 Fields per Subpolicy)**

| # | Field Label | v-model | Type | Required | Notes |
|---|-------------|---------|------|----------|-------|
| 1 | Subpolicy Title | `subpolicy.subpolicy_title` | Text Input | ✅ | |
| 2 | Description | `subpolicy.subpolicy_description` | Textarea (2 rows) | | |
| 3 | Control | `subpolicy.control` | Textarea (3 rows) | | |

**Additional Subpolicy Fields** (in data model):
- `subpolicy_id` - ID badge display

---

## ✅ **D. COMPLIANCE FORM (8 Fields per Compliance)**

| # | Field Label | v-model | Type | Required | Options | Notes |
|---|-------------|---------|------|----------|---------|-------|
| 1 | Compliance Title | `compliance.ComplianceTitle` | Text Input | ✅ | | |
| 2 | Description | `compliance.ComplianceItemDescription` | Textarea (3 rows) | | | |
| 3 | Type | `compliance.ComplianceType` | Select | | Regulatory, Internal, External | |
| 4 | Criticality | `compliance.Criticality` | Select | | Low, Medium, High, Critical | |
| 5 | Mandatory/Optional | `compliance.MandatoryOptional` | Select | | Mandatory, Optional | |
| 6 | Maturity Level | `compliance.MaturityLevel` | Select | | Initial, Developing, Defined, Managed, Optimized | |
| 7 | Possible Damage | `compliance.PossibleDamage` | Textarea (2 rows) | | | |
| 8 | Risk Category | `compliance.RiskCategory` | Text Input | | | |

---

## 🔍 **ALTERNATIVE VIEW: Content Viewer Modal**

When viewing extracted content, additional fields appear:

| # | Field Label | v-model | Type | Notes |
|---|-------------|---------|------|-------|
| 1 | Section | `currentPolicy.section_name` | Text Input | |
| 2 | Control ID | `currentPolicy.Sub_policy_id` | Text Input | |
| 3 | Policy Name | `currentPolicy.sub_policy_name` | Text Input | |
| 4 | Control | `currentPolicy.control` | Textarea (8 rows) | |
| 5 | Related Controls | `currentPolicy.related_controls` | Text Input | |
| 6 | Control Enhancements | `currentPolicy.control_enhancements` | Textarea (5 rows) | |

---

## 📊 FIELD COUNT SUMMARY

| Component | Count | Required Fields | Notes |
|-----------|-------|-----------------|-------|
| **Framework** | 7 main + 4 hidden | 1 (Name) | Single form at top |
| **Policy** | 7 per policy | 1 (Title) | Multiple instances (dynamic) |
| **Subpolicy** | 3 per subpolicy | 1 (Title) | Nested under policies |
| **Compliance** | 8 per compliance | 1 (Title) | Generated by AI, editable |
| **Content Viewer** | 6 alternative fields | 0 | Modal view for detailed editing |
| **Filters/Search** | 3 controls | 0 | Step 3 only |

**Total Editable Fields**: **25 base fields** + **Dynamic fields** based on uploaded document

**Typical Document**:
- 1 Framework = 7 fields
- 10 Policies = 70 fields
- 50 Subpolicies = 150 fields
- 100 Compliances = 800 fields
- **TOTAL: ~1,027 fields** for a medium-sized framework

---

## 🎨 VISUAL HIERARCHY

```
Framework (Blue Border - #007bff)
├── Section 1
│   ├── Policy 1 (Green Border - #28a745)
│   │   ├── Subpolicy 1.1 (Yellow Border - #ffc107)
│   │   │   ├── Compliance 1.1.1 (Red Border - #dc3545)
│   │   │   └── Compliance 1.1.2 (Red Border - #dc3545)
│   │   └── Subpolicy 1.2 (Yellow Border - #ffc107)
│   └── Policy 2 (Green Border - #28a745)
└── Section 2
    └── ...
```

**Indentation**:
- Framework: 0px
- Policy: +20px (margin-left)
- Subpolicy: +40px (margin-left)
- Compliance: +60px (margin-left)

---

## 🚀 KEY FEATURES

1. **Dynamic Form Generation** - Fields created based on AI extraction
2. **Hierarchical Editing** - 4-level nested structure
3. **Bulk Selection** - Checkbox tree in Step 3
4. **Real-time Progress** - Animated processing in Steps 2 & 4
5. **Pre-populated Data** - AI fills all fields automatically
6. **Manual Override** - Edit any field before saving
7. **Color-coded Levels** - Visual hierarchy with border colors
8. **Search & Filter** - Find specific sections/policies
9. **View Modes** - Collapsed/Expanded tree views
10. **Save All** - Single button saves entire framework hierarchy

---

## 💾 DATA FLOW

```
Upload File → AI Processing → Extract Sections → 
Select Content → Generate Compliances → Review Stats → 
Edit All Fields → Save to Database
```

**All fields are editable in Step 6 before final save.**
