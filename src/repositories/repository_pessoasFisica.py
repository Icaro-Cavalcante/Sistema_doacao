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
                query = text ("""SELECT * FROM pessoas_fisica WHERE id = :id""") # Query - Pegando os dados da pessoa física com esse ID
                tupla = conexao.execute(query, {"id" : id}).first() # Executando a query e pegando o resultado
                if not tupla: # Se a tupla não for encontrada
                    print("Dados não encontrados.")
                    raise FileNotFoundError # Tratamento de erro
                else:
                    pessoa_fisica_objeto = PessoaFisica(tupla[1], tupla[2], tupla[3]) # Transformando a tupla em objeto
            except Exception as erro: # Tratamento de erro
                print(f"Não foi possível realizar a consulta.")
                return None
            return pessoa_fisica_objeto
        else: # A conexão não existiu
            return "Não foi possível conectar"

    def update(self, id, nome_atributo, atributo_update):
        '''
        Recebe o ID de uma pessoa física, o nome do atributo e o atributo atualizado e atualiza o atributo
        '''
        conexao = self.database.connect() # Estabelecendo a conexão
        if conexao: # Se a conexão existir
            try:
                query = text (f'''UPDATE pessoas_fisica
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