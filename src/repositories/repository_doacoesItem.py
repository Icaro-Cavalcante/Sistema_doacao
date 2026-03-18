# src/repositories/repository_doacoesItem.py
from src.repositories.repository import Repo
from src.domain.doacoesItem import DoacaoItem
from src.database.database import Database
from src.database.tables import Tabela
from sqlalchemy import text

db = Database()
tb = Tabela()

class RepoDoacoesItem(Repo):
    def __init__(self, database, table):
        super().__init__(database, table)

    def create(self, doacao_item):
        conexao = self.database.connect()
        if conexao:
            try: 
                query = text(""" INSERT INTO doacoes_item (id_doacao, id_item, quantidade_utilizada) VALUES (:id_doacao, :id_item, :quantidade_utilizada)""")
                conexao.execute(query, {"id_doacao": doacao_item.id_doacao, "id_item": doacao_item.id_item, "quantidade_utilizada": doacao_item.quantidade_utilizada})
                conexao.commit()
                conexao.close()
            except Exception as erro:
                print(f"Não foi possível realizar o cadastro.")
                return "Não foi possível realizar o cadastro"
            return "Item de doação cadastrado"
        else:
            return "Não foi possível conectar"
    
    def read(self, id):
        conexao = self.database.connect()
        if conexao:
            try:
                query = text ("""SELECT * FROM doacoes_item WHERE id = :id""")
                tupla = conexao.execute(query, {"id" : id}).first()
                if not tupla:
                    print("Dados não encontrados.")
                    raise FileNotFoundError
                else:
                    item_objeto = {"id": tupla[0], "id_doacao": tupla[1], "id_item": tupla[2], "quantidade_utilizada": tupla[3]}
            except Exception as erro:
                print(f"Não foi possível realizar a consulta.")
                return "Não foi possível realizar a consulta"
            return item_objeto
        else:
            return "Não foi possível conectar"

    def update(self, id, doacao_item):
        conexao = self.database.connect()
        if conexao:
            try:
                query = text ('''UPDATE doacoes_item
                        SET id_doacao = :id_doacao, id_item = :id_item, quantidade_utilizada = :quantidade_utilizada
                        WHERE id = :id''')
                conexao.execute (query, 
                                 {
                                "id_doacao": doacao_item.id_doacao,
                                "id_item": doacao_item.id_item,
                                "quantidade_utilizada": doacao_item.quantidade_utilizada,
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
                query = text("DELETE FROM doacoes_item WHERE id = :id")
                conexao.execute(query, {"id": id})
                conexao.commit()
                conexao.close()
                return "Item de doação deletado"
            except Exception as erro:
                print(f"Não foi possível realizar a exclusão.")
                return "Não foi possível deletar"
        else:
            return "Não foi possível conectar"

    def get_all(self):
        conexao = self.database.connect()
        if conexao:
            try:
                query = text("SELECT * FROM doacoes_item")
                resultados = conexao.execute(query).fetchall()
                return [{"id": tupla[0], "id_doacao": tupla[1], "id_item": tupla[2], "quantidade_utilizada": tupla[3]} for tupla in resultados]
            except Exception as erro:
                print(f"Não foi possível listar.")
                return []
            finally:
                conexao.close()
        return []

    def get_items_by_doacao_details(self, id_doacao):
        conexao = self.database.connect()
        if conexao:
            try:
                query = text("SELECT * FROM doacoes_item WHERE id_doacao = :id_doacao")
                resultados = conexao.execute(query, {"id_doacao": id_doacao}).fetchall()
                return [{"id": tupla[0], "id_doacao": tupla[1], "id_item": tupla[2], "quantidade_utilizada": tupla[3]} for tupla in resultados]
            except Exception as erro:
                return []
            finally:
                conexao.close()
        return []

    def get_total_donated_by_category(self):
        return []

    def inactivate(self):
        pass