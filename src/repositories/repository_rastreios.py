from src.repositories.repository import Repo
from src.domain.rastreios import Rastreio
from src.database.database import Database
from src.database.tables import Tabela
from sqlalchemy import text # Usamos text para escrever queries

db = Database()
tb = Tabela()

class RepoRastreio(Repo):
    """
    Classe que interaje com o Banco de Dados de rastreios
    """
    def __init__(self, database, table):
        super().__init__(database, Tabela)

    def create(self, rastreio):
        """
        Recebe um objeto de rastreio e cadastra ele no banco de dados
        """
        conexao = self.database.connect()
        if conexao:
            try: 
                query = text(""" INSERT INTO rastreios (id_doacao_item, data_movimentacao, tipo_movimentacao, localizacao) VALUES (:id_doacao_item, :data_movimentacao, :tipo_movimentacao, :localizacao) ON CONFLICT (id) DO NOTHING""")

                conexao.execute(query, {"id_doacao_item": rastreio.id_doacao_item, "data_movimentacao": rastreio.data_movimentacao, "tipo_movimentacao": rastreio.tipo_movimentacao, "localizacao": rastreio.localizacao})

                conexao.commit()
                conexao.close()
            except Exception as erro:
                print(f"Erro ao verificar o rastreio")
            return "Rastreio criado com sucesso"
        else:
            return "Erro ao verificar o rastreio"
    
    def read(self, doacao_id):
        '''
        Recebe o ID de um rastreio e retorna um objeto com seus dados
        '''
        conexao = self.database.connect() # Estabelecendo conexão
        if conexao: # Se a conexão existir
            try: # Tratamento de erro
                query = text ("""SELECT * FROM rastreios WHERE id = :id""") # Query - Pegando os dados do rastreio com esse ID
                tupla = conexao.execute(query, {"id" : doacao_id}).first() # Executando a query e pegando o resultado
                if not tupla: # Se a tupla não for encontrada
                    print("Dados não encontrados.")
                    raise FileNotFoundError # Tratamento de erro
                else:
                    rastreio_objeto = Rastreio(tupla[1], tupla[2], tupla[3], tupla[4], tupla[0]) # Transformando a tupla em objeto
            except Exception as erro: # Tratamento de erro
                print(f"Não foi possível realizar a consulta.")
                return None
            return rastreio_objeto
        else: # A conexão não existiu
            return "Não foi possível conectar"

    def update(self, doacao_id, nome_atributo, atributo_update):
        '''
        Recebe o ID de um rastreio, o nome do atributo e o atributo atualizado e atualiza o atributo
        '''
        conexao = self.database.connect() # Estabelecendo a conexão
        if conexao: # Se a conexão existir
            try:
                query = text (f'''UPDATE rastreios
                        SET {nome_atributo} = :atributo_update
                        WHERE id = :id''') # query
                conexao.execute (query, 
                                 {
                                "atributo_update": atributo_update,
                                "id": doacao_id })
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

# self.rastreios = Table('rastreios', self.metadata,
#             Column('id', Integer, primary_key=True, autoincrement=True),
#             Column('id_doacao', Integer, ForeignKey('doacoes.id'), nullable=False),
#             Column('data_hora', Date, nullable=False),
#             Column('etapa', String(100)),
#             Column('localizacao', String(100))
#         ) 