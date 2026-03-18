import { api } from '../api.js';
import { state } from '../state.js';
import { getStatusColor, formatDate } from '../utils/helpers.js';

export async function renderBeneficiarios() {
    const termoBusca = (state.searchTerm || '').toLowerCase();
    
    try {
        // Busca beneficiários, usuários (para pegar o nome/contato) e pessoas físicas (para o documento)
        const [beneficiarios, usuarios, pessoasFisicas] = await Promise.all([
            api.getBeneficiarios().catch(() => []),
            api.getUsuarios().catch(() => []),
            api.getPessoasFisicas().catch(() => [])
        ]);

        const beneficiariosMapeados = beneficiarios.map(b => {
            const usuario = usuarios.find(u => u.id === b.id_usuario) || {};
            const pf = pessoasFisicas.find(p => p.id_usuario === b.id_usuario) || {};
            
            return {
                id_beneficiario: b.id_usuario, // No backend, o ID usado nas rotas é o id_usuario
                nome: usuario.nome || `Usuário #${b.id_usuario}`,
                contato: usuario.email || 'Sem contato',
                documento: pf.user_cpf || 'Não informado',
                tipo: pf.user_cpf ? 'Pessoa Física' : 'Outro',
                data_cadastro: b.data_cadastro_beneficiario,
                dependentes: 0, // Campo não existente no DB atual, fixado para o layout
                status: 'Ativo' // Campo não existente no DB atual, fixado para o layout
            };
        });

        // Filtra os beneficiários por Nome, Documento ou ID
        const beneficiariosFiltrados = beneficiariosMapeados.filter(b => 
            (b.nome || '').toLowerCase().includes(termoBusca) || 
            (b.documento || '').toLowerCase().includes(termoBusca) ||
            String(b.id_beneficiario).includes(termoBusca)
        ).reverse();

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
                                <th class="p-4 font-medium border-b w-16">ID</th>
                                <th class="p-4 font-medium border-b">Nome / Contato</th>
                                <th class="p-4 font-medium border-b">Documento / Tipo</th>
                                <th class="p-4 font-medium border-b text-center">Dependentes</th>
                                <th class="p-4 font-medium border-b text-center">Status</th>
                                <th class="p-4 font-medium border-b text-center">Ações</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-200 bg-white">
                            ${beneficiariosFiltrados.length > 0 ? beneficiariosFiltrados.map(b => `
                                <tr class="hover:bg-gray-50 transition-colors">
                                    <td class="p-4 text-xs font-mono text-gray-500 whitespace-nowrap">#${b.id_beneficiario}</td>
                                    <td class="p-4">
                                        <div class="font-bold text-gray-800">${b.nome}</div>
                                        <div class="text-xs text-gray-500 flex items-center gap-1 mt-0.5">
                                            <i data-lucide="mail" class="w-3 h-3"></i> ${b.contato}
                                        </div>
                                    </td>
                                    <td class="p-4 text-sm text-gray-600">
                                        <div>${b.documento}</div>
                                        <div class="text-xs text-gray-400 mt-0.5">${b.tipo}</div>
                                    </td>
                                    <td class="p-4 text-sm text-gray-600 text-center">${b.dependentes}</td>
                                    <td class="p-4 whitespace-nowrap text-center">
                                        <span class="px-2.5 py-1 text-xs font-medium rounded-full ${getStatusColor(b.status)}">
                                            ${b.status}
                                        </span>
                                    </td>
                                    <td class="p-4">
                                        <div class="flex items-center justify-center gap-2">
                                            <button class="p-1.5 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors border border-transparent hover:border-red-200" title="Excluir Beneficiário" onclick="window.deletarBeneficiario('${b.id_beneficiario}')">
                                                <i data-lucide="trash" class="w-4 h-4"></i>
                                            </button>
                                            <button class="p-1.5 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors ml-2" title="Editar Beneficiário" onclick="window.showToast('A Edição será implementada com a integração da API', 'info')">
                                                <i data-lucide="edit" class="w-4 h-4"></i>
                                            </button>
                                        </div>
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
    } catch (error) {
        console.error("Erro ao carregar os beneficiários:", error);
        return `<div class="p-8 text-center text-red-500">Erro ao carregar os beneficiários. Verifique a conexão com a API.</div>`;
    }
}