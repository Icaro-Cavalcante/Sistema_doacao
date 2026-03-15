class Inscricao():
    '''
    Classe que representa uma inscrição em uma vaga de voluntariado.
    '''
    def __init__(self, id_vaga, id_usuario, status, data_inscricao, id=None):
        self.id_vaga = id_vaga
        self.id_usuario = id_usuario
        self.status = status
        self.data_inscricao = data_inscricao
        self.id = id  