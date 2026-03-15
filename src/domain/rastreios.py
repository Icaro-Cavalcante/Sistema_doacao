class Rastreio():
    '''
    Classe que representa modelo do rastreio.
    '''
    def __init__(self, id_doacao_item, data_movimentacao, tipo_movimentacao, localizacao=None, id=None):
        self.id_doacao_item = id_doacao_item
        self.data_movimentacao = data_movimentacao
        self.tipo_movimentacao = tipo_movimentacao
        self.localizacao = localizacao
        self.id = id