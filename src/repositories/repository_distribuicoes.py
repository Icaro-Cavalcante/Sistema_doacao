from src.repositories.repository import Repo
from src.domain.distribuicoes import Distribuicao
from src.database.database import Database
from src.database.tables import Tabela
from sqlalchemy import text # Usamos text para escrever queries

db = Database() # Objeto do banco de dados
tb = Tabela() # Objeto da tabela

class RepoDistribuicao(Repo): # Importando da classe pai para polimorfismo
    '''
    Classe que interaje com o Banco de Dados das distribuições
    '''
    def __init__(self, database, table):
        super().__init__(database, table)

    def create(self, distribuicao):
        '''
        Recebe um objeto de distribuição e cadastra ele no banco de dados
        '''
        conexao = self.database.connect() # Estabelecendo a conexão
        if conexao: # Se a conexão existir
            try: # Tratamento de erro
                query = text ("""INSERT INTO distribuicoes (id_pedido_auxilio, data_distribuicao, status)
                            VALUES (:id_pedido_auxilio, :data_distribuicao, :status)
                            ON CONFLICT (id) DO NOTHING""") # Escreve a query
                conexao.execute(query, {"id_pedido_auxilio" : distribuicao.id_pedido_auxilio, "data_distribuicao" : distribuicao.data_distribuicao, "status" : distribuicao.status}) #Executa a query
                conexao.commit() # Salva as alterações no banco de dados
                conexao.close() # Fecha a conexão
            except Exception as erro: # Tratamento de erro
                print(f"Não foi possível realizar o cadastro.")
            return "Distribuição cadastrada"
        else: # A conexão não existiu
            return "Não foi possível conectar"
        
    def get_full_distribution_report(self, id_distribuicao):
        """
        Consulta complexa com múltiplos JOINs para relatório completo de distribuição
        """
        conexao = self.database.connect()
        if conexao:
            query = text("""
                SELECT d.id, d.data_distribuicao, u.nome as beneficiario, 
                       i.nome as item, di.quantidade_utilizada, pa.justificativa
                FROM distribuicoes d
                JOIN pedidos_auxilio pa ON d.id_pedido_auxilio = pa.id
                JOIN usuarios u ON pa.id_usuario = u.id
                JOIN distribuicoes_item di ON d.id = di.id_distribuicao
                JOIN itens i ON di.id_item = i.id
                WHERE d.id = :id_distribuicao
            """)
            result = conexao.execute(query, {"id_distribuicao": id_distribuicao}).fetchall()
            conexao.close()
            return result
        return None

    def get_all_distributions_with_details(self):
        """Consulta complexa com múltiplos JOINs para listar todas as distribuições"""
        conexao = self.database.connect()
        if conexao:
            query = text("""
                SELECT d.id, d.data_distribuicao, u.nome as beneficiario, 
                       pa.status as status_pedido, COUNT(di.id_item) as total_itens
                FROM distribuicoes d
                LEFT JOIN pedidos_auxilio pa ON d.id_pedido_auxilio = pa.id
                LEFT JOIN usuarios u ON pa.id_usuario = u.id
                LEFT JOIN distribuicoes_item di ON d.id = di.id_distribuicao
                GROUP BY d.id, d.data_distribuicao, u.nome, pa.status
                ORDER BY d.data_distribuicao DESC
            """)
            result = conexao.execute(query).fetchall()
            conexao.close()
            return result
        return None
        
    def read(self, id):
        '''
        Recebe o ID de uma distribuição e retorna um objeto com seus dados
        '''
        conexao = self.database.connect() # Estabelecendo conexão
        if conexao: # Se a conexão existir
            try: # Tratamento de erro
                query = text ("""SELECT * FROM distribuicoes WHERE id = :id""") # Query - Pegando os dados da distribuição com esse ID
                tupla = conexao.execute(query, {"id" : id}).first() # Executando a query e pegando o resultado
                if not tupla: # Se a tupla não for encontrada
                    print("Dados não encontrados.")
                    raise FileNotFoundError # Tratamento de erro
                else:
                    distribuicao_objeto = Distribuicao(tupla[1], tupla[2], tupla[3], tupla[0]) # Transformando a tupla em objeto
            except Exception as erro: # Tratamento de erro
                print(f"Não foi possível realizar a consulta.")
                return None
            return distribuicao_objeto
        else: # A conexão não existiu
            return "Não foi possível conectar"

    def update(self, id, nome_atributo, atributo_update):
        '''
        Recebe o ID de uma distribuição, o nome do atributo e o atributo atualizado e atualiza o atributo
        '''
        conexao = self.database.connect() # Estabelecendo a conexão
        if conexao: # Se a conexão existir
            try:
                query = text (f'''UPDATE distribuicoes
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





