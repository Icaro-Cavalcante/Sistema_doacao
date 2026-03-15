from src.repositories.repository import Repo
from src.domain.beneficiarios import Beneficiario
from src.database.database import Database
from src.database.tables import Tabela
from sqlalchemy import text # Usamos text para escrever queries

db = Database()
tb = Tabela()

class RepoBeneficiario(Repo):
    '''
    Classe que interaje com o Banco de Dados dos beneficiários
    '''
    def __init__(self, database, table):
        super().__init__(database, table)

    def create(self, beneficiario):
        '''
        Recebe um objeto de beneficiário e cadastra ele no banco de dados
        '''
        conexao = self.database.connect()
        if conexao:
            try: 
                query = text(""" INSERT INTO beneficiarios (id_usuario, data_cadastro_beneficiario) VALUES (:id_usuario, :data_cadastro_beneficiario) ON CONFLICT (id_usuario) DO NOTHING """)

                conexao.execute(query, {"id_usuario": beneficiario.id_usuario, "data_cadastro_beneficiario": beneficiario.data_cadastro_beneficiario})

                conexao.commit()
                conexao.close()
            except Exception as erro:
                print(f"Não foi possível realizar o cadastro.")
            return "Beneficiário cadastrado"
        else:
            return "Não foi possível conectar"
    
    def read(self, id):
        pass

    def update(self, id):
        pass

    def inactivate(self):
        pass
