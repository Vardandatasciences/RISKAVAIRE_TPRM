# Vendor Type Classification Logic

## Visual Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Vendor Classification                     │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────┐
        │  Check vendor_code in vendors table   │
        └───────────────────────────────────────┘
                            │
                ┌───────────┴───────────┐
                │                       │
            YES │                       │ NO
                ▼                       ▼
        ┌───────────────┐       ┌───────────────┐
        │ ONBOARDED     │       │ TEMPORARY     │
        │ VENDOR        │       │ VENDOR        │
        └───────────────┘       └───────────────┘
                │                       │
                ▼                       ▼
    Check temp_vendor.response_id   Check temp_vendor.response_id
                │                       │
        ┌───────┴───────┐       ┌───────┴───────┐
        │               │       │               │
    NOT NULL        NULL    NOT NULL        NULL
        │               │       │               │
        ▼               ▼       ▼               ▼
┌───────────────┐ ┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│   TYPE 1      │ │   TYPE 2      │ │   TYPE 3      │ │   TYPE 4      │
├───────────────┤ ├───────────────┤ ├───────────────┤ ├───────────────┤
│ Onboarded     │ │ Onboarded     │ │ Temporary     │ │ Temporary     │
│ with RFP      │ │ without RFP   │ │ with RFP      │ │ without RFP   │
├───────────────┤ ├───────────────┤ ├───────────────┤ ├───────────────┤
│ Data Source:  │ │ Data Source:  │ │ Data Source:  │ │ Data Source:  │
│ vendors table │ │ vendors table │ │ temp_vendor   │ │ temp_vendor   │
├───────────────┤ ├───────────────┤ ├───────────────┤ ├───────────────┤
│ Color: Green  │ │ Color: Blue   │ │ Color: Amber  │ │ Color: Purple │
│ #10b981       │ │ #3b82f6       │ │ #f59e0b       │ │ #8b5cf6       │
└───────────────┘ └───────────────┘ └───────────────┘ └───────────────┘
```

## Database Query Logic

### Step 1: Get All Vendor Codes
```sql
-- From vendors table
SELECT vendor_code FROM vendors WHERE TenantId = ?

-- From temp_vendor table  
SELECT vendor_code FROM temp_vendor WHERE TenantId = ?
```

### Step 2: Find Intersections
```python
vendor_codes_vendors = set(vendors.values_list('vendor_code', flat=True))
vendor_codes_temp = set(temp_vendor.values_list('vendor_code', flat=True))

# Onboarded vendors (in both tables)
onboarded_codes = vendor_codes_vendors & vendor_codes_temp

# Temporary vendors (only in temp_vendor)
temp_only_codes = vendor_codes_temp - vendor_codes_vendors
```

### Step 3: Categorize by Response ID
```python
for code in onboarded_codes:
    vendor = Vendors.get(vendor_code=code)
    temp = TempVendor.get(vendor_code=code)
    
    if temp.response_id:
        type = "ONBOARDED_WITH_RFP"
    else:
        type = "ONBOARDED_WITHOUT_RFP"
    
    # Return data from vendors table
    return VendorsSerializer(vendor).data

for code in temp_only_codes:
    temp = TempVendor.get(vendor_code=code)
    
    if temp.response_id:
        type = "TEMPORARY_WITH_RFP"
    else:
        type = "TEMPORARY_WITHOUT_RFP"
    
    # Return data from temp_vendor table
    return TempVendorSerializer(temp).data
```

## Field Mapping

### vendors Table Fields (Types 1 & 2)
```
✓ vendor_id
✓ vendor_code
✓ company_name
✓ legal_name
✓ business_type
✓ incorporation_date
✓ tax_id
✓ duns_number
✓ website
✓ industry_sector
✓ annual_revenue
✓ employee_count
✓ headquarters_country
✓ headquarters_address
✓ description
✓ vendor_category_id
✓ risk_level
✓ status
✓ lifecycle_stage
✓ onboarding_date
✓ last_assessment_date
✓ next_assessment_date
✓ is_critical_vendor
✓ has_data_access
✓ has_system_access
✓ created_by
✓ updated_by
✓ created_at
✓ updated_at
```

### temp_vendor Table Fields (Types 3 & 4)
```
✓ id
✓ vendor_code
✓ company_name
✓ legal_name
✓ lifecycle_stage
✓ business_type
✓ tax_id
✓ duns_number
✓ incorporation_date
✓ industry_sector
✓ website
✓ annual_revenue
✓ employee_count
✓ headquarters_address
✓ vendor_category
✓ risk_level
✓ status
✓ is_critical_vendor
✓ has_data_access
✓ has_system_access
✓ description
✓ contacts (JSON)
✓ documents (JSON)
✓ response_id
✓ created_at
✓ updated_at
```

## Response Structure

```json
{
  "success": true,
  "data": [
    {
      "vendor_code": "VEN001",
      "company_name": "Example Corp",
      "vendor_type": "ONBOARDED_WITH_RFP",
      "vendor_type_label": "Vendor Onboarded with RFP",
      "is_temporary": false,
      "response_id": 123,
      "risk_level": "MEDIUM",
      "status": "APPROVED",
      // ... other fields from vendors table
    }
  ],
  "total": 10,
  "counts": {
    "onboarded_with_rfp": 3,
    "onboarded_without_rfp": 2,
    "temporary_with_rfp": 3,
    "temporary_without_rfp": 2
  }
}
```

## Frontend Display Logic

### Card View Badge Colors
```css
.badge-onboarded-rfp {
  background: #d1fae5; /* Light green */
  color: #065f46;      /* Dark green */
}

.badge-onboarded-no-rfp {
  background: #dbeafe; /* Light blue */
  color: #1e40af;      /* Dark blue */
}

.badge-temp-rfp {
  background: #fef3c7; /* Light amber */
  color: #92400e;      /* Dark amber */
}

.badge-temp-no-rfp {
  background: #ede9fe; /* Light purple */
  color: #5b21b6;      /* Dark purple */
}
```

### Card View Border Colors
```css
.card-onboarded-rfp {
  border-left: 4px solid #10b981; /* Green */
}

.card-onboarded-no-rfp {
  border-left: 4px solid #3b82f6; /* Blue */
}

.card-temp-rfp {
  border-left: 4px solid #f59e0b; /* Amber */
}

.card-temp-no-rfp {
  border-left: 4px solid #8b5cf6; /* Purple */
}
```

## Use Cases

### Use Case 1: Normal Vendor Onboarding with RFP
1. Vendor submits RFP response → creates entry in `temp_vendor` with `response_id`
2. After approval, vendor data copied to `vendors` table
3. Result: Type 1 - Onboarded with RFP ✅

### Use Case 2: Direct Vendor Onboarding (No RFP)
1. Admin directly creates vendor in system → creates entry in `temp_vendor` without `response_id`
2. After approval, vendor data copied to `vendors` table
3. Result: Type 2 - Onboarded without RFP ✅

### Use Case 3: Pending RFP Response
1. Vendor submits RFP response → creates entry in `temp_vendor` with `response_id`
2. Awaiting approval, NOT yet in `vendors` table
3. Result: Type 3 - Temporary with RFP ⏳

### Use Case 4: Draft Vendor Registration
1. Admin creates draft vendor record → creates entry in `temp_vendor` without `response_id`
2. Not yet approved or completed, NOT in `vendors` table
3. Result: Type 4 - Temporary without RFP ⏳

## Edge Cases

### What if vendor_code exists in vendors but not temp_vendor?
- Scenario: Old vendor data or migrated data
- Behavior: Still shown as onboarded, but classified as "without RFP"
- Type: Type 2 (Onboarded without RFP)

### What if response_id is deleted after onboarding?
- Scenario: RFP response archived/deleted
- Behavior: Vendor remains Type 1 if previously onboarded with RFP
- Note: Classification is point-in-time based on current data

### What if vendor_code changes?
- Scenario: Vendor rebranding or code reassignment
- Behavior: Treated as separate vendor
- Recommendation: Use vendor_id as primary identifier where possible

## Performance Optimization

### Current Implementation
```python
# Two separate queries
vendors = Vendors.objects.filter(tenant_id=tenant_id)
temp_vendors = TempVendor.objects.filter(tenant_id=tenant_id)
```

### Future Optimization (if needed)
```python
# Use select_related for foreign keys
vendors = Vendors.objects.filter(
    tenant_id=tenant_id
).select_related('vendor_category', 'created_by')

# Prefetch related data
vendors = vendors.prefetch_related('contacts', 'documents')
```

### Caching Strategy (optional)
```python
from django.core.cache import cache

def get_vendor_counts(tenant_id):
    cache_key = f'vendor_counts_{tenant_id}'
    counts = cache.get(cache_key)
    
    if not counts:
        counts = calculate_vendor_counts(tenant_id)
        cache.set(cache_key, counts, timeout=300)  # 5 minutes
    
    return counts
```
