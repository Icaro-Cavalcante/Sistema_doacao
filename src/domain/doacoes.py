class Doacao():
    '''
    A classe das doações
    '''
    def __init__(self, id_usuario, data_doacao, motivo_recusa, status_atual, id=None):
        self.id_usuario = id_usuario
        self.data_doacao = data_doacao
        self.motivo_recusa = motivo_recusa
        self.status_atual = status_atual