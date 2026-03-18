import { mockData } from '../data/mockData.js';
import { state } from '../state.js';
import { getStatusColor, formatDate } from '../utils/helpers.js';

function renderResumoCards() {
    const stats = mockData.estatisticas;
    return `
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
            <div class="bg-white rounded-xl shadow-sm p-5 border border-gray-100 card-hover transition-all">
                <div class="flex justify-between items-start">
                    <div>
                        <p class="text-sm text-gray-500 mb-1 font-medium">Total de Doações</p>
                        <h3 class="text-2xl font-bold text-gray-800">${stats.doacoes.total}</h3>
                        <p class="text-xs text-green-500 mt-2 font-medium flex items-center gap-1">
                            <i data-lucide="trending-up" class="w-3 h-3"></i> ${stats.doacoes.variacao} este mês
                        </p>
                    </div>
                    <div class="p-3 rounded-lg bg-blue-50 text-blue-600"><i data-lucide="gift" class="w-5 h-5"></i></div>
                </div>
            </div>
            
            <div class="bg-white rounded-xl shadow-sm p-5 border border-gray-100 card-hover transition-all">
                <div class="flex justify-between items-start">
                    <div>
                        <p class="text-sm text-gray-500 mb-1 font-medium">Itens Distribuídos</p>
                        <h3 class="text-2xl font-bold text-gray-800">${stats.itens.distribuidos}</h3>
                        <p class="text-xs text-gray-400 mt-2 font-medium">
                            ${stats.itens.aguardando} aguardando
                        </p>
                    </div>
                    <div class="p-3 rounded-lg bg-green-50 text-green-600"><i data-lucide="package-check" class="w-5 h-5"></i></div>
                </div>
            </div>

            <div class="bg-white rounded-xl shadow-sm p-5 border border-gray-100 card-hover transition-all">
                <div class="flex justify-between items-start">
                    <div>
                        <p class="text-sm text-gray-500 mb-1 font-medium">Voluntários Ativos</p>
                        <h3 class="text-2xl font-bold text-gray-800">${stats.voluntarios.ativos}</h3>
                        <p class="text-xs text-blue-500 mt-2 font-medium flex items-center gap-1">
                            <i data-lucide="user-plus" class="w-3 h-3"></i> +${stats.voluntarios.novos} novos
                        </p>
                    </div>
                    <div class="p-3 rounded-lg bg-purple-50 text-purple-600"><i data-lucide="users" class="w-5 h-5"></i></div>
                </div>
            </div>

            <div class="bg-white rounded-xl shadow-sm p-5 border border-gray-100 card-hover transition-all">
                <div class="flex justify-between items-start">
                    <div>
                        <p class="text-sm text-gray-500 mb-1 font-medium">Famílias Atendidas</p>
                        <h3 class="text-2xl font-bold text-gray-800">${stats.beneficiarios.atendidos}</h3>
                        <p class="text-xs text-orange-500 mt-2 font-medium flex items-center gap-1">
                            <i data-lucide="alert-circle" class="w-3 h-3"></i> ${stats.beneficiarios.pendentes} pendentes
                        </p>
                    </div>
                    <div class="p-3 rounded-lg bg-orange-50 text-orange-600"><i data-lucide="heart-handshake" class="w-5 h-5"></i></div>
                </div>
            </div>
        </div>
    `;
}

function renderAcoesRapidas() {
    return `
        <div class="bg-white rounded-xl shadow-sm p-5 mb-6">
            <h2 class="text-lg font-semibold text-gray-800 mb-4">Ações Rápidas</h2>
            <div class="flex flex-wrap gap-3">
                <button class="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors shadow-sm" onclick="window.openNovaDoacaoModal()">
                    <i data-lucide="plus-circle" class="w-4 h-4"></i> Registrar Doação
                </button>
                <button class="flex items-center gap-2 px-4 py-2 bg-white border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors shadow-sm" onclick="window.openNovoPedidoModal()">
                    <i data-lucide="clipboard-list" class="w-4 h-4"></i> Novo Pedido
                </button>
                <button class="flex items-center gap-2 px-4 py-2 bg-white border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors shadow-sm" onclick="window.openNovoBeneficiarioModal()">
                    <i data-lucide="user-plus" class="w-4 h-4"></i> Cadastrar Beneficiário
                </button>
            </div>
        </div>
    `;
}

function renderTabelasDashboard() {
    const termoBusca = state.searchTerm.toLowerCase();
    
    // Filtra e pega apenas as 4 doações mais recentes
    const doacoesFiltradas = mockData.doacoes.filter(d => 
        d.doador.toLowerCase().includes(termoBusca) || d.id.toLowerCase().includes(termoBusca)
    ).slice(0, 4); 

    // Filtra e pega apenas os 4 pedidos pendentes mais recentes
    const pedidosPendentes = mockData.pedidos.filter(p => 
        p.status === 'Pendente' && 
        (p.beneficiario.toLowerCase().includes(termoBusca) || p.id.toLowerCase().includes(termoBusca))
    ).slice(0, 4);

    return `
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
            
            <div class="lg:col-span-2 bg-white rounded-xl shadow-sm p-5 flex flex-col">
                <div class="flex justify-between items-center mb-4">
                    <h2 class="text-lg font-semibold text-gray-800">Últimas Doações Recebidas</h2>
                    <button class="text-sm text-blue-600 hover:text-blue-800 font-medium transition-colors" onclick="window.mudarView('doacoes')">Ver todas</button>
                </div>
                <div class="overflow-x-auto flex-grow">
                    <table class="w-full text-left">
                        <thead class="bg-gray-50 text-xs text-gray-500 uppercase tracking-wider rounded-lg">
                            <tr>
                                <th class="px-4 py-3 font-medium rounded-tl-lg">ID</th>
                                <th class="px-4 py-3 font-medium">Doador</th>
                                <th class="px-4 py-3 font-medium">Data</th>
                                <th class="px-4 py-3 font-medium rounded-tr-lg text-center">Status</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-100">
                            ${doacoesFiltradas.length > 0 ? doacoesFiltradas.map(d => `
                                <tr class="hover:bg-gray-50 transition-colors">
                                    <td class="px-4 py-3 text-sm font-medium text-gray-900">${d.id}</td>
                                    <td class="px-4 py-3 text-sm text-gray-700">${d.doador}</td>
                                    <td class="px-4 py-3 text-sm text-gray-500">${formatDate(d.data)}</td>
                                    <td class="px-4 py-3 text-center">
                                        <span class="px-2.5 py-1 text-[11px] font-bold uppercase rounded-full whitespace-nowrap ${getStatusColor(d.status)}">${d.status}</span>
                                    </td>
                                </tr>
                            `).join('') : `
                                <tr><td colspan="4" class="px-4 py-8 text-center text-gray-500 text-sm">Nenhuma doação recente encontrada.</td></tr>
                            `}
                        </tbody>
                    </table>
                </div>
            </div>

            <div class="lg:col-span-1 bg-white rounded-xl shadow-sm p-5 flex flex-col">
                <div class="flex justify-between items-center mb-4">
                    <h2 class="text-lg font-semibold text-gray-800">Pedidos Pendentes</h2>
                    <button class="text-sm text-blue-600 hover:text-blue-800 font-medium transition-colors" onclick="window.mudarView('pedidos')">Ver todos</button>
                </div>
                <div class="flex flex-col gap-3 flex-grow">
                    ${pedidosPendentes.length > 0 ? pedidosPendentes.map(p => `
                        <div class="p-3 border border-gray-100 rounded-lg hover:border-blue-200 transition-colors bg-gray-50/50">
                            <div class="flex justify-between items-start mb-1">
                                <span class="font-bold text-sm text-gray-800 truncate pr-2">${p.beneficiario}</span>
                                <span class="px-2 py-0.5 text-[10px] font-bold uppercase rounded-full ${getStatusColor(p.prioridade)}">${p.prioridade}</span>
                            </div>
                            <p class="text-xs text-gray-500 mb-3 truncate">${p.tipo}</p>
                            <button class="w-full py-2 text-xs font-semibold text-blue-600 bg-blue-50 hover:bg-blue-600 hover:text-white rounded-lg transition-colors flex justify-center items-center gap-1" onclick="window.aprovarPedido('${p.id}')">
                                <i data-lucide="check" class="w-3.5 h-3.5"></i> Aprovar Pedido
                            </button>
                        </div>
                    `).join('') : `
                        <div class="flex flex-col items-center justify-center h-full text-gray-400 py-8">
                            <i data-lucide="check-circle-2" class="w-10 h-10 mb-3 text-green-400"></i>
                            <p class="text-sm text-center font-medium text-gray-500">Nenhum pedido pendente!</p>
                            <p class="text-xs text-center mt-1">Tudo em dia.</p>
                        </div>
                    `}
                </div>
            </div>
        </div>
    `;
}

export function renderDashboard() {
    return `
        ${renderResumoCards()}
        ${renderAcoesRapidas()}
        ${renderTabelasDashboard()}
    `;
}