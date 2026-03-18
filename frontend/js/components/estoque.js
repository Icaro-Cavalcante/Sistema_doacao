import { api } from '../api.js';
import { state } from '../state.js';
import { getStatusColor } from '../utils/helpers.js';

export async function renderEstoque() {
    const termoBusca = (state.searchTerm || '').toLowerCase();
    
    try {
        const [itens, categorias, doacoesItens, distItens] = await Promise.all([
            api.getItens().catch(() => []),
            api.getCategorias().catch(() => []),
            api.getDoacoesItens().catch(() => []),
            api.getDistribuicoesItens().catch(() => [])
        ]);

        const estoqueMapeado = itens.map(item => {
            const categoria = categorias.find(c => c.id === item.id_categoria_item);
            
            // Calculando o saldo do estoque (Entradas - Saídas)
            const entradas = doacoesItens.filter(di => di.id_item === item.id).reduce((sum, curr) => sum + curr.quantidade_utilizada, 0);
            const saidas = distItens.filter(di => di.id_item === item.id).reduce((sum, curr) => sum + curr.quantidade_utilizada, 0);
            const quantidadeReal = entradas - saidas;

            let status = quantidadeReal > 10 ? 'Em Estoque' : (quantidadeReal > 0 ? 'Baixo Estoque' : 'Sem Estoque');

            return {
                id: item.id,
                nome: item.nome,
                categoria: categoria ? categoria.nome_categoria : 'Sem Categoria',
                quantidade: quantidadeReal,
                unidade: item.unidade_medida || 'un',
                status: status
            };
        });

        const estoqueFiltrado = estoqueMapeado.filter(item => 
            (item.nome || '').toLowerCase().includes(termoBusca) || 
            (item.categoria || '').toLowerCase().includes(termoBusca) ||
            String(item.id).includes(termoBusca)
        );

        return `
            <div class="bg-white rounded-xl shadow-sm p-6 mb-6">
                <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4">
                    <div>
                        <h2 class="text-xl font-bold text-gray-800">Estoque de Itens</h2>
                        <p class="text-sm text-gray-500">Controlo de itens disponíveis para distribuição após a triagem.</p>
                    </div>
                    <div class="flex gap-2 w-full sm:w-auto">
                        <button class="flex-1 sm:flex-none flex items-center justify-center gap-2 px-4 py-2 bg-white border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors" onclick="window.showToast('Funcionalidade de Categorias em desenvolvimento', 'info')">
                            <i data-lucide="tags" class="w-4 h-4"></i> Categorias
                        </button>
                        <button class="flex-1 sm:flex-none flex items-center justify-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors" onclick="window.openNovoItemModal()">
                            <i data-lucide="plus" class="w-4 h-4"></i> Novo Item
                        </button>
                    </div>
                </div>

                <div class="overflow-x-auto border border-gray-200 rounded-lg">
                    <table class="w-full text-left border-collapse">
                        <thead class="bg-gray-50 text-gray-500 text-xs uppercase tracking-wider">
                            <tr>
                                <th class="p-4 font-medium border-b w-16">ID</th>
                                <th class="p-4 font-medium border-b">Nome do Item</th>
                                <th class="p-4 font-medium border-b">Categoria</th>
                                <th class="p-4 font-medium border-b text-right">Quantidade</th>
                                <th class="p-4 font-medium border-b text-center">Status</th>
                                <th class="p-4 font-medium border-b text-center">Ações</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-200 bg-white">
                            ${estoqueFiltrado.length > 0 ? estoqueFiltrado.map(item => `
                                <tr class="hover:bg-gray-50 transition-colors">
                                    <td class="p-4 text-xs font-mono text-gray-500 whitespace-nowrap">#${item.id}</td>
                                    <td class="p-4 font-bold text-gray-800">${item.nome}</td>
                                    <td class="p-4 text-sm text-gray-600">
                                        <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-gray-100 text-gray-700 text-xs font-medium border border-gray-200">
                                            ${item.categoria}
                                        </span>
                                    </td>
                                    <td class="p-4 text-right">
                                        <span class="font-bold text-lg ${item.quantidade <= 0 ? 'text-red-500' : 'text-gray-900'}">${item.quantidade}</span>
                                        <span class="text-xs text-gray-500 ml-1">${item.unidade}</span>
                                    </td>
                                    <td class="p-4 text-center whitespace-nowrap">
                                        <span class="px-2.5 py-1 text-xs font-medium rounded-full ${getStatusColor(item.status)}">
                                            ${item.status}
                                        </span>
                                    </td>
                                    <td class="p-4">
                                        <div class="flex items-center justify-center gap-2">
                                            <button class="p-1.5 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors border border-transparent hover:border-red-200" title="Excluir Item" onclick="window.deletarItem('${item.id}')">
                                                <i data-lucide="trash" class="w-4 h-4"></i>
                                            </button>
                                            
                                            <button class="p-1.5 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors ml-2" title="Editar Item" onclick="window.showToast('A Edição será implementada com a integração da API', 'info')">
                                                <i data-lucide="edit" class="w-4 h-4"></i>
                                            </button>
                                        </div>
                                    </td>
                                </tr>
                            `).join('') : `
                                <tr>
                                    <td colspan="6" class="p-8 text-center text-gray-500">
                                        Nenhum item encontrado no estoque para "<strong>${state.searchTerm}</strong>".
                                    </td>
                                </tr>
                            `}
                        </tbody>
                    </table>
                </div>
            </div>
        `;
    } catch (error) {
        console.error("Erro ao carregar o estoque:", error);
        return `<div class="p-8 text-center text-red-500">Erro ao carregar o estoque de itens.</div>`;
    }
}