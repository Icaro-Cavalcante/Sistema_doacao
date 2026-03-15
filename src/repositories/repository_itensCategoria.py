from src.repositories.repository import Repo
from src.domain.itensCategoria import ItemCategoria
from src.database.database import Database
from src.database.tables import Tabela
from sqlalchemy import text # Usamos text para escrever queries

db = Database()
tb = Tabela()

class RepoItemCategoria(Repo):
    '''
    Classe que interaje com o Banco de Dados das categorias de itens
    '''
    def __init__(self, database, table):
        super().__init__(database, table)

    def create(self, item_categoria):
        '''
        Recebe um objeto de categoria de item e cadastra ele no banco de dados
        '''
        conexao = self.database.connect()
        if conexao:
            try: 
                query = text(""" INSERT INTO itensCategoria (nome_categoria, descricao) VALUES (:nome_categoria, :descricao) ON CONFLICT (id) DO NOTHING """)

                conexao.execute(query, {"nome_categoria": item_categoria.nome_categoria, "descricao": item_categoria.descricao})

                conexao.commit()
                conexao.close()
            except Exception as erro:
                print(f"Não foi possível realizar o cadastro.")
            return "Categoria de item cadastrada"
        else:
            return "Não foi possível conectar"
    
    def read(self, id):
        pass

    def update(self, id):
        pass

    def inactivate(self):
        pass