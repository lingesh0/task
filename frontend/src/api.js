import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8001/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Sessions API
export const sessionsAPI = {
  // Create a new session
  createSession: async (sessionData) => {
    const response = await api.post('/sessions/', sessionData);
    return response.data;
  },

  // Get a specific session
  getSession: async (sessionId) => {
    const response = await api.get(`/sessions/${sessionId}`);
    return response.data;
  },

  // Start a session
  startSession: async (sessionId) => {
    const response = await api.patch(`/sessions/${sessionId}/start`);
    return response.data;
  },

  // Pause a session
  pauseSession: async (sessionId, reason) => {
    const response = await api.patch(`/sessions/${sessionId}/pause`, { reason });
    return response.data;
  },

  // Resume a session
  resumeSession: async (sessionId) => {
    const response = await api.patch(`/sessions/${sessionId}/resume`);
    return response.data;
  },

  // Complete a session
  completeSession: async (sessionId) => {
    const response = await api.patch(`/sessions/${sessionId}/complete`);
    return response.data;
  },

  // Get session history
  getSessionHistory: async () => {
    const response = await api.get('/sessions/history');
    return response.data;
  },
};

export default api;
