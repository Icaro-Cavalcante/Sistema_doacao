from src.repositories.repository import Repo
from src.domain.pessoasFisica import PessoaFisica
from src.database.database import Database
from src.database.tables import Tabela
from sqlalchemy import text # Usamos text para escrever queries

db = Database()
tb = Tabela()

class RepoPessoaFisica(Repo):
    '''
    Classe que interaje com o Banco de Dados das pessoas física
    '''
    def __init__(self, database, table):
        super().__init__(database, table)

    def create(self, pessoa_fisica):
        '''
        Recebe um objeto de pessoa física e cadastra ele no banco de dados
        '''
        conexao = self.database.connect()
        if conexao:
            try: 
                query = text(""" INSERT INTO pessoaFisica (id_usuario, user_cpf, data_nascimento) VALUES (:id_usuario, :user_cpf, :data_nascimento) ON CONFLICT (id_usuario) DO NOTHING """)

                conexao.execute(query, {"id_usuario": pessoa_fisica.id_usuario, "user_cpf": pessoa_fisica.user_cpf, "data_nascimento": pessoa_fisica.data_nascimento})

                conexao.commit()
                conexao.close()
            except Exception as erro:
                print(f"Não foi possível realizar o cadastro.")
            return "Pessoa física cadastrada"
        else:
            return "Não foi possível conectar"
    
    def read(self, id):
        pass

    def update(self, id):
        pass

    def inactivate(self):
        pass