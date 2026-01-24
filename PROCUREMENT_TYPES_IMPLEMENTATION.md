# Procurement Types Implementation Guide

## Overview
This document describes the implementation of five procurement types: **RFI**, **RPQ**, **Direct**, **Auction**, and **Emergency**. Each type has its own Vue component and database tables.

## Files Created

### 1. Database Tables (SQL)
**Location:** `grc_backend/tprm_backend/sql/procurement_tables.sql`

This SQL file contains table definitions for:
- `rfis` - Request for Information table
- `rfi_evaluation_criteria` - RFI evaluation criteria
- `rpqs` - Request for Quotation table
- `rpq_evaluation_criteria` - RPQ evaluation criteria
- `direct_procurements` - Direct procurement table
- `direct_evaluation_criteria` - Direct procurement evaluation criteria
- `auctions` - Auction table
- `auction_evaluation_criteria` - Auction evaluation criteria
- `auction_bids` - Auction bids tracking table
- `emergency_procurements` - Emergency procurement table
- `emergency_evaluation_criteria` - Emergency procurement evaluation criteria
- `procurement_type_custom_fields` - Shared custom fields table
- `procurement_responses` - Generic responses table for all types

### 2. Vue Components

#### RFI Component
**Location:** `grc_frontend/tprm_frontend/src/views/rfi/RFICreation.vue`
- **Purpose:** Create and manage Request for Information
- **Color Theme:** Blue/Indigo gradient
- **Key Features:**
  - Basic information (RFI Number, Title, Description, Type, Category)
  - Document upload
  - Budget & Timeline
  - Process Settings

#### RPQ Component
**Location:** `grc_frontend/tprm_frontend/src/views/rpq/RPQCreation.vue`
- **Purpose:** Create and manage Request for Quotation
- **Color Theme:** Green/Emerald gradient
- **Key Features:**
  - Basic information (RPQ Number, Title, Description, Type, Category)
  - Budget & Pricing
  - Process Settings

#### Direct Procurement Component
**Location:** `grc_frontend/tprm_frontend/src/views/direct/DirectCreation.vue`
- **Purpose:** Create and manage Direct Procurement (bypasses competitive bidding)
- **Color Theme:** Indigo/Purple gradient
- **Key Features:**
  - Basic information with pre-selected vendor
  - **Direct Justification** field (required for audit)
  - Budget & Financials
  - Process Settings

#### Auction Component
**Location:** `grc_frontend/tprm_frontend/src/views/auction/AuctionCreation.vue`
- **Purpose:** Create and manage Auctions
- **Color Theme:** Amber/Orange gradient
- **Key Features:**
  - Basic information
  - **Auction-specific fields:**
    - Auction Format (English, Dutch, Sealed Bid, Reverse)
    - Auction Start Time
    - Auction End Time
    - Starting Bid
    - Reserve Price
    - Bid Increment
  - Budget & Auction Pricing
  - Process Settings

#### Emergency Procurement Component
**Location:** `grc_frontend/tprm_frontend/src/views/emergency/EmergencyCreation.vue`
- **Purpose:** Create and manage Emergency Procurements
- **Color Theme:** Red/Rose gradient
- **Key Features:**
  - Basic information
  - **Emergency-specific fields:**
    - Emergency Type Category (Natural Disaster, System Failure, Security Breach, etc.)
    - **Emergency Justification** (required for audit)
    - **Impact Description** (required)
    - Urgency Level (Low, Medium, High, Critical)
    - Required Delivery Date
  - Budget & Financials
  - Process Settings

## Database Schema Details

### Common Fields (All Procurement Types)
All procurement tables share these common fields:
- `{type}_id` - Primary key (BIGINT AUTO_INCREMENT)
- `TenantId` - Multi-tenancy support
- `{type}_number` - Unique identifier (VARCHAR(50))
- `{type}_title` - Title (VARCHAR(255))
- `description` - Description (TEXT)
- `{type}_type` - Type (TEXT)
- `category` - Category (VARCHAR(100))
- `estimated_value` - Estimated value (DECIMAL(15, 2))
- `currency` - Currency (VARCHAR(10), default 'USD')
- `budget_range_min` / `budget_range_max` - Budget range
- `issue_date` - Issue date (DATE)
- `submission_deadline` - Submission deadline (DATETIME)
- `evaluation_period_end` - Evaluation period end (DATE)
- `status` - Status (VARCHAR(20), default 'DRAFT')
- `created_by` - Creator ID (INT)
- `approved_by` - Approver ID (INT, nullable)
- `auto_approve` - Auto-approve flag (BOOLEAN)
- `allow_late_submissions` - Allow late submissions (BOOLEAN)
- `approval_workflow_id` - Approval workflow ID (VARCHAR(50))
- `evaluation_method` - Evaluation method (VARCHAR(20))
- `criticality_level` - Criticality level (VARCHAR(10))
- `geographical_scope` - Geographical scope (VARCHAR(255))
- `compliance_requirements` - Compliance requirements (JSON)
- `custom_fields` - Custom fields (JSON)
- `data_inventory` - Data inventory mapping (JSON)
- `documents` - Documents array (JSON)
- `created_at` / `updated_at` - Timestamps

### Type-Specific Fields

#### Direct Procurement
- `direct_justification` (TEXT) - Required justification for direct procurement
- `vendor_id` (BIGINT) - Pre-selected vendor ID

#### Auction
- `auction_start_time` (DATETIME) - Auction start date and time
- `auction_end_time` (DATETIME) - Auction end date and time
- `starting_bid` (DECIMAL(15, 2)) - Starting bid amount
- `reserve_price` (DECIMAL(15, 2)) - Reserve price (minimum acceptable bid)
- `bid_increment` (DECIMAL(15, 2)) - Minimum bid increment
- `auction_format` (VARCHAR(50)) - Auction format (English, Dutch, Sealed Bid, etc.)

#### Emergency Procurement
- `emergency_justification` (TEXT) - Required justification for emergency procurement
- `emergency_type_category` (VARCHAR(100)) - Category (Natural Disaster, System Failure, etc.)
- `urgency_level` (VARCHAR(20)) - Urgency level (LOW, MEDIUM, HIGH, CRITICAL)
- `required_delivery_date` (DATE) - Required delivery/completion date
- `impact_description` (TEXT) - Description of impact if not procured immediately

## Component Structure

All components follow a similar structure:
1. **Header Section** - Title, save status, action buttons
2. **Tab Navigation** - Organized sections (Basic, Documents, Budget, Process)
3. **Form Sections** - Tabbed content with relevant fields
4. **Auto-save** - Automatic draft saving every 30 seconds
5. **Validation** - Form validation before submission
6. **API Integration** - Save/update endpoints for each procurement type

## API Endpoints Required

You'll need to create the following backend endpoints:

### RFI Endpoints
- `GET /api/v1/rfi-types/types/` - Get RFI types
- `GET /api/v1/rfi-types/custom_fields/?rfi_type={type}` - Get custom fields
- `POST /api/v1/rfis/` - Create RFI
- `PATCH /api/v1/rfis/{id}/` - Update RFI
- `GET /api/v1/rfis/{id}/` - Get RFI details

### RPQ Endpoints
- `GET /api/v1/rpq-types/types/` - Get RPQ types
- `GET /api/v1/rpq-types/custom_fields/?rpq_type={type}` - Get custom fields
- `POST /api/v1/rpqs/` - Create RPQ
- `PATCH /api/v1/rpqs/{id}/` - Update RPQ
- `GET /api/v1/rpqs/{id}/` - Get RPQ details

### Direct Procurement Endpoints
- `GET /api/v1/direct-types/types/` - Get Direct types
- `GET /api/v1/direct-types/custom_fields/?direct_type={type}` - Get custom fields
- `POST /api/v1/direct-procurements/` - Create Direct Procurement
- `PATCH /api/v1/direct-procurements/{id}/` - Update Direct Procurement
- `GET /api/v1/direct-procurements/{id}/` - Get Direct Procurement details

### Auction Endpoints
- `GET /api/v1/auction-types/types/` - Get Auction types
- `GET /api/v1/auction-types/custom_fields/?auction_type={type}` - Get custom fields
- `POST /api/v1/auctions/` - Create Auction
- `PATCH /api/v1/auctions/{id}/` - Update Auction
- `GET /api/v1/auctions/{id}/` - Get Auction details
- `POST /api/v1/auction-bids/` - Submit bid
- `GET /api/v1/auction-bids/?auction_id={id}` - Get bids for auction

### Emergency Procurement Endpoints
- `GET /api/v1/emergency-types/types/` - Get Emergency types
- `GET /api/v1/emergency-types/custom_fields/?emergency_type={type}` - Get custom fields
- `POST /api/v1/emergency-procurements/` - Create Emergency Procurement
- `PATCH /api/v1/emergency-procurements/{id}/` - Update Emergency Procurement
- `GET /api/v1/emergency-procurements/{id}/` - Get Emergency Procurement details

## Router Configuration

Add routes to `grc_frontend/tprm_frontend/src/router/index_rfp.js`:

```javascript
// RFI Routes
{
  path: '/tprm/rfi-creation',
  name: 'RFICreation',
  component: () => import('@/views/rfi/RFICreation.vue')
},
{
  path: '/tprm/rfi-list',
  name: 'RFIList',
  component: () => import('@/views/rfi/RFIList.vue') // Create this component
},
{
  path: '/tprm/rfi-dashboard',
  name: 'RFIDashboard',
  component: () => import('@/views/rfi/RFIDashboard.vue') // Create this component
},

// RPQ Routes
{
  path: '/tprm/rpq-creation',
  name: 'RPQCreation',
  component: () => import('@/views/rpq/RPQCreation.vue')
},
{
  path: '/tprm/rpq-list',
  name: 'RPQList',
  component: () => import('@/views/rpq/RPQList.vue') // Create this component
},
{
  path: '/tprm/rpq-dashboard',
  name: 'RPQDashboard',
  component: () => import('@/views/rpq/RPQDashboard.vue') // Create this component
},

// Direct Procurement Routes
{
  path: '/tprm/direct-creation',
  name: 'DirectCreation',
  component: () => import('@/views/direct/DirectCreation.vue')
},
{
  path: '/tprm/direct-list',
  name: 'DirectList',
  component: () => import('@/views/direct/DirectList.vue') // Create this component
},
{
  path: '/tprm/direct-dashboard',
  name: 'DirectDashboard',
  component: () => import('@/views/direct/DirectDashboard.vue') // Create this component
},

// Auction Routes
{
  path: '/tprm/auction-creation',
  name: 'AuctionCreation',
  component: () => import('@/views/auction/AuctionCreation.vue')
},
{
  path: '/tprm/auction-list',
  name: 'AuctionList',
  component: () => import('@/views/auction/AuctionList.vue') // Create this component
},
{
  path: '/tprm/auction-dashboard',
  name: 'AuctionDashboard',
  component: () => import('@/views/auction/AuctionDashboard.vue') // Create this component
},

// Emergency Procurement Routes
{
  path: '/tprm/emergency-creation',
  name: 'EmergencyCreation',
  component: () => import('@/views/emergency/EmergencyCreation.vue')
},
{
  path: '/tprm/emergency-list',
  name: 'EmergencyList',
  component: () => import('@/views/emergency/EmergencyList.vue') // Create this component
},
{
  path: '/tprm/emergency-dashboard',
  name: 'EmergencyDashboard',
  component: () => import('@/views/emergency/EmergencyDashboard.vue') // Create this component
}
```

## Next Steps

1. **Run SQL Script**: Execute `procurement_tables.sql` to create all database tables
2. **Create Django Models**: Create Django models in `grc_backend/tprm_backend/` for each procurement type
3. **Create API Views**: Implement REST API endpoints for each procurement type
4. **Create List/Dashboard Components**: Create list and dashboard views for each type
5. **Update Sidebar**: The sidebar has already been updated with the new menu structure
6. **Test Components**: Test each component with sample data

## Notes

- All components use the same UI components from `@/components_rfp/ui/`
- All components follow the same patterns as the RFP component
- Auto-save functionality is implemented for all types
- Form validation ensures required fields are filled
- Each type has its own color theme for visual distinction
- Type-specific fields are clearly marked and required where appropriate
