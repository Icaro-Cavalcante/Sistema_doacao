from src.repositories.repository import Repo
# from src.domain. import Rastreio #TODO: Importar corretamente
from src.database.database import Database
from src.database.tables import Tabela
from sqlalchemy import text # Usamos text para escrever queries

db = Database()
tb = Tabela()

class RepoX(Repo):
    """
    """
    def __init__(self, database, table):
        super().__init__(database, Tabela)

    def create(self, rastreio): #TODO: Colocar parâmetro correto
        """
        """
        conexao = self.database.connect()
        if conexao:
            try: 
                query = text(""" INSERT INTO x () VALUES () ON CONFLICT (id) DO NOTHING """)

                conexao.execute(query, {})

                conexao.commit()
                conexao.close()
            except Exception as erro:
                print(f"")
            return ""
        else:
            return ""
    
    def read(self, doacao_id):
        pass

    def update(self, doacao_id):
        pass

    def inactivate(self):
        pass

    # self.vagasVoluntario = Table('vagasVoluntario', self.metadata,
    #         Column('id', Integer, primary_key=True, autoincrement=True),
    #         Column('id_usuario', Integer, ForeignKey('usuarios.id'), nullable=False),
    #         Column('data_evento', Date, nullable=False),
    #         Column('carga_horaria', String(50)),
    #         Column('titulo', String(100), nullable=False),
    #         Column('descricao', String(500), nullable=False)
    #     )