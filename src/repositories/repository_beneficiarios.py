# src/repositories/repository_beneficiarios.py
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
                query = text(""" INSERT INTO beneficiarios (id_usuario, data_cadastro_beneficiario) VALUES (:id_usuario, :data_cadastro_beneficiario)""")

                conexao.execute(query, {"id_usuario": beneficiario.id_usuario, "data_cadastro_beneficiario": beneficiario.data_cadastro_beneficiario})

                conexao.commit()
                conexao.close()
            except Exception as erro:
                print(f"Não foi possível realizar o cadastro.")
                return "Não foi possível realizar o cadastro"
            return "Beneficiário cadastrado"
        else:
            return "Não foi possível conectar"
    
    def read(self, id):
        '''
        Recebe o ID de um beneficiário e retorna um objeto com seus dados
        '''
        conexao = self.database.connect() # Estabelecendo conexão
        if conexao: # Se a conexão existir
            try: # Tratamento de erro
                query = text ("""SELECT * FROM beneficiarios WHERE id_usuario = :id""") # Query - Pegando os dados do beneficiário com esse ID
                tupla = conexao.execute(query, {"id" : id}).first() # Executando a query e pegando o resultado
                if not tupla: # Se a tupla não for encontrada
                    print("Dados não encontrados.")
                    raise FileNotFoundError # Tratamento de erro
                else:
                    beneficiario_objeto = {"id_usuario": tupla[0], "data_cadastro_beneficiario": tupla[1]}
            except Exception as erro: # Tratamento de erro
                print(f"Não foi possível realizar a consulta.")
                return "Não foi possível realizar a consulta"
            return beneficiario_objeto
        else: # A conexão não existiu
            return "Não foi possível conectar"

    def update(self, id, beneficiario):
        '''
        Recebe o ID de um beneficiário e o objeto atualizado e atualiza no banco
        '''
        conexao = self.database.connect() # Estabelecendo a conexão
        if conexao: # Se a conexão existir
            try:
                query = text ('''UPDATE beneficiarios
                        SET data_cadastro_beneficiario = :data_cadastro_beneficiario
                        WHERE id_usuario = :id''') # query
                conexao.execute (query, 
                                 {
                                "data_cadastro_beneficiario": beneficiario.data_cadastro_beneficiario,
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
                query = text("DELETE FROM beneficiarios WHERE id_usuario = :id")
                conexao.execute(query, {"id": id})
                conexao.commit()
                conexao.close()
                return "Beneficiário deletado"
            except Exception as erro:
                print(f"Não foi possível realizar a exclusão.")
                return "Não foi possível deletar"
        else:
            return "Não foi possível conectar"

    def get_all(self):
        conexao = self.database.connect()
        if conexao:
            try:
                query = text("SELECT * FROM beneficiarios")
                resultados = conexao.execute(query).fetchall()
                return [{"id_usuario": tupla[0], "data_cadastro_beneficiario": tupla[1]} for tupla in resultados]
            except Exception as erro:
                print(f"Não foi possível listar.")
                return []
            finally:
                conexao.close()
        return []

    def inactivate(self):
        pass
