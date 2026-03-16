from src.database.database import Database
from src.database.tables import Tabela

# Repositórios
from src.repositories.repository_beneficiarios import RepoBeneficiario
from src.repositories.repository_doacoes import RepoDoacao
from src.repositories.repository_doacoesItem import RepoDoacoesItem
from src.repositories.repository_distribuicoes import RepoDistribuicao
from src.repositories.repository_distribuicoesItens import RepoDistribuicaoItem
from src.repositories.repository_inscricoes import RepoInscricoes
from src.repositories.repository_itens import RepoItens
from src.repositories.repository_itensCategoria import RepoItemCategoria
from src.repositories.repository_pedidosAuxilio import RepoPedidoAuxilio
from src.repositories.repository_pessoasFisica import RepoPessoaFisica
from src.repositories.repository_pessoasJuridica import RepoPessoaJuridica
from src.repositories.repository_rastreios import RepoRastreio
from src.repositories.repository_usuarios import RepoUsuario
from src.repositories.repository_vagasVoluntariado import RepoVagaVoluntariado

# Domínios
from src.domain.beneficiarios import Beneficiario
from src.domain.doacoes import Doacao
from src.domain.doacoesItem import DoacaoItem
from src.domain.distribuicoes import Distribuicao
from src.domain.distribuicoesItens import DistribuicaoItem
from src.domain.inscricoes import Inscricao
from src.domain.itens import Item
from src.domain.itensCategoria import ItemCategoria
from src.domain.pedidosAuxilio import PedidoAuxilio
from src.domain.pessoasFisica import PessoaFisica
from src.domain.pessoasJuridica import PessoaJuridica
from src.domain.rastreios import Rastreio
from src.domain.usuarios import Usuario
from src.domain.vagasVoluntariado import VagaVoluntariado

db = Database()
tb = Tabela()
tb.criar_tabelas(db)

repo_beneficiario = RepoBeneficiario(db, tb) #Feito
repo_vagasVoluntarido = RepoVagaVoluntariado(db,tb) #Feito
repo_inscricoes = RepoInscricoes(db,tb) #Feito
repo_doacao = RepoDoacao(db, tb) # Feito
repo_doacoesItem = RepoDoacoesItem(db,tb) #Feito
repo_usuario = RepoUsuario(db, tb) #Feito
repo_itens = RepoItens(db, tb) #Feito
repo_itensCategoria = RepoItemCategoria(db, tb) #Feito
repo_rastreios = RepoRastreio(db,tb) #Feito
repo_distribuicoesItem = RepoDistribuicaoItem(db, tb) #Feito
repo_distribuicoes = RepoDistribuicao(db,tb) #Feito
repo_pessoasFisica = RepoPessoaFisica(db,tb) #Feito
repo_pessoasJuridica = RepoPessoaJuridica(db,tb) #Feito
repo_pedidosAuxilio = RepoPedidoAuxilio(db,tb) #Feito


doacao_teste = Doacao(1, "12/10/2025", "Tudo certo", "Ativo")
usuario_teste2 = Usuario("Fernanda", "fernanda@gmail.com", "fernanda356356", "fernanda0982", "12/04/2025")
usuario_teste = Usuario("Julio", "julio@gmail.com", "senha1234", "julio712", "10/20/2004")
beneficiario_teste = Beneficiario(1, "12/10/2025")
categoria_teste = ItemCategoria("Alimentos", "Comida em geral.")
item_teste = Item(1, "Maçã", "É uma maçã", "gramas")
vaga_voluntario_teste = VagaVoluntariado(1, "Título", "É um voluntário", "10/4/2024", "5/7/2026", 8, 23)
incricao_teste = Inscricao(1, 1, "Completa", "20/5/2024")
doacoets_em_teste = DoacaoItem(1, 1, 500)
rastreios_teste = Rastreio(1, "7/1/2024", "movientação", "Rua do Pedrinho")
distribuicoes_item_teste = DistribuicaoItem(1, 1, 45)
distribuicoes_teste = Distribuicao(1, "7/1/2024", "Concluída")
fisica_teste = PessoaFisica(1, 12345678901, "20/10/2004")
juridica_teste = PessoaJuridica(2, 121454587, "Isenção")
pedido_auxilio_teste = PedidoAuxilio(1, "justificativa", "10/2/2004", "Atendido")

# self, id, nome_atributo, atributo_update)


# nome, email, senha, endereço, status, identificador, tipo_perfil, id=None

def main():
    # 1. Criar usuários primeiro (base para tudo)
    repo_usuario.create(usuario_teste)
    repo_usuario.create(usuario_teste2)
    print("Usuario\n\n\n\n")
    
    # 2. Criar categorias e itens
    repo_itensCategoria.create(categoria_teste)
    repo_itens.create(item_teste)
    print("itens\n\n\n\n")
    
    # 3. Criar extensões de usuários
    repo_beneficiario.create(beneficiario_teste)
    print("pessoas\n\n\n\n")
    repo_pessoasFisica.create(fisica_teste)
    print("pessoas\n\n\n\n")
    repo_pessoasJuridica.create(juridica_teste)
    print("pessoas\n\n\n\n")
    
    # 4. Criar vagas de voluntariado
    repo_vagasVoluntarido.create(vaga_voluntario_teste)
    print("vagas\n\n\n\n")
    
    # 5. Criar inscrições em vagas
    repo_inscricoes.create(incricao_teste)
    print("inscrição\n\n\n\n")
    
    # 6. Criar doações
    repo_doacao.create(doacao_teste)
    print("doações\n\n\n\n")
    
    # 7. Criar itens de doação (dependem de doações)
    repo_doacoesItem.create(doacoets_em_teste)
    print("doações item\n\n\n\n")
    
    # 8. Criar rastreios (dependem de itens de doação)
    repo_rastreios.create(rastreios_teste)
    print("rastreios\n\n\n\n")
    
    # 9. Criar pedidos de auxílio
    repo_pedidosAuxilio.create(pedido_auxilio_teste)
    print("pedido auxilio\n\n\n\n")
    
    # 10. Criar distribuições (dependem de pedidos de auxílio)
    repo_distribuicoes.create(distribuicoes_teste)
    print("distribuições\n\n\n\n")
    
    # 11. Criar itens de distribuição (dependem de distribuições)
    repo_distribuicoesItem.create(distribuicoes_item_teste)
    print("itens distribuição\n\n\n\n")



if __name__ == "__main__":
    main()


    # def get_full_distribution_report(self, id_distribuicao):
    #     """
    #     Consulta complexa com múltiplos JOINs para relatório completo de distribuição
    #     """
    #     conexao = self.database.connect()
    #     if conexao:
    #         query = text("""
    #             SELECT d.id, d.data_distribuicao, u.nome as beneficiario, 
    #                    i.nome as item, di.quantidade_utlizada, pa.justificativa
    #             FROM distribuicoes d
    #             JOIN pedidosAuxilio pa ON d.id_pedido_auxilio = pa.id
    #             JOIN usuarios u ON pa.id_usuario = u.id
    #             JOIN distribuicoesItem di ON d.id = di.id_distribuicao
    #             JOIN itens i ON di.id_item = i.id
    #             WHERE d.id = :id_distribuicao
    #         """)
    #         result = conexao.execute(query, {"id_distribuicao": id_distribuicao}).fetchall()
    #         conexao.close()
    #         return result
    #     return None

# class Beneficiario():
#     '''
#     Classe que representa um beneficiário no sistema.
#     '''
#     def __init__(self, id_usuario, data_cadastro_beneficiario):
#         self.id_usuario = id_usuario
#         self.data_cadastro_beneficiario = data_cadastro_beneficiario
