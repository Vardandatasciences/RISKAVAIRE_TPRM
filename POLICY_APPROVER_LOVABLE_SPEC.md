# Policy Approver Page - Lovable Spec

## 🎯 Overview
**Route**: `/policy/approver`  
**Purpose**: Review and approve/reject policies, subpolicies, and compliances

## 📐 Layout
- Sidebar: 280px left
- Main: margin-left 280px, padding-top 20px, padding-right 50px

---

## 📋 Header Section

```html
<div class="policy_header">
  <h1 class="policy_title">Policy Approval</h1>
  <p class="policy_subtitle">Review and manage policy approval requests</p>
</div>
```

---

## 🎛️ Filters Row

### User Selection (Admin Only)
```html
<div class="policy_user_selection">
  <div class="policy_user_card">
    <div class="policy_user_header">
      <i class="fas fa-user-cog"></i>
      <span>USER SELECTION</span>
    </div>
    <select v-model="selectedUserId" class="policy_user_dropdown">
      <option v-for="user in availableUsers" :value="user.UserId">
        {{ user.UserName }} ({{ user.Role }}) - ID: {{ user.UserId }}
      </option>
    </select>
    <small v-if="!selectedUserId">Please select a user to view their tasks</small>
  </div>
</div>
```

### Framework Filter
```html
<div class="policy_filter_section">
  <label class="policy_filter_label">
    <i class="fas fa-filter"></i>
    FILTER
  </label>
  <select v-model="selectedFrameworkId" class="policy_filter_dropdown">
    <option value="">All Frameworks</option>
    <option v-for="framework in filteredFrameworks" :value="framework.id">
      {{ framework.name }}
    </option>
  </select>
</div>
```

---

## 📊 Summary Cards (3 cards)

```html
<div class="policy_summary_section">
  <div class="policy_summary_item">
    <div class="policy_summary_icon"><i class="fas fa-clock"></i></div>
    <div class="policy_summary_content">
      <div class="policy_summary_number">{{ pendingApprovalsCount }}</div>
      <div class="policy_summary_label">Pending Review</div>
    </div>
  </div>
  
  <div class="policy_summary_item clickable">
    <div class="policy_summary_icon"><i class="fas fa-check-circle"></i></div>
    <div class="policy_summary_content">
      <div class="policy_summary_number">{{ approvedApprovalsCount }}</div>
      <div class="policy_summary_label">Approved</div>
    </div>
  </div>
  
  <div class="policy_summary_item clickable">
    <div class="policy_summary_icon"><i class="fas fa-times-circle"></i></div>
    <div class="policy_summary_content">
      <div class="policy_summary_number">{{ rejectedApprovalsCount }}</div>
      <div class="policy_summary_label">Rejected</div>
    </div>
  </div>
</div>
```

**Style**: White cards, colored icons (orange, green, red), hover lift on clickable

---

## 🔄 Tab Navigation

```html
<div class="policy_nav_tabs">
  <button class="policy_nav_tab active">
    <i class="fas fa-user"></i>
    My Tasks
    <span class="policy_tab_badge">{{ myTasksCount }}</span>
  </button>
  <button class="policy_nav_tab">
    <i class="fas fa-users"></i>
    Reviewer Tasks
    <span class="policy_tab_badge">{{ reviewerTasksCount }}</span>
  </button>
</div>
```

**Style**: White bg, blue bottom border on active, badge with count

---

## 📋 Tasks Table (Collapsible)

Uses `CollapsibleTable` component with sections:
- Pending Review
- Approved
- Rejected
- Rejected Policies (Edit & Resubmit)

**Table Headers**: Policy ID, Name, Framework, Status, Actions

---

## 📄 Details Modal

### Header
```html
<h3>
  <span class="detail-type-indicator">Policy</span>
  Details: {{ policyId }}
  <span class="version-pill">Version: {{ version }}</span>
</h3>
```

### Version History
```html
<div class="version-history">
  <div class="version-info">
    <div class="version-label">Current Version:</div>
    <div class="version-value">{{ version }}</div>
  </div>
  <div class="subpolicies-versions">
    <h4>Subpolicies Versions:</h4>
    <ul class="version-list">
      <li>
        <span class="subpolicy-name">{{ SubPolicyName }}</span>
        <span class="version-tag">v{{ version }}</span>
        <span class="resubmitted-tag">Resubmitted</span>
      </li>
    </ul>
  </div>
</div>
```

### Policy Details (Display Only)
- All fields from `ExtractedData` (PolicyName, Description, Scope, Objective, etc.)
- Subpolicies list with status badges

### Action Buttons
```html
<button class="approve-btn">Approve</button>
<button class="reject-btn">Reject</button>
<button class="submit-btn">Submit Review</button>
```

---

## ❌ Reject Modal (1 Field)

```html
<div class="reject-modal">
  <div class="reject-modal-content">
    <h4>Rejection Reason</h4>
    <p>Please provide a reason for rejecting...</p>
    <textarea 
      v-model="rejectionComment" 
      class="rejection-comment" 
      placeholder="Enter your comments here...">
    </textarea>
    <div class="reject-modal-actions">
      <button class="cancel-btn">Cancel</button>
      <button class="confirm-btn">Confirm Rejection</button>
    </div>
  </div>
</div>
```

**Field**: `rejectionComment` (textarea, required)

---

## ✏️ Edit Policy Modal (Rejected Items)

### Policy Fields (6 fields)

| # | Field | Type | v-model | Notes |
|---|-------|------|---------|-------|
| 1 | Scope | Text Input | `editingPolicy.ExtractedData.Scope` | |
| 2 | Objective | Text Input | `editingPolicy.ExtractedData.Objective` | |
| 3 | Policy Type | Select | `editingPolicy.ExtractedData.PolicyType` | Dropdown with options |
| 4 | Policy Category | Select | `editingPolicy.ExtractedData.PolicyCategory` | Filtered by Type |
| 5 | Policy Sub Category | Select | `editingPolicy.ExtractedData.PolicySubCategory` | Filtered by Type+Category |
| 6 | Rejection Reason | Display Only | - | Shows rejection remarks |

### Rejected Subpolicies Section (per subpolicy, 4 fields)

| # | Field | Type | v-model | Notes |
|---|-------|------|---------|-------|
| 1 | Name | Text Input | `sub.SubPolicyName` | |
| 2 | Description | Textarea | `sub.Description` | |
| 3 | Control | Textarea | `sub.Control` | |
| 4 | Rejection Reason | Display Only | - | Shows `sub.approval?.remarks` |

**Resubmit Button**: "Resubmit for Review" (disabled if no changes)

---

## ✏️ Edit Compliance Modal (Rejected Items)

### Compliance Fields (5 fields)

| # | Field | Type | v-model | Notes |
|---|-------|------|---------|-------|
| 1 | Description | Text Input | `editingCompliance.ExtractedData.ComplianceItemDescription` | |
| 2 | Criticality | Select | `editingCompliance.ExtractedData.Criticality` | High, Medium, Low |
| 3 | Impact | Text Input | `editingCompliance.ExtractedData.Impact` | |
| 4 | Probability | Text Input | `editingCompliance.ExtractedData.Probability` | |
| 5 | Mitigation | Textarea | `editingCompliance.ExtractedData.mitigation` | |
| 6 | Rejection Reason | Display Only | - | Shows `compliance_approval?.remarks` |

**Resubmit Button**: "Resubmit for Review"

---

## ✏️ Edit Subpolicy Modal (Rejected Items)

### Subpolicy Fields (4 fields)

| # | Field | Type | v-model | Notes |
|---|-------|------|---------|-------|
| 1 | Subpolicy Name | Text Input | `editingSubpolicy.SubPolicyName` | **Disabled** |
| 2 | Identifier | Text Input | `editingSubpolicy.Identifier` | **Disabled** |
| 3 | Description | Textarea | `editingSubpolicy.Description` | Editable |
| 4 | Control | Textarea | `editingSubpolicy.Control` | Editable |
| 5 | Rejection Reason | Display Only | - | Shows `approval.remarks` |

**Changes Summary**: Shows detected changes before resubmit  
**Resubmit Button**: "Resubmit with Changes" (disabled if no changes)

---

## 🎨 Key CSS Classes

```css
/* Container */
.policy_main_container {
  margin-left: 280px;
  padding-top: 20px;
  padding-right: 50px;
  background: transparent;
}

/* Header */
.policy_title {
  font-size: 28px;
  font-weight: 700;
  color: #212529;
  margin: 0 0 8px 0;
}
.policy_subtitle {
  font-size: 14px;
  color: #6c757d;
}

/* Filters */
.policy_user_card, .policy_filter_section {
  background: white;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 16px;
}
.policy_user_dropdown, .policy_filter_dropdown {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid #ced4da;
  border-radius: 6px;
  font-size: 14px;
}
.policy_user_dropdown:focus, .policy_filter_dropdown:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59,130,246,0.1);
}

/* Summary Cards */
.policy_summary_section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px;
  margin-bottom: 32px;
}
.policy_summary_item {
  background: white;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 16px;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  transition: all 0.2s;
}
.policy_summary_item:hover {
  border-color: #3b82f6;
  box-shadow: 0 2px 8px rgba(59,130,246,0.1);
}
.policy_summary_icon {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
}
.policy_summary_number {
  font-size: 20px;
  font-weight: 700;
  color: #212529;
}
.policy_summary_label {
  font-size: 14px;
  color: #6c757d;
  font-weight: 500;
}

/* Tabs */
.policy_nav_tabs {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
}
.policy_nav_tab {
  background: white;
  border: none;
  border-radius: 6px;
  padding: 12px 20px;
  font-size: 14px;
  font-weight: 600;
  color: #495057;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 12px;
}
.policy_nav_tab.active {
  color: #3b82f6;
  border-bottom: 2px solid #3b82f6;
}
.policy_tab_badge {
  background: #e5e7eb;
  color: #4b5563;
  padding: 2px 10px;
  border-radius: 12px;
  font-size: 13px;
  font-weight: 600;
}
.policy_nav_tab.active .policy_tab_badge {
  background: #3b82f6;
  color: white;
}

/* Buttons */
.approve-btn {
  background: #22c55e;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
}
.reject-btn {
  background: #ef4444;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
}
.submit-btn {
  background: #3b82f6;
  color: white;
  border: none;
  padding: 10px 24px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
}
.resubmit-btn {
  background: #3b82f6;
  color: white;
  border: none;
  padding: 10px 24px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
}
.resubmit-btn.disabled {
  background: #ccc;
  cursor: not-allowed;
}

/* Reject Modal */
.reject-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.reject-modal-content {
  background: white;
  border-radius: 8px;
  padding: 24px;
  max-width: 500px;
  width: 90%;
}
.rejection-comment {
  width: 100%;
  min-height: 120px;
  padding: 12px;
  border: 1px solid #ced4da;
  border-radius: 6px;
  font-size: 14px;
  resize: vertical;
}
.reject-modal-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 16px;
}
.cancel-btn {
  background: #e5e7eb;
  color: #4b5563;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
}
.confirm-btn {
  background: #ef4444;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
}

/* Edit Modals */
.edit-policy-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.edit-policy-content {
  background: white;
  border-radius: 8px;
  padding: 24px;
  max-width: 800px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
}
.edit-policy-content label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #495057;
}
.edit-policy-content input,
.edit-policy-content textarea,
.edit-policy-content select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ced4da;
  border-radius: 6px;
  font-size: 14px;
  margin-bottom: 16px;
}
.rejection-reason {
  background: #fff3cd;
  border: 1px solid #ffc107;
  padding: 12px;
  border-radius: 6px;
  color: #856404;
  margin-bottom: 16px;
}
```

---

## 📊 Field Summary

| Section | Fields | Type | Editable |
|---------|--------|------|----------|
| **Filters** | User Selection | Select | ✅ (Admin only) |
| | Framework Filter | Select | ✅ |
| **Reject Modal** | Rejection Comment | Textarea | ✅ Required |
| **Edit Policy** | Scope | Text Input | ✅ |
| | Objective | Text Input | ✅ |
| | Policy Type | Select | ✅ |
| | Policy Category | Select | ✅ |
| | Policy Sub Category | Select | ✅ |
| | Rejected Subpolicies | 4 fields each | ✅ |
| **Edit Compliance** | Description | Text Input | ✅ |
| | Criticality | Select | ✅ |
| | Impact | Text Input | ✅ |
| | Probability | Text Input | ✅ |
| | Mitigation | Textarea | ✅ |
| **Edit Subpolicy** | Name | Text Input | ❌ Disabled |
| | Identifier | Text Input | ❌ Disabled |
| | Description | Textarea | ✅ |
| | Control | Textarea | ✅ |

**Total Editable Fields**: **15 base fields** + dynamic subpolicies

---

## 🎬 Key Features

1. ✅ 2 filter dropdowns (User, Framework)
2. ✅ 3 summary cards (Pending, Approved, Rejected)
3. ✅ 2 tabs (My Tasks, Reviewer Tasks)
4. ✅ Collapsible task tables with pagination
5. ✅ Details modal with version history
6. ✅ Reject modal with comment textarea
7. ✅ Edit modals for rejected items (Policy, Compliance, Subpolicy)
8. ✅ Change detection (disable resubmit if no changes)
9. ✅ Status badges (Pending, Approved, Rejected, Resubmitted)
10. ✅ Approve/Reject buttons (reviewers only)
11. ✅ Version tracking (u1, R1, etc.)
12. ✅ Review history modal integration

**This is the complete, concise spec for Lovable to build Policy Approver page.** 🚀
