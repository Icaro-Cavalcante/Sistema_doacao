import { mockData } from '../data/mockData.js';
import { state } from '../state.js';
import { getStatusColor, formatDate } from '../utils/helpers.js';

export function renderDoacoes() {
    const termoBusca = state.searchTerm.toLowerCase();
    
    // Filtra as doações por Doador, Categoria ou ID
    const doacoesFiltradas = mockData.doacoes.filter(d => 
        d.doador.toLowerCase().includes(termoBusca) || 
        d.categoria.toLowerCase().includes(termoBusca) ||
        d.id.toLowerCase().includes(termoBusca)
    );

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
                            <th class="p-4 font-medium border-b">Doador</th>
                            <th class="p-4 font-medium border-b">Categoria</th>
                            <th class="p-4 font-medium border-b">Data</th>
                            <th class="p-4 font-medium border-b">Status</th>
                            <th class="p-4 font-medium border-b text-center">Ações</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-200 bg-white">
                        ${doacoesFiltradas.length > 0 ? doacoesFiltradas.map(d => `
                            <tr class="hover:bg-gray-50 transition-colors">
                                <td class="p-4 font-medium text-gray-900 whitespace-nowrap">${d.id}</td>
                                <td class="p-4">
                                    <div class="font-medium text-gray-800">${d.doador}</div>
                                    <div class="text-xs text-gray-500">${d.telefone}</div>
                                </td>
                                <td class="p-4 text-sm text-gray-600">
                                    <div class="flex items-center gap-2">
                                        <i data-lucide="package" class="w-4 h-4 text-gray-400"></i>
                                        ${d.categoria}
                                    </div>
                                </td>
                                <td class="p-4 text-sm text-gray-600 whitespace-nowrap">${formatDate(d.data)}</td>
                                <td class="p-4 whitespace-nowrap">
                                    <span class="px-2.5 py-1 text-xs font-medium rounded-full ${getStatusColor(d.status)}">
                                        ${d.status}
                                    </span>
                                </td>
                                <td class="p-4 text-center whitespace-nowrap">
                                    <button class="text-gray-400 hover:text-blue-600 p-2 rounded-lg hover:bg-blue-50 transition-colors" title="Editar">
                                        <i data-lucide="edit" class="w-4 h-4"></i>
                                    </button>
                                </td>
                            </tr>
                        `).join('') : `
                            <tr>
                                <td colspan="6" class="p-8 text-center text-gray-500">
                                    Nenhum resultado encontrado para "<strong>${state.searchTerm}</strong>".
                                </td>
                            </tr>
                        `}
                    </tbody>
                </table>
            </div>
        </div>
    `;
}