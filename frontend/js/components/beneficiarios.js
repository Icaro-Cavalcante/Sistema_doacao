import { mockData } from '../data/mockData.js';
import { state } from '../state.js';
import { getStatusColor } from '../utils/helpers.js';

export function renderBeneficiarios() {
    const termoBusca = state.searchTerm.toLowerCase();
    
    // Filtra os beneficiários por Nome, Documento ou ID
    const beneficiariosFiltrados = mockData.beneficiarios.filter(b => 
        b.nome.toLowerCase().includes(termoBusca) || 
        b.documento.toLowerCase().includes(termoBusca) ||
        b.id.toLowerCase().includes(termoBusca)
    );

    return `
        <div class="bg-white rounded-xl shadow-sm p-6 mb-6">
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4">
                <div>
                    <h2 class="text-xl font-bold text-gray-800">Beneficiários Cadastrados</h2>
                    <p class="text-sm text-gray-500">Gestão de pessoas e famílias que recebem auxílio da instituição.</p>
                </div>
                <button class="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors" onclick="window.openNovoBeneficiarioModal()">
                    <i data-lucide="user-plus" class="w-4 h-4"></i> Novo Beneficiário
                </button>
            </div>

            <div class="overflow-x-auto border border-gray-200 rounded-lg">
                <table class="w-full text-left border-collapse">
                    <thead class="bg-gray-50 text-gray-500 text-xs uppercase tracking-wider">
                        <tr>
                            <th class="p-4 font-medium border-b">ID</th>
                            <th class="p-4 font-medium border-b">Nome / Contato</th>
                            <th class="p-4 font-medium border-b">Documento / Tipo</th>
                            <th class="p-4 font-medium border-b text-center">Dependentes</th>
                            <th class="p-4 font-medium border-b">Status</th>
                            <th class="p-4 font-medium border-b text-center">Ações</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-200 bg-white">
                        ${beneficiariosFiltrados.length > 0 ? beneficiariosFiltrados.map(b => `
                            <tr class="hover:bg-gray-50 transition-colors">
                                <td class="p-4 text-xs font-mono text-gray-500 whitespace-nowrap">${b.id}</td>
                                <td class="p-4">
                                    <div class="font-bold text-gray-800">${b.nome}</div>
                                    <div class="text-xs text-gray-500 flex items-center gap-1 mt-0.5">
                                        <i data-lucide="phone" class="w-3 h-3"></i> ${b.contato}
                                    </div>
                                </td>
                                <td class="p-4 text-sm text-gray-600">
                                    <div>${b.documento}</div>
                                    <div class="text-xs text-gray-400 mt-0.5">${b.tipo}</div>
                                </td>
                                <td class="p-4 text-sm text-gray-600 text-center">${b.dependentes}</td>
                                <td class="p-4 whitespace-nowrap">
                                    <span class="px-2.5 py-1 text-xs font-medium rounded-full ${getStatusColor(b.status)}">
                                        ${b.status}
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
                                    Nenhum beneficiário encontrado para "<strong>${state.searchTerm}</strong>".
                                </td>
                            </tr>
                        `}
                    </tbody>
                </table>
            </div>
        </div>
    `;
}