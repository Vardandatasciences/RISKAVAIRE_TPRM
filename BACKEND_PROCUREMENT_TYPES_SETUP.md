# Backend Setup for Procurement Types (RFI, RPQ, Direct, Auction, Emergency)

## Overview
Complete backend implementation for all 5 procurement types with full CRUD operations, evaluation criteria management, and type endpoints.

## Created Backend Structure

### 1. RFI (Request for Information)
**Location:** `grc_backend/tprm_backend/rfp/rfi/`

- **Models:** `RFI`, `RFIEvaluationCriteria`
- **Serializers:** `RFISerializer`, `RFICreateSerializer`, `RFIListSerializer`, `RFIEvaluationCriteriaSerializer`
- **Views:** `RFIViewSet`, `RFIEvaluationCriteriaViewSet`, `RFITypeView`
- **URLs:** `/api/v1/rfis/`, `/api/v1/rfi-evaluation-criteria/`, `/api/v1/rfi-types/types/`

### 2. RPQ (Request for Quotation)
**Location:** `grc_backend/tprm_backend/rfp/rpq/`

- **Models:** `RPQ`, `RPQEvaluationCriteria`
- **Serializers:** `RPQSerializer`, `RPQCreateSerializer`, `RPQListSerializer`, `RPQEvaluationCriteriaSerializer`
- **Views:** `RPQViewSet`, `RPQEvaluationCriteriaViewSet`, `RPQTypeView`
- **URLs:** `/api/v1/rpqs/`, `/api/v1/rpq-evaluation-criteria/`, `/api/v1/rpq-types/types/`

### 3. Direct Procurement
**Location:** `grc_backend/tprm_backend/rfp/direct/`

- **Models:** `DirectProcurement`, `DirectEvaluationCriteria`
- **Serializers:** `DirectProcurementSerializer`, `DirectProcurementCreateSerializer`, `DirectProcurementListSerializer`, `DirectEvaluationCriteriaSerializer`
- **Views:** `DirectProcurementViewSet`, `DirectEvaluationCriteriaViewSet`, `DirectTypeView`
- **URLs:** `/api/v1/direct-procurements/`, `/api/v1/direct-evaluation-criteria/`, `/api/v1/direct-types/types/`

### 4. Auction
**Location:** `grc_backend/tprm_backend/rfp/auction/`

- **Models:** `Auction`, `AuctionEvaluationCriteria`, `AuctionBid`
- **Serializers:** `AuctionSerializer`, `AuctionCreateSerializer`, `AuctionListSerializer`, `AuctionEvaluationCriteriaSerializer`
- **Views:** `AuctionViewSet`, `AuctionEvaluationCriteriaViewSet`, `AuctionTypeView`
- **URLs:** `/api/v1/auctions/`, `/api/v1/auction-evaluation-criteria/`, `/api/v1/auction-types/types/`

### 5. Emergency Procurement
**Location:** `grc_backend/tprm_backend/rfp/emergency/`

- **Models:** `EmergencyProcurement`, `EmergencyEvaluationCriteria`
- **Serializers:** `EmergencyProcurementSerializer`, `EmergencyProcurementCreateSerializer`, `EmergencyProcurementListSerializer`, `EmergencyEvaluationCriteriaSerializer`
- **Views:** `EmergencyProcurementViewSet`, `EmergencyEvaluationCriteriaViewSet`, `EmergencyTypeView`
- **URLs:** `/api/v1/emergency-procurements/`, `/api/v1/emergency-evaluation-criteria/`, `/api/v1/emergency-types/types/`

## API Endpoints

### Main Procurement Endpoints
- `POST /api/v1/rfis/` - Create RFI
- `GET /api/v1/rfis/` - List RFIs
- `GET /api/v1/rfis/{id}/` - Get RFI details
- `PATCH /api/v1/rfis/{id}/` - Update RFI
- `DELETE /api/v1/rfis/{id}/` - Delete RFI

(Same pattern for RPQ, Direct, Auction, Emergency)

### Evaluation Criteria Endpoints
- `POST /api/v1/rfi-evaluation-criteria/` - Create evaluation criterion
- `GET /api/v1/rfi-evaluation-criteria/?rfi_id={id}` - List criteria for RFI
- `DELETE /api/v1/rfi-evaluation-criteria/?rfi_id={id}` - Bulk delete criteria for RFI
- `DELETE /api/v1/rfi-evaluation-criteria/{id}/` - Delete specific criterion

(Same pattern for RPQ, Direct, Auction, Emergency)

### Type Endpoints
- `GET /api/v1/rfi-types/types/` - Get list of RFI types
- `GET /api/v1/rpq-types/types/` - Get list of RPQ types
- `GET /api/v1/direct-types/types/` - Get list of Direct Procurement types
- `GET /api/v1/auction-types/types/` - Get list of Auction types
- `GET /api/v1/emergency-types/types/` - Get list of Emergency Procurement types

## Features Implemented

### 1. Multi-Tenancy Support
- All models include `tenant` ForeignKey to `core.Tenant`
- All viewsets filter by tenant automatically
- Tenant ID extracted from request headers/JWT

### 2. Automatic Number Generation
- RFI numbers: `RFI-YYYY-MM-XXXX`
- RPQ numbers: `RPQ-YYYY-MM-XXXX`
- Direct numbers: `DIRECT-YYYY-MM-XXXX`
- Auction numbers: `AUCTION-YYYY-MM-XXXX`
- Emergency numbers: `EMERGENCY-YYYY-MM-XXXX`

### 3. Evaluation Criteria Management
- Full CRUD operations for evaluation criteria
- Bulk delete support (delete all criteria for a procurement)
- Weight validation (0-100%)
- Veto criterion support

### 4. Field Mappings
All fields from SQL schema are mapped:
- Basic fields (title, description, type, category)
- Budget fields (estimated_value, budget_range_min/max, currency)
- Timeline fields (issue_date, submission_deadline, evaluation_period_end, award_date)
- Process fields (evaluation_method, criticality_level, geographical_scope, compliance_requirements)
- Type-specific fields (direct_justification, vendor_id, auction fields, emergency fields)

### 5. JSON Field Handling
- `compliance_requirements` - Parsed from comma/newline separated text
- `custom_fields` - Stored as JSON
- `data_inventory` - Stored as JSON
- `documents` - Stored as JSON

## Database Tables Used

All tables match the SQL schema:
- `rfis` / `rfi_evaluation_criteria`
- `rpqs` / `rpq_evaluation_criteria`
- `direct_procurements` / `direct_evaluation_criteria`
- `auctions` / `auction_evaluation_criteria` / `auction_bids`
- `emergency_procurements` / `emergency_evaluation_criteria`

## Next Steps

1. Run Django migrations to create the models:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. Test the endpoints using the frontend or API client

3. Verify data is being saved correctly to the database

## Notes

- All viewsets use `IsAuthenticated` permission
- Tenant ID is automatically extracted and set
- Created_by is set to admin user (for development)
- Evaluation criteria are saved separately after main procurement is created
- Type endpoints return unique types from existing records
