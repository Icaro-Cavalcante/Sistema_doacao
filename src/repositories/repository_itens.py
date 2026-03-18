# src/repositories/repository_itens.py
from src.repositories.repository import Repo
from src.domain.itens import Item
from src.database.database import Database
from src.database.tables import Tabela
from sqlalchemy import text

db = Database()
tb = Tabela()

class RepoItens(Repo):
    '''
    Classe que interaje com o Banco de Dados dos itens
    '''
    def __init__(self, database, table):
        super().__init__(database, table)

    def create(self, item):
        conexao = self.database.connect()
        if conexao:
            try: 
                query = text(""" INSERT INTO itens (id_categoria_item, descricao, nome, unidade_medida) VALUES (:id_categoria_item, :descricao, :nome, :unidade_medida)""")
                conexao.execute(query, {"id_categoria_item": item.id_categoria_item, "descricao": item.descricao, "nome": item.nome, "unidade_medida": item.unidade_medida})
                conexao.commit()
                conexao.close()
            except Exception as erro:
                print(f"Não foi possível realizar o cadastro.")
                return "Não foi possível realizar o cadastro"
            return "Item cadastrado"
        else:
            return "Não foi possível conectar"
    
    def read(self, id):
        conexao = self.database.connect()
        if conexao:
            try:
                query = text ("""SELECT * FROM itens WHERE id = :id""")
                tupla = conexao.execute(query, {"id" : id}).first()
                if not tupla:
                    print("Dados não encontrados.")
                    raise FileNotFoundError
                else:
                    item_objeto = {"id": tupla[0], "id_categoria_item": tupla[1], "descricao": tupla[2], "nome": tupla[3], "unidade_medida": tupla[4]}
            except Exception as erro:
                print(f"Não foi possível realizar a consulta.")
                return "Não foi possível realizar a consulta"
            return item_objeto
        else:
            return "Não foi possível conectar"

    def update(self, id, item):
        conexao = self.database.connect()
        if conexao:
            try:
                query = text ('''UPDATE itens
                        SET id_categoria_item = :id_categoria_item, descricao = :descricao, nome = :nome, unidade_medida = :unidade_medida
                        WHERE id = :id''')
                conexao.execute (query, 
                                 {
                                "id_categoria_item": item.id_categoria_item,
                                "descricao": item.descricao,
                                "nome": item.nome,
                                "unidade_medida": item.unidade_medida,
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
                query = text("DELETE FROM itens WHERE id = :id")
                conexao.execute(query, {"id": id})
                conexao.commit()
                conexao.close()
                return "Item deletado"
            except Exception as erro:
                print(f"Não foi possível realizar a exclusão.")
                return "Não foi possível deletar"
        else:
            return "Não foi possível conectar"

    def get_all(self):
        conexao = self.database.connect()
        if conexao:
            try:
                query = text("SELECT * FROM itens")
                resultados = conexao.execute(query).fetchall()
                return [{"id": tupla[0], "id_categoria_item": tupla[1], "descricao": tupla[2], "nome": tupla[3], "unidade_medida": tupla[4]} for tupla in resultados]
            except Exception as erro:
                print(f"Não foi possível listar.")
                return []
            finally:
                conexao.close()
        return []

    def inactivate(self):
        pass