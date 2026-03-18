import { api } from '../api.js';
import { state } from '../state.js';
import { formatDate } from '../utils/helpers.js';

export async function renderUsuarios() {
    const termoBusca = (state.searchTerm || '').toLowerCase();
    
    try {
        const usuarios = await api.getUsuarios().catch(() => []);

        // Filtra os usuários por Nome, E-mail, Login ou ID
        const usuariosFiltrados = usuarios.filter(u => 
            (u.nome || '').toLowerCase().includes(termoBusca) || 
            (u.email || '').toLowerCase().includes(termoBusca) ||
            (u.login || '').toLowerCase().includes(termoBusca) ||
            String(u.id).includes(termoBusca)
        ).reverse(); // Mais recentes primeiro

        return `
            <div class="bg-white rounded-xl shadow-sm p-6 mb-6">
                <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4">
                    <div>
                        <h2 class="text-xl font-bold text-gray-800">Gestão de Usuários</h2>
                        <p class="text-sm text-gray-500">Administração de contas de acesso ao sistema.</p>
                    </div>
                    <button class="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors" onclick="window.openNovoUsuarioModal()">
                        <i data-lucide="user-plus" class="w-4 h-4"></i> Novo Usuário
                    </button>
                </div>

                <div class="overflow-x-auto border border-gray-200 rounded-lg">
                    <table class="w-full text-left border-collapse">
                        <thead class="bg-gray-50 text-gray-500 text-xs uppercase tracking-wider">
                            <tr>
                                <th class="p-4 font-medium border-b w-16">ID</th>
                                <th class="p-4 font-medium border-b">Nome</th>
                                <th class="p-4 font-medium border-b">E-mail</th>
                                <th class="p-4 font-medium border-b">Login</th>
                                <th class="p-4 font-medium border-b text-center">Data de Cadastro</th>
                                <th class="p-4 font-medium border-b text-center">Ações</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-200 bg-white">
                            ${usuariosFiltrados.length > 0 ? usuariosFiltrados.map(u => `
                                <tr class="hover:bg-gray-50 transition-colors">
                                    <td class="p-4 text-xs font-mono text-gray-500 whitespace-nowrap">#${u.id}</td>
                                    <td class="p-4 font-bold text-gray-800">
                                        <div class="flex items-center gap-3">
                                            <div class="w-8 h-8 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center font-bold text-xs uppercase flex-shrink-0">
                                                ${(u.nome || 'U').charAt(0)}
                                            </div>
                                            ${u.nome}
                                        </div>
                                    </td>
                                    <td class="p-4 text-sm text-gray-600">${u.email}</td>
                                    <td class="p-4 text-sm text-gray-600 font-medium">@${u.login}</td>
                                    <td class="p-4 text-sm text-gray-600 text-center whitespace-nowrap">${formatDate(u.data_cadastro)}</td>
                                    <td class="p-4">
                                        <div class="flex items-center justify-center gap-2">
                                            <button class="p-1.5 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors border border-transparent hover:border-red-200" title="Excluir Usuário" onclick="window.deletarUsuario('${u.id}')">
                                                <i data-lucide="trash" class="w-4 h-4"></i>
                                            </button>
                                            <button class="p-1.5 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors ml-2" title="Editar Usuário" onclick="window.showToast('A Edição será implementada com a integração da API', 'info')">
                                                <i data-lucide="edit" class="w-4 h-4"></i>
                                            </button>
                                        </div>
                                    </td>
                                </tr>
                            `).join('') : `
                                <tr>
                                    <td colspan="6" class="p-8 text-center text-gray-500">
                                        Nenhum usuário encontrado para "<strong>${state.searchTerm}</strong>".
                                    </td>
                                </tr>
                            `}
                        </tbody>
                    </table>
                </div>
            </div>
        `;
    } catch (error) {
        console.error("Erro ao carregar os usuários:", error);
        return `<div class="p-8 text-center text-red-500">Erro ao carregar os usuários. Verifique a conexão com a API.</div>`;
    }
}