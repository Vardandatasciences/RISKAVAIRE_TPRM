# Data Workflow (Tree) & TreeNode - Lovable Spec

## 🎯 Overview
**Route**: Data Workflow - Hierarchical View (sidebar)  
**Purpose**: Interactive 5-column hierarchy: Framework → Policies → Sub Policies → Compliances → Risks  
**Components**: `tree.vue` (main page), `tree.css`, `TreeNode.vue` (recursive component; optional alternate view)

## 📐 Layout
- **Container**: margin 0 2rem 0 280px, width calc(100vw - 280px - 2rem), padding 1rem 2rem 1rem 0

---

# A. DATA WORKFLOW PAGE (tree.vue)

## 📋 Header
```html
<h1 class="main-title">Data Workflow - Hierarchical View</h1>
<p class="main-subtitle">Explore your framework hierarchy interactively</p>
```

## 🎛️ Framework Selector (1 field + 2 buttons)

### Framework Dropdown
```html
<div class="framework-selector">
  <label for="framework-select">Select Framework:</label>
  <select id="framework-select" v-model="selectedFramework" class="framework-dropdown">
    <option value="">-- Choose a Framework --</option>
    <option v-for="fw in frameworks" :value="fw.FrameworkId">{{ fw.FrameworkName }}</option>
  </select>
  <div class="control-buttons">
    <button class="control-btn expand-all-btn">EXPAND ALL</button>
    <button class="control-btn collapse-btn">COLLAPSE</button>
  </div>
</div>
```
**Field**: `selectedFramework` (select, required to show tree)

## ⏳ Loading / ❌ Error / 🏁 Initial State
- **Loading**: `.loading-container` — spinner + "Loading data..."
- **Error**: `.error-container` — icon + message + **Retry** (`.retry-button`)
- **Initial** (no framework): `.initial-state` — icon + "Please select a framework from the dropdown above to view the hierarchical structure"

## 📊 Tree Visualization (5-column table)

### Table Header
| Col 1 | Col 2 | Col 3 | Col 4 | Col 5 |
|-------|-------|-------|-------|-------|
| Framework | Policies | Sub Policies | Compliances | Risks |

Classes: `.header-row`, `.framework-header`, `.policies-header`, `.subpolicies-header`, `.compliances-header`, `.risks-header`

### Framework Cell (root node)
- **Structure**: `.framework-cell` > `.root-node` > `.framework-icon-container`
- **Content**: `.framework-icon` (fa-sitemap), `.framework-name` (selectedFrameworkName)
- **Hover**: `.framework-tooltip` (title), Teleported `.metadata-tooltip` (type badge + filtered metadata key-value list)
- **Click**: toggle expand/collapse (`.framework-icon.expanded`)

### Policy Nodes (column 2)
- **Structure**: `.policy-node` inside `.vertical-nodes` (`.policies-cell`)
- **Content**: `.node-label` (PolicyName), `.expand-icon` (chevron, `.rotated` when expanded)
- **Hover**: `.node-tooltip`, `.metadata-tooltip` (type: policy)
- **Click**: toggle policy expand
- **Data**: `policy.id`, `policy.PolicyName`

### Subpolicy Nodes (column 3)
- **Structure**: `.subpolicy-node` inside `.vertical-nodes` (`.subpolicies-cell`); shown when parent policy expanded
- **Content**: `.node-label` (SubPolicyName), `.expand-icon`
- **Hover**: `.node-tooltip`, `.metadata-tooltip` (type: subpolicy)
- **Click**: toggle subpolicy expand
- **Data**: `subpolicy.id`, `subpolicy.SubPolicyName`
- **Classes**: `getSubPolicyClasses` adds `expanded`, `child-of-policy-{id}`

### Compliance Nodes (column 4)
- **Structure**: `.compliance-node` inside `.vertical-nodes` (`.compliances-cell`); shown when parent subpolicy expanded
- **Content**: `.node-label` (ComplianceTitle or 'Compliance'), `.expand-icon`
- **Hover**: `.node-tooltip`, `.metadata-tooltip` (type: compliance)
- **Click**: toggle compliance expand
- **Data**: `compliance.id`, `compliance.ComplianceTitle`
- **Classes**: `getComplianceClasses` adds `expanded`, `child-of-subpolicy-{id}`

### Risk Nodes (column 5, leaf)
- **Structure**: `.risk-node` inside `.vertical-nodes` (`.risks-cell`); shown when parent compliance expanded
- **Content**: `.node-label` (RiskTitle or 'Risk'); **no** expand icon
- **Hover**: `.node-tooltip`, `.metadata-tooltip` (type: risk)
- **Data**: `risk.id`, `risk.RiskTitle`

### Connection Lines
- **SVG**: `.connection-lines-container` with `<path>` per connection (`connectionPaths`)
- **Props**: `path`, `stroke` (color), `stroke-width="2"`, `stroke-dasharray` (dashed or solid), `opacity="0.7"`

### Metadata Tooltip (all node types)
- **Header**: `h3` (name), `.metadata-type-badge` (framework | policy | subpolicy | compliance | risk)
- **Body**: `.metadata-content` — either "Loading metadata...", "No additional metadata available", or `.metadata-item` list (`formatLabel(key)`, `formatValue(value)`)

---

# B. TREE NODE COMPONENT (TreeNode.vue)

**Note**: Recursive component; not used in main 5-column tree. Use when building an alternate hierarchical tree.

### Structure
```html
<div class="tree-branch" :data-level="level" :data-index="siblingIndex" :data-count="siblingCount">
  <div class="node-wrapper">
    <div class="node-box" :class="[nodeClass, { 'clickable': hasChildren, 'expanded': isExpanded }]">
      <i :class="nodeIcon"></i>
      <span>{{ getNodeTitle() }}</span>
      <i v-if="hasChildren" class="expand-icon fas fa-chevron-down" :class="{ 'rotated': isExpanded }"></i>
    </div>
    <div v-if="isExpanded && (children.length > 0 || loading)" class="vertical-line"></div>
  </div>
  <div v-if="isExpanded" class="children-wrapper" :class="{ 'nested-children': level > 1 }">
    <div v-if="loading" class="loading-children">...</div>
    <div v-else-if="children.length > 1" class="horizontal-line"></div>
    <div class="tree-children">
      <TreeNode v-for="child in children" :node="child" :level="level+1" ... />
    </div>
  </div>
</div>
```

### Props
| Prop | Type | Default |
|------|------|---------|
| node | Object | required |
| level | Number | 1 |
| siblingIndex | Number | 0 |
| siblingCount | Number | 1 |

### Node types & titles
- **policy**: PolicyName, icon `fa-file-alt`
- **subpolicy**: SubPolicyName, icon `fa-file`
- **compliance**: ComplianceTitle \|\| 'Compliance', icon `fa-check-circle`
- **risk**: RiskTitle \|\| 'Risk', icon `fa-exclamation-triangle` (no children)

### CSS Classes (TreeNode has no dedicated CSS; style these if used)
- `.tree-branch`, `.node-wrapper`, `.node-box`, `.expand-icon`, `.rotated`
- `.vertical-line`, `.horizontal-line`, `.children-wrapper`, `.nested-children`, `.tree-children`
- `.loading-children`, `.{type}-node` (e.g. `.policy-node`)

---

## 📊 Field Summary

| Section | Fields | Type | Editable |
|---------|--------|------|----------|
| **Framework selector** | Select Framework | Select | ✅ |
| **Control buttons** | EXPAND ALL, COLLAPSE | Buttons | ❌ Actions only |
| **Tree** | All node labels, metadata | Display | ❌ |

**Total editable**: **1** (framework dropdown). All tree content is display + expand/collapse + hover tooltips.

---

## 🎨 Key CSS (tree.css)

```css
/* Container */
.tree-container {
  min-height: 100vh;
  background: transparent;
  margin: 0 2rem 0 280px;
  width: calc(100vw - 280px - 2rem);
  padding: 1rem 2rem 1rem 0;
}
.main-title { font-size: 2.2rem; font-weight: 700; color: #1f2937; margin: 2rem 0 0.5rem 0; }
.main-subtitle { font-size: 1rem; color: #6b7280; margin: 0 0 1.5rem 0; }

/* Framework selector */
.framework-selector { display: flex; align-items: center; gap: 1rem; flex-wrap: wrap; }
.framework-selector label { font-weight: 600; color: #2c3e50; font-size: 1.1rem; }
.framework-dropdown {
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  border: 2px solid #d1d5db;
  border-radius: 8px;
  background: white;
  min-width: 300px;
  max-width: 400px;
}
.framework-dropdown:focus { outline: none; border-color: #6366f1; box-shadow: 0 0 0 3px rgba(99,102,241,0.1); }
.control-buttons { display: flex; gap: 0.5rem; margin-left: 420px; }
.control-btn { padding: 0.35rem 0.65rem; border: none; border-radius: 6px; font-weight: 600; font-size: 0.75rem; cursor: pointer; }
.expand-all-btn { background: #3b82f6; color: white; }
.collapse-btn { background: #6b7280; color: white; }

/* Loading / Error / Initial */
.loading-container, .error-container { display: flex; flex-direction: column; align-items: center; padding: 3rem 1rem; }
.loading-container i { font-size: 2.5rem; color: #6366f1; }
.error-container i { font-size: 3rem; color: #dc2626; }
.retry-button { padding: 0.6rem 1.2rem; background: #3b82f6; color: white; border: none; border-radius: 6px; font-weight: 600; }
.initial-state { display: flex; flex-direction: column; align-items: center; padding: 4rem 2rem; color: #666; }
.initial-state i { font-size: 5rem; opacity: 0.5; color: #d1d5db; }

/* Tree */
.tree-visualization { background: white; padding: 2rem; overflow: auto; min-height: calc(100vh - 200px); position: relative; }
.connection-lines-container { position: absolute; inset: 0; pointer-events: none; z-index: 1; }
.tree-table { display: table; width: 100%; border-collapse: separate; border-spacing: 0; }
.tree-row { display: table-row; }
.tree-cell { display: table-cell; vertical-align: top; padding: 1rem; }
.header-row .tree-cell { font-weight: 600; font-size: 1rem; color: #374151; padding: 1rem; }
.framework-cell { width: 20%; }
.policies-cell, .subpolicies-cell, .compliances-cell, .risks-cell { width: 20%; vertical-align: top; }

/* Nodes */
.vertical-nodes { display: flex; flex-direction: column; gap: 1.5rem; align-items: center; min-height: 120px; padding: 1rem 0; }
.tree-node { cursor: pointer; transition: all 0.3s ease; width: 100%; justify-content: center; align-items: center; }
.node-content {
  display: flex; align-items: center; gap: 0.75rem;
  padding: 0.75rem 1.25rem;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
  min-width: 180px; max-width: 250px;
  position: relative; z-index: 2;
}
.node-label { font-weight: 600; font-size: 0.9rem; color: #2c3e50; flex: 1; text-overflow: ellipsis; overflow: hidden; white-space: nowrap; text-align: center; }
.expand-icon { font-size: 0.8rem; color: #6b7280; transition: transform 0.3s; }
.expand-icon.rotated { transform: rotate(90deg); }

/* Framework root */
.framework-icon-container { display: flex; flex-direction: column; align-items: center; padding: 1rem; min-height: 120px; cursor: pointer; }
.framework-icon { font-size: 2.8rem; color: #6b7280; }
.framework-icon.expanded { color: #374151; transform: scale(1.1); }
.framework-name { font-size: 1.1rem; font-weight: 700; color: #111827; text-align: center; max-width: 250px; min-width: 150px; }

/* Node type colors */
.policy-node .node-content { background: #f0fdf4; border-color: #bbf7d0; color: #166534; }
.subpolicy-node .node-content { background: #fffbeb; border-color: #fde68a; color: #92400e; }
.compliance-node .node-content { background: #eff6ff; border-color: #bfdbfe; color: #1e40af; }
.risk-node .node-content { background: #fef2f2; border-color: #fecaca; color: #dc2626; }
.root-node .node-content { background: #f9fafb; border-color: #d1d5db; color: #374151; }

/* Tooltips */
.node-tooltip, .framework-tooltip {
  position: absolute;
  background: rgba(0,0,0,0.8);
  color: white;
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
  font-size: 0.8rem;
  opacity: 0; visibility: hidden;
  transition: all 0.3s ease;
  z-index: 1000;
  max-width: 200px/300px;
  overflow: hidden; text-overflow: ellipsis;
}
.node-content:hover .node-tooltip,
.framework-icon-container:hover .framework-tooltip { opacity: 1; visibility: visible; }

/* Metadata tooltip (Teleport) */
.metadata-tooltip {
  position: fixed;
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.15);
  min-width: 320px; max-width: 450px;
  max-height: 500px;
  overflow-y: auto;
  z-index: 99999;
}
.metadata-header { display: flex; justify-content: space-between; align-items: center; padding: 1rem 1.25rem; border-bottom: 2px solid #f3f4f6; background: linear-gradient(135deg,#f9fafb,#fff); border-radius: 12px 12px 0 0; }
.metadata-header h3 { margin: 0; font-size: 1.1rem; font-weight: 700; color: #111827; overflow: hidden; text-overflow: ellipsis; }
.metadata-type-badge { padding: 0.25rem 0.75rem; background: linear-gradient(135deg,#6366f1,#8b5cf6); color: white; border-radius: 20px; font-size: 0.75rem; font-weight: 600; }
.metadata-content { padding: 1rem 1.25rem; max-height: 400px; overflow-y: auto; }
.metadata-item { display: flex; padding: 0.75rem 0; border-bottom: 1px solid #f3f4f6; }
.metadata-label { font-weight: 600; color: #374151; font-size: 0.875rem; min-width: 140px; margin-right: 0.75rem; }
.metadata-value { color: #6b7280; font-size: 0.875rem; flex: 1; word-break: break-word; }
.metadata-empty { padding: 1rem; text-align: center; color: #9ca3af; font-style: italic; }
.metadata-loading { padding: 1rem; text-align: center; color: #6366f1; }
```

---

## 🎬 Key Features

1. ✅ One dropdown: Select Framework
2. ✅ EXPAND ALL / COLLAPSE buttons
3. ✅ 5-column table: Framework | Policies | Sub Policies | Compliances | Risks
4. ✅ Click to expand/collapse framework, policies, subpolicies, compliances (risks are leaves)
5. ✅ SVG curved connection lines between nodes
6. ✅ Inline tooltip (node title) + rich metadata tooltip (type badge + key-value list) on hover
7. ✅ Node type colors: framework (gray), policy (green), subpolicy (amber), compliance (blue), risk (red)
8. ✅ Loading, error, initial (no framework) states
9. ✅ Custom scrollbar on tree area
10. ✅ Responsive: stacked layout, smaller nodes on small screens
11. ✅ TreeNode.vue: recursive branch layout (optional); vertical/horizontal connector lines, loading children

**Use tree.css for main page. TreeNode classes are not in tree.css; add styles if using TreeNode.**

**This is the complete, concise spec for Lovable to build Data Workflow (Tree) & TreeNode.** 🚀
