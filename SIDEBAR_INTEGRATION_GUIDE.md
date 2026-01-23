# Sidebar Integration Guide for All Vendors Page

This guide explains how to add the "All Vendors" link to your application's sidebar navigation.

## TPRM Application Sidebar

### Location
Look for the sidebar component in your TPRM application. Common locations:
- `grc_frontend/tprm_frontend/src/components/VendorLayout.vue`
- `grc_frontend/tprm_frontend/src/components/AppSidebar.vue`
- `grc_frontend/tprm_frontend/src/components/layout/Sidebar.vue`

### Add Menu Item

Find the navigation menu section and add:

```vue
<template>
  <div class="sidebar">
    <!-- Existing menu items -->
    
    <!-- Add this new menu item -->
    <router-link 
      to="/all-vendors" 
      class="sidebar-link"
      active-class="active"
    >
      <i class="fas fa-building"></i>
      <span>All Vendors</span>
    </router-link>
    
    <!-- Or if using a submenu structure -->
    <div class="menu-group">
      <div class="menu-group-title">
        <i class="fas fa-users"></i>
        <span>Vendor Management</span>
      </div>
      <div class="menu-group-items">
        <router-link to="/vendor-registration" class="sidebar-link">
          <i class="fas fa-user-plus"></i>
          <span>Add Vendor</span>
        </router-link>
        <router-link to="/all-vendors" class="sidebar-link">
          <i class="fas fa-building"></i>
          <span>All Vendors</span>
        </router-link>
        <!-- Other vendor-related links -->
      </div>
    </div>
  </div>
</template>
```

### Recommended Icons
- `fa-building` - Building icon (default)
- `fa-list` - List icon
- `fa-table` - Table icon
- `fa-users` - Users/vendors icon
- `fa-warehouse` - Warehouse/vendors icon

## Main GRC Application Sidebar

### Location
Typically in:
- `grc_frontend/src/components/Sidebar.vue`
- `grc_frontend/src/components/Layout.vue`

### Add Menu Item

```vue
<template>
  <!-- Existing sidebar structure -->
  
  <!-- Management Section -->
  <div class="sidebar-section">
    <h3 class="section-title">Management</h3>
    <ul class="menu-list">
      <!-- Existing items -->
      
      <!-- Add All Vendors -->
      <li>
        <router-link 
          to="/management/all-vendors"
          class="menu-item"
          active-class="active"
        >
          <i class="fas fa-building"></i>
          <span>All Vendors</span>
        </router-link>
      </li>
    </ul>
  </div>
</template>
```

## Permission-Based Display

If using RBAC, wrap the menu item with permission check:

```vue
<template>
  <!-- TPRM App -->
  <router-link 
    v-if="hasPermission('view')"
    to="/all-vendors" 
    class="sidebar-link"
  >
    <i class="fas fa-building"></i>
    <span>All Vendors</span>
  </router-link>
</template>

<script>
import { computed } from 'vue'
import permissionsService from '@/services/permissionsService'

export default {
  setup() {
    const hasPermission = computed(() => {
      return permissionsService.checkVendorPermission('view')
    })
    
    return { hasPermission }
  }
}
</script>
```

## Styling Examples

### Minimal Style
```css
.sidebar-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  color: #4a5568;
  text-decoration: none;
  transition: all 0.2s;
}

.sidebar-link:hover {
  background: #f7fafc;
  color: #2563eb;
}

.sidebar-link.active {
  background: #eff6ff;
  color: #2563eb;
  border-left: 3px solid #2563eb;
}

.sidebar-link i {
  width: 1.25rem;
  text-align: center;
}
```

### Enhanced Style with Badge
```vue
<template>
  <router-link to="/all-vendors" class="sidebar-link">
    <i class="fas fa-building"></i>
    <span>All Vendors</span>
    <span v-if="vendorCount > 0" class="badge">{{ vendorCount }}</span>
  </router-link>
</template>

<style scoped>
.badge {
  margin-left: auto;
  background: #2563eb;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
}
</style>
```

## Complete Example with Submenu

```vue
<template>
  <div class="sidebar">
    <!-- Dashboard -->
    <router-link to="/dashboard" class="sidebar-link">
      <i class="fas fa-home"></i>
      <span>Dashboard</span>
    </router-link>

    <!-- Vendor Management Submenu -->
    <div class="menu-group">
      <button 
        class="menu-group-toggle"
        @click="vendorMenuOpen = !vendorMenuOpen"
      >
        <i class="fas fa-users"></i>
        <span>Vendor Management</span>
        <i 
          class="fas fa-chevron-down toggle-icon"
          :class="{ rotated: vendorMenuOpen }"
        ></i>
      </button>
      
      <transition name="submenu">
        <div v-show="vendorMenuOpen" class="submenu">
          <router-link to="/vendor-registration" class="submenu-link">
            <i class="fas fa-user-plus"></i>
            <span>Add Vendor</span>
          </router-link>
          
          <router-link to="/all-vendors" class="submenu-link">
            <i class="fas fa-building"></i>
            <span>All Vendors</span>
            <span class="badge badge-info">{{ totalVendors }}</span>
          </router-link>
          
          <router-link to="/vendor-approval-dashboard" class="submenu-link">
            <i class="fas fa-check-circle"></i>
            <span>Approvals</span>
            <span v-if="pendingApprovals > 0" class="badge badge-warning">
              {{ pendingApprovals }}
            </span>
          </router-link>
          
          <router-link to="/lifecycle" class="submenu-link">
            <i class="fas fa-project-diagram"></i>
            <span>Lifecycle Tracker</span>
          </router-link>
          
          <router-link to="/risk-scoring" class="submenu-link">
            <i class="fas fa-shield-alt"></i>
            <span>Risk Scoring</span>
          </router-link>
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from '@/config/axios'

export default {
  setup() {
    const vendorMenuOpen = ref(false)
    const totalVendors = ref(0)
    const pendingApprovals = ref(0)

    const fetchVendorStats = async () => {
      try {
        const response = await axios.get('/api/v1/management/vendors/all/')
        if (response.data.success) {
          totalVendors.value = response.data.total
        }
      } catch (error) {
        console.error('Error fetching vendor stats:', error)
      }
    }

    onMounted(() => {
      fetchVendorStats()
    })

    return {
      vendorMenuOpen,
      totalVendors,
      pendingApprovals
    }
  }
}
</script>

<style scoped>
.sidebar {
  width: 260px;
  height: 100vh;
  background: #fff;
  border-right: 1px solid #e2e8f0;
  overflow-y: auto;
}

.sidebar-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.875rem 1.25rem;
  color: #4a5568;
  text-decoration: none;
  transition: all 0.2s;
  font-size: 0.875rem;
}

.sidebar-link:hover {
  background: #f7fafc;
  color: #2563eb;
}

.sidebar-link.active {
  background: #eff6ff;
  color: #2563eb;
  font-weight: 600;
}

.menu-group {
  margin: 0.5rem 0;
}

.menu-group-toggle {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.875rem 1.25rem;
  border: none;
  background: transparent;
  color: #4a5568;
  cursor: pointer;
  font-size: 0.875rem;
  transition: all 0.2s;
}

.menu-group-toggle:hover {
  background: #f7fafc;
  color: #2563eb;
}

.toggle-icon {
  margin-left: auto;
  font-size: 0.75rem;
  transition: transform 0.2s;
}

.toggle-icon.rotated {
  transform: rotate(180deg);
}

.submenu {
  background: #f7fafc;
  overflow: hidden;
}

.submenu-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1.25rem 0.75rem 3rem;
  color: #4a5568;
  text-decoration: none;
  font-size: 0.8125rem;
  transition: all 0.2s;
}

.submenu-link:hover {
  background: #e2e8f0;
  color: #2563eb;
}

.submenu-link.active {
  background: #dbeafe;
  color: #2563eb;
  font-weight: 600;
}

.badge {
  margin-left: auto;
  padding: 0.125rem 0.5rem;
  border-radius: 9999px;
  font-size: 0.6875rem;
  font-weight: 600;
}

.badge-info {
  background: #dbeafe;
  color: #1e40af;
}

.badge-warning {
  background: #fef3c7;
  color: #92400e;
}

/* Transition for submenu */
.submenu-enter-active,
.submenu-leave-active {
  transition: all 0.3s ease;
}

.submenu-enter-from,
.submenu-leave-to {
  max-height: 0;
  opacity: 0;
}

.submenu-enter-to,
.submenu-leave-from {
  max-height: 500px;
  opacity: 1;
}
</style>
```

## Quick Setup Checklist

1. **Locate Sidebar Component**
   - [ ] Find sidebar file in your project
   - [ ] Identify menu structure (flat or nested)

2. **Add Menu Item**
   - [ ] Add router-link with correct path
   - [ ] Choose appropriate icon
   - [ ] Add label text

3. **Add Styling**
   - [ ] Match existing sidebar styles
   - [ ] Add hover and active states
   - [ ] Ensure responsive behavior

4. **Add Permissions (if needed)**
   - [ ] Import permission service
   - [ ] Add v-if condition
   - [ ] Test with different user roles

5. **Test Navigation**
   - [ ] Click link from sidebar
   - [ ] Verify page loads correctly
   - [ ] Check active state highlighting
   - [ ] Test on different screen sizes

## Common Issues & Solutions

### Issue: Menu item not showing
**Solution:** Check if:
- Path is correct in router configuration
- Component is properly imported
- Permissions are set correctly

### Issue: Active state not working
**Solution:** Ensure:
- `active-class="active"` is set on router-link
- Active CSS class is defined
- Router is using correct matching mode

### Issue: Icon not displaying
**Solution:** Verify:
- Font Awesome is loaded
- Icon class name is correct
- CSS doesn't override icon display

## Next Steps

After adding to sidebar:
1. Test the navigation flow
2. Verify permissions work correctly
3. Check mobile responsiveness
4. Add analytics tracking (optional)
5. Update user documentation

---

Need help? Check the main implementation files or review the routing configuration.
