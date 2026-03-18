# src/repositories/repository_itensCategoria.py
from src.repositories.repository import Repo
from src.domain.itensCategoria import ItemCategoria
from src.database.database import Database
from src.database.tables import Tabela
from sqlalchemy import text

db = Database()
tb = Tabela()

class RepoItemCategoria(Repo):
    '''
    Classe que interaje com o Banco de Dados das categorias de itens
    '''
    def __init__(self, database, table):
        super().__init__(database, table)

    def create(self, categoria):
        conexao = self.database.connect()
        if conexao:
            try: 
                query = text(""" INSERT INTO itens_categoria (nome_categoria, descricao) VALUES (:nome_categoria, :descricao)""")
                conexao.execute(query, {"nome_categoria": categoria.nome_categoria, "descricao": categoria.descricao})
                conexao.commit()
                conexao.close()
            except Exception as erro:
                print(f"Não foi possível realizar o cadastro.")
                return "Não foi possível realizar o cadastro"
            return "Categoria cadastrada"
        else:
            return "Não foi possível conectar"
    
    def read(self, id):
        conexao = self.database.connect()
        if conexao:
            try:
                query = text ("""SELECT * FROM itens_categoria WHERE id = :id""")
                tupla = conexao.execute(query, {"id" : id}).first()
                if not tupla:
                    print("Dados não encontrados.")
                    raise FileNotFoundError
                else:
                    categoria_objeto = {"id": tupla[0], "nome_categoria": tupla[1], "descricao": tupla[2]}
            except Exception as erro:
                print(f"Não foi possível realizar a consulta.")
                return "Não foi possível realizar a consulta"
            return categoria_objeto
        else:
            return "Não foi possível conectar"

    def update(self, id, categoria):
        conexao = self.database.connect()
        if conexao:
            try:
                query = text ('''UPDATE itens_categoria
                        SET nome_categoria = :nome_categoria, descricao = :descricao
                        WHERE id = :id''')
                conexao.execute (query, 
                                 {
                                "nome_categoria": categoria.nome_categoria,
                                "descricao": categoria.descricao,
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
                query = text("DELETE FROM itens_categoria WHERE id = :id")
                conexao.execute(query, {"id": id})
                conexao.commit()
                conexao.close()
                return "Categoria deletada"
            except Exception as erro:
                print(f"Não foi possível realizar a exclusão.")
                return "Não foi possível deletar"
        else:
            return "Não foi possível conectar"

    def get_all(self):
        conexao = self.database.connect()
        if conexao:
            try:
                query = text("SELECT * FROM itens_categoria")
                resultados = conexao.execute(query).fetchall()
                return [{"id": tupla[0], "nome_categoria": tupla[1], "descricao": tupla[2]} for tupla in resultados]
            except Exception as erro:
                print(f"Não foi possível listar.")
                return []
            finally:
                conexao.close()
        return []

    def inactivate(self):
        pass