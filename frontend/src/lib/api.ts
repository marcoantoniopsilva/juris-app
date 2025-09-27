import axios from 'axios'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Interceptor para adicionar token de autenticação
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Interceptor para tratar erros
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('auth_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export const authAPI = {
  login: (email: string, password: string) =>
    api.post('/auth/login', new URLSearchParams({ username: email, password }), {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    }),
  
  register: (data: { name: string; email: string; password: string }) =>
    api.post('/auth/register', data),
  
  getProfile: () => api.get('/auth/me'),
  
  logout: () => api.post('/auth/logout'),
}

export const unitsAPI = {
  list: () => api.get('/units'),
  
  get: (id: string) => api.get(`/units/${id}`),
  
  create: (data: any) => api.post('/units', data),
  
  addMember: (unitId: string, data: any) =>
    api.post(`/units/${unitId}/members`, data),
  
  listMembers: (unitId: string) => api.get(`/units/${unitId}/members`),
}

export const documentsAPI = {
  upload: (file: File, ownerScope: string, ownerId: string) => {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('owner_scope', ownerScope)
    formData.append('owner_id', ownerId)
    return api.post('/documents/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
  
  list: (ownerScope?: string, ownerId?: string) =>
    api.get('/documents', { params: { owner_scope: ownerScope, owner_id: ownerId } }),
  
  get: (id: string) => api.get(`/documents/${id}`),
  
  delete: (id: string) => api.delete(`/documents/${id}`),
}

export const casesAPI = {
  create: (data: any) => api.post('/cases', data),
  
  list: (unitId?: string) => api.get('/cases', { params: { unit_id: unitId } }),
  
  get: (id: string) => api.get(`/cases/${id}`),
  
  addFile: (caseId: string, documentId: string, fileType: string) =>
    api.post(`/cases/${caseId}/files`, { document_id: documentId, file_type: fileType }),
}

export const ragAPI = {
  search: (data: any) => api.post('/rag/search', data),
  
  hybridSearch: (data: any) => api.post('/rag/hybrid-search', data),
}

export const jurisAPI = {
  scrape: (data: any) => api.post('/juris/scrape', data),
  
  list: (tribunal?: string) => api.get('/juris', { params: { tribunal } }),
  
  search: (data: any) => api.post('/juris/search', data),
  
  get: (id: string) => api.get(`/juris/${id}`),
  
  getTribunals: () => api.get('/juris/tribunais/disponiveis'),
}

export const draftsAPI = {
  generate: (data: any) => api.post('/drafts/generate', data),
  
  get: (id: string) => api.get(`/drafts/${id}`),
  
  update: (id: string, data: any) => api.put(`/drafts/${id}`, data),
  
  listCaseDrafts: (caseId: string) => api.get(`/drafts/case/${caseId}`),
}

export const templatesAPI = {
  list: (unitId?: string, tipoAto?: string) =>
    api.get('/templates', { params: { unit_id: unitId, tipo_ato: tipoAto } }),
  
  create: (data: any) => api.post('/templates', data),
  
  get: (id: string) => api.get(`/templates/${id}`),
  
  update: (id: string, data: any) => api.put(`/templates/${id}`, data),
  
  delete: (id: string) => api.delete(`/templates/${id}`),
}

export default api