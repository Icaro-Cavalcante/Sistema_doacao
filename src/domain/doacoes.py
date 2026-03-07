class Doacao():
    '''
    A classe das doações
    '''
    def __init__(self, id_usuario, data_registro, status, motivo_recusa, id=None):
        self.id_usuario = id_usuario
        self.data_registro = data_registro
        self.status = status
        self.motivo_recusa = motivo_recusa