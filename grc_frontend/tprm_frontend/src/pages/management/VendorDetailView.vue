<template>
  <div class="vendor-detail-container">
    <!-- Header with Back Button -->
    <div class="detail-header">
      <button @click="goBack" class="back-btn">
        <i class="fas fa-arrow-left"></i>
        <span>Back to Vendors</span>
      </button>
      <h1 class="detail-title">Vendor Details</h1>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p>Loading vendor details...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-container">
      <i class="fas fa-exclamation-triangle"></i>
      <p>{{ error }}</p>
      <button @click="fetchVendorDetails" class="btn btn-primary">Retry</button>
    </div>

    <!-- Vendor Details -->
    <div v-else-if="vendor" class="detail-content">
      <!-- Vendor Type Banner -->
      <div class="vendor-type-banner" :class="getBannerClass(vendor.vendor_type)">
        <i class="fas fa-info-circle"></i>
        <span>{{ vendor.vendor_type_label }}</span>
      </div>

      <!-- Tabs - Horizontal Layout -->
      <div class="tabs-container">
        <div class="tabs-wrapper">
          <button 
            v-for="tab in tabs" 
            :key="tab.id"
            class="tab"
            :class="{ active: activeTab === tab.id }"
            @click="activeTab = tab.id"
          >
            <i :class="tab.icon"></i>
            <span class="tab-label">{{ tab.label }}</span>
          </button>
        </div>

        <!-- Tab Content -->
        <div class="tab-content-wrapper">
          <div class="tab-content">
          <!-- Company Information Tab -->
          <div v-if="activeTab === 'company'" class="info-section">
            <h3 class="section-title">Company Information</h3>
            <div class="info-grid">
              <div class="info-item">
                <label>Vendor Code</label>
                <p>{{ vendor.vendor_code || 'N/A' }}</p>
              </div>
              <div class="info-item">
                <label>Company Name</label>
                <p>{{ vendor.company_name || 'N/A' }}</p>
              </div>
              <div class="info-item">
                <label>Legal Name</label>
                <p>{{ vendor.legal_name || 'N/A' }}</p>
              </div>
              <div class="info-item">
                <label>Business Type</label>
                <p>{{ vendor.business_type || 'N/A' }}</p>
              </div>
              <div class="info-item">
                <label>Industry Sector</label>
                <p>{{ vendor.industry_sector || 'N/A' }}</p>
              </div>
              <div class="info-item" v-if="!vendor.is_temporary">
                <label>Incorporation Date</label>
                <p>{{ formatDate(vendor.incorporation_date) }}</p>
              </div>
              <div class="info-item" v-if="!vendor.is_temporary">
                <label>Tax ID</label>
                <p>{{ vendor.tax_id || 'N/A' }}</p>
              </div>
              <div class="info-item" v-if="!vendor.is_temporary">
                <label>DUNS Number</label>
                <p>{{ vendor.duns_number || 'N/A' }}</p>
              </div>
              <div class="info-item">
                <label>Website</label>
                <p>
                  <a v-if="vendor.website" :href="vendor.website" target="_blank" class="link">
                    {{ vendor.website }}
                  </a>
                  <span v-else>N/A</span>
                </p>
              </div>
              <div class="info-item" v-if="!vendor.is_temporary">
                <label>Annual Revenue</label>
                <p>{{ formatCurrency(vendor.annual_revenue) }}</p>
              </div>
              <div class="info-item">
                <label>Employee Count</label>
                <p>{{ vendor.employee_count || 'N/A' }}</p>
              </div>
              <div class="info-item" v-if="!vendor.is_temporary">
                <label>Headquarters Country</label>
                <p>{{ vendor.headquarters_country || 'N/A' }}</p>
              </div>
              <div class="info-item full-width" v-if="!vendor.is_temporary">
                <label>Headquarters Address</label>
                <p>{{ vendor.headquarters_address || 'N/A' }}</p>
              </div>
              <div class="info-item full-width">
                <label>Description</label>
                <p>{{ vendor.description || 'N/A' }}</p>
              </div>
              <div class="info-item" v-if="!vendor.is_temporary && vendor.vendor_category_id">
                <label>Vendor Category ID</label>
                <p>{{ vendor.vendor_category_id }}</p>
              </div>
              <div class="info-item" v-if="!vendor.is_temporary && vendor.vendor_tier_id">
                <label>Vendor Tier ID</label>
                <p>{{ vendor.vendor_tier_id }}</p>
              </div>
              <div class="info-item" v-if="!vendor.is_temporary && vendor.parent_vendor_id">
                <label>Parent Vendor ID</label>
                <p>{{ vendor.parent_vendor_id }}</p>
              </div>
              <div class="info-item" v-if="!vendor.is_temporary && vendor.geographic_presence">
                <label>Geographic Presence</label>
                <p>{{ formatJSON(vendor.geographic_presence) }}</p>
              </div>
              <div class="info-item" v-if="!vendor.is_temporary && vendor.data_classification_handled">
                <label>Data Classification Handled</label>
                <p>{{ vendor.data_classification_handled }}</p>
              </div>
              <div class="info-item" v-if="!vendor.is_temporary && vendor.business_criticality">
                <label>Business Criticality</label>
                <p>{{ vendor.business_criticality }}</p>
              </div>
              <div class="info-item" v-if="!vendor.is_temporary && vendor.vendor_size_category">
                <label>Vendor Size Category</label>
                <p>{{ vendor.vendor_size_category }}</p>
              </div>
              <div class="info-item" v-if="!vendor.is_temporary">
                <label>Preferred Vendor</label>
                <p>{{ vendor.preferred_vendor_flag ? 'Yes' : 'No' }}</p>
              </div>
              <div class="info-item" v-if="!vendor.is_temporary && vendor.diversity_certification">
                <label>Diversity Certification</label>
                <p>{{ formatJSON(vendor.diversity_certification) }}</p>
              </div>
              <div class="info-item" v-if="!vendor.is_temporary && vendor.sustainability_rating">
                <label>Sustainability Rating</label>
                <p>{{ vendor.sustainability_rating }}</p>
              </div>
              <div class="info-item" v-if="!vendor.is_temporary && vendor.match_score">
                <label>Match Score</label>
                <p>{{ vendor.match_score }}</p>
              </div>
              <div class="info-item" v-if="!vendor.is_temporary && vendor.data_inventory">
                <label>Data Inventory</label>
                <p>{{ formatJSON(vendor.data_inventory) }}</p>
              </div>
              <div class="info-item" v-if="!vendor.is_temporary && vendor.retentionExpiry">
                <label>Retention Expiry</label>
                <p>{{ formatDate(vendor.retentionExpiry) }}</p>
              </div>
            </div>
          </div>

          <!-- Risk & Status Tab -->
          <div v-if="activeTab === 'risk'" class="info-section">
            <h3 class="section-title">Risk & Status Information</h3>
            <div class="info-grid">
              <div class="info-item">
                <label>Risk Level</label>
                <p>
                  <span 
                    v-if="vendor.risk_level" 
                    class="badge"
                    :class="getRiskLevelClass(vendor.risk_level)"
                  >
                    {{ vendor.risk_level }}
                  </span>
                  <span v-else>N/A</span>
                </p>
              </div>
              <div class="info-item">
                <label>Status</label>
                <p>
                  <span 
                    v-if="vendor.status" 
                    class="badge"
                    :class="getStatusClass(vendor.status)"
                  >
                    {{ vendor.status }}
                  </span>
                  <span v-else>N/A</span>
                </p>
              </div>
              <div class="info-item">
                <label>Lifecycle Stage</label>
                <p>{{ vendor.lifecycle_stage || 'N/A' }}</p>
              </div>
              <div class="info-item">
                <label>Critical Vendor</label>
                <p>
                  <span :class="vendor.is_critical_vendor ? 'text-danger' : 'text-muted'">
                    {{ vendor.is_critical_vendor ? 'Yes' : 'No' }}
                  </span>
                </p>
              </div>
              <div class="info-item">
                <label>Has Data Access</label>
                <p>
                  <span :class="vendor.has_data_access ? 'text-info' : 'text-muted'">
                    {{ vendor.has_data_access ? 'Yes' : 'No' }}
                  </span>
                </p>
              </div>
              <div class="info-item">
                <label>Has System Access</label>
                <p>
                  <span :class="vendor.has_system_access ? 'text-info' : 'text-muted'">
                    {{ vendor.has_system_access ? 'Yes' : 'No' }}
                  </span>
                </p>
              </div>
              <div class="info-item" v-if="!vendor.is_temporary">
                <label>Onboarding Date</label>
                <p>{{ formatDate(vendor.onboarding_date) }}</p>
              </div>
              <div class="info-item" v-if="!vendor.is_temporary">
                <label>Last Assessment Date</label>
                <p>{{ formatDate(vendor.last_assessment_date) }}</p>
              </div>
              <div class="info-item" v-if="!vendor.is_temporary">
                <label>Next Assessment Date</label>
                <p>{{ formatDate(vendor.next_assessment_date) }}</p>
              </div>
              <div class="info-item" v-if="vendor.response_id">
                <label>RFP Response ID</label>
                <p class="response-id">{{ vendor.response_id }}</p>
              </div>
            </div>
          </div>

          <!-- Contacts Tab (for temporary vendors with JSON contacts) -->
          <div v-if="activeTab === 'contacts'" class="info-section">
            <h3 class="section-title">Contact Information</h3>
            <div v-if="vendor.contacts && vendor.contacts.length > 0" class="contacts-list">
              <div 
                v-for="(contact, index) in vendor.contacts" 
                :key="index"
                class="contact-card"
              >
                <h4 class="contact-name">{{ contact.name || 'N/A' }}</h4>
                <div class="contact-details">
                  <div v-if="contact.email" class="contact-detail">
                    <i class="fas fa-envelope"></i>
                    <a :href="`mailto:${contact.email}`">{{ contact.email }}</a>
                  </div>
                  <div v-if="contact.phone" class="contact-detail">
                    <i class="fas fa-phone"></i>
                    <span>{{ contact.phone }}</span>
                  </div>
                  <div v-if="contact.designation" class="contact-detail">
                    <i class="fas fa-briefcase"></i>
                    <span>{{ contact.designation }}</span>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="empty-state">
              <i class="fas fa-address-book"></i>
              <p>No contact information available</p>
            </div>
          </div>

          <!-- Documents Tab (for temporary vendors with JSON documents) -->
          <div v-if="activeTab === 'documents'" class="info-section">
            <h3 class="section-title">Documents</h3>
            <div v-if="vendor.documents && vendor.documents.length > 0" class="documents-list">
              <div 
                v-for="(document, index) in vendor.documents" 
                :key="index"
                class="document-card"
              >
                <i class="fas fa-file-alt document-icon"></i>
                <div class="document-info">
                  <h4 class="document-name">{{ document.name || 'Document' }}</h4>
                  <p class="document-type">{{ document.type || 'Unknown Type' }}</p>
                </div>
              </div>
            </div>
            <div v-else class="empty-state">
              <i class="fas fa-folder-open"></i>
              <p>No documents available</p>
            </div>
          </div>

          <!-- Contracts Tab -->
          <div v-if="activeTab === 'contracts'" class="info-section">
            <h3 class="section-title">Vendor Contracts</h3>
            <div v-if="vendor.related_data && vendor.related_data.contracts && vendor.related_data.contracts.length > 0" class="contracts-list">
              <div 
                v-for="contract in vendor.related_data.contracts" 
                :key="contract.contract_id"
                class="contract-card"
              >
                <div class="contract-header">
                  <h4 class="contract-title">{{ contract.contract_title || 'Untitled Contract' }}</h4>
                  <span class="contract-number">{{ contract.contract_number }}</span>
                </div>
                <div class="contract-details-grid">
                  <div class="contract-detail-item">
                    <label>Contract Type</label>
                    <p>{{ contract.contract_type || 'N/A' }}</p>
                  </div>
                  <div class="contract-detail-item">
                    <label>Status</label>
                    <p><span class="badge" :class="getStatusClass(contract.status)">{{ contract.status || 'N/A' }}</span></p>
                  </div>
                  <div class="contract-detail-item">
                    <label>Value</label>
                    <p>{{ formatCurrency(contract.contract_value) }} {{ contract.currency || '' }}</p>
                  </div>
                  <div class="contract-detail-item">
                    <label>Start Date</label>
                    <p>{{ formatDate(contract.start_date) }}</p>
                  </div>
                  <div class="contract-detail-item">
                    <label>End Date</label>
                    <p>{{ formatDate(contract.end_date) }}</p>
                  </div>
                  <div class="contract-detail-item">
                    <label>Workflow Stage</label>
                    <p>{{ contract.workflow_stage || 'N/A' }}</p>
                  </div>
                </div>
                
                <!-- Contract Terms -->
                <div v-if="getContractTerms(contract.contract_id).length > 0" class="contract-subsection">
                  <h5>Terms</h5>
                  <div class="terms-list">
                    <div v-for="term in getContractTerms(contract.contract_id)" :key="term.id" class="term-item">
                      <strong>{{ term.term_title || term.term_id }}</strong>
                      <span class="badge badge-small" :class="getRiskLevelClass(term.risk_level)">{{ term.risk_level }}</span>
                      <p>{{ term.term_text }}</p>
                    </div>
                  </div>
                </div>
                
                <!-- Contract Clauses -->
                <div v-if="getContractClauses(contract.contract_id).length > 0" class="contract-subsection">
                  <h5>Clauses</h5>
                  <div class="clauses-list">
                    <div v-for="clause in getContractClauses(contract.contract_id)" :key="clause.id" class="clause-item">
                      <strong>{{ clause.clause_name }}</strong>
                      <span class="badge badge-small" :class="getRiskLevelClass(clause.risk_level)">{{ clause.risk_level }}</span>
                      <p>{{ clause.clause_text }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="empty-state">
              <i class="fas fa-file-contract"></i>
              <p>No contracts found for this vendor</p>
            </div>
          </div>

          <!-- SLAs Tab -->
          <div v-if="activeTab === 'slas'" class="info-section">
            <h3 class="section-title">Service Level Agreements (SLAs)</h3>
            <div v-if="vendor.related_data && vendor.related_data.slas && vendor.related_data.slas.length > 0" class="slas-list">
              <div 
                v-for="sla in vendor.related_data.slas" 
                :key="sla.sla_id"
                class="sla-card"
              >
                <div class="sla-header">
                  <h4 class="sla-name">{{ sla.sla_name }}</h4>
                  <span class="badge" :class="getStatusClass(sla.status)">{{ sla.status || 'N/A' }}</span>
                </div>
                <div class="sla-details-grid">
                  <div class="sla-detail-item">
                    <label>SLA Type</label>
                    <p>{{ sla.sla_type || 'N/A' }}</p>
                  </div>
                  <div class="sla-detail-item">
                    <label>Effective Date</label>
                    <p>{{ formatDate(sla.effective_date) }}</p>
                  </div>
                  <div class="sla-detail-item">
                    <label>Expiry Date</label>
                    <p>{{ formatDate(sla.expiry_date) }}</p>
                  </div>
                  <div class="sla-detail-item">
                    <label>Priority</label>
                    <p><span class="badge" :class="getRiskLevelClass(sla.priority)">{{ sla.priority || 'N/A' }}</span></p>
                  </div>
                  <div class="sla-detail-item">
                    <label>Compliance Score</label>
                    <p>{{ sla.compliance_score || 'N/A' }}</p>
                  </div>
                  <div class="sla-detail-item">
                    <label>Reporting Frequency</label>
                    <p>{{ sla.reporting_frequency || 'N/A' }}</p>
                  </div>
                </div>
                
                <!-- SLA Metrics -->
                <div v-if="getSLAMetrics(sla.sla_id).length > 0" class="sla-subsection">
                  <h5>Metrics</h5>
                  <div class="metrics-list">
                    <div v-for="metric in getSLAMetrics(sla.sla_id)" :key="metric.metric_id" class="metric-item">
                      <strong>{{ metric.metric_name }}</strong>
                      <p>Threshold: {{ metric.threshold }} {{ metric.measurement_unit || '' }}</p>
                      <p>Frequency: {{ metric.frequency || 'N/A' }}</p>
                      <p v-if="metric.penalty">{{ metric.penalty }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="empty-state">
              <i class="fas fa-chart-line"></i>
              <p>No SLAs found for this vendor</p>
            </div>
          </div>

          <!-- BCP/DRP Plans Tab -->
          <div v-if="activeTab === 'bcp_plans'" class="info-section">
            <h3 class="section-title">BCP/DRP Plans</h3>
            <div v-if="vendor.related_data && vendor.related_data.bcp_drp_plans && vendor.related_data.bcp_drp_plans.length > 0" class="plans-list">
              <div 
                v-for="plan in vendor.related_data.bcp_drp_plans" 
                :key="plan.plan_id"
                class="plan-card"
              >
                <div class="plan-header">
                  <h4 class="plan-name">{{ plan.plan_name }}</h4>
                  <span class="badge" :class="getRiskLevelClass(plan.criticality)">{{ plan.criticality || 'N/A' }}</span>
                </div>
                <div class="plan-details-grid">
                  <div class="plan-detail-item">
                    <label>Plan Type</label>
                    <p>{{ plan.plan_type || 'N/A' }}</p>
                  </div>
                  <div class="plan-detail-item">
                    <label>Strategy Name</label>
                    <p>{{ plan.strategy_name || 'N/A' }}</p>
                  </div>
                  <div class="plan-detail-item">
                    <label>Version</label>
                    <p>{{ plan.version || 'N/A' }}</p>
                  </div>
                  <div class="plan-detail-item">
                    <label>Status</label>
                    <p><span class="badge" :class="getStatusClass(plan.status)">{{ plan.status || 'N/A' }}</span></p>
                  </div>
                  <div class="plan-detail-item">
                    <label>Document Date</label>
                    <p>{{ formatDate(plan.document_date) }}</p>
                  </div>
                  <div class="plan-detail-item">
                    <label>Submitted At</label>
                    <p>{{ formatDateTime(plan.submitted_at) }}</p>
                  </div>
                </div>
                <div v-if="plan.plan_scope" class="plan-scope">
                  <label>Plan Scope</label>
                  <p>{{ plan.plan_scope }}</p>
                </div>
              </div>
            </div>
            <div v-else class="empty-state">
              <i class="fas fa-clipboard-list"></i>
              <p>No BCP/DRP plans found for this vendor</p>
            </div>
          </div>

          <!-- Audit Trail Tab -->
          <div v-if="activeTab === 'audit'" class="info-section">
            <h3 class="section-title">Audit Trail & Performance</h3>
            
            <!-- Vendor Record Audit -->
            <div class="audit-subsection">
              <h4 class="subsection-title">
                <i class="fas fa-history"></i>
                Vendor Record History
              </h4>
              <div class="info-grid">
                <div class="info-item" v-if="!vendor.is_temporary && vendor.created_by">
                  <label>Created By</label>
                  <p>{{ vendor.created_by }}</p>
                </div>
                <div class="info-item">
                  <label>Created At</label>
                  <p>{{ formatDateTime(vendor.created_at) }}</p>
                </div>
                <div class="info-item" v-if="!vendor.is_temporary && vendor.updated_by">
                  <label>Updated By</label>
                  <p>{{ vendor.updated_by }}</p>
                </div>
                <div class="info-item">
                  <label>Updated At</label>
                  <p>{{ formatDateTime(vendor.updated_at) }}</p>
                </div>
                <div class="info-item" v-if="vendor.is_temporary && vendor.UserId">
                  <label>User ID</label>
                  <p>{{ vendor.UserId }}</p>
                </div>
              </div>
            </div>

            <!-- Contract Audits -->
            <div class="audit-subsection" v-if="vendor.related_data && (vendor.related_data.contract_audits?.length > 0 || vendor.related_data.sla_audits?.length > 0)">
              <h4 class="subsection-title">
                <i class="fas fa-file-contract"></i>
                Contract Audits
              </h4>
              <div v-if="vendor.related_data.contract_audits && vendor.related_data.contract_audits.length > 0" class="audits-list">
                <div 
                  v-for="audit in vendor.related_data.contract_audits" 
                  :key="audit.audit_id"
                  class="audit-card"
                >
                  <div class="audit-header">
                    <h5 class="audit-title">{{ audit.title || 'Contract Audit' }}</h5>
                    <div class="audit-badges">
                      <span class="badge" :class="getAuditStatusClass(audit.status)">{{ audit.status || 'N/A' }}</span>
                      <span class="badge" :class="getReviewStatusClass(audit.review_status)">{{ audit.review_status || 'N/A' }}</span>
                    </div>
                  </div>
                  <div class="audit-body">
                    <div class="audit-info-grid">
                      <div class="audit-info-item">
                        <i class="fas fa-user-tie"></i>
                        <div>
                          <label>Audit Type</label>
                          <p>{{ audit.audit_type || 'N/A' }}</p>
                        </div>
                      </div>
                      <div class="audit-info-item">
                        <i class="fas fa-calendar-alt"></i>
                        <div>
                          <label>Assigned</label>
                          <p>{{ formatDate(audit.assign_date) }}</p>
                        </div>
                      </div>
                      <div class="audit-info-item">
                        <i class="fas fa-calendar-check"></i>
                        <div>
                          <label>Due Date</label>
                          <p>{{ formatDate(audit.due_date) }}</p>
                        </div>
                      </div>
                      <div class="audit-info-item">
                        <i class="fas fa-sync-alt"></i>
                        <div>
                          <label>Frequency</label>
                          <p>{{ audit.frequency || 'N/A' }}</p>
                        </div>
                      </div>
                    </div>
                    <div v-if="audit.scope" class="audit-scope">
                      <label>Scope:</label>
                      <p>{{ audit.scope }}</p>
                    </div>
                    <div v-if="audit.review_comments" class="audit-comments">
                      <label>Review Comments:</label>
                      <p>{{ audit.review_comments }}</p>
                    </div>
                    <!-- Contract Audit Findings -->
                    <div v-if="getContractAuditFindings(audit.audit_id).length > 0" class="audit-findings">
                      <label><i class="fas fa-exclamation-triangle"></i> Findings ({{ getContractAuditFindings(audit.audit_id).length }})</label>
                      <div class="findings-list">
                        <div 
                          v-for="finding in getContractAuditFindings(audit.audit_id)" 
                          :key="finding.audit_finding_id"
                          class="finding-item"
                        >
                          <div class="finding-header">
                            <span class="finding-date">{{ formatDate(finding.check_date) }}</span>
                          </div>
                          <p v-if="finding.details_of_finding" class="finding-details">{{ finding.details_of_finding }}</p>
                          <p v-if="finding.impact_recommendations" class="finding-impact"><strong>Impact:</strong> {{ finding.impact_recommendations }}</p>
                          <p v-if="finding.comment" class="finding-comment"><strong>Comment:</strong> {{ finding.comment }}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div v-else class="empty-state-small">
                <i class="fas fa-clipboard-check"></i>
                <p>No contract audits performed yet</p>
              </div>
            </div>

            <!-- SLA Audits -->
            <div class="audit-subsection" v-if="vendor.related_data && vendor.related_data.sla_audits?.length > 0">
              <h4 class="subsection-title">
                <i class="fas fa-chart-line"></i>
                SLA Performance Audits
              </h4>
              <div class="audits-list">
                <div 
                  v-for="audit in vendor.related_data.sla_audits" 
                  :key="audit.audit_id"
                  class="audit-card"
                >
                  <div class="audit-header">
                    <h5 class="audit-title">{{ audit.title || 'SLA Audit' }}</h5>
                    <div class="audit-badges">
                      <span class="badge" :class="getAuditStatusClass(audit.status)">{{ audit.status || 'N/A' }}</span>
                      <span class="badge" :class="getReviewStatusClass(audit.review_status)">{{ audit.review_status || 'N/A' }}</span>
                    </div>
                  </div>
                  <div class="audit-body">
                    <div class="audit-info-grid">
                      <div class="audit-info-item">
                        <i class="fas fa-user-tie"></i>
                        <div>
                          <label>Audit Type</label>
                          <p>{{ audit.audit_type || 'N/A' }}</p>
                        </div>
                      </div>
                      <div class="audit-info-item">
                        <i class="fas fa-calendar-alt"></i>
                        <div>
                          <label>Assigned</label>
                          <p>{{ formatDate(audit.assign_date) }}</p>
                        </div>
                      </div>
                      <div class="audit-info-item">
                        <i class="fas fa-calendar-check"></i>
                        <div>
                          <label>Due Date</label>
                          <p>{{ formatDate(audit.due_date) }}</p>
                        </div>
                      </div>
                      <div class="audit-info-item">
                        <i class="fas fa-sync-alt"></i>
                        <div>
                          <label>Frequency</label>
                          <p>{{ audit.frequency || 'N/A' }}</p>
                        </div>
                      </div>
                    </div>
                    <div v-if="audit.scope" class="audit-scope">
                      <label>Scope:</label>
                      <p>{{ audit.scope }}</p>
                    </div>
                    <div v-if="audit.review_comments" class="audit-comments">
                      <label>Review Comments:</label>
                      <p>{{ audit.review_comments }}</p>
                    </div>
                    <!-- SLA Audit Findings -->
                    <div v-if="getSLAAuditFindings(audit.audit_id).length > 0" class="audit-findings">
                      <label><i class="fas fa-exclamation-triangle"></i> Findings ({{ getSLAAuditFindings(audit.audit_id).length }})</label>
                      <div class="findings-list">
                        <div 
                          v-for="finding in getSLAAuditFindings(audit.audit_id)" 
                          :key="finding.audit_finding_id"
                          class="finding-item"
                        >
                          <div class="finding-header">
                            <span class="finding-date">{{ formatDate(finding.check_date) }}</span>
                          </div>
                          <p v-if="finding.details_of_finding" class="finding-details">{{ finding.details_of_finding }}</p>
                          <p v-if="finding.impact_recommendations" class="finding-impact"><strong>Impact:</strong> {{ finding.impact_recommendations }}</p>
                          <p v-if="finding.comment" class="finding-comment"><strong>Comment:</strong> {{ finding.comment }}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import axios from '@/config/axios'

export default {
  name: 'VendorDetailView',
  props: {
    vendorCode: {
      type: String,
      required: true
    }
  },
  emits: ['back'],
  setup(props, { emit }) {
    const vendor = ref(null)
    const loading = ref(false)
    const error = ref(null)
    const activeTab = ref('company')

    const tabs = computed(() => {
      const baseTabs = [
        { id: 'company', label: 'Company Info', icon: 'fas fa-building' },
        { id: 'risk', label: 'Risk & Status', icon: 'fas fa-shield-alt' },
        { id: 'contracts', label: 'Contracts', icon: 'fas fa-file-contract' },
        { id: 'slas', label: 'SLAs', icon: 'fas fa-chart-line' },
        { id: 'bcp_plans', label: 'BCP/DRP Plans', icon: 'fas fa-clipboard-list' },
        { id: 'audit', label: 'Audit Trail', icon: 'fas fa-history' }
      ]

      // Add contacts and documents tabs for temporary vendors
      if (vendor.value?.is_temporary) {
        baseTabs.splice(2, 0, 
          { id: 'contacts', label: 'Contacts', icon: 'fas fa-address-book' },
          { id: 'documents', label: 'Documents', icon: 'fas fa-file-alt' }
        )
      }

      return baseTabs
    })

    const fetchVendorDetails = async () => {
      loading.value = true
      error.value = null

      try {
        const response = await axios.get(`/api/v1/management/vendors/${props.vendorCode}/`)

        if (response.data.success) {
          vendor.value = response.data.data
          
          // Log related data for debugging
          console.log('[VendorDetailView] Vendor data loaded:', {
            vendor_code: vendor.value.vendor_code,
            has_related_data: !!vendor.value.related_data,
            contracts_count: vendor.value.related_data?.contracts?.length || 0,
            slas_count: vendor.value.related_data?.slas?.length || 0,
            plans_count: vendor.value.related_data?.bcp_drp_plans?.length || 0
          })
          
          // Parse JSON fields if they are strings
          if (vendor.value.contacts && typeof vendor.value.contacts === 'string') {
            try {
              vendor.value.contacts = JSON.parse(vendor.value.contacts)
            } catch (e) {
              console.warn('Failed to parse contacts JSON:', e)
              vendor.value.contacts = []
            }
          }
          
          if (vendor.value.documents && typeof vendor.value.documents === 'string') {
            try {
              vendor.value.documents = JSON.parse(vendor.value.documents)
            } catch (e) {
              console.warn('Failed to parse documents JSON:', e)
              vendor.value.documents = []
            }
          }
          
          // Ensure related_data exists even if empty
          if (!vendor.value.related_data) {
            vendor.value.related_data = {
              contracts: [],
              contract_terms: [],
              contract_clauses: [],
              slas: [],
              sla_metrics: [],
              bcp_drp_plans: []
            }
          }
        } else {
          error.value = 'Failed to load vendor details'
        }
      } catch (err) {
        console.error('Error fetching vendor details:', err)
        error.value = err.response?.data?.error || 'Failed to load vendor details'
      } finally {
        loading.value = false
      }
    }

    const goBack = () => {
      emit('back')
    }

    const getBannerClass = (vendorType) => {
      const classMap = {
        'ONBOARDED_WITH_RFP': 'banner-onboarded-rfp',
        'ONBOARDED_WITHOUT_RFP': 'banner-onboarded-no-rfp',
        'TEMPORARY_WITH_RFP': 'banner-temp-rfp',
        'TEMPORARY_WITHOUT_RFP': 'banner-temp-no-rfp'
      }
      return classMap[vendorType] || ''
    }

    const getRiskLevelClass = (riskLevel) => {
      const classMap = {
        'LOW': 'badge-success',
        'MEDIUM': 'badge-warning',
        'HIGH': 'badge-danger',
        'CRITICAL': 'badge-critical'
      }
      return classMap[riskLevel] || ''
    }

    const getStatusClass = (status) => {
      const classMap = {
        'DRAFT': 'badge-secondary',
        'SUBMITTED': 'badge-info',
        'IN_REVIEW': 'badge-warning',
        'APPROVED': 'badge-success',
        'REJECTED': 'badge-danger',
        'SUSPENDED': 'badge-warning',
        'TERMINATED': 'badge-dark'
      }
      return classMap[status] || ''
    }

    const formatDate = (dateString) => {
      if (!dateString) return 'N/A'
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
      })
    }

    const formatDateTime = (dateString) => {
      if (!dateString) return 'N/A'
      const date = new Date(dateString)
      return date.toLocaleString('en-US', { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    const formatCurrency = (amount) => {
      if (!amount) return 'N/A'
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
      }).format(amount)
    }

    const formatJSON = (jsonData) => {
      if (!jsonData) return 'N/A'
      if (typeof jsonData === 'string') {
        try {
          jsonData = JSON.parse(jsonData)
        } catch (e) {
          return jsonData
        }
      }
      return JSON.stringify(jsonData, null, 2)
    }

    // Helper to get contract audit findings for a specific audit
    const getContractAuditFindings = (auditId) => {
      if (!vendor.value?.related_data?.contract_audit_findings) return []
      return vendor.value.related_data.contract_audit_findings.filter(f => f.audit_id === auditId)
    }

    // Helper to get SLA audit findings for a specific audit
    const getSLAAuditFindings = (auditId) => {
      if (!vendor.value?.related_data?.sla_audit_findings) return []
      return vendor.value.related_data.sla_audit_findings.filter(f => f.audit_id === auditId)
    }

    // Helper for audit status badge class
    const getAuditStatusClass = (status) => {
      const classMap = {
        'created': 'badge-secondary',
        'in_progress': 'badge-info',
        'under_review': 'badge-warning',
        'completed': 'badge-success',
        'rejected': 'badge-danger'
      }
      return classMap[status] || 'badge-secondary'
    }

    // Helper for review status badge class
    const getReviewStatusClass = (reviewStatus) => {
      const classMap = {
        'pending': 'badge-warning',
        'approved': 'badge-success',
        'rejected': 'badge-danger'
      }
      return classMap[reviewStatus] || 'badge-secondary'
    }

    const getContractTerms = (contractId) => {
      if (!vendor.value?.related_data?.contract_terms) return []
      return vendor.value.related_data.contract_terms.filter(term => term.contract_id === contractId)
    }

    const getContractClauses = (contractId) => {
      if (!vendor.value?.related_data?.contract_clauses) return []
      return vendor.value.related_data.contract_clauses.filter(clause => clause.contract_id === contractId)
    }

    const getSLAMetrics = (slaId) => {
      if (!vendor.value?.related_data?.sla_metrics) return []
      return vendor.value.related_data.sla_metrics.filter(metric => metric.sla_id === slaId)
    }

    onMounted(() => {
      fetchVendorDetails()
    })

    return {
      vendor,
      loading,
      error,
      activeTab,
      tabs,
      fetchVendorDetails,
      goBack,
      getBannerClass,
      getRiskLevelClass,
      getStatusClass,
      formatDate,
      formatDateTime,
      formatCurrency,
      formatJSON,
      getContractTerms,
      getContractClauses,
      getSLAMetrics,
      getContractAuditFindings,
      getSLAAuditFindings,
      getAuditStatusClass,
      getReviewStatusClass
    }
  }
}
</script>

<style scoped>
.vendor-detail-container {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
  min-height: 100vh;
  background: #f7fafc;
}

.detail-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
  background: #fff;
  padding: 1.5rem;
  border-radius: 0.75rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: #f3f4f6;
  border: none;
  border-radius: 0.375rem;
  color: #374151;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.back-btn:hover {
  background: #e5e7eb;
  color: #1f2937;
}

.detail-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1a202c;
  margin: 0;
}

.loading-container,
.error-container {
  text-align: center;
  padding: 4rem 2rem;
  background: #fff;
  border-radius: 0.75rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.spinner {
  width: 3rem;
  height: 3rem;
  border: 4px solid #e2e8f0;
  border-top-color: #2563eb;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-container i {
  font-size: 3rem;
  color: #dc2626;
  margin-bottom: 1rem;
}

.detail-content {
  background: #fff;
  border-radius: 0.75rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.vendor-type-banner {
  padding: 1rem 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-weight: 600;
  margin: 0;
}

.banner-onboarded-rfp {
  background: #d1fae5;
  color: #065f46;
}

.banner-onboarded-no-rfp {
  background: #dbeafe;
  color: #1e40af;
}

.banner-temp-rfp {
  background: #fef3c7;
  color: #92400e;
}

.banner-temp-no-rfp {
  background: #ede9fe;
  color: #5b21b6;
}

.tabs-container {
  padding: 0;
  background: #fff;
  border-bottom: 1px solid #e2e8f0;
}

.tabs-wrapper {
  padding: 0 1.5rem;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  display: flex !important;
  flex-direction: row !important;
  flex-wrap: nowrap !important;
  gap: 0;
  scrollbar-width: thin;
}

.tab {
  padding: 1rem 1.5rem;
  border: none;
  background: transparent;
  color: #718096;
  cursor: pointer;
  border-bottom: 3px solid transparent;
  margin-bottom: -1px;
  transition: all 0.2s;
  font-weight: 500;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  white-space: nowrap;
  position: relative;
  font-size: 0.875rem;
  flex-shrink: 0;
  flex-grow: 0;
}

.tab:hover {
  color: #2563eb;
  background: #f7fafc;
}

.tab.active {
  color: #2563eb;
  border-bottom-color: #2563eb;
  background: #f7fafc;
  font-weight: 600;
}

.tab.active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  right: 0;
  height: 1px;
  background: #fff;
}

.tab-label {
  display: inline-block;
}

.tab i {
  font-size: 0.875rem;
}

.tab-content-wrapper {
  padding: 1.5rem;
}

.tab-content {
  /* Tab content styles */
}

.section-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1a202c;
  margin: 0 0 1.5rem 0;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #e2e8f0;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.info-item.full-width {
  grid-column: 1 / -1;
}

.info-item label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #718096;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.info-item p {
  font-size: 1rem;
  color: #1a202c;
  margin: 0;
  word-break: break-word;
}

.link {
  color: #2563eb;
  text-decoration: none;
}

.link:hover {
  text-decoration: underline;
}

.badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.badge-success {
  background: #d1fae5;
  color: #065f46;
}

.badge-warning {
  background: #fef3c7;
  color: #92400e;
}

.badge-danger {
  background: #fee2e2;
  color: #991b1b;
}

.badge-critical {
  background: #fecaca;
  color: #7f1d1d;
}

.badge-info {
  background: #dbeafe;
  color: #1e40af;
}

.badge-secondary {
  background: #f3f4f6;
  color: #374151;
}

.badge-dark {
  background: #e5e7eb;
  color: #1f2937;
}

.text-danger {
  color: #dc2626;
  font-weight: 600;
}

.text-info {
  color: #2563eb;
  font-weight: 600;
}

.text-muted {
  color: #9ca3af;
}

.response-id {
  font-family: monospace;
  color: #2563eb;
  font-weight: 600;
}

/* Contacts */
.contacts-list {
  display: grid;
  gap: 1rem;
}

.contact-card {
  padding: 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  background: #f7fafc;
}

.contact-name {
  font-size: 1rem;
  font-weight: 600;
  color: #1a202c;
  margin: 0 0 0.75rem 0;
}

.contact-details {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.contact-detail {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #4a5568;
}

.contact-detail i {
  width: 1.25rem;
  color: #718096;
}

.contact-detail a {
  color: #2563eb;
  text-decoration: none;
}

.contact-detail a:hover {
  text-decoration: underline;
}

/* Documents */
.documents-list {
  display: grid;
  gap: 1rem;
}

.document-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  background: #f7fafc;
}

.document-icon {
  font-size: 2rem;
  color: #2563eb;
}

.document-info {
  flex: 1;
}

.document-name {
  font-size: 1rem;
  font-weight: 600;
  color: #1a202c;
  margin: 0 0 0.25rem 0;
}

.document-type {
  font-size: 0.875rem;
  color: #718096;
  margin: 0;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 3rem 1.5rem;
  color: #9ca3af;
}

.empty-state i {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.375rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary {
  background: #2563eb;
  color: #fff;
}

.btn-primary:hover {
  background: #1d4ed8;
}

/* Contracts */
.contracts-list {
  display: grid;
  gap: 1.5rem;
}

.contract-card {
  padding: 1.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  background: #f7fafc;
}

.contract-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e2e8f0;
}

.contract-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1a202c;
  margin: 0;
}

.contract-number {
  font-size: 0.875rem;
  color: #718096;
  font-family: monospace;
}

.contract-details-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}

.contract-detail-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.contract-detail-item label {
  font-size: 0.75rem;
  font-weight: 600;
  color: #718096;
  text-transform: uppercase;
}

.contract-detail-item p {
  font-size: 0.875rem;
  color: #1a202c;
  margin: 0;
}

.contract-subsection {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
}

.contract-subsection h5 {
  font-size: 0.875rem;
  font-weight: 600;
  color: #4a5568;
  margin: 0 0 0.75rem 0;
}

.terms-list,
.clauses-list {
  display: grid;
  gap: 0.75rem;
}

.term-item,
.clause-item {
  padding: 0.75rem;
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 0.375rem;
}

.term-item strong,
.clause-item strong {
  display: block;
  font-size: 0.875rem;
  font-weight: 600;
  color: #1a202c;
  margin-bottom: 0.5rem;
}

.term-item p,
.clause-item p {
  font-size: 0.875rem;
  color: #4a5568;
  margin: 0.5rem 0 0 0;
  line-height: 1.5;
}

.badge-small {
  font-size: 0.625rem;
  padding: 0.125rem 0.5rem;
}

/* SLAs */
.slas-list {
  display: grid;
  gap: 1.5rem;
}

.sla-card {
  padding: 1.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  background: #f7fafc;
}

.sla-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e2e8f0;
}

.sla-name {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1a202c;
  margin: 0;
}

.sla-details-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}

.sla-detail-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.sla-detail-item label {
  font-size: 0.75rem;
  font-weight: 600;
  color: #718096;
  text-transform: uppercase;
}

.sla-detail-item p {
  font-size: 0.875rem;
  color: #1a202c;
  margin: 0;
}

.sla-subsection {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
}

.sla-subsection h5 {
  font-size: 0.875rem;
  font-weight: 600;
  color: #4a5568;
  margin: 0 0 0.75rem 0;
}

.metrics-list {
  display: grid;
  gap: 0.75rem;
}

.metric-item {
  padding: 0.75rem;
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 0.375rem;
}

.metric-item strong {
  display: block;
  font-size: 0.875rem;
  font-weight: 600;
  color: #1a202c;
  margin-bottom: 0.5rem;
}

.metric-item p {
  font-size: 0.875rem;
  color: #4a5568;
  margin: 0.25rem 0;
}

/* BCP/DRP Plans */
.plans-list {
  display: grid;
  gap: 1.5rem;
}

.plan-card {
  padding: 1.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  background: #f7fafc;
}

.plan-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e2e8f0;
}

.plan-name {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1a202c;
  margin: 0;
}

.plan-details-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}

.plan-detail-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.plan-detail-item label {
  font-size: 0.75rem;
  font-weight: 600;
  color: #718096;
  text-transform: uppercase;
}

.plan-detail-item p {
  font-size: 0.875rem;
  color: #1a202c;
  margin: 0;
}

.plan-scope {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
}

.plan-scope label {
  font-size: 0.75rem;
  font-weight: 600;
  color: #718096;
  text-transform: uppercase;
  display: block;
  margin-bottom: 0.5rem;
}

.plan-scope p {
  font-size: 0.875rem;
  color: #4a5568;
  line-height: 1.5;
  margin: 0;
}

/* Responsive */
@media (max-width: 768px) {
  .vendor-detail-container {
    padding: 1rem;
  }

  .detail-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .tabs-wrapper {
    padding: 0 1rem;
  }

  .tab {
    padding: 0.75rem 1rem;
    font-size: 0.8125rem;
  }

  .tab-label {
    display: none;
  }

  .tab i {
    font-size: 1rem;
  }

  .tab-content-wrapper {
    padding: 1rem;
  }

  .contract-details-grid,
  .sla-details-grid,
  .plan-details-grid,
  .audit-info-grid {
    grid-template-columns: 1fr;
  }

  .audit-header {
    flex-direction: column;
    align-items: flex-start;
  }
}

/* Audit Subsections */
.audit-subsection {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 2px solid #e2e8f0;
}

.audit-subsection:first-child {
  margin-top: 0;
  padding-top: 0;
  border-top: none;
}

.subsection-title {
  font-size: 1rem;
  font-weight: 600;
  color: #1a202c;
  margin: 0 0 1rem 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.subsection-title i {
  color: #2563eb;
}

.audits-list {
  display: grid;
  gap: 1.5rem;
}

.audit-card {
  background: #f7fafc;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  overflow: hidden;
}

.audit-header {
  padding: 1rem 1.5rem;
  background: #fff;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.audit-title {
  font-size: 1rem;
  font-weight: 600;
  color: #1a202c;
  margin: 0;
}

.audit-badges {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.audit-body {
  padding: 1.5rem;
}

.audit-info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}

.audit-info-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
}

.audit-info-item i {
  color: #2563eb;
  font-size: 1.25rem;
  margin-top: 0.25rem;
}

.audit-info-item label {
  font-size: 0.75rem;
  font-weight: 600;
  color: #718096;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  display: block;
  margin-bottom: 0.25rem;
}

.audit-info-item p {
  font-size: 0.875rem;
  color: #1a202c;
  margin: 0;
}

.audit-scope,
.audit-comments {
  margin-top: 1rem;
  padding: 1rem;
  background: #fff;
  border-radius: 0.375rem;
  border-left: 3px solid #2563eb;
}

.audit-scope label,
.audit-comments label {
  font-size: 0.75rem;
  font-weight: 600;
  color: #718096;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  display: block;
  margin-bottom: 0.5rem;
}

.audit-scope p,
.audit-comments p {
  font-size: 0.875rem;
  color: #4a5568;
  margin: 0;
  line-height: 1.6;
}

.audit-findings {
  margin-top: 1rem;
  padding: 1rem;
  background: #fef3c7;
  border-radius: 0.375rem;
  border-left: 3px solid #f59e0b;
}

.audit-findings label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #92400e;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.audit-findings label i {
  color: #f59e0b;
}

.findings-list {
  display: grid;
  gap: 0.75rem;
}

.finding-item {
  background: #fff;
  padding: 0.75rem;
  border-radius: 0.375rem;
  border: 1px solid #fbbf24;
}

.finding-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.finding-date {
  font-size: 0.75rem;
  color: #718096;
  font-weight: 600;
}

.finding-details {
  font-size: 0.875rem;
  color: #1a202c;
  margin: 0 0 0.5rem 0;
  line-height: 1.5;
}

.finding-impact,
.finding-comment {
  font-size: 0.8125rem;
  color: #4a5568;
  margin: 0.25rem 0;
  line-height: 1.5;
}

.empty-state-small {
  text-align: center;
  padding: 2rem 1rem;
  color: #9ca3af;
}

.empty-state-small i {
  font-size: 2rem;
  margin-bottom: 0.5rem;
  display: block;
}

.empty-state-small p {
  margin: 0;
  font-size: 0.875rem;
}
</style>
