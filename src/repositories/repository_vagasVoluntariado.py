from src.repositories.repository import Repo
from src.domain.vagasVoluntariado import VagaVoluntariado
from src.database.database import Database
from src.database.tables import Tabela
from sqlalchemy import text # Usamos text para escrever queries

db = Database()
tb = Tabela()

class RepoVagaVoluntariado(Repo):
    '''
    Classe que interaje com o Banco de Dados das vagas de voluntariado
    '''
    def __init__(self, database, table):
        super().__init__(database, table)

    def create(self, vaga_voluntariado):
        '''
        Recebe um objeto de vaga de voluntariado e cadastra ele no banco de dados
        '''
        conexao = self.database.connect()
        if conexao:
            try: 
                query = text(""" INSERT INTO vagas_voluntario (id_usuario, titulo, descricao, data_inicio, data_fim, carga_horaria, quantidade_vagas) VALUES (:id_usuario, :titulo, :descricao, :data_inicio, :data_fim, :carga_horaria, :quantidade_vagas) ON CONFLICT (id) DO NOTHING """)

                conexao.execute(query, {"id_usuario": vaga_voluntariado.id_usuario, "titulo": vaga_voluntariado.titulo, "descricao": vaga_voluntariado.descricao, "data_inicio": vaga_voluntariado.data_inicio, "data_fim": vaga_voluntariado.data_fim, "carga_horaria": vaga_voluntariado.carga_horaria, "quantidade_vagas": vaga_voluntariado.quantidade_vagas})

                conexao.commit()
                conexao.close()
            except Exception as erro:
                print(f"Não foi possível realizar o cadastro.")
            return "Vaga de voluntariado cadastrada"
        else:
            return "Não foi possível conectar"
    
    def read(self, id):
        '''
        Recebe o ID de uma vaga de voluntariado e retorna um objeto com seus dados
        '''
        conexao = self.database.connect() # Estabelecendo conexão
        if conexao: # Se a conexão existir
            try: # Tratamento de erro
                query = text ("""SELECT * FROM vagas_voluntario WHERE id = :id""") # Query - Pegando os dados da vaga com esse ID
                tupla = conexao.execute(query, {"id" : id}).first() # Executando a query e pegando o resultado
                if not tupla: # Se a tupla não for encontrada
                    print("Dados não encontrados.")
                    raise FileNotFoundError # Tratamento de erro
                else:
                    vaga_voluntariado_objeto = VagaVoluntariado(tupla[1], tupla[2], tupla[3], tupla[4], tupla[5], tupla[6], tupla[7], tupla[0]) # Transformando a tupla em objeto
            except Exception as erro: # Tratamento de erro
                print(f"Não foi possível realizar a consulta.")
                return None
            return vaga_voluntariado_objeto
        else: # A conexão não existiu
            return "Não foi possível conectar"

    def update(self, id, nome_atributo, atributo_update):
        '''
        Recebe o ID de uma vaga de voluntariado, o nome do atributo e o atributo atualizado e atualiza o atributo
        '''
        conexao = self.database.connect() # Estabelecendo a conexão
        if conexao: # Se a conexão existir
            try:
                query = text (f'''UPDATE vagas_voluntario
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