import { api } from '../api.js';
import { showToast } from '../utils/helpers.js';

// Modal padrão (com botão de salvar)
function createModal(title, content, onSave) {
    const modalId = 'modal-' + Math.random().toString(36).substr(2, 9);
    const modalHtml = `
        <div id="${modalId}" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 transition-opacity p-4">
            <div class="bg-white rounded-xl shadow-lg w-full max-w-md p-6 relative animate-fade-in-up max-h-[90vh] overflow-y-auto">
                <button type="button" onclick="document.getElementById('${modalId}').remove()" class="absolute top-4 right-4 text-gray-400 hover:text-gray-600 transition-colors">
                    <i data-lucide="x" class="w-5 h-5"></i>
                </button>
                <h3 class="text-lg font-bold text-gray-800 mb-4">${title}</h3>
                <form onsubmit="event.preventDefault(); ${onSave}(this)">
                    ${content}
                    <div class="flex justify-end gap-3 mt-6">
                        <button type="button" onclick="document.getElementById('${modalId}').remove()" class="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors font-medium">
                            Cancelar
                        </button>
                        <button type="submit" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium shadow-sm flex items-center gap-2">
                            Salvar
                        </button>
                    </div>
                </form>
            </div>
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    if (window.lucide) window.lucide.createIcons();
}

// Modal de visualização (só botão fechar)
function createViewModal(title, content) {
    const modalId = 'modal-' + Math.random().toString(36).substr(2, 9);
    const modalHtml = `
        <div id="${modalId}" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 transition-opacity p-4">
            <div class="bg-white rounded-xl shadow-lg w-full max-w-md p-6 relative animate-fade-in-up max-h-[90vh] overflow-y-auto">
                <button type="button" onclick="document.getElementById('${modalId}').remove()" class="absolute top-4 right-4 text-gray-400 hover:text-gray-600 transition-colors">
                    <i data-lucide="x" class="w-5 h-5"></i>
                </button>
                <h3 class="text-lg font-bold text-gray-800 mb-4">${title}</h3>
                ${content}
                <div class="flex justify-end mt-6">
                    <button type="button" onclick="document.getElementById('${modalId}').remove()" class="px-4 py-2 bg-gray-100 text-gray-700 hover:bg-gray-200 rounded-lg transition-colors font-medium">
                        Fechar
                    </button>
                </div>
            </div>
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    if (window.lucide) window.lucide.createIcons();
}

// === DOAÇÕES ===
export function openNovaDoacaoModal() {
    const content = `
        <div class="space-y-4 text-left">
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">ID do Usuário (Doador)</label>
                <input type="number" name="id_usuario" required min="1" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition-shadow">
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Descrição</label>
                <input type="text" name="descricao" required placeholder="Ex: Doação de roupas de inverno" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition-shadow">
            </div>
        </div>
    `;
    createModal('Registrar Nova Doação', content, 'window.salvarNovaDoacao');
}

export async function salvarNovaDoacao(form) {
    const btn = form.querySelector('button[type="submit"]');
    const originalText = btn.innerHTML;
    btn.innerHTML = '<i data-lucide="loader-2" class="w-4 h-4 animate-spin"></i> Salvando...';
    btn.disabled = true;

    try {
        const payload = {
            id_usuario: parseInt(form.querySelector('[name="id_usuario"]').value),
            descricao: form.querySelector('[name="descricao"]').value,
            status_doacao: "Recebida",
            data_doacao: new Date().toISOString().split('T')[0]
        };

        await api.criarDoacao(payload);
        showToast('Doação salva com sucesso!', 'success');
        form.closest('.fixed').remove();
        if (window.mudarView) window.mudarView('doacoes');
    } catch (error) {
        showToast(error.message || 'Erro ao salvar doação.', 'error');
        btn.innerHTML = originalText;
        btn.disabled = false;
        if (window.lucide) window.lucide.createIcons();
    }
}

export async function deletarDoacao(id) {
    if (!confirm('Tem certeza que deseja excluir esta doação?')) return;
    try {
        await api.deletarDoacao(id);
        showToast('Doação excluída com sucesso!', 'success');
        if (window.mudarView) window.mudarView('doacoes');
    } catch (error) {
        showToast('Erro ao excluir: verifique dependências (itens doados).', 'error');
    }
}

// === BENEFICIÁRIOS ===
export function openNovoBeneficiarioModal() {
    const content = `
        <div class="space-y-4 text-left">
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">ID do Usuário (Pré-cadastrado)</label>
                <input type="number" name="id_usuario" required min="1" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
                <p class="text-xs text-gray-500 mt-1">O usuário deve existir na tabela de usuários.</p>
            </div>
        </div>
    `;
    createModal('Vincular Beneficiário', content, 'window.salvarNovoBeneficiario');
}

export async function salvarNovoBeneficiario(form) {
    const btn = form.querySelector('button[type="submit"]');
    btn.disabled = true;

    try {
        const payload = {
            id_usuario: parseInt(form.querySelector('[name="id_usuario"]').value),
            data_cadastro_beneficiario: new Date().toISOString().split('T')[0]
        };
        
        await api.vincularBeneficiario(payload);
        showToast('Beneficiário vinculado com sucesso!', 'success');
        form.closest('.fixed').remove();
        if(window.mudarView) window.mudarView('beneficiarios');
    } catch (error) {
        showToast('Erro: Verifique se o ID do usuário existe.', 'error');
        btn.disabled = false;
    }
}

export async function deletarBeneficiario(id) {
    if (!confirm('Tem certeza que deseja desvincular este beneficiário?')) return;
    try {
        await api.deletarBeneficiario(id);
        showToast('Beneficiário removido com sucesso!', 'success');
        if (window.mudarView) window.mudarView('beneficiarios');
    } catch (error) {
        showToast('Erro ao remover beneficiário.', 'error');
    }
}

// === ESTOQUE (ITENS E MOVIMENTAÇÃO) ===
export function openNovoItemModal() {
    const content = `
        <div class="space-y-4 text-left">
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Nome do Item</label>
                <input type="text" name="nome" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Descrição</label>
                <input type="text" name="descricao" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
            </div>
            <div class="grid grid-cols-2 gap-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">ID Categoria</label>
                    <input type="number" name="id_categoria" required min="1" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Unidade (ex: un, kg)</label>
                    <input type="text" name="unidade" required placeholder="un" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
                </div>
            </div>
        </div>
    `;
    createModal('Cadastrar Novo Item', content, 'window.salvarNovoItem');
}

export async function salvarNovoItem(form) {
    const btn = form.querySelector('button[type="submit"]');
    btn.disabled = true;

    try {
        const payload = {
            id_categoria_item: parseInt(form.querySelector('[name="id_categoria"]').value),
            nome: form.querySelector('[name="nome"]').value,
            descricao: form.querySelector('[name="descricao"]').value,
            unidade_medida: form.querySelector('[name="unidade"]').value
        };
        
        await api.criarItem(payload);
        showToast('Item cadastrado com sucesso!', 'success');
        form.closest('.fixed').remove();
        if(window.mudarView) window.mudarView('estoque');
    } catch (error) {
        showToast('Erro: A categoria informada existe?', 'error');
        btn.disabled = false;
    }
}

export async function deletarItem(id) {
    if (!confirm('Tem certeza que deseja excluir este item?')) return;
    try {
        await api.deletarItem(id);
        showToast('Item excluído com sucesso!', 'success');
        if (window.mudarView) window.mudarView('estoque');
    } catch (error) {
        showToast('Erro ao excluir: O item já possui movimentações?', 'error');
    }
}

export function abrirMovimentacaoModal(id_item, tipo) {
    const isEntrada = tipo === 'entrada';
    const title = isEntrada ? 'Registrar Entrada (Doação)' : 'Registrar Saída (Distribuição)';
    const idField = isEntrada ? 'id_doacao' : 'id_distribuicao';
    const idLabel = isEntrada ? 'ID da Doação' : 'ID da Distribuição';

    const content = `
        <input type="hidden" name="id_item" value="${id_item}">
        <input type="hidden" name="tipoMov" value="${tipo}">
        <div class="space-y-4 text-left">
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">${idLabel}</label>
                <input type="number" name="${idField}" required min="1" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Quantidade</label>
                <input type="number" name="quantidade" required min="1" value="1" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
            </div>
        </div>
    `;
    createModal(title, content, 'window.salvarMovimentacao');
}

export async function salvarMovimentacao(form) {
    const btn = form.querySelector('button[type="submit"]');
    btn.disabled = true;

    try {
        const id_item = parseInt(form.querySelector('[name="id_item"]').value);
        const tipo = form.querySelector('[name="tipoMov"]').value;
        const quantidade = parseInt(form.querySelector('[name="quantidade"]').value);

        if (tipo === 'entrada') {
            const id_doacao = parseInt(form.querySelector('[name="id_doacao"]').value);
            await api.adicionarItemDoacao({
                id_doacao: id_doacao,
                id_item: id_item,
                quantidade_utilizada: quantidade
            });
        } else {
            const id_distribuicao = parseInt(form.querySelector('[name="id_distribuicao"]').value);
            await api.adicionarItemDistribuicao({
                id_distribuicao: id_distribuicao,
                id_item: id_item,
                quantidade_utilizada: quantidade
            });
        }

        showToast('Movimentação registrada com sucesso!', 'success');
        form.closest('.fixed').remove();
        if(window.mudarView) window.mudarView('estoque');
    } catch (error) {
        showToast('Erro: Verifique se o ID informado (Doação/Distribuição) existe.', 'error');
        btn.disabled = false;
    }
}

// === VAGAS DE VOLUNTARIADO E INSCRITOS ===
export function openNovaVagaModal() {
    const content = `
        <div class="space-y-4 text-left">
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">ID do Responsável (Usuário)</label>
                <input type="number" name="id_usuario" required min="1" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Título da Vaga</label>
                <input type="text" name="titulo" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Descrição</label>
                <input type="text" name="descricao" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
            </div>
            <div class="grid grid-cols-2 gap-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Data Início</label>
                    <input type="date" name="data_inicio" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Data Fim</label>
                    <input type="date" name="data_fim" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
                </div>
            </div>
            <div class="grid grid-cols-2 gap-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Carga Horária</label>
                    <input type="text" name="carga_horaria" placeholder="Ex: 40h" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Qtd de Vagas</label>
                    <input type="number" name="quantidade_vagas" required min="1" value="1" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
                </div>
            </div>
        </div>
    `;
    createModal('Abrir Nova Vaga', content, 'window.salvarNovaVaga');
}

export async function salvarNovaVaga(form) {
    const btn = form.querySelector('button[type="submit"]');
    btn.disabled = true;

    try {
        const payload = {
            id_usuario: parseInt(form.querySelector('[name="id_usuario"]').value),
            titulo: form.querySelector('[name="titulo"]').value,
            descricao: form.querySelector('[name="descricao"]').value,
            data_inicio: form.querySelector('[name="data_inicio"]').value,
            data_fim: form.querySelector('[name="data_fim"]').value,
            carga_horaria: form.querySelector('[name="carga_horaria"]').value,
            quantidade_vagas: parseInt(form.querySelector('[name="quantidade_vagas"]').value)
        };
        
        await api.criarVagaVoluntariado(payload);
        showToast('Nova vaga criada com sucesso!', 'success');
        form.closest('.fixed').remove();
        if(window.mudarView) window.mudarView('voluntarios');
    } catch (error) {
        showToast('Erro ao criar vaga.', 'error');
        btn.disabled = false;
    }
}

export async function deletarVaga(id) {
    if (!confirm('Tem certeza que deseja excluir esta vaga?')) return;
    try {
        await api.deletarVagaVoluntariado(id);
        showToast('Vaga excluída com sucesso!', 'success');
        if (window.mudarView) window.mudarView('voluntarios');
    } catch (error) {
        showToast('Erro ao excluir: a vaga possui inscritos?', 'error');
    }
}

export async function verInscritosModal(id_vaga) {
    try {
        const [inscricoes, usuarios] = await Promise.all([
            api.getInscricoes(),
            api.getUsuarios()
        ]);

        const inscritos = inscricoes.filter(i => i.id_vaga === id_vaga);
        
        const inscritosHtml = inscritos.map(i => {
            const usuario = usuarios.find(u => u.id === i.id_usuario);
            const nome = usuario ? usuario.nome : `ID #${i.id_usuario}`;
            return `
                <div class="flex items-center gap-3 p-3 hover:bg-gray-50 border-b border-gray-100 last:border-0 transition-colors">
                    <div class="w-8 h-8 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center font-bold text-xs uppercase">
                        ${nome.charAt(0)}
                    </div>
                    <div>
                        <p class="text-sm font-bold text-gray-800">${nome}</p>
                        <p class="text-[10px] text-gray-500 uppercase tracking-wider mt-0.5">Status: ${i.status}</p>
                    </div>
                </div>
            `;
        }).join('');

        const content = `
            <div class="text-left">
                <div class="border border-gray-200 rounded-lg overflow-hidden max-h-60 overflow-y-auto">
                    ${inscritos.length > 0 ? inscritosHtml : '<div class="p-8 text-center text-gray-500"><p class="text-sm font-medium">Nenhum inscrito até o momento.</p></div>'}
                </div>
            </div>
        `;
        createViewModal(`Inscritos na Vaga #${id_vaga}`, content);
    } catch (error) {
        showToast('Erro ao carregar os inscritos', 'error');
    }
}

// === PEDIDOS DE AUXÍLIO ===
export function openNovoPedidoModal() { 
    const content = `
        <div class="space-y-4 text-left">
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">ID do Beneficiário (Usuário)</label>
                <input type="number" name="id_usuario" required min="1" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Justificativa / Necessidade</label>
                <textarea name="justificativa" required rows="3" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"></textarea>
            </div>
        </div>
    `;
    createModal('Registrar Pedido de Auxílio', content, 'window.salvarNovoPedido');
}

export async function salvarNovoPedido(form) {
    const btn = form.querySelector('button[type="submit"]');
    btn.disabled = true;

    try {
        const payload = {
            id_usuario: parseInt(form.querySelector('[name="id_usuario"]').value),
            justificativa: form.querySelector('[name="justificativa"]').value,
            data_pedido: new Date().toISOString().split('T')[0],
            status: "Pendente"
        };
        
        await api.criarPedidoAuxilio(payload);
        showToast('Pedido registrado com sucesso!', 'success');
        form.closest('.fixed').remove();
        if(window.mudarView) window.mudarView('pedidos');
    } catch (error) {
        showToast('Erro: Verifique o ID do usuário.', 'error');
        btn.disabled = false;
    }
}

export async function atualizarStatusPedido(id, novoStatus) {
    try {
        const pedido = await api.getPedidoAuxilio(id);
        pedido.status = novoStatus;
        await api.atualizarPedidoAuxilio(id, pedido);
        showToast(`Pedido marcado como ${novoStatus}!`, 'success');
        if(window.mudarView) window.mudarView('pedidos');
    } catch (error) {
        showToast('Erro ao atualizar status do pedido.', 'error');
    }
}

export async function deletarPedido(id) {
    if (!confirm('Tem certeza que deseja excluir este pedido?')) return;
    try {
        await api.deletarPedidoAuxilio(id);
        showToast('Pedido excluído com sucesso!', 'success');
        if (window.mudarView) window.mudarView('pedidos');
    } catch (error) {
        showToast('Erro ao excluir pedido.', 'error');
    }
}

export function distribuirPedido(id_pedido) {
    const content = `
        <input type="hidden" name="id_pedido" value="${id_pedido}">
        <div class="space-y-4 text-left">
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Data da Distribuição</label>
                <input type="date" name="data_dist" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none" value="${new Date().toISOString().split('T')[0]}">
            </div>
            <p class="text-xs text-gray-500">Isto criará o registo de distribuição. Após criar, vá ao Estoque para dar a saída nos itens associando ao ID gerado.</p>
        </div>
    `;
    createModal('Iniciar Distribuição', content, 'window.salvarDistribuicao');
}

export async function salvarDistribuicao(form) {
    const btn = form.querySelector('button[type="submit"]');
    btn.disabled = true;

    try {
        const id_pedido = parseInt(form.querySelector('[name="id_pedido"]').value);
        const data_dist = form.querySelector('[name="data_dist"]').value;

        const payload = {
            id_pedido_auxilio: id_pedido,
            status: "Em separação",
            data_distribuicao: data_dist
        };
        
        await api.registrarDistribuicao(payload);
        
        // Atualiza status do pedido para "Atendido"
        await atualizarStatusPedido(id_pedido, "Atendido");

        showToast('Distribuição iniciada com sucesso!', 'success');
        form.closest('.fixed').remove();
    } catch (error) {
        showToast('Erro ao criar distribuição.', 'error');
        btn.disabled = false;
    }
}

// === USUÁRIOS ===
export function openNovoUsuarioModal() {
    const content = `
        <div class="space-y-4 text-left">
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Nome Completo</label>
                <input type="text" name="nome" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">E-mail</label>
                <input type="email" name="email" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
            </div>
            <div class="grid grid-cols-2 gap-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Login (Username)</label>
                    <input type="text" name="login" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Senha</label>
                    <input type="password" name="senha" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
                </div>
            </div>
        </div>
    `;
    createModal('Cadastrar Novo Usuário', content, 'window.salvarNovoUsuario');
}

export async function salvarNovoUsuario(form) {
    const btn = form.querySelector('button[type="submit"]');
    btn.disabled = true;

    try {
        const payload = {
            nome: form.querySelector('[name="nome"]').value,
            email: form.querySelector('[name="email"]').value,
            login: form.querySelector('[name="login"]').value,
            senha: form.querySelector('[name="senha"]').value
        };
        
        await api.criarUsuario(payload);
        showToast('Usuário cadastrado com sucesso!', 'success');
        form.closest('.fixed').remove();
        if(window.mudarView) window.mudarView('usuarios');
    } catch (error) {
        showToast('Erro ao cadastrar usuário.', 'error');
        btn.disabled = false;
    }
}

export async function deletarUsuario(id) {
    if (!confirm('Tem certeza que deseja excluir este usuário? (O banco impedirá se ele possuir doações/pedidos vinculados)')) return;
    try {
        await api.deletarUsuario(id);
        showToast('Usuário excluído com sucesso!', 'success');
        if (window.mudarView) window.mudarView('usuarios');
    } catch (error) {
        showToast('Erro ao excluir: o usuário possui registros associados (doações/pedidos).', 'error');
    }
}

// Globalizar funções para que possam ser chamadas no onclick (HTML inserido dinamicamente)
window.salvarNovaDoacao = salvarNovaDoacao;
window.deletarDoacao = deletarDoacao;
window.salvarNovoBeneficiario = salvarNovoBeneficiario;
window.deletarBeneficiario = deletarBeneficiario;
window.salvarNovoItem = salvarNovoItem;
window.deletarItem = deletarItem;
window.abrirMovimentacaoModal = abrirMovimentacaoModal;
window.salvarMovimentacao = salvarMovimentacao;
window.salvarNovaVaga = salvarNovaVaga;
window.deletarVaga = deletarVaga;
window.verInscritosModal = verInscritosModal;
window.salvarNovoPedido = salvarNovoPedido;
window.atualizarStatusPedido = atualizarStatusPedido;
window.deletarPedido = deletarPedido;
window.distribuirPedido = distribuirPedido;
window.salvarDistribuicao = salvarDistribuicao;
window.openNovoUsuarioModal = openNovoUsuarioModal;
window.salvarNovoUsuario = salvarNovoUsuario;
window.deletarUsuario = deletarUsuario;
