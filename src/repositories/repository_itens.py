from src.repositories.repository import Repo
from src.domain.itens import Item
from src.database.database import Database
from src.database.tables import Tabela
from sqlalchemy import text # Usamos text para escrever queries


db = Database()
tb = Tabela()

class RepoItens(Repo):
    '''
    Classe que interaje com o Banco de Dados das categorias de itens
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
        '''
        Recebe o ID de um item e retorna um objeto com seus dados
        '''
        conexao = self.database.connect() # Estabelecendo conexão
        if conexao: # Se a conexão existir
            try: # Tratamento de erro
                query = text ("""SELECT * FROM itens WHERE id = :id""") # Query - Pegando os dados do item com esse ID
                tupla = conexao.execute(query, {"id" : id}).first() # Executando a query e pegando o resultado
                if not tupla: # Se a tupla não for encontrada
                    print("Dados não encontrados.")
                    raise FileNotFoundError # Tratamento de erro
                else:
                    item_objeto = Item(tupla[1], tupla[2], tupla[3], tupla[4], tupla[0]) # Transformando a tupla em objeto
            except Exception as erro: # Tratamento de erro
                print(f"Não foi possível realizar a consulta.")
                return None
            return item_objeto
        else: # A conexão não existiu
            return "Não foi possível conectar"

    def update(self, id, nome_atributo, atributo_update):
        '''
        Recebe o ID de um item, o nome do atributo e o atributo atualizado e atualiza o atributo
        '''
        conexao = self.database.connect() # Estabelecendo a conexão
        if conexao: # Se a conexão existir
            try:
                query = text (f'''UPDATE itens
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