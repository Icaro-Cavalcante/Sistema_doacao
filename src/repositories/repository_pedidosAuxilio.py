# src/repositories/repository_pedidosAuxilio.py
from src.repositories.repository import Repo
from src.domain.pedidosAuxilio import PedidoAuxilio
from src.database.database import Database
from src.database.tables import Tabela
from sqlalchemy import text

db = Database()
tb = Tabela()

class RepoPedidoAuxilio(Repo):
    '''
    Classe que interaje com o Banco de Dados dos pedidos de auxílio
    '''
    def __init__(self, database, table):
        super().__init__(database, table)

    def create(self, pedido):
        conexao = self.database.connect()
        if conexao:
            try: 
                query = text(""" INSERT INTO pedidos_auxilio (id_usuario, justificativa, data_pedido, status) VALUES (:id_usuario, :justificativa, :data_pedido, :status)""")
                conexao.execute(query, {"id_usuario": pedido.id_usuario, "justificativa": pedido.justificativa, "data_pedido": pedido.data_pedido, "status": pedido.status})
                conexao.commit()
                conexao.close()
            except Exception as erro:
                print(f"Não foi possível realizar o cadastro.")
                return "Não foi possível realizar o cadastro"
            return "Pedido cadastrado"
        else:
            return "Não foi possível conectar"
    
    def read(self, id):
        conexao = self.database.connect()
        if conexao:
            try:
                query = text ("""SELECT * FROM pedidos_auxilio WHERE id = :id""")
                tupla = conexao.execute(query, {"id" : id}).first()
                if not tupla:
                    print("Dados não encontrados.")
                    raise FileNotFoundError
                else:
                    pedido_objeto = {"id": tupla[0], "id_usuario": tupla[1], "justificativa": tupla[2], "data_pedido": tupla[3], "status": tupla[4]}
            except Exception as erro:
                print(f"Não foi possível realizar a consulta.")
                return "Não foi possível realizar a consulta"
            return pedido_objeto
        else:
            return "Não foi possível conectar"

    def update(self, id, pedido):
        conexao = self.database.connect()
        if conexao:
            try:
                query = text ('''UPDATE pedidos_auxilio
                        SET id_usuario = :id_usuario, justificativa = :justificativa, data_pedido = :data_pedido, status = :status
                        WHERE id = :id''')
                conexao.execute (query, 
                                 {
                                "id_usuario": pedido.id_usuario,
                                "justificativa": pedido.justificativa,
                                "data_pedido": pedido.data_pedido,
                                "status": pedido.status,
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
                query = text("DELETE FROM pedidos_auxilio WHERE id = :id")
                conexao.execute(query, {"id": id})
                conexao.commit()
                conexao.close()
                return "Pedido deletado"
            except Exception as erro:
                print(f"Não foi possível realizar a exclusão.")
                return "Não foi possível deletar"
        else:
            return "Não foi possível conectar"

    def get_all(self):
        conexao = self.database.connect()
        if conexao:
            try:
                query = text("SELECT * FROM pedidos_auxilio")
                resultados = conexao.execute(query).fetchall()
                return [{"id": tupla[0], "id_usuario": tupla[1], "justificativa": tupla[2], "data_pedido": tupla[3], "status": tupla[4]} for tupla in resultados]
            except Exception as erro:
                print(f"Não foi possível listar.")
                return []
            finally:
                conexao.close()
        return []

    def inactivate(self):
        pass