class VagaVoluntariado():
    '''
    Classe que representa uma vaga de voluntariado.
    '''
    def __init__(self, id_usuario, titulo, descricao, data_inicio, data_fim, carga_horaria=None, quantidade_vagas=None, id=None):
        self.id_usuario = id_usuario
        self.titulo = titulo
        self.descricao = descricao
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.carga_horaria = carga_horaria
        self.quantidade_vagas = quantidade_vagas
        self.id = id