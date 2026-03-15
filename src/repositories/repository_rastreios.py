from src.repositories.repository import Repo
from src.domain.rastreios import Rastreio
from src.database.database import Database
from src.database.tables import Tabela
from sqlalchemy import text # Usamos text para escrever queries

db = Database()
tb = Tabela()

class RepoRastreio(Repo):
    """
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
        pass

    def update(self, doacao_id):
        pass

    def inactivate(self):
        pass

# self.rastreios = Table('rastreios', self.metadata,
#             Column('id', Integer, primary_key=True, autoincrement=True),
#             Column('id_doacao', Integer, ForeignKey('doacoes.id'), nullable=False),
#             Column('data_hora', Date, nullable=False),
#             Column('etapa', String(100)),
#             Column('localizacao', String(100))
#         ) 