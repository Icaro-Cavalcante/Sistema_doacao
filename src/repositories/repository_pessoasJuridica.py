# src/repositories/repository_pessoasJuridica.py
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
                query = text(""" INSERT INTO pessoas_juridica (id_usuario, user_cnpj, razao_social) VALUES (:id_usuario, :user_cnpj, :razao_social) ON CONFLICT (id_usuario) DO NOTHING """)

                conexao.execute(query, {"id_usuario": pessoa_juridica.id_usuario, "user_cnpj": pessoa_juridica.user_cnpj, "razao_social": pessoa_juridica.razao_social})

                conexao.commit()
                conexao.close()
            except Exception as erro:
                print(f"Não foi possível realizar o cadastro.")
                return "Não foi possível realizar o cadastro"
            return "Pessoa jurídica cadastrada"
        else:
            return "Não foi possível conectar"
    
    def read(self, id):
        '''
        Recebe o ID de uma pessoa jurídica e retorna um objeto com seus dados
        '''
        conexao = self.database.connect() # Estabelecendo conexão
        if conexao: # Se a conexão existir
            try: # Tratamento de erro
                query = text ("""SELECT * FROM pessoas_juridica WHERE id_usuario = :id""") # Query - Pegando os dados da pessoa jurídica com esse ID
                tupla = conexao.execute(query, {"id" : id}).first() # Executando a query e pegando o resultado
                if not tupla: # Se a tupla não for encontrada
                    print("Dados não encontrados.")
                    raise FileNotFoundError # Tratamento de erro
                else:
                    pessoa_juridica_objeto = {"id_usuario": tupla[0], "user_cnpj": tupla[1], "razao_social": tupla[2]}
            except Exception as erro: # Tratamento de erro
                print(f"Não foi possível realizar a consulta.")
                return "Não foi possível realizar a consulta"
            return pessoa_juridica_objeto
        else: # A conexão não existiu
            return "Não foi possível conectar"

    def update(self, id, pessoa_juridica):
        '''
        Recebe o ID de uma pessoa jurídica e o objeto atualizado e atualiza no banco
        '''
        conexao = self.database.connect() # Estabelecendo a conexão
        if conexao: # Se a conexão existir
            try:
                query = text ('''UPDATE pessoas_juridica
                        SET user_cnpj = :user_cnpj, razao_social = :razao_social
                        WHERE id_usuario = :id''') # query
                conexao.execute (query, 
                                 {
                                "user_cnpj": pessoa_juridica.user_cnpj,
                                "razao_social": pessoa_juridica.razao_social,
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
                query = text("DELETE FROM pessoas_juridica WHERE id_usuario = :id")
                conexao.execute(query, {"id": id})
                conexao.commit()
                conexao.close()
                return "Pessoa Jurídica deletada"
            except Exception as erro:
                print(f"Não foi possível realizar a exclusão.")
                return "Não foi possível deletar"
        else:
            return "Não foi possível conectar"

    def get_all(self):
        conexao = self.database.connect()
        if conexao:
            try:
                query = text("SELECT * FROM pessoas_juridica")
                resultados = conexao.execute(query).fetchall()
                return [{"id_usuario": tupla[0], "user_cnpj": tupla[1], "razao_social": tupla[2]} for tupla in resultados]
            except Exception as erro:
                print(f"Não foi possível listar.")
                return []
            finally:
                conexao.close()
        return []

    def inactivate(self):
        pass