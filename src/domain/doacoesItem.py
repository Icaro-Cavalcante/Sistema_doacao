class DoacaoItem():
    '''
    Classe responsável por definir padrão de doação de itens.
    '''
    def __init__(self, id_doacao, id_item, quantidade_utilizada, id=None):
        self.id_doacao = id_doacao
        self.id_item = id_item
        self.quantidade_utilizada = quantidade_utilizada
        self.id = id