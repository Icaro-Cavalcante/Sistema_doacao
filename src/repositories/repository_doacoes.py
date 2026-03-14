from src.domain.doacoes import Doacao
from src.repositories.repository import Repo
from src.database.database import Database
from src.database.tables import Tabela
from sqlalchemy import text

db = Database()
tb = Tabela()

class RepoDoacao(Repo):
    '''
    Classe que interaje com o Banco de Dados das doações
    '''
    def __init__(self, database, table):
        super().__init__(database, table)

    def create(self, doacao):
        '''
        Recebe um objeto de doação e cadastra ele no banco de dados
        '''
        conexao = self.database.connect()
        if conexao:
            try:
                query = text ("""INSERT INTO doacoes (id_usuario, data_doacao, motivo_recusa, status_atual)
                            VALUES (:id_usuario, :data_doacao, :motivo_recusa, :status_atual)
                            ON CONFLICT (id) DO NOTHING""")
                
                conexao.execute(query, {"id_usuario" : doacao.id_usuario, "data_doacao" : doacao.data_doacao, "motivo_recusa" : doacao.motivo_recusa, "status_atual" : doacao.status_atual})

                conexao.commit()
                conexao.close()
            except Exception as erro:
                print(f"Não foi possível realizar o cadastro.")
            return "Doação cadastrada"
        else:
            return "Não foi possível conectar"

    def read(self, doacao_id):
        pass

    def update(self, doacao_id):
        pass

    def inactivate(self):
        pass