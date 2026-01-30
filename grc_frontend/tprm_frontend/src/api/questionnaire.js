import http from './http.js'

// Questionnaire API service
export const questionnaireApi = {
  // Get all questionnaires with optional filtering
  async getQuestionnaires(params = {}) {
    const queryParams = new URLSearchParams()
    
    if (params.search) queryParams.append('search', params.search)
    if (params.planType && params.planType !== 'ALL') queryParams.append('plan_type', params.planType)
    if (params.status && params.status !== 'ALL') queryParams.append('status', params.status)
    if (params.owner && params.owner !== 'ALL') queryParams.append('owner', params.owner)
    
    const queryString = queryParams.toString()
    const url = queryString ? `/api/tprm/v1/bcpdrp/questionnaires/?${queryString}` : '/api/tprm/v1/bcpdrp/questionnaires/'
    
    console.log('API Call - URL:', url)
    console.log('API Call - Params:', params)
    
    const response = await http.get(url)
    console.log('API Call - Raw Response:', response)
    
    return response
  },

  // Get detailed questionnaire information
  async getQuestionnaireDetail(questionnaireId) {
    return await http.get(`/api/tprm/v1/bcpdrp/questionnaires/${questionnaireId}/`)
  },


  // Create new questionnaire
  async createQuestionnaire(data) {
    return await http.post('/api/tprm/v1/bcpdrp/questionnaires/', data)
  },

  // Update questionnaire
  async updateQuestionnaire(questionnaireId, data) {
    return await http.patch(`/api/tprm/v1/bcpdrp/questionnaires/${questionnaireId}/`, data)
  },

  // Delete questionnaire
  async deleteQuestionnaire(questionnaireId) {
    return await http.delete(`/api/tprm/v1/bcpdrp/questionnaires/${questionnaireId}/`)
  }
}

export default questionnaireApi
