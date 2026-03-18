# src/repositories/repository_vagasVoluntariado.py
from src.repositories.repository import Repo
from src.domain.vagasVoluntariado import VagaVoluntariado
from src.database.database import Database
from src.database.tables import Tabela
from sqlalchemy import text

db = Database()
tb = Tabela()

class RepoVagaVoluntariado(Repo):
    '''
    Classe que interaje com o Banco de Dados das vagas de voluntariado
    '''
    def __init__(self, database, table):
        super().__init__(database, table)

    def create(self, vaga):
        conexao = self.database.connect()
        if conexao:
            try: 
                query = text(""" INSERT INTO vagas_voluntario (id_usuario, titulo, descricao, data_inicio, data_fim, carga_horaria, quantidade_vagas) VALUES (:id_usuario, :titulo, :descricao, :data_inicio, :data_fim, :carga_horaria, :quantidade_vagas)""")
                conexao.execute(query, {"id_usuario": vaga.id_usuario, "titulo": vaga.titulo, "descricao": vaga.descricao, "data_inicio": vaga.data_inicio, "data_fim": vaga.data_fim, "carga_horaria": vaga.carga_horaria, "quantidade_vagas": vaga.quantidade_vagas})
                conexao.commit()
                conexao.close()
            except Exception as erro:
                print(f"Não foi possível realizar o cadastro.")
                return "Não foi possível realizar o cadastro"
            return "Vaga cadastrada"
        else:
            return "Não foi possível conectar"
    
    def read(self, id):
        conexao = self.database.connect()
        if conexao:
            try:
                query = text ("""SELECT * FROM vagas_voluntario WHERE id = :id""")
                tupla = conexao.execute(query, {"id" : id}).first()
                if not tupla:
                    print("Dados não encontrados.")
                    raise FileNotFoundError
                else:
                    vaga_objeto = {"id": tupla[0], "id_usuario": tupla[1], "titulo": tupla[2], "descricao": tupla[3], "data_inicio": tupla[4], "data_fim": tupla[5], "carga_horaria": tupla[6], "quantidade_vagas": tupla[7]}
            except Exception as erro:
                print(f"Não foi possível realizar a consulta.")
                return "Não foi possível realizar a consulta"
            return vaga_objeto
        else:
            return "Não foi possível conectar"

    def update(self, id, vaga):
        conexao = self.database.connect()
        if conexao:
            try:
                query = text ('''UPDATE vagas_voluntario
                        SET id_usuario = :id_usuario, titulo = :titulo, descricao = :descricao, data_inicio = :data_inicio, data_fim = :data_fim, carga_horaria = :carga_horaria, quantidade_vagas = :quantidade_vagas
                        WHERE id = :id''')
                conexao.execute (query, 
                                 {
                                "id_usuario": vaga.id_usuario,
                                "titulo": vaga.titulo,
                                "descricao": vaga.descricao,
                                "data_inicio": vaga.data_inicio,
                                "data_fim": vaga.data_fim,
                                "carga_horaria": vaga.carga_horaria,
                                "quantidade_vagas": vaga.quantidade_vagas,
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
                query = text("DELETE FROM vagas_voluntario WHERE id = :id")
                conexao.execute(query, {"id": id})
                conexao.commit()
                conexao.close()
                return "Vaga deletada"
            except Exception as erro:
                print(f"Não foi possível realizar a exclusão.")
                return "Não foi possível deletar"
        else:
            return "Não foi possível conectar"

    def get_all(self):
        conexao = self.database.connect()
        if conexao:
            try:
                query = text("SELECT * FROM vagas_voluntario")
                resultados = conexao.execute(query).fetchall()
                return [{"id": tupla[0], "id_usuario": tupla[1], "titulo": tupla[2], "descricao": tupla[3], "data_inicio": tupla[4], "data_fim": tupla[5], "carga_horaria": tupla[6], "quantidade_vagas": tupla[7]} for tupla in resultados]
            except Exception as erro:
                print(f"Não foi possível listar.")
                return []
            finally:
                conexao.close()
        return []

    def inactivate(self):
        pass