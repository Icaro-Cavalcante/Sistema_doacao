import { showToast } from '../utils/helpers.js';
import { mockData } from '../data/mockData.js';

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
                        <button type="submit" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium shadow-sm">
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
                <label class="block text-sm font-medium text-gray-700 mb-1">Nome do Doador</label>
                <input type="text" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition-shadow">
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Telefone / Contato</label>
                <input type="text" placeholder="(00) 00000-0000" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition-shadow">
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Categoria da Doação</label>
                <select required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition-shadow bg-white">
                    <option value="">Selecione uma categoria</option>
                    <option value="Alimentos não perecíveis">Alimentos não perecíveis</option>
                    <option value="Roupas e Calçados">Roupas e Calçados</option>
                    <option value="Higiene Pessoal">Higiene Pessoal</option>
                    <option value="Outros">Outros</option>
                </select>
            </div>
        </div>
    `;
    createModal('Registrar Nova Doação', content, 'window.salvarNovaDoacao');
}

export async function salvarNovaDoacao(form) {
    const inputs = form.querySelectorAll('input');
    const selects = form.querySelectorAll('select');
    
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = 'A guardar...';
    submitBtn.disabled = true;

    const payload = {
        id_usuario: 1,
        descricao: inputs[0].value,
        status_doacao: "Recebida",
        data_doacao: new Date().toISOString().split('T')[0]
    };

    try {
        await api.criarDoacao(payload);
        window.showToast('Doação guardada com sucesso!', 'success');
        form.closest('.fixed').remove(); // Fecha o modal
        if (window.carregarConteudoGlobal) window.carregarConteudoGlobal(); // Recarrega a tabela atualizada
    } catch (erro) {
        window.showToast('Falha ao contactar o servidor.', 'error');
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    }
}

// === BENEFICIÁRIOS ===
export function openNovoBeneficiarioModal() {
    const content = `
        <div class="space-y-4 text-left">
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Nome Completo / Instituição</label>
                <input type="text" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
            </div>
            <div class="grid grid-cols-2 gap-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Tipo</label>
                    <select required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none bg-white">
                        <option value="Física">Pessoa Física</option>
                        <option value="Jurídica">Pessoa Jurídica</option>
                    </select>
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Documento</label>
                    <input type="text" required placeholder="NIF/BI/CPF" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
                </div>
            </div>
            <div class="grid grid-cols-2 gap-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Contacto</label>
                    <input type="text" required placeholder="(00) 00000-0000" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Dependentes</label>
                    <input type="number" required min="0" value="0" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
                </div>
            </div>
        </div>
    `;
    createModal('Cadastrar Novo Beneficiário', content, 'window.salvarNovoBeneficiario');
}

export function salvarNovoBeneficiario(form) {
    const inputs = form.querySelectorAll('input');
    const select = form.querySelector('select');
    
    const novoBeneficiario = {
        id: "BEN-" + Math.floor(Math.random() * 1000).toString().padStart(3, '0'),
        nome: inputs[0].value,
        tipo: select.value,
        documento: inputs[1].value,
        contato: inputs[2].value,
        dependentes: parseInt(inputs[3].value),
        dataCadastro: new Date().toISOString().split('T')[0],
        status: "Ativa"
    };
    
    mockData.beneficiarios.unshift(novoBeneficiario);
    showToast('Beneficiário cadastrado com sucesso!', 'success');
    form.closest('.fixed').remove();
    if(window.carregarConteudoGlobal) window.carregarConteudoGlobal();
}

// === ESTOQUE (ITENS E MOVIMENTAÇÃO) ===
export function openNovoItemModal() {
    const content = `
        <div class="space-y-4 text-left">
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Nome do Item</label>
                <input type="text" required placeholder="Ex: Arroz Agulhinha 5kg" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Categoria</label>
                <select required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none bg-white">
                    <option value="Alimentos">Alimentos</option>
                    <option value="Roupas e Calçados">Roupas e Calçados</option>
                    <option value="Higiene Pessoal">Higiene Pessoal</option>
                    <option value="Outros">Outros</option>
                </select>
            </div>
            <div class="grid grid-cols-2 gap-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Quantidade Inicial</label>
                    <input type="number" required min="0" value="0" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Unidade (ex: un, kg)</label>
                    <input type="text" required placeholder="un" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
                </div>
            </div>
        </div>
    `;
    createModal('Adicionar Novo Item ao Estoque', content, 'window.salvarNovoItem');
}

export function salvarNovoItem(form) {
    const inputs = form.querySelectorAll('input');
    const select = form.querySelector('select');
    const qtd = parseInt(inputs[1].value);
    
    const novoItem = {
        id: "ITEM-" + Math.floor(Math.random() * 1000).toString().padStart(3, '0'),
        nome: inputs[0].value,
        categoria: select.value,
        quantidade: qtd,
        unidade: inputs[2].value,
        status: qtd > 10 ? "Em Estoque" : (qtd > 0 ? "Baixo Estoque" : "Esgotado")
    };
    
    mockData.estoque.unshift(novoItem);
    showToast('Item adicionado ao estoque!', 'success');
    form.closest('.fixed').remove();
    if(window.carregarConteudoGlobal) window.carregarConteudoGlobal();
}

// NOVA FUNÇÃO: Entrada e Saída de Estoque
export function abrirMovimentacaoModal(id, tipo) {
    const item = mockData.estoque.find(i => i.id === id);
    if(!item) return;

    const isEntrada = tipo === 'entrada';
    const title = isEntrada ? 'Registrar Entrada de Estoque' : 'Registrar Saída de Estoque';
    const maxAttr = isEntrada ? '' : `max="${item.quantidade}"`;

    const content = `
        <input type="hidden" name="itemId" value="${id}">
        <input type="hidden" name="tipoMov" value="${tipo}">
        <div class="space-y-4 text-left">
            <div class="p-3 bg-gray-50 rounded-lg border border-gray-100 mb-4">
                <p class="text-sm text-gray-500">Item selecionado:</p>
                <p class="font-bold text-gray-800">${item.nome}</p>
                <p class="text-xs text-gray-500 mt-1">Estoque atual: ${item.quantidade} ${item.unidade}</p>
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Quantidade da ${isEntrada ? 'Entrada' : 'Saída'}</label>
                <input type="number" required min="1" ${maxAttr} value="1" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
            </div>
        </div>
    `;
    createModal(title, content, 'window.salvarMovimentacao');
}

export function salvarMovimentacao(form) {
    const id = form.querySelector('input[name="itemId"]').value;
    const tipo = form.querySelector('input[name="tipoMov"]').value;
    const qtd = parseInt(form.querySelector('input[type="number"]').value);

    const item = mockData.estoque.find(i => i.id === id);
    if(item) {
        if(tipo === 'entrada') {
            item.quantidade += qtd;
        } else {
            item.quantidade -= qtd;
        }

        // Atualiza os Status visualmente
        if(item.quantidade > 10) item.status = "Em Estoque";
        else if(item.quantidade > 0) item.status = "Baixo Estoque";
        else item.status = "Esgotado";

        showToast(`${tipo === 'entrada' ? 'Entrada' : 'Saída'} registrada com sucesso!`, 'success');
        form.closest('.fixed').remove();
        if(window.carregarConteudoGlobal) window.carregarConteudoGlobal();
    }
}

// === VAGAS DE VOLUNTARIADO E INSCRITOS ===
export function openNovaVagaModal() {
    const content = `
        <div class="space-y-4 text-left">
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Título da Vaga</label>
                <input type="text" required placeholder="Ex: Triagem de Roupas" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Descrição das Atividades</label>
                <input type="text" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
            </div>
            <div class="grid grid-cols-2 gap-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Horário / Turno</label>
                    <input type="text" required placeholder="Ex: Sábados 9h-12h" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Nº de Vagas</label>
                    <input type="number" required min="1" value="1" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
                </div>
            </div>
        </div>
    `;
    createModal('Abrir Nova Vaga de Voluntariado', content, 'window.salvarNovaVaga');
}

export function salvarNovaVaga(form) {
    const inputs = form.querySelectorAll('input');
    
    const novaVaga = {
        id: Math.floor(Math.random() * 1000),
        titulo: inputs[0].value,
        descricao: inputs[1].value,
        horario: inputs[2].value,
        vagas: parseInt(inputs[3].value),
        inscritos: 0,
        status: "Ativa"
    };
    
    mockData.vagas.unshift(novaVaga);
    showToast('Nova vaga criada com sucesso!', 'success');
    form.closest('.fixed').remove();
    if(window.carregarConteudoGlobal) window.carregarConteudoGlobal();
}

// NOVA FUNÇÃO: Ver Lista de Inscritos
export function verInscritosModal(id) {
    const vaga = mockData.vagas.find(v => v.id === id);
    if(!vaga) return;

    const nomesFake = ["Ana Clara", "João Pedro", "Maria Silva", "Carlos Eduardo", "Beatriz Costa", "Lucas Mendes"];
    
    const inscritosHtml = Array.from({length: vaga.inscritos}).map((_, i) => `
        <div class="flex items-center gap-3 p-3 hover:bg-gray-50 border-b border-gray-100 last:border-0 transition-colors cursor-default">
            <div class="w-8 h-8 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center font-bold text-xs uppercase">
                ${nomesFake[i % nomesFake.length].charAt(0)}
            </div>
            <div>
                <p class="text-sm font-bold text-gray-800">${nomesFake[i % nomesFake.length]}</p>
                <p class="text-[10px] text-gray-500 uppercase tracking-wider mt-0.5">Voluntário Registado</p>
            </div>
        </div>
    `).join('');

    const content = `
        <div class="text-left">
            <p class="text-sm text-gray-500 mb-4">Vaga: <span class="font-bold text-gray-800">${vaga.titulo}</span></p>
            <div class="border border-gray-200 rounded-lg overflow-hidden max-h-60 overflow-y-auto">
                ${vaga.inscritos > 0 ? inscritosHtml : '<div class="p-8 text-center text-gray-500"><i data-lucide="users" class="w-8 h-8 mx-auto mb-2 text-gray-400"></i><p class="text-sm font-medium">Nenhum inscrito até o momento.</p></div>'}
            </div>
        </div>
    `;
    createViewModal(`Inscritos (${vaga.inscritos}/${vaga.vagas})`, content);
}

// === PEDIDOS DE AUXÍLIO ===
export function openNovoPedidoModal() { 
    const content = `
        <div class="space-y-4 text-left">
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Beneficiário / Família</label>
                <input type="text" required placeholder="Ex: Família Souza" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
            </div>
            <div class="grid grid-cols-2 gap-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Necessidade</label>
                    <select required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none bg-white">
                        <option value="Cesta Básica">Cesta Básica</option>
                        <option value="Roupas">Roupas</option>
                        <option value="Kit Higiene">Kit Higiene</option>
                        <option value="Outros">Outros</option>
                    </select>
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Prioridade</label>
                    <select required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none bg-white">
                        <option value="Alta">Alta (Urgente)</option>
                        <option value="Média">Média</option>
                        <option value="Baixa">Baixa</option>
                    </select>
                </div>
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Telefone / Contato</label>
                <input type="text" required placeholder="(00) 00000-0000" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Itens Específicos (Separados por vírgula)</label>
                <input type="text" required placeholder="Ex: Arroz, Feijão, Fralda G" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
            </div>
        </div>
    `;
    createModal('Registrar Novo Pedido de Auxílio', content, 'window.salvarNovoPedido');
}

export function salvarNovoPedido(form) {
    const inputs = form.querySelectorAll('input');
    const selects = form.querySelectorAll('select');
    
    const itensTexto = inputs[2].value;
    const itensArray = itensTexto.split(',').map(item => item.trim()).filter(item => item !== "");

    const novoPedido = {
        id: "PED-" + Math.floor(Math.random() * 1000).toString().padStart(3, '0'),
        beneficiario: inputs[0].value,
        tipo: selects[0].value,
        prioridade: selects[1].value,
        dataSolicitacao: new Date().toISOString().split('T')[0],
        itensNecessarios: itensArray.length > 0 ? itensArray : ["Cesta Padrão"],
        status: "Pendente",
        contato: inputs[1].value,
        endereco: "Endereço cadastrado"
    };
    
    mockData.pedidos.unshift(novoPedido);
    showToast('Novo pedido registrado com sucesso!', 'success');
    form.closest('.fixed').remove();
    if(window.carregarConteudoGlobal) window.carregarConteudoGlobal();
}

export function aprovarPedido(id) {
    const pedido = mockData.pedidos.find(p => p.id === id);
    if(pedido) {
        pedido.status = "Aprovado";
        showToast('Pedido aprovado com sucesso!', 'success');
        if(window.carregarConteudoGlobal) window.carregarConteudoGlobal();
    }
}

export function distribuirPedido(id) {
    const pedido = mockData.pedidos.find(p => p.id === id);
    if(pedido) {
        pedido.status = "Entregue";
        showToast('Pedido marcado como entregue!', 'success');
        if(window.carregarConteudoGlobal) window.carregarConteudoGlobal();
    }
}

export function openDistribuirModal() { }