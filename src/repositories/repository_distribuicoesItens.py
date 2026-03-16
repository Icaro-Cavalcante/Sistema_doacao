from src.repositories.repository import Repo
from src.domain.distribuicoesItens import DistribuicaoItem
from src.database.database import Database
from src.database.tables import Tabela
from sqlalchemy import text # Usamos text para escrever queries

db = Database()
tb = Tabela()


class RepoDistribuicaoItem(Repo):
    '''
    Classe que interaje com o Banco de Dados dos itens de distribuição
    '''
    def __init__(self, database, table):
        super().__init__(database, table)

    def create(self, distribuicao_item):
        '''
        Recebe um objeto de item de distribuição e cadastra ele no banco de dados
        '''
        conexao = self.database.connect()
        if conexao:
            try: 
                query = text(""" INSERT INTO distribuicoes_item (id_distribuicao, id_item, quantidade_utilizada) VALUES (:id_distribuicao, :id_item, :quantidade_utilizada) """)
                conexao.execute(query, {
                    "id_distribuicao": distribuicao_item.id_distribuicao, 
                    "id_item": distribuicao_item.id_item, 
                    "quantidade_utilizada": distribuicao_item.quantidade_utilizada
                })
                conexao.commit()
                conexao.close()
                return "Item de distribuição cadastrado"
            except Exception as erro:
                print(f"Erro ao cadastrar item distribuição: {erro}")
                return "Não foi possível realizar o cadastro"
        else:
            return "Não foi possível conectar"


    
    def read(self, id):
        '''
        Recebe o ID de um item de distribuição e retorna um objeto com seus dados
        '''
        conexao = self.database.connect() # Estabelecendo conexão
        if conexao: # Se a conexão existir
            try: # Tratamento de erro
                query = text ("""SELECT * FROM distribuicoes_item WHERE id = :id""") # Query - Pegando os dados do item de distribuição com esse ID
                tupla = conexao.execute(query, {"id" : id}).first() # Executando a query e pegando o resultado
                if not tupla: # Se a tupla não for encontrada
                    print("Dados não encontrados.")
                    raise FileNotFoundError # Tratamento de erro
                else:
                    distribuicao_item_objeto = DistribuicaoItem(tupla[1], tupla[2], tupla[3]) # Transformando a tupla em objeto
            except Exception as erro: # Tratamento de erro
                print(f"Não foi possível realizar a consulta.")
                return None
            return distribuicao_item_objeto
        else: # A conexão não existiu
            return "Não foi possível conectar"

    def update(self, id, nome_atributo, atributo_update):
        '''
        Recebe o ID de um item de distribuição, o nome do atributo e o atributo atualizado e atualiza o atributo
        '''
        conexao = self.database.connect() # Estabelecendo a conexão
        if conexao: # Se a conexão existir
            try:
                query = text (f'''UPDATE distribuicoes_item
                        SET {nome_atributo} = :atributo_update
                        WHERE id = :id''') # query
                conexao.execute (query, 
                                 {
                                "atributo_update": atributo_update,
                                "id": id })
                conexao.commit()
                conexao.close()
                return "Atributo atualizado"
            except Exception as erro: # Tratamento de erro
                print(f"Não foi possível realizar a consulta.")
                return None
        else:
            return "Não foi possível conectar"

    def inactivate(self):
        pass