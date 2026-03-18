# src/repositories/repository_doacoes.py
from src.repositories.repository import Repo
from src.domain.doacoes import Doacao
from src.database.database import Database
from src.database.tables import Tabela
from sqlalchemy import text

db = Database()
tb = Tabela()

class RepoDoacao(Repo):
    def __init__(self, database, table):
        super().__init__(database, table)

    def create(self, doacao):
        conexao = self.database.connect()
        if conexao:
            try: 
                query = text(""" INSERT INTO doacoes (id_usuario, data_doacao, descricao, status_doacao) VALUES (:id_usuario, :data_doacao, :descricao, :status_doacao)""")
                conexao.execute(query, {"id_usuario": doacao.id_usuario, "data_doacao": doacao.data_doacao, "descricao": doacao.descricao, "status_doacao": doacao.status_doacao})
                conexao.commit()
                conexao.close()
            except Exception as erro:
                print(f"Não foi possível realizar o cadastro.")
                return "Não foi possível realizar o cadastro"
            return "Doação cadastrada"
        else:
            return "Não foi possível conectar"
    
    def read(self, id):
        conexao = self.database.connect()
        if conexao:
            try:
                query = text ("""SELECT * FROM doacoes WHERE id = :id""")
                tupla = conexao.execute(query, {"id" : id}).first()
                if not tupla:
                    print("Dados não encontrados.")
                    raise FileNotFoundError
                else:
                    doacao_objeto = {"id": tupla[0], "id_usuario": tupla[1], "data_doacao": tupla[2], "descricao": tupla[3], "status_doacao": tupla[4]}
            except Exception as erro:
                print(f"Não foi possível realizar a consulta.")
                return "Não foi possível realizar a consulta"
            return doacao_objeto
        else:
            return "Não foi possível conectar"

    def update(self, id, doacao):
        conexao = self.database.connect()
        if conexao:
            try:
                query = text ('''UPDATE doacoes
                        SET id_usuario = :id_usuario, data_doacao = :data_doacao, descricao = :descricao, status_doacao = :status_doacao
                        WHERE id = :id''')
                conexao.execute (query, 
                                 {
                                "id_usuario": doacao.id_usuario,
                                "data_doacao": doacao.data_doacao,
                                "descricao": doacao.descricao,
                                "status_doacao": doacao.status_doacao,
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
                query = text("DELETE FROM doacoes WHERE id = :id")
                conexao.execute(query, {"id": id})
                conexao.commit()
                conexao.close()
                return "Doação deletada"
            except Exception as erro:
                print(f"Não foi possível realizar a exclusão.")
                return "Não foi possível deletar"
        else:
            return "Não foi possível conectar"

    def get_all(self):
        conexao = self.database.connect()
        if conexao:
            try:
                query = text("SELECT * FROM doacoes")
                resultados = conexao.execute(query).fetchall()
                return [{"id": tupla[0], "id_usuario": tupla[1], "data_doacao": tupla[2], "descricao": tupla[3], "status_doacao": tupla[4]} for tupla in resultados]
            except Exception as erro:
                print(f"Não foi possível listar.")
                return []
            finally:
                conexao.close()
        return []

    def inactivate(self):
        pass