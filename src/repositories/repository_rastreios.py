# src/repositories/repository_rastreios.py
from src.repositories.repository import Repo
from src.domain.rastreios import Rastreio
from src.database.database import Database
from src.database.tables import Tabela
from sqlalchemy import text

db = Database()
tb = Tabela()

class RepoRastreio(Repo):
    '''
    Classe que interaje com o Banco de Dados dos rastreios
    '''
    def __init__(self, database, table):
        super().__init__(database, table)

    def create(self, rastreio):
        conexao = self.database.connect()
        if conexao:
            try: 
                query = text(""" INSERT INTO rastreios (id_doacao_item, data_movimentacao, tipo_movimentacao, localizacao) VALUES (:id_doacao_item, :data_movimentacao, :tipo_movimentacao, :localizacao)""")
                conexao.execute(query, {"id_doacao_item": rastreio.id_doacao_item, "data_movimentacao": rastreio.data_movimentacao, "tipo_movimentacao": rastreio.tipo_movimentacao, "localizacao": rastreio.localizacao})
                conexao.commit()
                conexao.close()
            except Exception as erro:
                print(f"Não foi possível realizar o cadastro.")
                return "Não foi possível realizar o cadastro"
            return "Rastreio cadastrado"
        else:
            return "Não foi possível conectar"
    
    def read(self, id):
        conexao = self.database.connect()
        if conexao:
            try:
                query = text ("""SELECT * FROM rastreios WHERE id = :id""")
                tupla = conexao.execute(query, {"id" : id}).first()
                if not tupla:
                    print("Dados não encontrados.")
                    raise FileNotFoundError
                else:
                    rastreio_objeto = {"id": tupla[0], "id_doacao_item": tupla[1], "data_movimentacao": tupla[2], "tipo_movimentacao": tupla[3], "localizacao": tupla[4]}
            except Exception as erro:
                print(f"Não foi possível realizar a consulta.")
                return "Não foi possível realizar a consulta"
            return rastreio_objeto
        else:
            return "Não foi possível conectar"

    def update(self, id, rastreio):
        conexao = self.database.connect()
        if conexao:
            try:
                query = text ('''UPDATE rastreios
                        SET id_doacao_item = :id_doacao_item, data_movimentacao = :data_movimentacao, tipo_movimentacao = :tipo_movimentacao, localizacao = :localizacao
                        WHERE id = :id''')
                conexao.execute (query, 
                                 {
                                "id_doacao_item": rastreio.id_doacao_item,
                                "data_movimentacao": rastreio.data_movimentacao,
                                "tipo_movimentacao": rastreio.tipo_movimentacao,
                                "localizacao": rastreio.localizacao,
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
                query = text("DELETE FROM rastreios WHERE id = :id")
                conexao.execute(query, {"id": id})
                conexao.commit()
                conexao.close()
                return "Rastreio deletado"
            except Exception as erro:
                print(f"Não foi possível realizar a exclusão.")
                return "Não foi possível deletar"
        else:
            return "Não foi possível conectar"

    def get_all(self):
        conexao = self.database.connect()
        if conexao:
            try:
                query = text("SELECT * FROM rastreios")
                resultados = conexao.execute(query).fetchall()
                return [{"id": tupla[0], "id_doacao_item": tupla[1], "data_movimentacao": tupla[2], "tipo_movimentacao": tupla[3], "localizacao": tupla[4]} for tupla in resultados]
            except Exception as erro:
                print(f"Não foi possível listar.")
                return []
            finally:
                conexao.close()
        return []

    def inactivate(self):
        pass