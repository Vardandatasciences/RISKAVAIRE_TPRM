import http from '../api/http.js'

// Create API service with methods for different endpoints
const api = {

  // Plans endpoints
  plans: {
    list: (params) => http.get('/api/tprm/v1/bcpdrp/plans/', { params }),
    get: (id) => http.get(`/api/tprm/v1/bcpdrp/plans/${id}/`),
    create: (data) => http.post('/api/tprm/v1/bcpdrp/plans/', data),
    update: (id, data) => http.patch(`/api/tprm/v1/bcpdrp/plans/${id}/`, data),
    delete: (id) => http.delete(`/api/tprm/v1/bcpdrp/plans/${id}/`),
    getEvaluations: (id) => http.get(`/api/tprm/v1/bcpdrp/evaluations/${id}/`),
    approve: (id) => http.post(`/api/tprm/v1/bcpdrp/plans/${id}/approve/`),
    reject: (id) => http.post(`/api/tprm/v1/bcpdrp/plans/${id}/reject/`),
  },

  // Strategies endpoints
  strategies: {
    list: (params) => http.get('/api/tprm/v1/bcpdrp/strategies/', { params }),
  },

  // OCR endpoints
  ocr: {
    plans: (params) => http.get('/api/tprm/v1/bcpdrp/ocr/plans/', { params }),
    planDetail: (id) => http.get(`/api/tprm/v1/bcpdrp/ocr/plans/${id}/`),
    extract: (id, data) => http.post(`/api/tprm/v1/bcpdrp/ocr/plans/${id}/extract/`, data),
    updateStatus: (id, data) => http.patch(`/api/tprm/v1/bcpdrp/ocr/plans/${id}/status/`, data),
  },

  // Evaluations endpoints
  evaluations: {
    list: (planId) => http.get(`/api/tprm/v1/bcpdrp/evaluations/${planId}/`),
    save: (planId, data) => {
      // Evaluation saves now use background tasks for risk generation, so normal timeout is fine
      return http.post(`/api/tprm/v1/bcpdrp/evaluations/${planId}/save/`, data)
    },
  },

  // Risks endpoints
  risks: {
    getPlanRisks: (planId) => http.get(`/api/tprm/v1/bcpdrp/plans/${planId}/risks/`),
  },

  // Vendor upload endpoint
  vendorUpload: (data) => http.post('/api/tprm/v1/bcpdrp/vendor-upload/', data),

  // Dropdowns endpoint
  dropdowns: (params) => http.get('/api/tprm/v1/bcpdrp/dropdowns/', { params }),

  // Plan types endpoints
  planTypes: {
    list: () => http.get('/api/tprm/v1/bcpdrp/plan-types/'),
    create: (data) => http.post('/api/tprm/v1/bcpdrp/plan-types/create/', data),
    update: (id, data) => http.put(`/api/tprm/v1/bcpdrp/plan-types/${id}/update/`, data),
    delete: (id) => http.delete(`/api/tprm/v1/bcpdrp/plan-types/${id}/delete/`),
  },
  
  // Questionnaires endpoints
  questionnaires: {
    list: (params) => http.get('/api/tprm/v1/bcpdrp/questionnaires/', { params }),
    get: (id) => http.get(`/api/tprm/v1/bcpdrp/questionnaires/${id}/`),
    save: (data) => http.post('/api/tprm/v1/bcpdrp/questionnaires/save/', data),
    assignments: (params) => http.get('/api/tprm/v1/bcpdrp/questionnaires/assignments/', { params }),
    saveAnswers: (assignmentId, data) => http.put(`/api/tprm/v1/bcpdrp/questionnaires/assignments/${assignmentId}/save/`, data),
    getDetails: (id) => http.get(`/api/tprm/v1/bcpdrp/questionnaires/${id}/`),
    approve: (id) => http.post(`/api/tprm/v1/bcpdrp/questionnaires/${id}/approve/`),
    reject: (id) => http.post(`/api/tprm/v1/bcpdrp/questionnaires/${id}/reject/`),
  },

  // Questionnaire Workflow endpoints
  questionnaireWorkflow: {
    // Create questionnaire with plan association
    createQuestionnaire: (data) => http.post('/api/tprm/v1/bcpdrp/questionnaires/save/', data),
    // Assign questionnaire for testing
    assignQuestionnaire: (data) => http.post('/api/tprm/v1/bcpdrp/approvals/assignments/', data),
    // Get workflow status
    getWorkflowStatus: (questionnaireId) => http.get(`/api/tprm/v1/bcpdrp/questionnaires/${questionnaireId}/workflow/`),
    // Complete workflow (questionnaire creation + assignment)
    completeWorkflow: (data) => http.post('/api/tprm/v1/bcpdrp/questionnaire-workflow/complete/', data),
  },
  // Questionnaire Template endpoints
  questionnaireTemplates: {
    list: (params) => http.get('/api/tprm/v1/bcpdrp/questionnaire-templates/', { params }),
    get: (id) => http.get(`/api/tprm/v1/bcpdrp/questionnaire-templates/${id}/`),
    save: (data) => http.post('/api/tprm/v1/bcpdrp/questionnaire-templates/save/', data),
  },
  // Plan decisions endpoint
  planDecision: (id, data) => http.patch(`/api/tprm/v1/bcpdrp/plans/${id}/decision/`, data),

  // Users endpoints
  users: {
    list: (params) => http.get('/api/tprm/v1/bcpdrp/users/', { params }),
  },

  // Approvals endpoints
  approvals: {
    list: (params) => http.get('/api/tprm/v1/bcpdrp/approvals/', { params }),
    createAssignment: (data) => http.post('/api/tprm/v1/bcpdrp/approvals/assignments/', data),
    myApprovals: (params) => http.get('/api/tprm/v1/bcpdrp/my-approvals/', { params }),
    updateStatus: (approvalId, data) => http.patch(`/api/tprm/v1/bcpdrp/approvals/${approvalId}/status/`, data),
  },

  // Assignment responses endpoints
  assignments: {
    getResponseDetails: (id) => http.get(`/api/tprm/v1/bcpdrp/questionnaires/assignments/`, { params: { assignment_response_id: id } }),
    approve: (id) => http.post(`/api/tprm/v1/bcpdrp/questionnaires/assignments/${id}/approve/`),
    reject: (id) => http.post(`/api/tprm/v1/bcpdrp/questionnaires/assignments/${id}/reject/`),
  },

   // Dashboard endpoints
   dashboard: {
    overview: () => http.get('/api/tprm/v1/bcpdrp/dashboard/overview/'),
    kpi: () => http.get('/api/tprm/v1/bcpdrp/dashboard/kpi/'),
    plans: () => http.get('/api/tprm/v1/bcpdrp/dashboard/plans/'),
    evaluations: () => http.get('/api/tprm/v1/bcpdrp/dashboard/evaluations/'),
    evaluationScores: () => http.get('/api/tprm/v1/bcpdrp/dashboard/evaluation-scores/'),
    testing: () => http.get('/api/tprm/v1/bcpdrp/dashboard/testing/'),
    risks: () => http.get('/api/tprm/v1/bcpdrp/dashboard/risks/'),
    temporal: () => http.get('/api/tprm/v1/bcpdrp/dashboard/temporal/'),
  },
}

export default api
