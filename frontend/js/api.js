// frontend/js/api.js
const API_URL = 'http://localhost:8000';

// Helper genérico para fazer as requisições
async function request(endpoint, method = 'GET', data = null) {
    const headers = { 'Content-Type': 'application/json' };
    
    // Pega o token se houver (para garantir que funciona logado)
    const token = localStorage.getItem('access_token');
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const config = { method, headers };
    
    if (data) {
        config.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(`${API_URL}${endpoint}`, config);
        
        if (!response.ok) {
            const errInfo = await response.json().catch(() => ({}));
            throw new Error(errInfo.detail || `Falha na requisição: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error(`Erro na API (${method} ${endpoint}):`, error);
        if (window.showToast) window.showToast(error.message || 'Erro ao ligar ao servidor', 'error');
        throw error;
    }
}

export const api = {
    // 0. Autenticação
    login: (dados) => request('/login/', 'POST', dados),

    // 1. Atores - Usuários
    getUsuarios: () => request('/usuarios/'),
    getUsuario: (id) => request(`/usuarios/${id}`),
    criarUsuario: (dados) => request('/usuarios/', 'POST', dados),
    atualizarUsuario: (id, dados) => request(`/usuarios/${id}`, 'PUT', dados),
    deletarUsuario: (id) => request(`/usuarios/${id}`, 'DELETE'),

    // 1. Atores - Perfis (Pessoa Física)
    getPessoasFisicas: () => request('/pessoas-fisica/'),
    getPessoaFisica: (id) => request(`/pessoas-fisica/${id}`),
    vincularPF: (dados) => request('/pessoas-fisica/', 'POST', dados),
    atualizarPF: (id, dados) => request(`/pessoas-fisica/${id}`, 'PUT', dados),
    deletarPF: (id) => request(`/pessoas-fisica/${id}`, 'DELETE'),

    // 1. Atores - Perfis (Pessoa Jurídica)
    getPessoasJuridicas: () => request('/pessoas-juridica/'),
    getPessoaJuridica: (id) => request(`/pessoas-juridica/${id}`),
    vincularPJ: (dados) => request('/pessoas-juridica/', 'POST', dados),
    atualizarPJ: (id, dados) => request(`/pessoas-juridica/${id}`, 'PUT', dados),
    deletarPJ: (id) => request(`/pessoas-juridica/${id}`, 'DELETE'),

    // 1. Atores - Perfis (Beneficiários)
    getBeneficiarios: () => request('/beneficiarios/'),
    getBeneficiario: (id) => request(`/beneficiarios/${id}`),
    vincularBeneficiario: (dados) => request('/beneficiarios/', 'POST', dados),
    atualizarBeneficiario: (id, dados) => request(`/beneficiarios/${id}`, 'PUT', dados),
    deletarBeneficiario: (id) => request(`/beneficiarios/${id}`, 'DELETE'),

    // 2. Inventário - Categorias
    getCategorias: () => request('/categorias/'),
    getCategoria: (id) => request(`/categorias/${id}`),
    criarCategoria: (dados) => request('/categorias/', 'POST', dados),
    atualizarCategoria: (id, dados) => request(`/categorias/${id}`, 'PUT', dados),
    deletarCategoria: (id) => request(`/categorias/${id}`, 'DELETE'),

    // 2. Inventário - Itens
    getItens: () => request('/itens/'),
    getItem: (id) => request(`/itens/${id}`),
    criarItem: (dados) => request('/itens/', 'POST', dados),
    atualizarItem: (id, dados) => request(`/itens/${id}`, 'PUT', dados),
    deletarItem: (id) => request(`/itens/${id}`, 'DELETE'),

    // 3. Doações
    getDoacoes: () => request('/doacoes/'),
    getDoacao: (id) => request(`/doacoes/${id}`),
    criarDoacao: (dados) => request('/doacoes/', 'POST', dados),
    atualizarDoacao: (id, dados) => request(`/doacoes/${id}`, 'PUT', dados),
    deletarDoacao: (id) => request(`/doacoes/${id}`, 'DELETE'),

    // 3. Doações - Itens
    getDoacoesItens: () => request('/doacoes-item/'),
    getDoacaoItem: (id) => request(`/doacoes-item/${id}`),
    adicionarItemDoacao: (dados) => request('/doacoes-item/', 'POST', dados),
    atualizarDoacaoItem: (id, dados) => request(`/doacoes-item/${id}`, 'PUT', dados),
    deletarDoacaoItem: (id) => request(`/doacoes-item/${id}`, 'DELETE'),
    getItensPorDoacao: (idDoacao) => request(`/doacoes/${idDoacao}/itens`),
    getRelatorioCategoriasDoacao: () => request('/doacoes/relatorio'),

    // 3. Doações - Rastreio
    getRastreios: () => request('/rastreios/'),
    getRastreio: (id) => request(`/rastreios/${id}`),
    registrarRastreio: (dados) => request('/rastreios/', 'POST', dados),
    atualizarRastreio: (id, dados) => request(`/rastreios/${id}`, 'PUT', dados),
    deletarRastreio: (id) => request(`/rastreios/${id}`, 'DELETE'),

    // 4. Saída e Distribuição - Pedidos
    getPedidosAuxilio: () => request('/pedidos-auxilio/'),
    getPedidoAuxilio: (id) => request(`/pedidos-auxilio/${id}`),
    criarPedidoAuxilio: (dados) => request('/pedidos-auxilio/', 'POST', dados),
    atualizarPedidoAuxilio: (id, dados) => request(`/pedidos-auxilio/${id}`, 'PUT', dados),
    deletarPedidoAuxilio: (id) => request(`/pedidos-auxilio/${id}`, 'DELETE'),

    // 4. Saída e Distribuição - Distribuições
    getDistribuicoes: () => request('/distribuicoes/'),
    getDistribuicao: (id) => request(`/distribuicoes/${id}`),
    registrarDistribuicao: (dados) => request('/distribuicoes/', 'POST', dados),
    atualizarDistribuicao: (id, dados) => request(`/distribuicoes/${id}`, 'PUT', dados),
    deletarDistribuicao: (id) => request(`/distribuicoes/${id}`, 'DELETE'),
    getDistribuicoesDetalhadas: () => request('/distribuicoes-detalhadas/'),
    getRelatorioDistribuicao: (id) => request(`/distribuicoes/relatorio/${id}`),

    // 4. Saída e Distribuição - Itens da Distribuição
    getDistribuicoesItens: () => request('/distribuicoes-item/'),
    getDistribuicaoItem: (id) => request(`/distribuicoes-item/${id}`),
    adicionarItemDistribuicao: (dados) => request('/distribuicoes-item/', 'POST', dados),
    atualizarDistribuicaoItem: (id, dados) => request(`/distribuicoes-item/${id}`, 'PUT', dados),
    deletarDistribuicaoItem: (id) => request(`/distribuicoes-item/${id}`, 'DELETE'),

    // 5. Voluntariado - Vagas
    getVagasVoluntariado: () => request('/vagas-voluntario/'),
    getVagaVoluntariado: (id) => request(`/vagas-voluntario/${id}`),
    criarVagaVoluntariado: (dados) => request('/vagas-voluntario/', 'POST', dados),
    atualizarVagaVoluntariado: (id, dados) => request(`/vagas-voluntario/${id}`, 'PUT', dados),
    deletarVagaVoluntariado: (id) => request(`/vagas-voluntario/${id}`, 'DELETE'),

    // 5. Voluntariado - Inscrições
    getInscricoes: () => request('/inscricoes/'),
    getInscricao: (id) => request(`/inscricoes/${id}`),
    inscreverVoluntario: (dados) => request('/inscricoes/', 'POST', dados),
    atualizarInscricao: (id, dados) => request(`/inscricoes/${id}`, 'PUT', dados),
    deletarInscricao: (id) => request(`/inscricoes/${id}`, 'DELETE')
};