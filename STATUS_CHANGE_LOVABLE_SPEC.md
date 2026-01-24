# Status Change Requests & Details - Lovable Spec

## 🎯 Overview
**Routes**: `/policy/status-change-requests`, `/policy/status-change-details/:requestId`  
**Purpose**: Review and approve/reject framework/policy status change requests (Active → Inactive)

## 📐 Layout
- **Requests**: margin-left 280px, padding-right 40px, margin-top 45px
- **Details**: margin-left 200px, padding 32px 40px, max-width calc(100vw - 240px)

---

# A. STATUS CHANGE REQUESTS PAGE

## 📋 Header
```html
<div class="statuschange-header">
  <h2 class="statuschange-heading">Status Change Approval Tasks</h2>
</div>
```
**Style**: 30px font, #1f2937, 60×3px gradient underline (#3b82f6 → #8b5cf6)

## 🎛️ Filters Row (1–2 dropdowns)

### Framework Filter (always)
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

### User Selection (Admin only)
```html
<div v-if="isAdministrator" class="framework_filter_block">
  <div class="framework_filter_label">
    <i class="fas fa-users"></i>
    <span>USER SELECTION</span>
  </div>
  <select v-model="selectedUserId" class="framework_filter_dropdown">
    <option value="" disabled>Select a user...</option>
    <option v-for="user in availableUsers" :value="user.UserId">
      {{ user.UserName }} ({{ user.Role }}) - ID: {{ user.UserId }}
    </option>
  </select>
</div>
```

## 🔄 Tabs (2)
```html
<div class="tabs-container">
  <div class="tabs">
    <button class="tab-button" :class="{ active: activeTab === 'myTasks' }">
      My Tasks
      <span class="tab-count">{{ myTasksCount }}</span>
    </button>
    <button class="tab-button" :class="{ active: activeTab === 'reviewerTasks' }">
      Reviewer Tasks
      <span class="tab-count">{{ reviewerTasksCount }}</span>
    </button>
  </div>
</div>
```

## 📋 Tab Content

### Pending (CollapsibleTable)
- **Headers**: Name, Type, Category/Department, Request Date, Reason, Actions
- **Rows**: From `myTasksPendingTableRows` / `reviewerTasksPendingTableRows`
- Click row → navigate to Details page

### Non-Pending (Framework Grid)
```html
<div class="framework-grid">
  <div class="framework-card" v-for="request in ...">
    <div class="framework-header">
      <i :class="request.ItemType === 'policy' ? 'fas fa-file-alt' : 'fas fa-book'"></i>
      <span>{{ request.FrameworkName || request.PolicyName }}</span>
    </div>
    <div class="category-tag">{{ Category/Department }}: {{ value }}</div>
    <div class="framework-description">{{ request.Reason }}</div>
    <div class="framework-footer">
      <div class="status-toggle">
        <input type="checkbox" :checked="request.Status === 'Approved'" disabled />
        <span class="switch-label">{{ Active|Inactive|Pending }}</span>
      </div>
      <button class="view-btn" @click="openRequestDetails(request)"><i class="fas fa-eye"></i></button>
    </div>
  </div>
</div>
```

### No Tasks / Loading
- **Loading**: `.loading-indicator` — spinner + "Loading my tasks..." / "Loading reviewer tasks..."
- **No tasks**: `.no-tasks-message` — icon, "No My Tasks" / "No Reviewer Tasks", short message

## 📄 Details Modal (in-page before navigation)

**Note**: Requests page can show a details modal; navigation to Details page uses same structure. Below applies to both modal and Details page.

### Modal Header
```html
<h3>
  <span class="detail-type-indicator">{{ POLICY|FRAMEWORK }} STATUS CHANGE REQUEST</span>
  Details: {{ name }}
  <span class="version-pill">Version: {{ Version }}</span>
</h3>
<span class="close-x" @click="close">×</span>
```

### Status Change Approval Section
- **Request Type**: "Change Status to Inactive" (`.status-value.status-inactive`)
- **Status**: Approved | Rejected | Pending Approval (badges)
- **Actions** (if Pending + reviewer): Approve, Reject
- **Restriction** (if Pending + not reviewer): `.reviewer-restriction-message` — icon + text
- **Result** (if not Pending): Remarks, Approved Date

### Request Details (Display Only)
| # | Label | Value |
|---|-------|-------|
| 1 | Policy/Framework Name | `FrameworkName` or `PolicyName` |
| 2 | Department/Category | `Department` or `Category` |
| 3 | Request Date | `formatDate(RequestDate)` |
| 4 | Current Status | Active or Inactive |
| 5 | Reason for Change | `Reason` |
| 6 | Cascade to Policies *(framework)* | Yes/No + `(N policies will be affected)` |
| 7 | Cascade to Subpolicies *(policy)* | Yes/No + `(N subpolicies will be affected)` |

### Affected Policies / Subpolicies
- **Section title**: "Affected Subpolicies" (policy) or "Affected Policies" (framework)
- **Description**: conditional on Status (approved vs pending)
- **List**: `.policy-item` — header (name + status badge), details (Identifier, Department/Control, Description)
- **Summary** (if Pending): `.affected-policies-summary` — warning "All of these… will be changed to **Inactive**…"
- **Empty** (cascade but none): `.no-policies-message` — "No active policies…"

### Approval Implications (if Pending)
- **If approved**: framework → Inactive; optional "N policies also inactive"
- **If rejected**: framework remains Active

---

# B. STATUS CHANGE DETAILS PAGE

## 📋 Header
```html
<div class="page-header">
  <div class="header-left">
    <button class="back-btn" @click="goBack"><i class="fas fa-arrow-left"></i></button>
    <div class="page-title">
      <div class="page-title-primary">
        <span class="detail-type-indicator">Policy|Framework Status Change Request</span>
      </div>
      <div class="page-title-secondary">
        <span class="page-title-details">Details: {{ name }}</span>
        <span class="version-pill">Version: {{ Version }}</span>
      </div>
    </div>
  </div>
</div>
```

## ⏳ Loading / ❌ Error
- **Loading**: `.loading-container` — spinner + "Loading status change request details..."
- **Error**: `.error-container` — icon, "Error Loading Request", message, **Try Again** (`.retry-btn`)

## 📄 Content
Same as Details modal: Status Change Approval, Request Details, Affected Policies/Subpolicies, Approval Implications.  
Approve/Reject use **PopupService.confirm** + **PopupService.comment** (remarks optional); no form fields in page.

---

## 📊 Field Summary

| Page | Section | Fields | Editable |
|------|---------|--------|----------|
| **Requests** | Filters | Framework Filter | ✅ |
| **Requests** | Filters | User Selection | ✅ (Admin only) |
| **Requests** | Pending table | Name, Type, Category/Department, Date, Reason, Actions | ❌ Display + actions |
| **Requests** | Cards | Name, Category/Dept, Reason, Status, View | ❌ Display + view |
| **Modal / Details** | Request details | Name, Category/Dept, Request Date, Status, Reason, Cascade | ❌ Display only |
| **Modal / Details** | Affected | Policy/Subpolicy name, status, Identifier, Dept/Control, Description | ❌ Display only |
| **Modal / Details** | Actions | Approve, Reject | ✅ (reviewer only; remarks via popup) |

**No v-model form inputs** in either page except filter dropdowns. Approve/Reject remarks collected via PopupService.

---

## 🎨 Key CSS Classes

```css
/* Requests Container */
.statuschange-container {
  margin-left: 280px;
  padding-right: 40px;
  margin-top: 45px;
  min-height: 100vh;
  background: white;
}
.statuschange-heading {
  font-size: 30px;
  font-weight: 600;
  color: #1f2937;
}
.statuschange-heading::after {
  content: '';
  display: block;
  width: 60px;
  height: 3px;
  background: linear-gradient(90deg, #3b82f6, #8b5cf6);
  margin-top: 8px;
  border-radius: 2px;
}

/* Filters (shared with Framework Approver) */
.framework_filter_section { display: flex; gap: 16px; margin-bottom: 24px; }
.framework_filter_block {
  flex: 1;
  background: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 12px;
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

/* Tabs */
.tabs-container { margin-bottom: 24px; }
.tabs { display: flex; gap: -2px; border-bottom: 1px solid #e0e0e0; }
.tab-button {
  background: #f8f9fa;
  padding: 12px 24px;
  font-size: 1rem; font-weight: 600;
  color: #333;
  border-radius: 8px 8px 0 0;
  display: flex; align-items: center; gap: 8px;
}
.tab-button.active {
  background: #4f6cff;
  color: white;
  border-bottom: 3px solid #4f6cff;
}
.tab-count {
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.9rem; font-weight: 600;
}

/* Grid & Cards */
.framework-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 24px;
}
.framework-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  padding: 20px;
}
.framework-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0,0,0,0.1);
}
.framework-header { display: flex; align-items: center; gap: 12px; }
.framework-header i { color: #4f6cff; }
.category-tag { position: absolute; top: 20px; right: 20px; font-size: 0.8rem; background: #f0f0f0; padding: 4px 8px; border-radius: 4px; }
.framework-description { color: #666; font-size: 0.9rem; -webkit-line-clamp: 2; overflow: hidden; }
.framework-footer { display: flex; justify-content: space-between; align-items: center; margin-top: auto; }
.status-toggle { display: flex; align-items: center; gap: 8px; }
.switch-label.active { color: #22a722; }
.switch-label.inactive { color: #e53935; }
.switch-label.pending { color: #f5a623; }
.view-btn {
  width: 32px; height: 32px;
  border-radius: 50%;
  background: #f5f6fa;
  color: #4f6cff;
  display: flex; align-items: center; justify-content: center;
}
.view-btn:hover { background: #4f6cff; color: white; }

/* Modal */
.framework-details-modal {
  position: fixed; inset: 0;
  background: rgba(0,0,0,0.5);
  display: flex; justify-content: center; align-items: center;
  z-index: 1000;
}
.framework-details-content {
  background: white;
  border-radius: 12px;
  width: 90%; max-width: 900px;
  max-height: 85vh;
  overflow-y: auto;
  padding: 32px;
  position: relative;
}
.detail-type-indicator {
  font-size: 0.9rem;
  padding: 4px 10px;
  border-radius: 8px;
  background: #ffebee;
  color: #e53935;
  font-weight: 600;
}
.version-pill { font-size: 0.85rem; padding: 2px 8px; border-radius: 10px; background: #f0f0f0; color: #666; }
.close-x { position: absolute; top: 1px; right: 10px; font-size: 2rem; cursor: pointer; }

/* Approval Section */
.framework-approval-section {
  background: #f9faff;
  border-radius: 10px;
  padding: 20px;
  margin-bottom: 24px;
}
.framework-approval-section h4 { color: #4f6cff; }
.status-approved { background: #e8f7ee; color: #22a722; }
.status-inactive { background: #ffebee; color: #e53935; }
.status-pending { background: #fff5e6; color: #f5a623; }
.approve-btn { background: #22a722; color: white; padding: 10px 20px; border-radius: 8px; }
.reject-btn { background: #e53935; color: white; padding: 10px 20px; border-radius: 8px; }
.reviewer-restriction-message {
  display: flex; align-items: center; gap: 12px;
  background: #e3f0ff;
  border: 1px solid #b3d9ff;
  border-radius: 8px;
  padding: 16px;
  color: #4f6cff;
}

/* Request Details */
.framework-detail-row {
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
  display: flex; flex-wrap: wrap;
}
.framework-detail-row strong { width: 180px; color: #444; }
.cascade-yes { color: #22a722; font-weight: 600; }
.cascade-no { color: #e53935; font-weight: 600; }
.policy-count { color: #666; font-size: 0.85rem; margin-left: 6px; }

/* Affected Section */
.affected-policies-section {
  background: #f9faff;
  border-radius: 10px;
  padding: 20px;
  margin-bottom: 24px;
}
.policy-item {
  background: white;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.policy-name { font-weight: 600; color: #4f6cff; }
.policy-status.active { background: #e8f7ee; color: #22a722; }
.policy-status.inactive { background: #ffebee; color: #e53935; }
.affected-policies-summary { background: #fff5e6; border-radius: 10px; padding: 16px; }
.summary-warning { display: flex; align-items: center; gap: 12px; color: #f5a623; }
.no-policies-message {
  display: flex; align-items: center; gap: 12px;
  background: #e3f0ff;
  border-radius: 10px;
  padding: 16px;
  color: #4f6cff;
}

/* Implications */
.approval-implications { background: #f9faff; border-radius: 10px; padding: 20px; }
.implication-item.warning { background: #fff5e6; }
.implication-item.info { background: #e3f0ff; }

/* Details Page */
.status-change-details-page {
  margin-left: 200px;
  padding: 32px 40px;
  max-width: calc(100vw - 240px);
  min-height: 100vh;
  background: #fff;
}
.back-btn {
  width: 40px; height: 40px;
  border-radius: 50%;
  background: transparent;
  border: none;
  color: #333;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.back-btn:hover { background: rgba(0,0,0,0.06); }
.loading-spinner {
  width: 40px; height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #4f6cff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}
.retry-btn { background: #4f6cff; color: white; padding: 8px 16px; border-radius: 6px; font-weight: 600; }
```

---

## 🎬 Key Features

1. ✅ Framework + User filters (User: Admin only)
2. ✅ My Tasks / Reviewer Tasks tabs with counts
3. ✅ Pending: CollapsibleTable; non-pending: card grid
4. ✅ Cards: icon, name, category/dept, reason, status toggle (disabled), view
5. ✅ Details modal or page: type pill, version, approval section, request details, affected list
6. ✅ Approve/Reject (reviewer only); remarks via PopupService
7. ✅ Reviewer restriction message when not assigned
8. ✅ Status badges: Approved (green), Rejected (red), Pending (amber)
9. ✅ Cascade to Policies / Subpolicies + affected count
10. ✅ Approval implications when Pending
11. ✅ Loading and empty states
12. ✅ Responsive: stacked filters, full-width tabs on small screens

**This is the complete, concise spec for Lovable to build Status Change Requests & Details.** 🚀
