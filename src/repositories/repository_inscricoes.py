# src/repositories/repository_inscricoes.py
from src.repositories.repository import Repo
from src.domain.inscricoes import Inscricao
from src.database.database import Database
from src.database.tables import Tabela
from sqlalchemy import text

db = Database()
tb = Tabela()

class RepoInscricoes(Repo):
    '''
    Classe que interaje com o Banco de Dados das inscrições em vagas de voluntariado
    '''
    def __init__(self, database, table):
        super().__init__(database, table)

    def create(self, inscricao):
        conexao = self.database.connect()
        if conexao:
            try: 
                query = text(""" INSERT INTO inscricoes (id_vaga, id_usuario, status, data_inscricao) VALUES (:id_vaga, :id_usuario, :status, :data_inscricao)""")
                conexao.execute(query, {"id_vaga": inscricao.id_vaga, "id_usuario": inscricao.id_usuario, "status": inscricao.status, "data_inscricao": inscricao.data_inscricao})
                conexao.commit()
                conexao.close()
            except Exception as erro:
                print(f"Não foi possível realizar o cadastro.")
                return "Não foi possível realizar o cadastro"
            return "Inscrição cadastrada"
        else:
            return "Não foi possível conectar"
    
    def read(self, id):
        conexao = self.database.connect()
        if conexao:
            try:
                query = text ("""SELECT * FROM inscricoes WHERE id = :id""")
                tupla = conexao.execute(query, {"id" : id}).first()
                if not tupla:
                    print("Dados não encontrados.")
                    raise FileNotFoundError
                else:
                    inscricao_objeto = {"id": tupla[0], "id_vaga": tupla[1], "id_usuario": tupla[2], "status": tupla[3], "data_inscricao": tupla[4]}
            except Exception as erro:
                print(f"Não foi possível realizar a consulta.")
                return "Não foi possível realizar a consulta"
            return inscricao_objeto
        else:
            return "Não foi possível conectar"

    def update(self, id, inscricao):
        conexao = self.database.connect()
        if conexao:
            try:
                query = text ('''UPDATE inscricoes
                        SET id_vaga = :id_vaga, id_usuario = :id_usuario, status = :status, data_inscricao = :data_inscricao
                        WHERE id = :id''')
                conexao.execute (query, 
                                 {
                                "id_vaga": inscricao.id_vaga,
                                "id_usuario": inscricao.id_usuario,
                                "status": inscricao.status,
                                "data_inscricao": inscricao.data_inscricao,
                                "id": id })
                conexao.commit()
                conexao.close()
                return "Atributo atualizado"
            except Exception as erro:
                print(f"Não foi possível realizar a consulta.")
                return "Não foi possível atualizar"
        else:
            return "Não foi possível conectar"

    def delete(self, id):
        conexao = self.database.connect()
        if conexao:
            try:
                query = text("DELETE FROM inscricoes WHERE id = :id")
                conexao.execute(query, {"id": id})
                conexao.commit()
                conexao.close()
                return "Inscrição deletada"
            except Exception as erro:
                print(f"Não foi possível realizar a exclusão.")
                return "Não foi possível deletar"
        else:
            return "Não foi possível conectar"

    def get_all(self):
        conexao = self.database.connect()
        if conexao:
            try:
                query = text("SELECT * FROM inscricoes")
                resultados = conexao.execute(query).fetchall()
                return [{"id": tupla[0], "id_vaga": tupla[1], "id_usuario": tupla[2], "status": tupla[3], "data_inscricao": tupla[4]} for tupla in resultados]
            except Exception as erro:
                print(f"Não foi possível listar.")
                return []
            finally:
                conexao.close()
        return []

    def inactivate(self):
        pass