class DistribuicaoItem():
    '''
    Classe que representa a distribuição de um item em um pedido.
    '''
    def __init__(self, item, quantidade):
        self.item = item
        self.quantidade_utilizada = quantidade