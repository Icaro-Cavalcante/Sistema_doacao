from src.repositories.repository import Repo
from src.domain.pedidosAuxilio import PedidoAuxilio
from src.database.database import Database
from src.database.tables import Tabela
from sqlalchemy import text # Usamos text para escrever queries

db = Database()
tb = Tabela()

class RepoPedidoAuxilio(Repo):
    '''
    Classe que interaje com o Banco de Dados dos pedidos de auxílio
    '''
    def __init__(self, database, table):
        super().__init__(database, table)

    def create(self, pedido_auxilio):
        '''
        Recebe um objeto de pedido de auxílio e cadastra ele no banco de dados
        '''
        conexao = self.database.connect()
        if conexao:
            try: 
                query = text(""" INSERT INTO pedidos_auxilio (id_usuario, justificativa, data_pedido, status) VALUES (:id_usuario, :justificativa, :data_pedido, :status) ON CONFLICT (id) DO NOTHING """)

                conexao.execute(query, {"id_usuario": pedido_auxilio.id_usuario, "justificativa": pedido_auxilio.justificativa, "data_pedido": pedido_auxilio.data_pedido, "status": pedido_auxilio.status})

                conexao.commit()
                conexao.close()
            except Exception as erro:
                print(f"Não foi possível realizar o cadastro.")
            return "Pedido de auxílio cadastrado"
        else:
            return "Não foi possível conectar"
    
    def read(self, id):
        '''
        Recebe o ID de um pedido de auxílio e retorna um objeto com seus dados
        '''
        conexao = self.database.connect() # Estabelecendo conexão
        if conexao: # Se a conexão existir
            try: # Tratamento de erro
                query = text ("""SELECT * FROM pedidos_auxilio WHERE id = :id""") # Query - Pegando os dados do pedido com esse ID
                tupla = conexao.execute(query, {"id" : id}).first() # Executando a query e pegando o resultado
                if not tupla: # Se a tupla não for encontrada
                    print("Dados não encontrados.")
                    raise FileNotFoundError # Tratamento de erro
                else:
                    pedido_auxilio_objeto = PedidoAuxilio(tupla[1], tupla[2], tupla[3], tupla[4], tupla[0]) # Transformando a tupla em objeto
            except Exception as erro: # Tratamento de erro
                print(f"Não foi possível realizar a consulta.")
                return None
            return pedido_auxilio_objeto
        else: # A conexão não existiu
            return "Não foi possível conectar"

    def update(self, id, nome_atributo, atributo_update):
        '''
        Recebe o ID de um pedido de auxílio, o nome do atributo e o atributo atualizado e atualiza o atributo
        '''
        conexao = self.database.connect() # Estabelecendo a conexão
        if conexao: # Se a conexão existir
            try:
                query = text (f'''UPDATE pedidos_auxilio
                        SET {nome_atributo} = :atributo_update
                        WHERE id = :id''') # query
                conexao.execute (query, 
                                 {
                                "atributo_update": atributo_update,
                                "id": id })
                conexao.commit()
                conexao.close()
                return "Atributo atualizado"
            except Exception as erro: # Tratamento de erro
                print(f"Não foi possível realizar a consulta.")
                return None
        else:
            return "Não foi possível conectar"

    def inactivate(self):
        pass