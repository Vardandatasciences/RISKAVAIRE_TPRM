import { createRouter, createWebHistory } from 'vue-router'
import authService from '@/services/authService'
import permissionsService from '@/services/permissionsService'
import store from '@/store'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/Login.vue'),
      meta: { requiresAuth: false, publicRoute: true }
    },
    {
      path: '/otp-verification',
      name: 'OtpVerification',
      component: () => import('@/views/OtpVerification.vue'),
      meta: { requiresAuth: false, publicRoute: true }
    },
    {
      path: '/',
      redirect: '/contracts'
    },
    {
      path: '/sla-index',
      name: 'SlaIndex',
      component: () => import('@/pages/Sla/Index.vue'),
      meta: { requiresAuth: true, permission: 'ViewSLA' }
    },
    {
      path: '/dashboard',
      name: 'Dashboard',
      component: () => import('@/pages/Sla/Dashboard.vue'),
      meta: { requiresAuth: true, permission: 'ViewSLA' }
    },
    // SLA Management Routes
    {
      path: '/slas',
      name: 'SLA Management',
      component: () => import('@/pages/Sla/SLAManagement.vue'),
      meta: { requiresAuth: true, permission: 'ViewSLA' }
    },
    {
      path: '/slas/create',
      name: 'SLA CreateEdit',
      component: () => import('@/pages/Sla/SLACreateEdit.vue'),
      meta: { requiresAuth: true, permission: 'CreateSLA' }
    },
    {
      path: '/slas/:id',
      name: 'SLA Detail',
      component: () => import('@/pages/Sla/SLADetail.vue'),
      meta: { requiresAuth: true, permission: 'ViewSLA' }
    },
    {
      path: '/slas/:id/edit',
      name: 'SLA Edit',
      component: () => import('@/pages/Sla/SLACreateEdit.vue'),
      meta: { requiresAuth: true, permission: 'UpdateSLA' }
    },
    {
      path: '/slas/active',
      name: 'SLA Active',
      component: () => import('@/pages/Sla/SLAActive.vue'),
      meta: { requiresAuth: true, permission: 'ViewSLA' }
    },
    {
      path: '/slas/expiring',
      name: 'SLA Expiring',
      component: () => import('@/pages/Sla/SLAExpiring.vue'),
      meta: { requiresAuth: true, permission: 'ViewSLA' }
    },
    {
      path: '/slas/renew',
      name: 'SLA Renew',
      component: () => import('@/pages/Sla/SLARenew.vue'),
      meta: { requiresAuth: true, permission: 'UpdateSLA' }
    },
    // SLA Approval Routes
    {
      path: '/slas/approvals',
      name: 'My SLA Approvals',
      component: () => import('@/pages/Sla/MySlaApprovals.vue'),
      meta: { requiresAuth: true, permission: 'ApproveContract' }
    },
    {
      path: '/slas/approvals/:id/review',
      name: 'SLA Review',
      component: () => import('@/pages/Sla/SLAReview.vue'),
      meta: { requiresAuth: true, permissions: ['ApproveContract', 'RejectContract'] }
    },
    {
      path: '/slas/approval-assignment',
      name: 'Sla Approval Assignment',
      component: () => import('@/pages/Sla/SlaApprovalAssignment.vue'),
      meta: { requiresAuth: true, permission: 'CreateSLA' }
    },
    // Performance Routes
    {
      path: '/performance',
      name: 'Performance Dashboard',
      component: () => import('@/pages/Sla/PerformanceDashboard.vue'),
      meta: { requiresAuth: true, permission: 'ViewSLA' }
    },
    // Audit Routes
    {
      path: '/audit',
      name: 'Audit Dashboard',
      component: () => import('@/pages/Sla/AuditDashboard.vue'),
      meta: { requiresAuth: true, permission: 'PerformContractAudit' }
    },
    {
      path: '/audit/create',
      name: 'Audit Create',
      component: () => import('@/pages/Sla/AuditCreate.vue'),
      meta: { requiresAuth: true, permission: 'PerformContractAudit' }
    },
    {
      path: '/audit/my-audits',
      name: 'My Audits',
      component: () => import('@/pages/Sla/MyAudits.vue'),
      meta: { requiresAuth: true, permission: 'PerformContractAudit' }
    },
    {
      path: '/audit/:auditId',
      name: 'Audit Execution',
      component: () => import('@/pages/Sla/AuditExecution.vue'),
      meta: { requiresAuth: true, permission: 'PerformContractAudit' }
    },
    {
      path: '/audit/:auditId/review',
      name: 'Audit Review',
      component: () => import('@/pages/Sla/AuditReview.vue'),
      meta: { requiresAuth: true, permission: 'PerformContractAudit' }
    },
    {
      path: '/audit/reports',
      name: 'Audit Reports',
      component: () => import('@/pages/Sla/AuditReports.vue'),
      meta: { requiresAuth: true, permission: 'PerformContractAudit' }
    },
    // Vendor Routes
    {
      path: '/vendors/compliance',
      name: 'Vendor Compliance',
      component: () => import('@/pages/Sla/VendorCompliance.vue'),
      meta: { requiresAuth: true, permission: 'ViewSLA' }
    },
    {
      path: '/vendors/performance',
      name: 'Vendor Performance Summary',
      component: () => import('@/pages/Sla/VendorPerformanceSummary.vue'),
      meta: { requiresAuth: true, permission: 'ViewSLA' }
    },
    // Analytics Routes
    {
      path: '/analytics/trends',
      name: 'Trend Analysis',
      component: () => import('@/pages/Sla/TrendAnalysis.vue'),
      meta: { requiresAuth: true, permission: 'ViewSLA' }
    },
    {
      path: '/kpi-dashboard',
      name: 'KPI Dashboard',
      component: () => import('@/pages/Sla/KPIDashboard.vue'),
      meta: { requiresAuth: true, permission: 'ViewSLA' }
    },
    {
      path: '/notifications',
      name: 'Notifications',
      component: () => import('@/pages/Sla/Notifications.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/settings',
      name: 'Settings',
      component: () => import('@/pages/Settings.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/admin-access',
      name: 'Admin Access',
      component: () => import('@/pages/AdminAccess.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/quick-access',
      name: 'Quick Access Dashboard',
      component: () => import('@/pages/Sla/QuickAccessDashboard.vue'),
      meta: { requiresAuth: true, permission: 'ViewSLA' }
    },
    // BCP/DRP Routes
    {
      path: '/bcp/vendor-upload',
      name: 'BCP Vendor Upload',
      component: () => import('@/pages/BCP/VendorUpload.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/bcp/plan-submission-ocr',
      name: 'BCP Plan Submission OCR',
      component: () => import('@/pages/BCP/PlanSubmissionOcr.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/bcp/evaluation',
      name: 'BCP Plan Evaluation',
      component: () => import('@/pages/BCP/PlanEvaluation.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/bcp/library',
      name: 'BCP Plan Library',
      component: () => import('@/pages/BCP/PlanLibrary.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/bcp/questionnaire-library',
      name: 'BCP Questionnaire Library',
      component: () => import('@/pages/BCP/QuestionnaireLibrary.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/bcp/testing-library',
      name: 'BCP Testing Library',
      component: () => import('@/pages/BCP/TestingLibrary.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/bcp/questionnaire-builder',
      name: 'BCP Questionnaire Builder',
      component: () => import('@/pages/BCP/QuestionnaireBuilder.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/bcp/questionnaire-workflow',
      name: 'BCP Questionnaire Workflow',
      component: () => import('@/pages/BCP/QuestionnaireWorkflow.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/bcp/questionnaire-assignment',
      name: 'BCP Questionnaire Assignment',
      component: () => import('@/pages/BCP/QuestionnaireAssignment.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/bcp/approval-assignment',
      name: 'BCP Approval Assignment',
      component: () => import('@/pages/BCP/ApprovalAssignment.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/bcp/questionnaire-assignment-workflow',
      name: 'BCP Questionnaire Assignment Workflow',
      component: () => import('@/pages/BCP/QuestionnaireAssignmentWorkflow.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/bcp/my-approvals',
      name: 'BCP My Approvals',
      component: () => import('@/pages/BCP/MyApprovals.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/bcp/vendor-hub',
      name: 'BCP Vendor Hub',
      component: () => import('@/pages/BCP/VendorHub.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/bcp/vendor-overview/:vendorId',
      name: 'BCP Vendor Overview',
      component: () => import('@/pages/BCP/VendorOverview.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/bcp/kpi-dashboard',
      name: 'BCP KPI Dashboard',
      component: () => import('@/pages/BCP/KPIDashboard.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/bcp/dashboard',
      name: 'BCP Dashboard',
      component: () => import('@/pages/BCP/Dashboard.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/bcp/risk-analytics',
      name: 'BCP Risk Analytics',
      component: () => import('@/pages/BCP/RiskAnalytics.vue'),
      meta: { requiresAuth: true }
    },
    // Contract Authentication
    {
      path: '/contract-login',
      name: 'Contract Login',
      component: () => import('@/pages/contract/Login.vue')
    },
    // Contract Management Routes
    {
      path: '/contractdashboard',
      name: 'Contract Dashboard',
      component: () => import('@/pages/contract/ContractDashboard.vue')
    },
    {
      path: '/contracts',
      name: 'Contracts',
      component: () => import('@/pages/contract/Contracts.vue')
    },
    {
      path: '/contracts/new',
      redirect: '/contracts/create'
    },
    {
      path: '/contracts/preview',
      name: 'Contract Preview',
      component: () => import('@/pages/contract/ContractPreview.vue')
    },
    {
      path: '/contracts/create',
      name: 'Create Contract',
      component: () => import('@/pages/contract/CreateContract.vue')
    },
    {
      path: '/contracts/:id',
      name: 'Contract Detail',
      component: () => import('@/pages/contract/ContractDetail.vue')
    },
    {
      path: '/contracts/:id/edit',
      name: 'Edit Contract',
      component: () => import('@/pages/contract/EditContract.vue')
    },
    {
      path: '/contracts/:id/edit-advanced',
      name: 'Edit Contract Advanced',
      component: () => import('@/pages/contract/EditContractAdvanced.vue')
    },
    {
      path: '/contracts/:id/renewal',
      name: 'Contract Renewal',
      component: () => import('@/pages/contract/ContractRenewal.vue')
    },
    {
      path: '/renewals/:renewalId',
      name: 'View Contract Renewal',
      component: () => import('@/pages/contract/ContractRenewal.vue')
    },
    {
      path: '/contracts/:id/subcontract',
      name: 'Create Subcontract',
      component: () => import('@/pages/contract/CreateSubcontract.vue')
    },
    {
      path: '/contracts/:id/create-subcontract-advanced',
      name: 'Create Subcontract Advanced',
      component: () => import('@/pages/contract/CreateSubcontractAdvanced.vue')
    },
    {
      path: '/contracts/:id/create-amendment',
      name: 'Create Amendment',
      component: () => import('@/pages/contract/CreateAmendment.vue')
    },
    {
      path: '/contracts/:contractId/detail',
      name: 'Contract Detail View',
      component: () => import('@/pages/contract/ContractDetailView.vue')
    },
    {
      path: '/contracts/:contractId/review',
      name: 'Contract Review',
      component: () => import('@/pages/contract/ContractReviewEdit.vue')
    },
    {
      path: '/contract-audit/:auditId/execute',
      name: 'Contract Audit Execution',
      component: () => import('@/pages/contract/ContractAuditExecution.vue')
    },
    {
      path: '/contract-audit/:auditId/review',
      name: 'Contract Audit Review',
      component: () => import('@/pages/contract/ContractAuditReview.vue')
    },
    {
      path: '/vendors',
      name: 'Vendor Contracts',
      component: () => import('@/pages/contract/VendorContracts.vue')
    },
    {
      path: '/vendors/:id',
      name: 'Vendor Detail',
      component: () => import('@/pages/contract/VendorDetail.vue')
    },
    {
      path: '/contract-approval-assignment',
      name: 'Contract Approval Assignment',
      component: () => import('@/pages/contract/ContractApprovalAssignment.vue')
    },
    {
      path: '/my-contract-approvals',
      name: 'My Contract Approvals',
      component: () => import('@/pages/contract/MyContractApprovals.vue')
    },
    {
      path: '/approvals',
      name: 'Approvals',
      component: () => import('@/pages/contract/MyContractApprovals.vue')
    },
    {
      path: '/archive',
      name: 'Contract Archive',
      component: () => import('@/pages/contract/ContractArchive.vue')
    },
    {
      path: '/search',
      name: 'Contract Search',
      component: () => import('@/pages/contract/Search.vue')
    },
    {
      path: '/contract-comparison',
      name: 'Contract Comparison',
      component: () => import('@/pages/contract/ContractComparison.vue')
    },
    {
      path: '/analytics',
      name: 'Contract Analytics',
      component: () => import('@/pages/contract/ContractAnalytics.vue')
    },
    {
      path: '/contract-kpi-dashboard',
      name: 'Contract KPI Dashboard',
      component: () => import('@/pages/contract/ContractKPIDashboard.vue')
    },
    // Contract Audit Routes
    {
      path: '/audit/dashboard',
      name: 'Contract Audit Dashboard',
      component: () => import('@/pages/contract/ContractAuditDashboard.vue')
    },
    {
      path: '/contract-audit/all',
      name: 'Contract Audits',
      component: () => import('@/pages/contract/ContractAudits.vue')
    },
    {
      path: '/contract-audit/create',
      name: 'Contract Audit Create',
      component: () => import('@/pages/contract/ContractAuditCreate.vue')
    },
    {
      path: '/contract-audit/reports',
      name: 'Contract Audit Reports',
      component: () => import('@/pages/contract/ContractAuditReports.vue')
    },
    
    // Vendor Management Routes
    {
      path: '/vendor-dashboard',
      name: 'Vendor Dashboard',
      component: () => import('@/pages/vendor/VendorDashboard.vue'),
      meta: { requiresAuth: true, permission: 'vendor_view' }
    },
    {
      path: '/vendor-kpi-dashboard',
      name: 'Vendor KPI Dashboard',
      component: () => import('@/pages/vendor/VendorKPIDashboard.vue'),
      meta: { requiresAuth: true, permission: 'vendor_view' }
    },
    {
      path: '/vendor-registration',
      name: 'Vendor Registration',
      component: () => import('@/pages/vendor/VendorRegistration.vue'),
      meta: { requiresAuth: true, permission: 'vendor_create' }
    },
    {
      path: '/vendor-verification',
      name: 'Vendor External Screening',
      component: () => import('@/pages/vendor/VendorExternalScreening.vue'),
      meta: { requiresAuth: true, permission: 'vendor_view' }
    },
    {
      path: '/vendor-questionnaire',
      name: 'Vendor Questionnaire Builder',
      component: () => import('@/pages/vendor/VendorQuestionnaireBuilder.vue'),
      meta: { requiresAuth: true, permission: 'vendor_create' }
    },
    {
      path: '/vendor-questionnaire-response',
      name: 'Vendor Questionnaire Response',
      component: () => import('@/pages/vendor/VendorQuestionnaireResponse.vue'),
      meta: { requiresAuth: true, permission: 'vendor_update' }
    },
    {
      path: '/vendor-questionnaire-assignment',
      name: 'Questionnaire Assignment',
      component: () => import('@/pages/vendor/QuestionnaireAssignment.vue'),
      meta: { requiresAuth: true, permission: 'vendor_update' }
    },
    {
      path: '/vendor-risk-scoring',
      name: 'Vendor Risk Scoring',
      component: () => import('@/pages/vendor/VendorRiskScoring.vue'),
      meta: { requiresAuth: true, permission: 'vendor_view' }
    },
    {
      path: '/vendor-lifecycle',
      name: 'Vendor Lifecycle Tracker',
      component: () => import('@/pages/vendor/VendorLifecycleTracker.vue'),
      meta: { requiresAuth: true, permission: 'vendor_view' }
    },
    {
      path: '/vendor-approval-dashboard',
      name: 'Vendor Approval Dashboard',
      component: () => import('@/pages/vendor/VenderApprovalDashboard.vue'),
      meta: { requiresAuth: true, permission: 'vendor_approve_reject' }
    },
    {
      path: '/vendor-approval-workflow-creator',
      name: 'Vendor Approval Workflow Creator',
      component: () => import('@/pages/vendor/ApprovalWorkflowCreator.vue'),
      meta: { requiresAuth: true, permission: 'vendor_create' }
    },
    {
      path: '/vendor-my-approvals',
      name: 'Vendor MyApprovals',
      component: () => import('@/pages/vendor/MyApprovals.vue'),
      meta: { requiresAuth: true, permission: 'vendor_approve_reject' }
    },
    {
      path: '/vendor-all-approvals',
      name: 'Vendor AllApprovals',
      component: () => import('@/pages/vendor/AllApprovals.vue'),
      meta: { requiresAuth: true, permission: 'vendor_approve_reject' }
    },
    {
      path: '/vendor-stage-reviewer',
      name: 'Vendor Stage Reviewer',
      component: () => import('@/pages/vendor/StageReviewer.vue'),
      meta: { requiresAuth: true, permission: 'vendor_approve_reject' }
    },
    {
      path: '/vendor-assignee-decision',
      name: 'Vendor Assignee Decision',
      component: () => import('@/pages/vendor/AssigneeDecision.vue'),
      meta: { requiresAuth: true, permission: 'vendor_approve_reject' }
    },
    {
      path: '/vendor-login',
      name: 'Vendor Login',
      component: () => import('@/pages/vendor/Login.vue'),
      meta: { publicRoute: true }
    },
    
    // RFP Management Routes
    {
      path: '/rfp-dashboard',
      name: 'RFP Dashboard',
      component: () => import('@/views/rfp/Dashboard.vue'),
      meta: { requiresAuth: true, permission: 'view_rfp' }
    },
    {
      path: '/rfp-workflow',
      name: 'RFP Workflow',
      component: () => import('@/views/rfp/RFPWorkflow.vue'),
      meta: { requiresAuth: true, permission: 'view_rfp' }
    },
    {
      path: '/rfp-creation',
      name: 'RFP Creation',
      component: () => import('@/views/rfp/Phase1Creation.vue'),
      meta: { requiresAuth: true, permission: 'create_rfp' }
    },
    {
      path: '/rfp-approval',
      name: 'RFP Approval',
      component: () => import('@/views/rfp/Phase2Approval.vue'),
      meta: { requiresAuth: true, permission: 'approve_rfp' }
    },
    {
      path: '/rfp-vendor-selection',
      name: 'RFP Vendor Selection',
      component: () => import('@/views/rfp/Phase3VendorSelection.vue'),
      meta: { requiresAuth: true, permission: 'view_rfp' }
    },
    {
      path: '/rfp-url-generation',
      name: 'RFP Url Generation',
      component: () => import('@/views/rfp/Phase4URLGeneration.vue'),
      meta: { requiresAuth: true, permission: 'view_rfp' }
    },
    {
      path: '/rfp-evaluation',
      name: 'RFP Evaluation',
      component: () => import('@/views/rfp/Phase6Evaluation.vue'),
      meta: { requiresAuth: true, permission: 'evaluate_rfp' }
    },
    {
      path: '/rfp-list',
      name: 'RFP List',
      component: () => import('@/views/rfp/RFPList.vue'),
      meta: { requiresAuth: true, permission: 'view_rfp' }
    },
    {
      path: '/rfp-comparison',
      name: 'RFP Comparison',
      component: () => import('@/views/rfp/Phase7Comparison.vue'),
      meta: { requiresAuth: true, permission: 'view_rfp' }
    },
    {
      path: '/rfp-consensus',
      name: 'RFP Consensus & Award',
      component: () => import('@/views/rfp/Phase8ConsensusAndAward.vue'),
      meta: { requiresAuth: true, permission: 'view_rfp' }
    },
    {
      path: '/rfp-award',
      redirect: '/rfp-consensus'
    },
    {
      path: '/award-response/:token',
      name: 'AwardResponse',
      component: () => import('@/views/rfp/AwardResponse.vue'),
      meta: { requiresAuth: false, publicRoute: true, standalone: true }
    },
    {
      path: '/vendor-portal/:token?',
      name: 'Vendor Portal',
      component: () => import('@/views/rfp/VendorPortal.vue'),
      props: true,
      meta: { requiresAuth: false, publicRoute: true }
    },
    {
      path: '/submit',
      name: 'Vendor Portal - Submit',
      component: () => import('@/views/rfp/VendorPortal.vue'),
      meta: { requiresAuth: false, publicRoute: true }
    },
    {
      path: '/submit/open',
      name: 'Vendor Portal - Open',
      component: () => import('@/views/rfp/VendorPortal.vue'),
      meta: { requiresAuth: false, publicRoute: true }
    },
    {
      path: '/rfp-analytics',
      name: 'RFP Analytics - KPIs',
      component: () => import('@/views/rfp/KPIs.vue'),
      meta: { requiresAuth: true, permission: 'view_rfp' }
    },
    {
      path: '/draft-manager',
      name: 'Draft Manager',
      component: () => import('@/views/rfp/DraftManager.vue'),
      meta: { requiresAuth: true, permission: 'view_rfp' }
    },
    
    // RFP Approval Routes
    {
      path: '/approval-management',
      name: 'Approval Management',
      component: () => import('@/views/rfp-approval/ApprovalWorkflowCreator.vue'),
      meta: { requiresAuth: true, permission: 'approve_rfp' }
    },
    {
      path: '/approval-workflow-creator',
      name: 'Approval Workflow Creator',
      component: () => import('@/views/rfp-approval/ApprovalWorkflowCreator.vue'),
      meta: { requiresAuth: true, permission: 'approve_rfp' }
    },
    {
      path: '/my-approvals',
      name: 'MyApprovals',
      component: () => import('@/views/rfp-approval/MyApprovals.vue'),
      meta: { requiresAuth: true, permission: 'approve_rfp' }
    },
    {
      path: '/all-approvals',
      name: 'AllApprovals',
      component: () => import('@/views/rfp-approval/AllApprovals.vue'),
      meta: { requiresAuth: true, permission: 'approve_rfp' }
    },
    {
      path: '/stage-reviewer',
      name: 'StageReviewer',
      component: () => import('@/views/rfp-approval/StageReviewer.vue'),
      meta: { requiresAuth: true, permission: 'approve_rfp' }
    },
    {
      path: '/assignee-decision',
      name: 'AssigneeDecision',
      component: () => import('@/views/rfp-approval/AssigneeDecision.vue'),
      meta: { requiresAuth: true, permission: 'approve_rfp' }
    },
    {
      path: '/proposal-evaluation',
      name: 'ProposalEvaluation',
      component: () => import('@/views/rfp-approval/ProposalEvaluation.vue'),
      meta: { requiresAuth: true, permission: 'evaluate_rfp' }
    },
    {
      path: '/committee-selection',
      name: 'CommitteeSelection',
      component: () => import('@/views/rfp-approval/CommitteeSelection.vue').catch((error) => {
        console.error('Failed to load CommitteeSelection component:', error)
        // Return a fallback component or redirect
        return import('@/views/rfp/NotFound.vue').catch(() => {
          // If even the fallback fails, return a simple error component
          return {
            template: '<div class="p-8 text-center"><h2 class="text-xl font-bold text-red-600 mb-4">Component Load Error</h2><p class="text-gray-600">Failed to load Committee Selection component. Please refresh the page.</p></div>'
          }
        })
      }),
      meta: { requiresAuth: true, permission: 'view_rfp' }
    },
    {
      path: '/committee-evaluation',
      name: 'CommitteeEvaluation',
      component: () => import('@/views/rfp-approval/CommitteeEvaluation.vue'),
      meta: { requiresAuth: true, permission: 'evaluate_rfp' }
    },
    {
      path: '/rfp-approval/version-manager',
      name: 'VersionManager',
      component: () => import('@/views/rfp-approval/VersionManager.vue'),
      meta: { requiresAuth: true, permission: 'view_rfp' }
    },
    {
      path: '/rfp-approval/change-request-manager',
      name: 'ChangeRequestManager',
      component: () => import('@/views/rfp-approval/ChangeRequestManager.vue'),
      meta: { requiresAuth: true, permission: 'create_rfp' }
    },
    {
      path: '/rfp-creation',
      name: 'RFPCreation',
      component: () => import('@/views/rfp/Phase1Creation.vue'),
      meta: { requiresAuth: true, permission: 'create_rfp' }
    },
    {
      path: '/review/:id',
      name: 'Vendor Review',
      component: () => import('@/pages/vendor/StageReviewer.vue'),
      props: true,
      meta: { requiresAuth: true, permission: 'vendor_approve_reject' }
    },

    // Global Search Routes
    {
      path: '/global-search',
      name: 'GlobalSearch',
      component: () => import('@/pages/GlobalSearch_TPRM.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/questionnaire-templates',
      name: 'QuestionnaireTemplates',
      component: () => import('@/pages/QuestionnaireTemplates.vue'),
      meta: { requiresAuth: true }
    },
 
    
    // Access Denied Route
    {
      path: '/access-denied',
      name: 'Access Denied',
      component: () => import('@/components/AccessDenied.vue'),
      meta: { requiresAuth: true }
    },
    
    // 404 Route
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: () => import('@/pages/Sla/NotFound.vue')
    }
  ]
})

// Navigation guard to check authentication
router.beforeEach(async (to, from, next) => {
  // Check if we're in an iframe (embedded in GRC)
  const isInIframe = window.self !== window.top
  const isAuthenticated = authService.isAuthenticated()
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth !== false)
  const isPublicRoute = to.matched.some(record => record.meta.publicRoute === true)
  const requiredPermission = to.meta.permission
  const requiredPermissions = to.meta.permissions
  console.log('Router guard:', {
    to: to.path,
    isAuthenticated,
    requiresAuth,
    isPublicRoute,
    requiredPermission,
    isInIframe
  })
  
  // If route requires auth and user is not authenticated
  if (requiresAuth && !isAuthenticated) {
    // If in iframe, don't redirect to login - allow access and let GRC auth sync
    if (isInIframe) {
      console.log('[Router Guard] In iframe mode - allowing access, GRC auth will sync')
      // Check for GRC tokens one more time
      const grcToken = localStorage.getItem('access_token') || 
                      localStorage.getItem('session_token') || 
                      localStorage.getItem('token')
      if (grcToken) {
        // Sync GRC auth
        if (!localStorage.getItem('session_token')) {
          localStorage.setItem('session_token', grcToken)
        }
        const grcUser = localStorage.getItem('user') || localStorage.getItem('current_user')
        if (grcUser && !localStorage.getItem('current_user')) {
          try {
            const parsedUser = typeof grcUser === 'string' ? JSON.parse(grcUser) : grcUser
            localStorage.setItem('current_user', JSON.stringify(parsedUser))
          } catch (e) {
            localStorage.setItem('current_user', grcUser)
          }
        }
        // Re-check authentication
        if (authService.isAuthenticated()) {
          next()
          return
        }
      }
      // Even without token, allow access in iframe - parent will handle auth
      console.log('[Router Guard] Allowing access in iframe mode (no redirect to login)')
      next()
      return
    }
    
    // Not in iframe - redirect to login as normal
    console.log('Redirecting to login - authentication required')
    next('/login')
    return
  }
  
  // If trying to access login page while already authenticated
  if (to.path === '/login' && isAuthenticated) {
    console.log('Already authenticated, redirecting to contracts')
    next('/contracts')
    return
  }
  
  // If in iframe and trying to access login page, redirect to contracts instead
  if (isInIframe && to.path === '/login') {
    console.log('[Router Guard] In iframe - redirecting from login to contracts')
    next('/contracts')
    return
  }
  
  // Check RBAC permission if required
  if ((requiredPermission || (requiredPermissions && requiredPermissions.length)) && isAuthenticated) {
    const permissionsToCheck = requiredPermissions && requiredPermissions.length
      ? requiredPermissions
      : [requiredPermission]
 
    console.log(`[Router Guard] Checking permission(s): ${permissionsToCheck.join(', ')} for route: ${to.path}`)
   
    try {
      // If in iframe and user might still be syncing, wait a bit and retry
      let hasPermission = false
      let retries = isInIframe ? 2 : 1 // Give iframe mode one retry
      
      for (let attempt = 0; attempt < retries && !hasPermission; attempt++) {
        if (attempt > 0) {
          console.log(`[Router Guard] Retrying permission check (attempt ${attempt + 1})...`)
          // Wait a bit for auth to sync
          await new Promise(resolve => setTimeout(resolve, 500))
          // Re-check authentication
          if (!authService.isAuthenticated()) {
            console.log('[Router Guard] Auth lost during retry, re-initializing...')
            await store.dispatch('auth/initializeAuth')
          }
        }
        
        for (const permission of permissionsToCheck) {
          const result = await permissionsService.checkPermission(permission)
          if (result) {
            hasPermission = true
            break
          }
        }
        
        // If we got permission, break out of retry loop
        if (hasPermission) break
      }
     
      console.log(`[Router Guard] Permission check complete:`, {
        permissionsChecked: permissionsToCheck,
        hasPermission,
        route: to.path
      })
     
      if (!hasPermission) {
        // In iframe mode, if permission check fails but we have auth, allow access anyway
        // (GRC parent will handle permissions)
        if (isInIframe && isAuthenticated) {
          console.log('[Router Guard] In iframe mode - allowing access despite permission check failure (GRC handles permissions)')
          next()
          return
        }
        
        console.warn(`[Router Guard] Permission DENIED: ${requiredPermission} for route: ${to.path}`)
       
        // Store error details for AccessDenied page
        sessionStorage.setItem('access_denied_error', JSON.stringify({
          message: `You do not have permission to access this page`,
          code: '403',
          permission: permissionsToCheck.join(', '),
          timestamp: new Date().toISOString(),
          path: to.path
        }))
       
        next('/access-denied')
        return
      }
     
      console.log(`[Router Guard] Permission GRANTED: ${requiredPermission} for route: ${to.path}`)
    } catch (error) {
      console.error('[Router Guard] Error checking permission:', error)
      
      // In iframe mode, if there's an error but we have auth, allow access
      if (isInIframe && isAuthenticated) {
        console.log('[Router Guard] In iframe mode - allowing access despite permission check error (GRC handles permissions)')
        next()
        return
      }
      
      // On error, deny access for security
      sessionStorage.setItem('access_denied_error', JSON.stringify({
        message: 'Unable to verify permissions',
        code: '500',
        permission: requiredPermission,
        timestamp: new Date().toISOString(),
        path: to.path
      }))
      next('/access-denied')
      return
    }
  }
 
  // All checks passed, allow navigation
  next()
})
// Global error handler for route navigation
router.onError((error) => {
  console.error('Router navigation error:', error)
  // Log the error but don't break the app
  const errorMessage = error.message || 'Unknown navigation error'
 
  // If it's a module loading error, try to provide helpful information
  if (errorMessage.includes('Failed to fetch dynamically imported module') ||
      errorMessage.includes('Loading chunk') ||
      errorMessage.includes('ChunkLoadError')) {
    console.warn('Module loading error detected. This might be a build or network issue.')
    console.warn('Error details:', {
      message: errorMessage,
      stack: error.stack,
      name: error.name
    })
    
    // For BCP pages, don't redirect - let the error be handled by the component
    const currentPath = window.location.pathname
    if (currentPath.startsWith('/bcp/')) {
      console.warn('[Router Error] BCP page load error - staying on page, component will handle error')
      // Don't redirect - let the component handle the error
      return
    }
  }
 
  // Don't throw - let Vue Router handle it gracefully
  // Don't redirect on errors - let the current route handle it
})
export default router
 
 