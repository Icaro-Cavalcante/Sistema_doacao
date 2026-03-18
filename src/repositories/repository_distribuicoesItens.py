# src/repositories/repository_distribuicoesItens.py
from src.repositories.repository import Repo
from src.domain.distribuicoesItens import DistribuicaoItem
from src.database.database import Database
from src.database.tables import Tabela
from sqlalchemy import text

db = Database()
tb = Tabela()

class RepoDistribuicaoItem(Repo):
    def __init__(self, database, table):
        super().__init__(database, table)

    def create(self, distribuicao_item):
        conexao = self.database.connect()
        if conexao:
            try: 
                query = text(""" INSERT INTO distribuicoes_item (id_distribuicao, id_item, quantidade_utilizada) VALUES (:id_distribuicao, :id_item, :quantidade_utilizada)""")
                conexao.execute(query, {"id_distribuicao": distribuicao_item.id_distribuicao, "id_item": distribuicao_item.id_item, "quantidade_utilizada": distribuicao_item.quantidade_utilizada})
                conexao.commit()
                conexao.close()
            except Exception as erro:
                print(f"Não foi possível realizar o cadastro.")
                return "Não foi possível realizar o cadastro"
            return "Item de distribuição cadastrado"
        else:
            return "Não foi possível conectar"
    
    def read(self, id):
        conexao = self.database.connect()
        if conexao:
            try:
                query = text ("""SELECT * FROM distribuicoes_item WHERE id_distribuicao = :id""")
                tupla = conexao.execute(query, {"id" : id}).first()
                if not tupla:
                    print("Dados não encontrados.")
                    raise FileNotFoundError
                else:
                    item_objeto = {"id_distribuicao": tupla[0], "id_item": tupla[1], "quantidade_utilizada": tupla[2]}
            except Exception as erro:
                print(f"Não foi possível realizar a consulta.")
                return "Não foi possível realizar a consulta"
            return item_objeto
        else:
            return "Não foi possível conectar"

    def update(self, id, distribuicao_item):
        conexao = self.database.connect()
        if conexao:
            try:
                query = text ('''UPDATE distribuicoes_item
                        SET id_item = :id_item, quantidade_utilizada = :quantidade_utilizada
                        WHERE id_distribuicao = :id''')
                conexao.execute (query, 
                                 {
                                "id_item": distribuicao_item.id_item,
                                "quantidade_utilizada": distribuicao_item.quantidade_utilizada,
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
                query = text("DELETE FROM distribuicoes_item WHERE id_distribuicao = :id")
                conexao.execute(query, {"id": id})
                conexao.commit()
                conexao.close()
                return "Item de distribuição deletado"
            except Exception as erro:
                print(f"Não foi possível realizar a exclusão.")
                return "Não foi possível deletar"
        else:
            return "Não foi possível conectar"

    def get_all(self):
        conexao = self.database.connect()
        if conexao:
            try:
                query = text("SELECT * FROM distribuicoes_item")
                resultados = conexao.execute(query).fetchall()
                return [{"id_distribuicao": tupla[0], "id_item": tupla[1], "quantidade_utilizada": tupla[2]} for tupla in resultados]
            except Exception as erro:
                print(f"Não foi possível listar.")
                return []
            finally:
                conexao.close()
        return []

    def inactivate(self):
        pass