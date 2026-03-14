from src.repositories.repository import Repo
from src.domain.doacoesItem import DoacaoItem
from src.database.database import Database
from src.database.tables import Tabela
from sqlalchemy import text # Usamos text para escrever queries

db = Database() # Objeto do banco de dados
tb = Tabela() # Objeto da tabela

class RepoDoacoesItem(Repo): # Importando da classe pai para polimorfismo
    '''
    Classe que interaje com o Banco de Dados dos itens doação
    '''
    def __init__(self, database, table):
        super().__init__(database, table)

    def create(self, doacao_item):
        '''
        Recebe um objeto de doação item e cadastra ele no banco de dados
        '''
        conexao = self.database.connect() # Estabelecendo a conexão
        if conexao: # Se a conexão existir
            try: # Tratamento de erro
                query = text ("""INSERT INTO doacoesItem (id_item, quantidade_utilizada)
                            VALUES (:id_item, :quantidade_utilizada)
                            ON CONFLICT (id) DO NOTHING""") # Escreve a query
                conexao.execute(query, {"id_item" : doacao_item.id_item, "quantidade_utilizada" : doacao_item.quantidade_utilizada}) #Executa a query
                conexao.commit() # Salva as alterações no banco de dados
                conexao.close() # Fecha a conexão
            except Exception as erro: # Tratamento de erro
                print(f"Não foi possível realizar o cadastro.")
            return "Item doação cadastrado"
        else: # A conexão não existiu
            return "Não foi possível conectar"
        
    def read(self, id):
        pass

    def update(self, id):
        pass

    def inactivate(self):
        pass