# src/repositories/repository_usuarios.py
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
                return "Não foi possível realizar o cadastro"
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
                    usuario_objeto = {"id": tupla[0], "nome": tupla[1], "email": tupla[2], "senha": tupla[3], "login": tupla[4], "data_cadastro": tupla[5]}
            except Exception as erro: # Tratamento de erro
                print(f"Não foi possível realizar a consulta.")
                return "Não foi possível realizar a consulta"
            return usuario_objeto
        else: # A conexão não existiu
            return "Não foi possível conectar"

    def update(self, id, usuario):
        '''
        Recebe o ID de um usuário e o objeto atualizado e atualiza no banco
        '''
        conexao = self.database.connect() # Estabelecendo a conexão
        if conexao: # Se a conexão existir
            try:
                query = text ('''UPDATE usuarios
                        SET nome = :nome, email = :email, senha = :senha, login = :login, data_cadastro = :data_cadastro
                        WHERE id = :id''') # query
                conexao.execute (query, 
                                 {
                                "nome": usuario.nome,
                                "email": usuario.email,
                                "senha": usuario.senha,
                                "login": usuario.login,
                                "data_cadastro": usuario.data_cadastro,
                                "id": id })
                conexao.commit()
                conexao.close()
                return "Atributo atualizado"
            except Exception as erro: # Tratamento de erro
                print(f"Não foi possível realizar a consulta.")
                return "Não foi possível atualizar"
        else:
            return "Não foi possível conectar"

    def delete(self, id):
        conexao = self.database.connect()
        if conexao:
            try:
                query = text("DELETE FROM usuarios WHERE id = :id")
                conexao.execute(query, {"id": id})
                conexao.commit()
                conexao.close()
                return "Usuário deletado"
            except Exception as erro:
                print(f"Não foi possível realizar a exclusão.")
                return "Não foi possível deletar"
        else:
            return "Não foi possível conectar"

    def get_all(self):
        conexao = self.database.connect()
        if conexao:
            try:
                query = text("SELECT * FROM usuarios")
                resultados = conexao.execute(query).fetchall()
                usuarios = [{"id": tupla[0], "nome": tupla[1], "email": tupla[2], "login": tupla[4], "data_cadastro": tupla[5]} for tupla in resultados]
                return usuarios
            except Exception as erro:
                print(f"Não foi possível listar os usuários.")
                return []
            finally:
                conexao.close()
        return []

    def inactivate(self):
        pass