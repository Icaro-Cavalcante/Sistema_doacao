class DistribuicaoItem():
    '''
    Classe que representa a distribuição de um item em um pedido.
    '''
    def __init__(self, id_distribuicao, id_item, quantidade_utilizada):
        self.id_distribuicao = id_distribuicao
        self.id_item = id_item
        self.quantidade_utilizada = quantidade_utilizada