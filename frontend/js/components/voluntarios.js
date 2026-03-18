import { api } from '../api.js';
import { state } from '../state.js';
import { getStatusColor, formatDate } from '../utils/helpers.js';

export async function renderVoluntarios() {
    const termoBusca = (state.searchTerm || '').toLowerCase();
    
    try {
        const [vagas, inscricoes] = await Promise.all([
            api.getVagasVoluntariado().catch(() => []),
            api.getInscricoes().catch(() => [])
        ]);

        const vagasMapeadas = vagas.map(vaga => {
            const inscritos = inscricoes.filter(i => i.id_vaga === vaga.id).length;
            const statusVaga = new Date(vaga.data_fim) >= new Date(new Date().setHours(0,0,0,0)) ? 'Ativa' : 'Encerrada';

            return {
                ...vaga,
                inscritos: inscritos,
                status: statusVaga,
                vagasTotal: vaga.quantidade_vagas || 1 
            };
        });

        const vagasFiltradas = vagasMapeadas.filter(v => 
            (v.titulo || '').toLowerCase().includes(termoBusca) || 
            (v.descricao || '').toLowerCase().includes(termoBusca)
        );

        return `
            <div class="bg-white rounded-xl shadow-sm p-6 mb-6">
                <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4">
                    <div>
                        <h2 class="text-xl font-bold text-gray-800">Gestão de Voluntariado</h2>
                        <p class="text-sm text-gray-500">Vagas disponíveis e controlo de inscrições de voluntários.</p>
                    </div>
                    <button class="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors" onclick="window.openNovaVagaModal()">
                        <i data-lucide="plus" class="w-4 h-4"></i> Nova Vaga
                    </button>
                </div>

                ${vagasFiltradas.length === 0 ? `
                    <div class="p-12 text-center text-gray-500 border-2 border-dashed border-gray-200 rounded-xl">
                        <i data-lucide="search-x" class="w-10 h-10 mx-auto mb-3 text-gray-400"></i>
                        <p>Nenhuma vaga de voluntariado encontrada para "<strong>${state.searchTerm}</strong>".</p>
                    </div>
                ` : `
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        ${vagasFiltradas.map(v => `
                            <div class="bg-white border border-gray-200 rounded-xl p-5 hover:border-blue-300 hover:shadow-md transition-all flex flex-col h-full">
                                <div class="flex justify-between items-start mb-4">
                                    <h3 class="font-bold text-gray-800 text-lg leading-tight">${v.titulo}</h3>
                                    <span class="px-2.5 py-1 text-xs font-medium rounded-full whitespace-nowrap ${getStatusColor(v.status)}">
                                        ${v.status}
                                    </span>
                                </div>
                                
                                <p class="text-sm text-gray-600 mb-5 flex-grow">${v.descricao}</p>
                                
                                <div class="space-y-3 mb-5">
                                    <div class="flex items-center text-sm text-gray-500 gap-2">
                                        <i data-lucide="clock" class="w-4 h-4 text-gray-400"></i>
                                        <span>${v.carga_horaria || 'Carga horária não informada'}</span>
                                    </div>
                                    <div class="flex items-center text-sm text-gray-500 gap-2">
                                        <i data-lucide="calendar" class="w-4 h-4 text-gray-400"></i>
                                        <span>${formatDate(v.data_inicio)} a ${formatDate(v.data_fim)}</span>
                                    </div>
                                    <div class="flex items-center text-sm text-gray-500 gap-2">
                                        <i data-lucide="users" class="w-4 h-4 text-gray-400"></i>
                                        <span>${v.inscritos} / ${v.quantidade_vagas || 'Ilimitado'} inscritos</span>
                                    </div>
                                    
                                    <div class="w-full bg-gray-100 rounded-full h-2 mt-2 overflow-hidden">
                                        <div class="bg-blue-600 h-2 rounded-full transition-all duration-500" style="width: ${Math.min((v.inscritos / v.vagasTotal) * 100, 100)}%"></div>
                                    </div>
                                </div>
                                
                                <div class="flex gap-2 mt-auto pt-4 border-t border-gray-100">
                                    <button class="flex-1 py-2 bg-white border border-gray-300 text-gray-700 font-medium rounded-lg hover:bg-gray-50 transition-colors flex justify-center items-center gap-2" onclick="window.verInscritosModal(${v.id})">
                                        <i data-lucide="list" class="w-4 h-4"></i> Inscritos
                                    </button>
                                    <button class="flex-1 py-2 bg-red-50 text-red-700 border border-red-200 font-medium rounded-lg hover:bg-red-100 transition-colors flex justify-center items-center gap-2" onclick="window.deletarVaga(${v.id})">
                                        <i data-lucide="trash" class="w-4 h-4"></i> Excluir
                                    </button>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                `}
            </div>
        `;
    } catch (error) {
        console.error("Erro ao carregar as vagas:", error);
        return `<div class="p-8 text-center text-red-500">Erro ao carregar as vagas de voluntariado.</div>`;
    }
}