# src/repositories/repository_pessoasFisica.py
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
                query = text(""" INSERT INTO pessoas_fisica (id_usuario, user_cpf, data_nascimento) VALUES (:id_usuario, :user_cpf, :data_nascimento) ON CONFLICT (id_usuario) DO NOTHING """)

                conexao.execute(query, {"id_usuario": pessoa_fisica.id_usuario, "user_cpf": pessoa_fisica.user_cpf, "data_nascimento": pessoa_fisica.data_nascimento})

                conexao.commit()
                conexao.close()
            except Exception as erro:
                print(f"Não foi possível realizar o cadastro.\n\n{erro}")
                return "Não foi possível realizar o cadastro"
            return "Pessoa física cadastrada"
        else:
            return "Não foi possível conectar"
    
    def read(self, id):
        '''
        Recebe o ID de uma pessoa física e retorna um objeto com seus dados
        '''
        conexao = self.database.connect() # Estabelecendo conexão
        if conexao: # Se a conexão existir
            try: # Tratamento de erro
                query = text ("""SELECT * FROM pessoas_fisica WHERE id_usuario = :id""") # Query - Pegando os dados da pessoa física com esse ID
                tupla = conexao.execute(query, {"id" : id}).first() # Executando a query e pegando o resultado
                if not tupla: # Se a tupla não for encontrada
                    print("Dados não encontrados.")
                    raise FileNotFoundError # Tratamento de erro
                else:
                    pessoa_fisica_objeto = {"id_usuario": tupla[0], "user_cpf": tupla[1], "data_nascimento": tupla[2]}
            except Exception as erro: # Tratamento de erro
                print(f"Não foi possível realizar a consulta.")
                return "Não foi possível realizar a consulta"
            return pessoa_fisica_objeto
        else: # A conexão não existiu
            return "Não foi possível conectar"

    def update(self, id, pessoa_fisica):
        '''
        Recebe o ID de uma pessoa física e o objeto atualizado e atualiza no banco
        '''
        conexao = self.database.connect() # Estabelecendo a conexão
        if conexao: # Se a conexão existir
            try:
                query = text ('''UPDATE pessoas_fisica
                        SET user_cpf = :user_cpf, data_nascimento = :data_nascimento
                        WHERE id_usuario = :id''') # query
                conexao.execute (query, 
                                 {
                                "user_cpf": pessoa_fisica.user_cpf,
                                "data_nascimento": pessoa_fisica.data_nascimento,
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
                query = text("DELETE FROM pessoas_fisica WHERE id_usuario = :id")
                conexao.execute(query, {"id": id})
                conexao.commit()
                conexao.close()
                return "Pessoa Física deletada"
            except Exception as erro:
                print(f"Não foi possível realizar a exclusão.")
                return "Não foi possível deletar"
        else:
            return "Não foi possível conectar"

    def get_all(self):
        conexao = self.database.connect()
        if conexao:
            try:
                query = text("SELECT * FROM pessoas_fisica")
                resultados = conexao.execute(query).fetchall()
                return [{"id_usuario": tupla[0], "user_cpf": tupla[1], "data_nascimento": tupla[2]} for tupla in resultados]
            except Exception as erro:
                print(f"Não foi possível listar.")
                return []
            finally:
                conexao.close()
        return []

    def inactivate(self):
        pass