import { api } from '../api.js';
import { state } from '../state.js';
import { getStatusColor, formatDate } from '../utils/helpers.js';

export async function renderDoacoes() {
    const termoBusca = (state.searchTerm || '').toLowerCase();
    
    try {
        const [doacoes, usuarios] = await Promise.all([
            api.getDoacoes().catch(() => []),
            api.getUsuarios().catch(() => [])
        ]);

        const doacoesMapeadas = doacoes.map(d => {
            const usuario = usuarios.find(u => u.id === d.id_usuario);
            return {
                ...d,
                nome_doador: usuario ? usuario.nome : `Usuário #${d.id_usuario}`
            };
        });

        const doacoesFiltradas = doacoesMapeadas.filter(d => 
            (d.descricao || '').toLowerCase().includes(termoBusca) || 
            (d.nome_doador || '').toLowerCase().includes(termoBusca) ||
            String(d.id).includes(termoBusca)
        ).reverse(); // Mais recentes primeiro

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
                                <th class="p-4 font-medium border-b w-16">ID</th>
                                <th class="p-4 font-medium border-b">Doador</th>
                                <th class="p-4 font-medium border-b">Descrição</th>
                                <th class="p-4 font-medium border-b">Data</th>
                                <th class="p-4 font-medium border-b text-center">Status</th>
                                <th class="p-4 font-medium border-b text-center">Ações</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-200 bg-white">
                            ${doacoesFiltradas.length > 0 ? doacoesFiltradas.map(d => `
                                <tr class="hover:bg-gray-50 transition-colors">
                                    <td class="p-4 text-xs font-mono text-gray-500 whitespace-nowrap">#${d.id}</td>
                                    <td class="p-4 font-bold text-gray-800">${d.nome_doador}</td>
                                    <td class="p-4 text-sm text-gray-600">${d.descricao || 'Sem descrição'}</td>
                                    <td class="p-4 text-sm text-gray-600 whitespace-nowrap">${formatDate(d.data_doacao)}</td>
                                    <td class="p-4 text-center whitespace-nowrap">
                                        <span class="px-2.5 py-1 text-xs font-medium rounded-full ${getStatusColor(d.status_doacao)}">
                                            ${d.status_doacao}
                                        </span>
                                    </td>
                                    <td class="p-4">
                                        <div class="flex items-center justify-center gap-2">
                                            <button class="p-1.5 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors border border-transparent hover:border-red-200" title="Excluir Doação" onclick="window.deletarDoacao('${d.id}')">
                                                <i data-lucide="trash" class="w-4 h-4"></i>
                                            </button>
                                            <button class="p-1.5 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors ml-2" title="Editar Doação" onclick="window.showToast('A Edição será implementada com a integração da API', 'info')">
                                                <i data-lucide="edit" class="w-4 h-4"></i>
                                            </button>
                                        </div>
                                    </td>
                                </tr>
                            `).join('') : `
                                <tr>
                                    <td colspan="6" class="p-8 text-center text-gray-500">
                                        Nenhuma doação encontrada para "<strong>${state.searchTerm}</strong>".
                                    </td>
                                </tr>
                            `}
                        </tbody>
                    </table>
                </div>
            </div>
        `;
    } catch (error) {
        console.error("Erro ao carregar as doações:", error);
        return `<div class="p-8 text-center text-red-500">Erro ao carregar as doações. Verifique a conexão com a API.</div>`;
    }
}