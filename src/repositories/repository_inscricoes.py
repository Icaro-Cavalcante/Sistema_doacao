from src.repositories.repository import Repo
from src.domain.inscricoes import Inscricao
from src.database.database import Database
from src.database.tables import Tabela
from sqlalchemy import text # Usamos text para escrever queries

db = Database() # Objeto do banco de dados
tb = Tabela() # Objeto da tabela

class RepoInscricoes(Repo): # Importando da classe pai para polimorfismo
    '''
    Classe que interaje com o Banco de Dados das inscrições
    '''
    def __init__(self, database, table):
        super().__init__(database, table)

    def create(self, inscricao):
        '''
        Recebe um objeto de inscrição e cadastra ele no banco de dados
        '''
        conexao = self.database.connect() # Estabelecendo a conexão
        conexao = self.database.connect() # Estabelecendo a conexão
        if conexao: # Se a conexão existir
            try: # Tratamento de erro
                query = text ("""INSERT INTO inscricoes (id_vaga, id_usuario, data_inscricao, status, checkin_presenca)
                            VALUES (:id_vaga, :id_usuario, :data_inscricao, :status, :checkin_presenca)
                            ON CONFLICT (id) DO NOTHING""") # Escreve a query
                conexao.execute(query, {"id_vaga" : inscricao.id_vaga, "id_usuario" : inscricao.id_usuario, "data_inscricao" : inscricao.data_inscricao, "status" : inscricao.status, "checkin_presenca" : inscricao.checkin_presenca}) #Executa a query
                conexao.commit() # Salva as alterações no banco de dados
                conexao.close() # Fecha a conexão
            except Exception as erro: # Tratamento de erro
                print(f"Não foi possível realizar o cadastro.")
            return "Inscrição cadastrada"
        else: # A conexão não existiu
            return "Não foi possível conectar"

        
    def read(self, id):
        pass

    def update(self, id):
        pass

    def inactivate(self):
        pass