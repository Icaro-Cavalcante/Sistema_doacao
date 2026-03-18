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

    def read_by_login(self, login: str):
        '''
        Busca um utilizador na base de dados através do seu login (username).
        '''
        conexao = self.database.connect()
        if conexao:
            try:
                # Procura o utilizador onde a coluna login corresponde ao que foi digitado
                query = text("SELECT * FROM usuarios WHERE login = :login")
                tupla = conexao.execute(query, {"login": login}).first()
                
                if tupla:
                    # O banco retorna (id, nome, email, senha, login, data_cadastro)
                    # Vamos instanciar o objeto passando os atributos de forma explícita
                    return Usuario(
                        nome=tupla[1], 
                        email=tupla[2], 
                        senha=tupla[3], 
                        login=tupla[4], 
                        data_cadastro=tupla[5]
                    )
                return None
            except Exception as erro:
                print(f"Erro ao procurar utilizador por login: {erro}")
                return None
            finally:
                conexao.close()
        return None

    def create(self, usuario):
        '''
        Recebe um objeto de usuário e cadastra ele no banco de dados
        '''
        conexao = self.database.connect() # Estabelecendo a conexão
        if conexao: # Se a conexão existir
            try: # Tratamento de erro
                query = text ("""INSERT INTO usuarios (nome, email, senha, login, data_cadastro)
                            VALUES (:nome, :email, :senha, :login, :data_cadastro)""") # Escreve a query
                conexao.execute(query, {
                    "nome" : usuario.nome,
                    "email" : usuario.email,
                    "senha" : usuario.senha,
                    "login" : usuario.login,
                    "data_cadastro" : usuario.data_cadastro }) #Executa a query
                conexao.commit() # Salva as alterações no banco de dados
                conexao.close() # Fecha a conexão
            except Exception as erro: # Tratamento de erro
                print(f"Não foi possível realizar o cadastro.")
                return None
            return "Usuário cadastrado"
        else: # A conexão não existiu
            return "Não foi possível conectar"
        
    def read(self, id):
        '''
        Recebe o ID de um usuário e retorna um objeto com seus dados
        '''
        conexao = self.database.connect() # Estabelecendo conexão
        if conexao: # Se a conexão existir
            try: # Tratamento de erro
                query = text ("""SELECT * FROM usuarios WHERE id = :id""") # Query - Pegando os dados do usuário com esse ID
                tupla = conexao.execute(query, {"id" : id}).first() # Executando a query e pegando o resultado
                if not tupla: # Se a tupla não for encontrada
                    print("Dados não encontrados.")
                    raise FileNotFoundError # Tratamento de erro
                else:
                    usuario_objeto = Usuario(tupla[1], tupla[2], tupla[3], tupla[4], tupla[5], tupla[0]) # Transformando a tupla em objeto
            except Exception as erro: # Tratamento de erro
                print(f"Não foi possível realizar a consulta.")
                return None
            return usuario_objeto
        else: # A conexão não existiu
            return "Não foi possível conectar"

    def update(self, id, nome_atributo, atributo_update):
        '''
        Recebe o ID de um usuário, o nome do atributo e o atributo atualizado e atualiza o atributo
        '''
        conexao = self.database.connect() # Estabelecendo a conexão
        if conexao: # Se a conexão existir
            try:
                query = text (f'''UPDATE usuarios
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