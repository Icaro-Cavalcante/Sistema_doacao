from src.repositories.repository import Repo
from src.domain.vagasVoluntariado import VagaVoluntariado
from src.database.database import Database
from src.database.tables import Tabela
from sqlalchemy import text # Usamos text para escrever queries

db = Database()
tb = Tabela()

class RepoVagaVoluntariado(Repo):
    '''
    Classe que interaje com o Banco de Dados das vagas de voluntariado
    '''
    def __init__(self, database, table):
        super().__init__(database, table)

    def create(self, vaga_voluntariado):
        '''
        Recebe um objeto de vaga de voluntariado e cadastra ele no banco de dados
        '''
        conexao = self.database.connect()
        if conexao:
            try: 
                query = text(""" INSERT INTO vagasVoluntario (id_usuario, titulo, descricao, data_inicio, data_fim, carga_horaria, quantidade_vagas) VALUES (:id_usuario, :titulo, :descricao, :data_inicio, :data_fim, :carga_horaria, :quantidade_vagas) ON CONFLICT (id) DO NOTHING """)

                conexao.execute(query, {"id_usuario": vaga_voluntariado.id_usuario, "titulo": vaga_voluntariado.titulo, "descricao": vaga_voluntariado.descricao, "data_inicio": vaga_voluntariado.data_inicio, "data_fim": vaga_voluntariado.data_fim, "carga_horaria": vaga_voluntariado.carga_horaria, "quantidade_vagas": vaga_voluntariado.quantidade_vagas})

                conexao.commit()
                conexao.close()
            except Exception as erro:
                print(f"Não foi possível realizar o cadastro.")
            return "Vaga de voluntariado cadastrada"
        else:
            return "Não foi possível conectar"
    
    def read(self, id):
        pass

    def update(self, id):
        pass

    def inactivate(self):
        pass