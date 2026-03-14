class DoacaoItem():
    '''
    Classe responsável por definir padrão de doação de itens, 
    contendo os atributos id, id_doacao, itemId e quantidade.
    '''
    def __init__(self, id, id_doacao, itemId, quantidade):
        self.id = id
        self.id_doacao = id_doacao
        self.itemId = itemId
        self.quantidade = quantidade