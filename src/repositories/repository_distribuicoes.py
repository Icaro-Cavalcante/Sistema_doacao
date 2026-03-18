# src/repositories/repository_distribuicoes.py
from src.repositories.repository import Repo
from src.domain.distribuicoes import Distribuicao
from src.database.database import Database
from src.database.tables import Tabela
from sqlalchemy import text

db = Database()
tb = Tabela()

class RepoDistribuicao(Repo):
    def __init__(self, database, table):
        super().__init__(database, table)

    def create(self, distribuicao):
        conexao = self.database.connect()
        if conexao:
            try: 
                query = text(""" INSERT INTO distribuicoes (id_pedido_auxilio, status, data_distribuicao) VALUES (:id_pedido_auxilio, :status, :data_distribuicao)""")
                conexao.execute(query, {"id_pedido_auxilio": distribuicao.id_pedido_auxilio, "status": distribuicao.status, "data_distribuicao": distribuicao.data_distribuicao})
                conexao.commit()
                conexao.close()
            except Exception as erro:
                print(f"Não foi possível realizar o cadastro.")
                return "Não foi possível realizar o cadastro"
            return "Distribuição cadastrada"
        else:
            return "Não foi possível conectar"
    
    def read(self, id):
        conexao = self.database.connect()
        if conexao:
            try:
                query = text ("""SELECT * FROM distribuicoes WHERE id = :id""")
                tupla = conexao.execute(query, {"id" : id}).first()
                if not tupla:
                    print("Dados não encontrados.")
                    raise FileNotFoundError
                else:
                    dist_objeto = {"id": tupla[0], "id_pedido_auxilio": tupla[1], "status": tupla[2], "data_distribuicao": tupla[3]}
            except Exception as erro:
                print(f"Não foi possível realizar a consulta.")
                return "Não foi possível realizar a consulta"
            return dist_objeto
        else:
            return "Não foi possível conectar"

    def update(self, id, distribuicao):
        conexao = self.database.connect()
        if conexao:
            try:
                query = text ('''UPDATE distribuicoes
                        SET id_pedido_auxilio = :id_pedido_auxilio, status = :status, data_distribuicao = :data_distribuicao
                        WHERE id = :id''')
                conexao.execute (query, 
                                 {
                                "id_pedido_auxilio": distribuicao.id_pedido_auxilio,
                                "status": distribuicao.status,
                                "data_distribuicao": distribuicao.data_distribuicao,
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
                query = text("DELETE FROM distribuicoes WHERE id = :id")
                conexao.execute(query, {"id": id})
                conexao.commit()
                conexao.close()
                return "Distribuição deletada"
            except Exception as erro:
                print(f"Não foi possível realizar a exclusão.")
                return "Não foi possível deletar"
        else:
            return "Não foi possível conectar"

    def get_all(self):
        conexao = self.database.connect()
        if conexao:
            try:
                query = text("SELECT * FROM distribuicoes")
                resultados = conexao.execute(query).fetchall()
                return [{"id": tupla[0], "id_pedido_auxilio": tupla[1], "status": tupla[2], "data_distribuicao": tupla[3]} for tupla in resultados]
            except Exception as erro:
                print(f"Não foi possível listar.")
                return []
            finally:
                conexao.close()
        return []

    def get_all_distributions_with_details(self):
        return self.get_all()

    def get_full_distribution_report(self, id):
        return self.read(id)

    def inactivate(self):
        pass