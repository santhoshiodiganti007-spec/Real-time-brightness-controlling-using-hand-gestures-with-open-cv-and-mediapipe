import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getHealth = async () => (await api.get('/health')).data;
export const getDiagnostics = async () => (await api.get('/diagnostics')).data;

export const getBrightness = async () => (await api.get('/brightness')).data;
export const setBrightness = async (brightness) => (await api.post('/brightness', { brightness })).data;

export const getGestureStatus = async () => (await api.get('/gesture/status')).data;
export const startGestureControl = async () => (await api.post('/gesture/start')).data;
export const stopGestureControl = async () => (await api.post('/gesture/stop')).data;

export const startCalibration = async () => (await api.post('/calibration/start')).data;
export const recordCalibrationStep = async (step) => (await api.post('/calibration/record', { step })).data;
export const saveCalibration = async () => (await api.post('/calibration/save')).data;

export const getSettings = async () => (await api.get('/settings')).data;
export const updateSettings = async (settings) => (await api.put('/settings', settings)).data;

export const getStatistics = async () => (await api.get('/statistics')).data;
export const getHistory = async (limit = 50) => (await api.get(`/history?limit=${limit}`)).data;

export const startCamera = async (cameraIndex = 0) => (await api.post(`/camera/start?camera_index=${cameraIndex}`)).data;
export const stopCamera = async () => (await api.post('/camera/stop')).data;

export default api;
