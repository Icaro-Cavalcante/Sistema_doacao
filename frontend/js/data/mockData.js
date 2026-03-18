export const mockData = {
    doacoes: [
        {
            id: "DOA-001", doador: "Ana Silva", email: "ana.silva@email.com", telefone: "(11) 98765-4321",
            categoria: "Alimentos não perecíveis", status: "Recebido", data: "2024-01-15", itens: 12,
            rastreio: {
                codigo: "RAS123456789BR", status: "Em trânsito", ultimaAtualizacao: "2024-01-15 14:30",
                historico: [
                    { data: "2024-01-15 14:30", status: "Em trânsito", local: "Centro de Distribuição" },
                    { data: "2024-01-15 10:15", status: "Coletado", local: "Doador" }
                ]
            }
        },
        {
            id: "DOA-002", doador: "João Santos", email: "joao.santos@email.com", telefone: "(11) 91234-5678",
            categoria: "Roupas e Calçados", status: "Triagem", data: "2024-01-14", itens: 25,
            rastreio: {
                codigo: "RAS987654321BR", status: "Em triagem", ultimaAtualizacao: "2024-01-15 09:15",
                historico: [
                    { data: "2024-01-15 09:15", status: "Em triagem", local: "Centro de Distribuição" },
                    { data: "2024-01-14 16:30", status: "Recebido", local: "ONG" }
                ]
            }
        }
    ],
    pedidos: [
        {
            id: "PED-001", beneficiario: "Família Souza", tipo: "Cesta Básica", prioridade: "Alta",
            dataSolicitacao: "2024-01-14", itensNecessarios: ["Arroz 5kg", "Feijão 3kg", "Óleo 2L", "Leite 6L"],
            status: "Pendente", contato: "(11) 98888-7777", endereco: "Rua das Flores, 123"
        }
    ],
    beneficiarios: [
        {
            id: "BEN-001", nome: "Maria Silva", tipo: "Física", documento: "123.456.789-00", 
            contato: "(11) 98888-7777", dataCadastro: "2023-11-10", status: "Ativa", dependentes: 4
        },
        {
            id: "BEN-002", nome: "Associação Bairro Unido", tipo: "Jurídica", documento: "12.345.678/0001-99", 
            contato: "(11) 97777-6666", dataCadastro: "2023-05-22", status: "Ativa", dependentes: 50
        },
        {
            id: "BEN-003", nome: "Carlos Oliveira", tipo: "Física", documento: "987.654.321-11", 
            contato: "(11) 96666-5555", dataCadastro: "2024-01-05", status: "Pendente", dependentes: 2
        }
    ],
    estoque: [
        { id: "ITEM-001", nome: "Arroz Agulhinha 5kg", categoria: "Alimentos", quantidade: 150, unidade: "un", status: "Em Estoque" },
        { id: "ITEM-002", nome: "Feijão Carioca 1kg", categoria: "Alimentos", quantidade: 15, unidade: "un", status: "Baixo Estoque" },
        { id: "ITEM-003", nome: "Agasalho Adulto", categoria: "Roupas e Calçados", quantidade: 45, unidade: "peças", status: "Em Estoque" },
        { id: "ITEM-004", nome: "Sabonete Líquido", categoria: "Higiene Pessoal", quantidade: 0, unidade: "un", status: "Esgotado" },
        { id: "ITEM-005", nome: "Leite em Pó 400g", categoria: "Alimentos", quantidade: 8, unidade: "latas", status: "Baixo Estoque" }
    ],
    vagas: [
        {
            id: 1, titulo: "Distribuição de Alimentos", vagas: 5, inscritos: 3, status: "Ativa",
            descricao: "Ajudar na organização e distribuição de cestas", horario: "Sábados 9h-12h"
        }
    ],
    estatisticas: {
        doacoes: { total: 156, ultimos30dias: 45, variacao: "+12%" },
        itens: { aguardando: 48, emTriagem: 23, distribuidos: 85 },
        voluntarios: { ativos: 23, novos: 5, total: 89 },
        beneficiarios: { atendidos: 189, cadastrados: 245, pendentes: 12 }
    },
    notificacoes: [
        { id: 1, message: "Nova doação recebida", time: "5 min atrás", read: false },
        { id: 2, message: "Pedido de auxílio pendente", time: "1 hora atrás", read: false }
    ]
};