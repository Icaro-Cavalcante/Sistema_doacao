from src.domain.usuarios import Usuario
from src.repositories.repository import Repo
from src.database.database import Database
from src.database.tables import Tabela
from sqlalchemy import text # Usamos text para escrever queries

db = Database() # Objeto do banco de dados
tb = Tabela() # Objeto da tabela

class RepoUsuario(Repo): # Importando da classe pai para polimorfismo
    '''
    Classe que interaje com o Banco de Dados dos usuários
    '''
    def __init__(self, database, table):
        super().__init__(database, table)

    def create(self, usuario):
        '''
        Recebe um objeto de usuário e cadastra ele no banco de dados
        '''
        conexao = self.database.connect() # Estabelecendo a conexão
        if conexao: # Se a conexão existir
            try: # Tratamento de erro
                query = text ("""INSERT INTO usuarios (nome, email, senha, login, data_cadastro)
                            VALUES (:nome, :email, :senha, :login, :data_cadastro)
                            ON CONFLICT (id) DO NOTHING""") # Escreve a query
                conexao.execute(query, {"nome" : usuario.nome, "email" : usuario.email, "senha" : usuario.senha, "login" : usuario.login, "data_cadastro" : usuario.data_cadastro}) #Executa a query
                conexao.commit() # Salva as alterações no banco de dados
                conexao.close() # Fecha a conexão
            except Exception as erro: # Tratamento de erro
                print(f"Não foi possível realizar o cadastro.")
            return "Usuário cadastrado"
        else: # A conexão não existiu
            return "Não foi possível conectar"
        
    def read(self, id):
        pass

    def update(self, id):
        pass

    def inactivate(self):
        pass