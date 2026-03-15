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
                query = text(""" INSERT INTO distribuicoesItem (id_distribuicao, id_item, quantidade_utlizada) VALUES (:id_distribuicao, :id_item, :quantidade_utlizada) ON CONFLICT (id_distribuicao, id_item) DO NOTHING """)

                conexao.execute(query, {"id_distribuicao": distribuicao_item.id_distribuicao, "id_item": distribuicao_item.id_item, "quantidade_utlizada": distribuicao_item.quantidade_utilizada})

                conexao.commit()
                conexao.close()
            except Exception as erro:
                print(f"Não foi possível realizar o cadastro.")
            return "Item de distribuição cadastrado"
        else:
            return "Não foi possível conectar"
    
    def read(self, id):
        pass

    def update(self, id):
        pass

    def inactivate(self):
        pass