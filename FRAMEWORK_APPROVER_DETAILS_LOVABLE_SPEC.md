# Framework Approver & Framework Details - Lovable Spec

## 🎯 Overview
**Routes**: `/framework/approver`, `/framework/details/:id`  
**Purpose**: Review and approve/reject frameworks, policies, and subpolicies

## 📐 Layout
- Sidebar: 250px left (Approver), 230px (Details)
- Main: margin-left 250px, padding 50px 32px (Approver); margin-left 230px, padding 24px 32px (Details)

---

# A. FRAMEWORK APPROVER PAGE

## 📋 Header
```html
<div class="framework_header">
  <h1 class="framework_title">Framework Approval</h1>
  <p class="framework_subtitle">Review and manage framework approval requests</p>
</div>
```

## 🎛️ Filters Row (2 dropdowns)

### User Selection (GRC Admin Only)
```html
<div class="framework_filter_block">
  <div class="framework_filter_label">
    <i class="fas fa-users"></i>
    <span>USER SELECTION</span>
  </div>
  <select v-model="selectedUserId" class="framework_filter_dropdown">
    <option v-for="user in availableUsers" :value="user.UserId">
      {{ user.UserName }} ({{ user.Role }}) - ID: {{ user.UserId }}
    </option>
  </select>
</div>
```

### Framework Filter
```html
<div class="framework_filter_block">
  <div class="framework_filter_label">
    <i class="fas fa-filter"></i>
    <span>FRAMEWORK FILTER</span>
  </div>
  <select v-model="selectedFrameworkId" class="framework_filter_dropdown">
    <option value="">All Frameworks</option>
    <option v-for="fw in filteredFrameworks" :value="fw.id">{{ fw.name }}</option>
  </select>
</div>
```

## 📊 Summary Cards (3)
```html
<div class="framework_summary_section">
  <div class="framework_summary_item">
    <div class="framework_summary_icon pending"><i class="fas fa-clock"></i></div>
    <div class="framework_summary_content">
      <div class="framework_summary_number">{{ pendingApprovalsCount }}</div>
      <div class="framework_summary_label">Pending Review</div>
    </div>
  </div>
  <div class="framework_summary_item clickable">...</div>  <!-- Approved -->
  <div class="framework_summary_item clickable">...</div>  <!-- Rejected -->
</div>
```

## 🔄 Tabs (2)
```html
<div class="framework_nav_tabs">
  <button class="framework_nav_tab active">
    <i class="fas fa-user"></i> My Tasks
    <span class="framework_tab_badge">{{ myTasksCount }}</span>
  </button>
  <button class="framework_nav_tab">
    <i class="fas fa-users"></i> Reviewer Tasks
    <span class="framework_tab_badge">{{ reviewerTasksCount }}</span>
  </button>
</div>
```

## 📋 Tasks Table
Uses `CollapsibleTable`. Sections: Pending, Approved, Rejected, **Rejected Frameworks (Edit & Resubmit)**.  
**Headers**: Framework ID, Name, Category, Created By, Created Date, Status, Actions.

## ❌ Reject Modal (1 Field)
```html
<div class="reject-modal">
  <div class="reject-modal-content">
    <h4>Rejection Reason</h4>
    <p>Please provide a reason for rejecting this {{ currentRejectionType }}</p>
    <textarea v-model="rejectionComment" class="rejection-comment" 
      placeholder="Enter your comments here..."></textarea>
    <div class="reject-modal-actions">
      <button class="cancel-btn">Cancel</button>
      <button class="confirm-btn">Confirm Rejection</button>
    </div>
  </div>
</div>
```
**Field**: `rejectionComment` (textarea, required)

## ✏️ Edit Framework Modal (Rejected Items)

### Framework Form (6 fields)
| # | Field | Type | v-model |
|---|-------|------|---------|
| 1 | Framework Name | Text Input | `editingFramework.ExtractedData.FrameworkName` |
| 2 | Category | Text Input | `editingFramework.ExtractedData.Category` |
| 3 | Effective Date | Date | `editingFramework.ExtractedData.EffectiveDate` |
| 4 | Framework Description | Textarea | `editingFramework.ExtractedData.FrameworkDescription` |
| 5 | Start Date | Date | `editingFramework.ExtractedData.StartDate` |
| 6 | End Date | Date | `editingFramework.ExtractedData.EndDate` |
| 7 | Rejection Reason | Display Only | `editingFramework.rejection_reason` |

**Layout**: 2-column grid (`.form-columns`)

### Per-Policy Form (7 fields)
| # | Field | Type | v-model |
|---|-------|------|---------|
| 1 | Policy Name | Text Input | `policy.PolicyName` |
| 2 | Description | Textarea | `policy.PolicyDescription` |
| 3 | Objective | Textarea | `policy.Objective` |
| 4 | Scope | Textarea | `policy.Scope` |
| 5 | Policy Type | Select | `policy.PolicyType` |
| 6 | Policy Category | Select | `policy.PolicyCategory` |
| 7 | Policy Sub Category | Select | `policy.PolicySubCategory` |

### Per-Subpolicy Form (4 fields)
| # | Field | Type | v-model |
|---|-------|------|---------|
| 1 | Sub-Policy Name | Text Input | `subpolicy.SubPolicyName` |
| 2 | Description | Textarea | `subpolicy.Description` |
| 3 | Control | Textarea | `subpolicy.Control` |
| 4 | Identifier | Text Input | `subpolicy.Identifier` |

**Resubmit**: "Resubmit for Review" (disabled if `!hasFrameworkChanges`). **No Changes** warning: yellow box.

---

# B. FRAMEWORK DETAILS PAGE

## 📋 Header
```html
<div class="framework_header">
  <div class="framework_header_left">
    <button class="policy-dashboard-back-btn" @click="goBack">
      <i class="fas fa-arrow-left"></i>
    </button>
    <h1 class="framework_title">
      Framework Details: {{ frameworkId }}
      <span class="version-text">(Version: {{ version }})</span>
    </h1>
  </div>
</div>
```

## ⏳ Loading / ❌ Error
- **Loading**: spinner + "Loading framework details..."
- **Error**: icon + message + **Try Again** button (`.framework_retry_btn`)

## 📄 Framework Approval Section
- **Status**: Approved / Rejected / Under Review (badges)
- **Approved Date** (if approved)
- **Buttons**: Final Approval, Approve Framework, Reject, Submit Review

## 📄 Framework Information (Display Only)
- All `ExtractedData` keys (except policies, framework_approval, type, totalPolicies, totalSubpolicies)
- Grid: `200px` label | `1fr` value (`.framework_detail_row`)

## 📄 Policies Section
Per policy:
- **Header**: Policy name, status badge, Approve/Reject buttons (reviewers only)
- **Details**: Description, Objective, Scope, Department, Applicability, Identifier, Coverage Rate, Policy Type, Category, Sub Category
- **Subpolicies**: SubPolicyName, Description, Control, Identifier, status, Approve/Reject

## ❌ Reject Modal
Same as Approver: `rejectionComment` textarea, Cancel, Confirm Rejection.

## 🎨 Key CSS (Approver + Details)

```css
/* Approver Container */
.framework_main_container {
  margin-left: 250px;
  padding: 50px 32px;
  max-width: 1400px;
  background: transparent;
}

/* Filters */
.framework_filter_section { display: flex; gap: 16px; margin-bottom: 24px; }
.framework_filter_block {
  flex: 1;
  background: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 16px;
}
.framework_filter_label {
  display: flex; align-items: center; gap: 8px;
  margin-bottom: 12px;
  font-size: 0.75rem; font-weight: 500; color: #6c757d;
  text-transform: uppercase; letter-spacing: 0.5px;
}
.framework_filter_dropdown {
  width: 100%; padding: 8px 12px;
  border: 1px solid #ced4da; border-radius: 4px;
  font-size: 14px; height: 38px;
}
.framework_filter_dropdown:focus { border-color: #6366f1; }

/* Summary Cards */
.framework_summary_section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px;
  margin-bottom: 32px;
}
.framework_summary_item {
  background: #fff; border: 1px solid #e0e0e0;
  border-radius: 8px; padding: 16px;
  display: flex; align-items: flex-start; gap: 12px;
}
.framework_summary_item:hover { border-color: #3b82f6; box-shadow: 0 2px 8px rgba(59,130,246,0.1); }
.framework_summary_icon.pending { color: #f59e0b; }
.framework_summary_icon.approved { color: #22c55e; }
.framework_summary_icon.rejected { color: #ef4444; }
.framework_summary_number { font-size: 20px; font-weight: 700; color: #212529; }
.framework_summary_label { font-size: 14px; color: #6c757d; }

/* Tabs */
.framework_nav_tab {
  padding: 12px 24px; border: none; background: white;
  border-radius: 6px; font-size: 14px; font-weight: 500;
  color: #495057; cursor: pointer;
  display: flex; align-items: center; gap: 12px;
}
.framework_nav_tab.active {
  color: #3b82f6;
  border-bottom: 2px solid #3b82f6;
}
.framework_tab_badge {
  background: rgba(0,0,0,0.1);
  padding: 2px 8px; border-radius: 12px;
  font-size: 12px; font-weight: 600;
}

/* Reject Modal */
.reject-modal {
  position: fixed; inset: 0;
  background: rgba(0,0,0,0.7);
  display: flex; align-items: center; justify-content: center;
  z-index: 1100;
}
.reject-modal-content {
  background: #fff; border-radius: 12px; padding: 24px;
  width: 90%; max-width: 500px;
}
.rejection-comment {
  width: 100%; min-height: 120px;
  padding: 12px; border: 1px solid #e2e8f0;
  border-radius: 8px; resize: vertical;
}
.cancel-btn { background: #e2e8f0; color: #4a5568; padding: 10px 20px; border-radius: 8px; }
.confirm-btn { background: #e53e3e; color: white; padding: 10px 20px; border-radius: 8px; }

/* Edit Framework Modal */
.edit-framework-modal {
  position: fixed; inset: 0;
  background: rgba(0,0,0,0.5);
  display: flex; align-items: center; justify-content: center;
  z-index: 1000;
}
.edit-framework-content {
  background: #fff; border-radius: 12px;
  width: 90%; max-width: 900px; max-height: 90vh;
  overflow-y: auto;
}
.form-columns { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
.form-field label { font-size: 14px; font-weight: 600; color: #495057; }
.form-field input, .form-field textarea {
  padding: 10px 14px;
  border: 1px solid #ced4da; border-radius: 6px;
  font-size: 14px;
}
.rejection-reason {
  padding: 12px; background: #fee;
  border-left: 3px solid #f56565; color: #c53030;
}
.resubmit-btn { background: #3b82f6; color: white; padding: 12px 24px; border-radius: 8px; font-weight: 600; }
.resubmit-btn:disabled { background: #cbd5e0; cursor: not-allowed; }
.no-changes-warning {
  display: flex; gap: 12px; padding: 16px;
  background: #fef3c7; border: 1px solid #f59e0b; border-radius: 8px;
}

/* Details Page */
.framework_details_page { margin-left: 230px; padding: 24px 32px; }
.policy-dashboard-back-btn {
  background: white; border: 2px solid #e2e8f0;
  border-radius: 8px; padding: 6px 12px;
  color: #4f6cff; font-weight: 600; cursor: pointer;
}
.policy-dashboard-back-btn:hover { background: #4f6cff; color: white; }
.framework_detail_row {
  display: grid;
  grid-template-columns: 200px 1fr;
  gap: 16px; padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}
.status-approved { background: #d1f4e0; color: #0c6e3e; }
.status-rejected { background: #fed7d7; color: #c53030; }
.status-pending { background: #fef5e7; color: #c27803; }
.approve-btn { background: #38a169; color: white; }
.reject-btn { background: #e53e3e; color: white; }
.submit-btn { background: #4299e1; color: white; }
.final-approve-btn { background: #22543d; color: white; }
```

---

## 📊 Field Summary

| Page | Section | Fields | Editable |
|------|---------|--------|----------|
| **Approver** | Filters | User, Framework | ✅ (User: Admin only) |
| **Approver** | Reject Modal | Rejection Comment | ✅ Required |
| **Approver** | Edit Framework | 6 framework + 7 per policy + 4 per subpolicy | ✅ |
| **Details** | Framework Info | All ExtractedData | ❌ Display only |
| **Details** | Reject Modal | Rejection Comment | ✅ Required |

**Approver total editable**: 2 filters + 1 reject field + 6 framework + N×(7 policy + M×4 subpolicy)

---

## 🎬 Key Features

1. ✅ User + Framework filters (User: GRC Admin only)
2. ✅ 3 summary cards (Pending, Approved, Rejected)
3. ✅ My Tasks / Reviewer Tasks tabs
4. ✅ Collapsible task tables + Rejected Frameworks (Edit & Resubmit)
5. ✅ Reject modal with comment (framework/policy/subpolicy)
6. ✅ Edit Framework modal: 2-column form, policies, subpolicies
7. ✅ Framework Details: back button, version, status, approve/reject/submit
8. ✅ Details: framework info grid, policies list, subpolicies per policy
9. ✅ Change detection; Resubmit disabled when no changes
10. ✅ Status badges (Approved, Rejected, Pending)
11. ✅ Responsive: single column filters, stacked forms

**Use FrameworkApprover.css + FrameworkDetails.css for full styles.**

**This is the complete, concise spec for Lovable to build Framework Approver & Details.** 🚀
