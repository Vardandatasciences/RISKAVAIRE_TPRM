# Procurement Components Update Summary

## Missing Features Across All Components

### 1. Evaluation Criteria (CRITICAL - Missing in ALL)
- All components (RFI, RPQ, Direct, Auction, Emergency) are missing the evaluation criteria tab
- SQL schema has evaluation criteria tables for all types
- Need to add:
  - Evaluation criteria tab in formTabs
  - Evaluation criteria UI section
  - Criteria management functions (add, remove, normalize weights)
  - Data type classification for criteria fields
  - API integration for saving criteria

### 2. Missing Common Fields (All Components)
From SQL schema, these fields are missing:
- `evaluation_period_end` (DATE)
- `award_date` (DATE)
- `budget_range_min` (DECIMAL)
- `budget_range_max` (DECIMAL)
- `compliance_requirements` (JSON/TEXT)
- `approval_workflow_id` (VARCHAR)
- `primary_reviewer_id` (INT)
- `executive_reviewer_id` (INT)
- `version_number` (INT, default 1)
- `evaluation_method` (VARCHAR, default 'weighted_scoring')
- `retentionExpiry` (DATE)
- `data_inventory` (JSON)

### 3. Type-Specific Missing Fields

#### RFI
- All common fields above
- Evaluation criteria

#### RPQ
- All common fields above
- Evaluation criteria

#### Direct
- All common fields above
- Evaluation criteria
- Has `direct_justification` and `vendor_id` ✓

#### Auction
- All common fields above
- Evaluation criteria
- Has auction-specific fields ✓ (auction_start_time, auction_end_time, starting_bid, reserve_price, bid_increment, auction_format)

#### Emergency
- All common fields above
- Evaluation criteria
- Has emergency-specific fields ✓ (emergency_justification, emergency_type_category, urgency_level, required_delivery_date, impact_description)

## Implementation Plan

1. Add evaluation criteria tab and functionality to all components
2. Add missing common fields to formData
3. Add missing fields to UI (Budget tab should include budget_range_min/max)
4. Add Process Settings fields (evaluation_method, compliance_requirements, etc.)
5. Update API submission to include all fields
6. Ensure evaluation criteria are saved separately via their respective API endpoints
