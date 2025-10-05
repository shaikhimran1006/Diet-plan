import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const generatePlan = async (userData) => {
    try {
        const response = await api.post('/generate-plan', userData);
        return response.data;
    } catch (error) {
        console.error('Error generating plan:', error);
        throw error;
    }
};

export const getUserHistory = async (userId) => {
    try {
        const response = await api.get(`/history/${userId}`);
        return response.data;
    } catch (error) {
        console.error('Error fetching history:', error);
        throw error;
    }
};

export default api;
