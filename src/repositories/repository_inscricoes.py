from src.repositories.repository import Repo
from src.domain.inscricoes import Inscricao
from src.database.database import Database
from src.database.tables import Tabela
from sqlalchemy import text # Usamos text para escrever queries

db = Database() # Objeto do banco de dados
tb = Tabela() # Objeto da tabela

class RepoInscricoes(Repo): # Importando da classe pai para polimorfismo
    '''
    Classe que interaje com o Banco de Dados das inscrições
    '''
    def __init__(self, database, table):
        super().__init__(database, table)

    def create(self, inscricao):
        '''
        Recebe um objeto de inscrição e cadastra ele no banco de dados
        '''
        conexao = self.database.connect() # Estabelecendo a conexão
        if conexao: # Se a conexão existir
            try: # Tratamento de erro
                query = text ("""INSERT INTO inscricoes (id_vaga, id_usuario, status, data_inscricao)
                            VALUES (:id_vaga, :id_usuario, :status, :data_inscricao)
                            ON CONFLICT (id) DO NOTHING""") # Escreve a query
                conexao.execute(query, {"id_vaga" : inscricao.id_vaga, "id_usuario" : inscricao.id_usuario, "status" : inscricao.status, "data_inscricao" : inscricao.data_inscricao}) #Executa a query
                conexao.commit() # Salva as alterações no banco de dados
                conexao.close() # Fecha a conexão
            except Exception as erro: # Tratamento de erro
                print(f"Não foi possível realizar o cadastro.")
            return "Inscrição cadastrada"
        else: # A conexão não existiu
            return "Não foi possível conectar"

        
    def read(self, id):
        '''
        Recebe o ID de uma inscrição e retorna um objeto com seus dados
        '''
        conexao = self.database.connect() # Estabelecendo conexão
        if conexao: # Se a conexão existir
            try: # Tratamento de erro
                query = text ("""SELECT * FROM inscricoes WHERE id = :id""") # Query - Pegando os dados da inscrição com esse ID
                tupla = conexao.execute(query, {"id" : id}).first() # Executando a query e pegando o resultado
                if not tupla: # Se a tupla não for encontrada
                    print("Dados não encontrados.")
                    raise FileNotFoundError # Tratamento de erro
                else:
                    inscricao_objeto = Inscricao(tupla[1], tupla[2], tupla[3], tupla[4], tupla[0]) # Transformando a tupla em objeto
            except Exception as erro: # Tratamento de erro
                print(f"Não foi possível realizar a consulta.")
                return None
            return inscricao_objeto
        else: # A conexão não existiu
            return "Não foi possível conectar"

    def update(self, id, nome_atributo, atributo_update):
        '''
        Recebe o ID de uma inscrição, o nome do atributo e o atributo atualizado e atualiza o atributo
        '''
        conexao = self.database.connect() # Estabelecendo a conexão
        if conexao: # Se a conexão existir
            try:
                query = text (f'''UPDATE inscricoes
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