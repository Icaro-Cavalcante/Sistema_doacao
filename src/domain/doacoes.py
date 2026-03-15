class Doacao():
    '''
    A classe das doações
    '''
    def __init__(self, id_usuario, data_doacao, status_doacao, descricao=None, id=None):
        self.id_usuario = id_usuario
        self.data_doacao = data_doacao
        self.descricao = descricao
        self.status_doacao = status_doacao
        self.id = id