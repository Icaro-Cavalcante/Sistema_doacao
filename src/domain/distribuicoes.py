class Distribuicao():
    """
    Classe responsável pela distribuição dos itens.
    """
    def __init__(self, id_pedido_auxilio, data_distribuicao, status=None, id=None):
        self.id_pedido_auxilio = id_pedido_auxilio
        self.status = status
        self.data_distribuicao = data_distribuicao
        self.id = id