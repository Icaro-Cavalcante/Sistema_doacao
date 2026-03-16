from src.repositories.repository import Repo
from src.domain.doacoesItem import DoacaoItem
from src.database.database import Database
from src.database.tables import Tabela
from sqlalchemy import text # Usamos text para escrever queries

db = Database() # Objeto do banco de dados
tb = Tabela() # Objeto da tabela

class RepoDoacoesItem(Repo): # Importando da classe pai para polimorfismo
    '''
    Classe que interaje com o Banco de Dados dos itens doação
    '''
    def __init__(self, database, table):
        super().__init__(database, table)

    def create(self, doacao_item):
        '''
        Recebe um objeto de doação item e cadastra ele no banco de dados
        '''
        conexao = self.database.connect() # Estabelecendo a conexão
        if conexao:
            try:
                query = text("""INSERT INTO doacoes_item (id_doacao, id_item, quantidade_utilizada)
                            VALUES (:id_doacao, :id_item, :quantidade_utilizada)""")
                conexao.execute(query, {
                    "id_doacao": doacao_item.id_doacao, 
                    "id_item": doacao_item.id_item, 
                    "quantidade_utilizada": doacao_item.quantidade_utilizada
                })
                conexao.commit()
                conexao.close()
                return "Item doação cadastrado"
            except Exception as erro:
                print(f"Erro ao cadastrar item doação: {erro}")
                return "Não foi possível realizar o cadastro"
        return "Não foi possível conectar"

    def get_items_by_doacao_details(self, id_doacao):
        """Consulta complexa com JOIN para listar detalhes dos itens de uma doação"""
        conexao = self.database.connect()
        if conexao:
            query = text("""
                SELECT i.nome, i.descricao, di.quantidade_utilizada, ic.nome_categoria
                FROM doacoes_item di
                JOIN itens i ON di.id_item = i.id
                JOIN itens_categoria ic ON i.id_categoria_item = ic.id
                WHERE di.id_doacao = :id_doacao
            """)
            result = conexao.execute(query, {"id_doacao": id_doacao}).fetchall()
            conexao.close()
            return result
        return None

    def get_total_donated_by_category(self):
        """Consulta complexa com JOIN e GROUP BY para relatório de categorias"""
        conexao = self.database.connect()
        if conexao:
            query = text("""
                SELECT ic.nome_categoria, SUM(di.quantidade_utilizada) as total
                FROM doacoes_item di
                JOIN itens i ON di.id_item = i.id
                JOIN itens_categoria ic ON i.id_categoria_item = ic.id
                GROUP BY ic.nome_categoria
            """)
            result = conexao.execute(query).fetchall()
            conexao.close()
            return result
        return None
        
    def read(self, id):
        '''
        Recebe o ID de um item de doação e retorna um objeto com seus dados
        '''
        conexao = self.database.connect() # Estabelecendo conexão
        if conexao: # Se a conexão existir
            try: # Tratamento de erro
                query = text ("""SELECT * FROM doacoes_item WHERE id = :id""") # Query - Pegando os dados do item de doação com esse ID
                tupla = conexao.execute(query, {"id" : id}).first() # Executando a query e pegando o resultado
                if not tupla: # Se a tupla não for encontrada
                    print("Dados não encontrados.")
                    raise FileNotFoundError # Tratamento de erro
                else:
                    doacao_item_objeto = DoacaoItem(tupla[1], tupla[2], tupla[3], tupla[0]) # Transformando a tupla em objeto
            except Exception as erro: # Tratamento de erro
                print(f"Não foi possível realizar a consulta.")
                return None
            return doacao_item_objeto
        else: # A conexão não existiu
            return "Não foi possível conectar"

    def update(self, id, nome_atributo, atributo_update):
        '''
        Recebe o ID de um item de doação, o nome do atributo e o atributo atualizado e atualiza o atributo
        '''
        conexao = self.database.connect() # Estabelecendo a conexão
        if conexao: # Se a conexão existir
            try:
                query = text (f'''UPDATE doacoes_item
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