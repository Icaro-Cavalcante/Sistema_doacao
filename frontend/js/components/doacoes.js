// frontend/js/components/doacoes.js
import { api } from '../api.js';
import { state } from '../state.js';
import { getStatusColor, formatDate } from '../utils/helpers.js';

export function renderDoacoes() {
    const termoBusca = state.searchTerm.toLowerCase();
    
    // O truque aqui é arrancar a busca assíncrona logo após devolver o HTML base
    setTimeout(() => carregarTabela(termoBusca), 0);

    return `
        <div class="bg-white rounded-xl shadow-sm p-6 mb-6">
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4">
                <div>
                    <h2 class="text-xl font-bold text-gray-800">Gestão de Doações</h2>
                    <p class="text-sm text-gray-500">Lista completa de todas as doações recebidas e em trânsito.</p>
                </div>
                <button class="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors" onclick="window.openNovaDoacaoModal()">
                    <i data-lucide="plus" class="w-4 h-4"></i> Nova Doação
                </button>
            </div>

            <div class="overflow-x-auto border border-gray-200 rounded-lg">
                <table class="w-full text-left border-collapse">
                    <thead class="bg-gray-50 text-gray-500 text-xs uppercase tracking-wider">
                        <tr>
                            <th class="p-4 font-medium border-b">ID</th>
                            <th class="p-4 font-medium border-b">ID Usuário</th>
                            <th class="p-4 font-medium border-b">Descrição</th>
                            <th class="p-4 font-medium border-b">Data</th>
                            <th class="p-4 font-medium border-b">Status</th>
                            <th class="p-4 font-medium border-b text-center">Ações</th>
                        </tr>
                    </thead>
                    <tbody id="corpo-tabela-doacoes" class="divide-y divide-gray-200 bg-white">
                        <tr>
                            <td colspan="6" class="p-8 text-center text-gray-500">
                                <i data-lucide="loader-2" class="w-6 h-6 animate-spin mx-auto mb-2 text-blue-500"></i>
                                A carregar doações da API...
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    `;
}

// Função auxiliar que preenche os dados reais
async function carregarTabela(termoBusca) {
    const tbody = document.getElementById('corpo-tabela-doacoes');
    if (!tbody) return; // Utilizador já mudou de página, interromper a operação

    try {
        const doacoes = await api.getDoacoes();
        
        // Filtra pelo que foi devolvido no Pydantic schema
        const doacoesFiltradas = doacoes.filter(d => 
            (d.descricao || '').toLowerCase().includes(termoBusca) || 
            String(d.id).includes(termoBusca)
        );

        if (doacoesFiltradas.length === 0) {
            tbody.innerHTML = `<tr><td colspan="6" class="p-8 text-center text-gray-500">Nenhum resultado encontrado para "<strong>${termoBusca}</strong>".</td></tr>`;
        } else {
            tbody.innerHTML = doacoesFiltradas.map(d => `
                <tr class="hover:bg-gray-50 transition-colors">
                    <td class="p-4 font-medium text-gray-900 whitespace-nowrap">#${d.id}</td>
                    <td class="p-4">
                        <div class="font-medium text-gray-800">Utilizador #${d.id_usuario}</div>
                    </td>
                    <td class="p-4 text-sm text-gray-600">
                        ${d.descricao || 'Sem descrição'}
                    </td>
                    <td class="p-4 text-sm text-gray-600 whitespace-nowrap">${formatDate(d.data_doacao)}</td>
                    <td class="p-4 whitespace-nowrap">
                        <span class="px-2.5 py-1 text-xs font-medium rounded-full ${getStatusColor(d.status_doacao)}">
                            ${d.status_doacao}
                        </span>
                    </td>
                    <td class="p-4 text-center whitespace-nowrap">
                        <button class="text-gray-400 hover:text-blue-600 p-2 rounded-lg hover:bg-blue-50 transition-colors" title="Editar">
                            <i data-lucide="edit" class="w-4 h-4"></i>
                        </button>
                    </td>
                </tr>
            `).join('');
        }
        if (window.lucide) window.lucide.createIcons();
    } catch (error) {
        tbody.innerHTML = `<tr><td colspan="6" class="p-8 text-center text-red-500">Erro ao carregar dados. Verifique se o Uvicorn está a correr.</td></tr>`;
    }
}