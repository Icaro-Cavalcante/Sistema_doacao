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
                query = text ("""SELECT * FROM beneficiarios WHERE id = :id""") # Query - Pegando os dados do beneficiário com esse ID
                tupla = conexao.execute(query, {"id" : id}).first() # Executando a query e pegando o resultado
                if not tupla: # Se a tupla não for encontrada
                    print("Dados não encontrados.")
                    raise FileNotFoundError # Tratamento de erro
                else:
                    beneficiario_objeto = Beneficiario(tupla[1], tupla[2]) # Transformando a tupla em objeto
            except Exception as erro: # Tratamento de erro
                print(f"Não foi possível realizar a consulta.")
                return None
            return beneficiario_objeto
        else: # A conexão não existiu
            return "Não foi possível conectar"

    def update(self, id, nome_atributo, atributo_update):
        '''
        Recebe o ID de um beneficiário, o nome do atributo e o atributo atualizado e atualiza o atributo
        '''
        conexao = self.database.connect() # Estabelecendo a conexão
        if conexao: # Se a conexão existir
            try:
                query = text (f'''UPDATE beneficiarios
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
