from src.repositories.repository import Repo
from src.domain.itens import Item
from src.database.database import Database
from src.database.tables import Tabela
from sqlalchemy import text # Usamos text para escrever queries


db = Database()
tb = Tabela()

class RepoItens(Repo):
    '''
    a
    '''

    def __init__(self, database, table):
        super().__init__(database, table)

    def create(self, item):
        '''
        '''
        conexao = self.database.connect()
        if conexao:
            try:
                query = text (""" INSERT INTO itens (id_categoria_item, nome, descricao, unidade_medida)
                              VALUES (:id_categoria_item, :nome, :descricao, :unidade_medida)
                              ON CONFLICT (id) DO NOTHING""")
                conexao.execute(query, {"id_categoria_item" : item.id_categoria_item, "nome" : item.nome, "descricao" : item.descricao, "unidade_medida" : item.unidade_medida})
                conexao.commit()
                conexao.close()
            except Exception as erro: # Tratamento de erro
                print(f"Não foi possível realizar o cadastro.")
                return "O item não foi cadastrado."
            return "Item cadastrado."
        else: 
            return "O item não foi cadastrado."

    def read(self, id):
        pass

    def update(self, id):
        pass

    def inactivate(self):
        pass