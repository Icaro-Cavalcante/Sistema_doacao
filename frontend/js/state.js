import { mockData } from './data/mockData.js';

export const state = {
    sidebarOpen: true,
    currentView: 'dashboard',
    searchTerm: '',
    notifications: [...mockData.notificacoes],
    showNotifications: false
};