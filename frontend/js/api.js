// frontend/js/api.js
const API_URL = 'http://localhost:8000';

export const api = {
    // Buscar todas as doações (GET /doacoes/)
    getDoacoes: async () => {
        try {
            const response = await fetch(`${API_URL}/doacoes/`);
            if (!response.ok) throw new Error('Falha ao carregar doações');
            return await response.json();
        } catch (error) {
            console.error('Erro na API:', error);
            if(window.showToast) window.showToast('Erro ao ligar ao servidor', 'error');
            return [];
        }
    },

    // Criar nova doação (POST /doacoes/)
    criarDoacao: async (dadosDoacao) => {
        try {
            const response = await fetch(`${API_URL}/doacoes/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(dadosDoacao)
            });
            if (!response.ok) throw new Error('Falha ao registar doação');
            return await response.json();
        } catch (error) {
            console.error('Erro na API:', error);
            throw error;
        }
    }
};
