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
                query = text ("""SELECT * FROM pessoas_juridica WHERE id = :id""") # Query - Pegando os dados da pessoa jurídica com esse ID
                tupla = conexao.execute(query, {"id" : id}).first() # Executando a query e pegando o resultado
                if not tupla: # Se a tupla não for encontrada
                    print("Dados não encontrados.")
                    raise FileNotFoundError # Tratamento de erro
                else:
                    pessoa_juridica_objeto = PessoaJuridica(tupla[1], tupla[2], tupla[3]) # Transformando a tupla em objeto
            except Exception as erro: # Tratamento de erro
                print(f"Não foi possível realizar a consulta.")
                return None
            return pessoa_juridica_objeto
        else: # A conexão não existiu
            return "Não foi possível conectar"

    def update(self, id, nome_atributo, atributo_update):
        '''
        Recebe o ID de uma pessoa jurídica, o nome do atributo e o atributo atualizado e atualiza o atributo
        '''
        conexao = self.database.connect() # Estabelecendo a conexão
        if conexao: # Se a conexão existir
            try:
                query = text (f'''UPDATE pessoas_juridica
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