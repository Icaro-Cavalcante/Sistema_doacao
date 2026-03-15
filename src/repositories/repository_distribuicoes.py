from src.repositories.repository import Repo
from src.domain.distribuicoes import Distribuicao
from src.database.database import Database
from src.database.tables import Tabela
from sqlalchemy import text # Usamos text para escrever queries

db = Database() # Objeto do banco de dados
tb = Tabela() # Objeto da tabela

class RepoDistribuicao(Repo): # Importando da classe pai para polimorfismo
    '''
    Classe que interaje com o Banco de Dados das distribuições
    '''
    def __init__(self, database, table):
        super().__init__(database, table)

    def create(self, distribuicao):
        '''
        Recebe um objeto de distribuição e cadastra ele no banco de dados
        '''
        conexao = self.database.connect() # Estabelecendo a conexão
        if conexao: # Se a conexão existir
            try: # Tratamento de erro
                query = text ("""INSERT INTO distribuicoes (id_pedido_auxilio, data_distribuicao, status)
                            VALUES (:id_pedido_auxilio, :data_distribuicao, :status)
                            ON CONFLICT (id) DO NOTHING""") # Escreve a query
                conexao.execute(query, {"id_pedido_auxilio" : distribuicao.id_pedido_auxilio, "data_distribuicao" : distribuicao.data_distribuicao, "status" : distribuicao.status}) #Executa a query
                conexao.commit() # Salva as alterações no banco de dados
                conexao.close() # Fecha a conexão
            except Exception as erro: # Tratamento de erro
                print(f"Não foi possível realizar o cadastro.")
            return "Distribuição cadastrada"
        else: # A conexão não existiu
            return "Não foi possível conectar"
        
    def read(self, id):
        pass

    def update(self, id):
        pass

    def inactivate(self):
        pass    





