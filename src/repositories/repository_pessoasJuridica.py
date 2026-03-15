from src.repositories.repository import Repo
from src.domain.pessoasJuridica import PessoaJuridica
from src.database.database import Database
from src.database.tables import Tabela
from sqlalchemy import text # Usamos text para escrever queries

db = Database()
tb = Tabela()

class RepoPessoaJuridica(Repo):
    '''
    Classe que interaje com o Banco de Dados das pessoas jurídica
    '''
    def __init__(self, database, table):
        super().__init__(database, table)

    def create(self, pessoa_juridica):
        '''
        Recebe um objeto de pessoa jurídica e cadastra ele no banco de dados
        '''
        conexao = self.database.connect()
        if conexao:
            try: 
                query = text(""" INSERT INTO pessoasJuridica (id_usuario, user_cnpj, razao_social) VALUES (:id_usuario, :user_cnpj, :razao_social) ON CONFLICT (id_usuario) DO NOTHING """)

                conexao.execute(query, {"id_usuario": pessoa_juridica.id_usuario, "user_cnpj": pessoa_juridica.user_cnpj, "razao_social": pessoa_juridica.razao_social})

                conexao.commit()
                conexao.close()
            except Exception as erro:
                print(f"Não foi possível realizar o cadastro.")
            return "Pessoa jurídica cadastrada"
        else:
            return "Não foi possível conectar"
    
    def read(self, id):
        pass

    def update(self, id):
        pass

    def inactivate(self):
        pass