import { mockData } from '../data/mockData.js';
import { state } from '../state.js';
import { getStatusColor, formatDate } from '../utils/helpers.js';

export function renderPedidos() {
    const termoBusca = state.searchTerm.toLowerCase();
    
    // Filtra os pedidos por Beneficiário ou Tipo de necessidade
    const pedidosFiltrados = mockData.pedidos.filter(p => 
        p.beneficiario.toLowerCase().includes(termoBusca) || 
        p.tipo.toLowerCase().includes(termoBusca) ||
        p.id.toLowerCase().includes(termoBusca)
    );

    return `
        <div class="bg-white rounded-xl shadow-sm p-6 mb-6">
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4">
                <div>
                    <h2 class="text-xl font-bold text-gray-800">Pedidos de Auxílio</h2>
                    <p class="text-sm text-gray-500">Avalie e distribua doações para os beneficiários cadastrados.</p>
                </div>
                <button class="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors" onclick="window.openNovoPedidoModal()">
                    <i data-lucide="file-text" class="w-4 h-4"></i> Novo Pedido
                </button>
            </div>

            ${pedidosFiltrados.length === 0 ? `
                <div class="p-12 text-center text-gray-500 border-2 border-dashed border-gray-200 rounded-xl">
                    <i data-lucide="search-x" class="w-10 h-10 mx-auto mb-3 text-gray-400"></i>
                    <p>Nenhum pedido de auxílio encontrado para "<strong>${state.searchTerm}</strong>".</p>
                </div>
            ` : `
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    ${pedidosFiltrados.map(p => `
                        <div class="bg-white border border-gray-200 rounded-xl p-5 hover:border-blue-300 hover:shadow-md transition-all flex flex-col h-full relative overflow-hidden">
                            
                            <div class="absolute top-0 left-0 w-full h-1 ${p.prioridade === 'Alta' ? 'bg-red-500' : p.prioridade === 'Média' ? 'bg-yellow-400' : 'bg-green-500'}"></div>
                            
                            <div class="flex justify-between items-start mb-4 mt-2">
                                <div>
                                    <h3 class="font-bold text-gray-800 text-lg leading-tight">${p.beneficiario}</h3>
                                    <p class="text-xs text-gray-500 mt-1">Solicitado em: ${formatDate(p.dataSolicitacao)}</p>
                                </div>
                                <span class="px-2.5 py-1 text-xs rounded-full whitespace-nowrap ${getStatusColor(p.status)}">${p.status}</span>
                            </div>
                            
                            <div class="mb-5 flex-grow">
                                <div class="flex items-center gap-2 mb-2">
                                    <span class="text-xs font-bold text-gray-500 uppercase tracking-wider">Necessidade:</span>
                                    <span class="text-sm font-semibold text-gray-700">${p.tipo}</span>
                                </div>
                                
                                <div class="bg-gray-50 rounded-lg p-3 text-sm text-gray-600 border border-gray-100">
                                    <span class="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-1">Itens Solicitados:</span>
                                    <ul class="list-disc list-inside space-y-1">
                                        ${p.itensNecessarios.map(item => `<li>${item}</li>`).join('')}
                                    </ul>
                                </div>
                            </div>
                            
                            <div class="flex items-center justify-between text-sm text-gray-500 mb-5 pt-3 border-t border-gray-100">
                                <div class="flex items-center gap-1.5" title="Prioridade">
                                    <i data-lucide="alert-triangle" class="w-4 h-4 ${p.prioridade === 'Alta' ? 'text-red-500' : 'text-gray-400'}"></i>
                                    <span class="font-medium ${getStatusColor(p.prioridade).replace('bg-', 'text-').split(' ')[1]}">${p.prioridade}</span>
                                </div>
                                <div class="flex items-center gap-1.5" title="Contato">
                                    <i data-lucide="phone" class="w-4 h-4 text-gray-400"></i>
                                    <span>${p.contato}</span>
                                </div>
                            </div>
                            
                            <div class="flex gap-2 mt-auto">
                                ${p.status === 'Pendente' ? `
                                    <button class="flex-1 py-2 bg-green-50 text-green-700 border border-green-200 font-medium rounded-lg hover:bg-green-600 hover:text-white transition-colors flex justify-center items-center gap-2" onclick="window.aprovarPedido('${p.id}')">
                                        <i data-lucide="check" class="w-4 h-4"></i> Aprovar
                                    </button>
                                ` : `
                                    <button class="flex-1 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors flex justify-center items-center gap-2" onclick="window.distribuirPedido('${p.id}')">
                                        <i data-lucide="truck" class="w-4 h-4"></i> Distribuir
                                    </button>
                                `}
                            </div>
                        </div>
                    `).join('')}
                </div>
            `}
        </div>
    `;
}