from src.domain.doacoes import Doacao
from src.repositories.repository import Repo
from src.database.database import Database
from src.database.tables import Tabela
from sqlalchemy import text

db = Database()
tb = Tabela()

class RepoDoacao(Repo):
    '''
    Classe que interaje com o Banco de Dados das doações
    '''
    def __init__(self, database, table):
        super().__init__(database, table)

    def create(self, doacao):
        '''
        Recebe um objeto de doação e cadastra ele no banco de dados
        '''
        conexao = self.database.connect()
        if conexao:
            try:
                query = text ("""INSERT INTO doacoes (id_usuario, data_doacao, descricao, status_doacao)
                            VALUES (:id_usuario, :data_doacao, :descricao, :status_doacao)""")         
                conexao.execute(query, {
                    "id_usuario" : doacao.id_usuario,
                    "data_doacao" : doacao.data_doacao,
                    "descricao" : doacao.descricao,
                    "status_doacao" : doacao.status_doacao})
                conexao.commit()
                conexao.close()
            except Exception as erro:
                print(f"Não foi possível realizar o cadastro.")
                return None
            return "Doação cadastrada"
        else:
            return "Não foi possível conectar"

    def read(self, id):
        '''
        Recebe o ID de uma doação e retorna um objeto com seus dados
        '''
        conexao = self.database.connect() # Estabelecendo conexão
        if conexao: # Se a conexão existir
            try: # Tratamento de erro
                query = text ("""SELECT * FROM doacoes WHERE id = :id""") # Query - Pegando os dados do usuário com esse ID
                tupla = conexao.execute(query, {"id" : id}).first() # Executando a query e pegando o resultado
                if not tupla: # Se a tupla não for encontrada
                    print("Dados não encontrados.")
                    raise FileNotFoundError # Tratamento de erro
                else:
                    usuario_objeto = Doacao(tupla[4], tupla[1], tupla[2], tupla[3], tupla[0]) # Transformando a tupla em objeto
            except Exception as erro: # Tratamento de erro
                print(f"Não foi possível realizar a consulta.")
                return None
            return usuario_objeto
        else: # A conexão não existiu
            return "Não foi possível conectar"

    def update(self, id, nome_atributo, atributo_update):
        '''
        Recebe o ID de uma doação, o nome do atributo e o atributo atualizado e atualiza o atributo
        '''
        conexao = self.database.conectar() # Estabelecendo a conexão
        if conexao: # Se a conexão existir
            try:
                query = text (f'''UPDATE doacoes
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