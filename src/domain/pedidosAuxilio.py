class PedidoAuxilio:
    '''
    Classe que representa um pedido de auxílio.
    '''
    def __init__(self, id_usuario, justificativa, data_pedido, status, id=None):
        self.id_usuario = id_usuario
        self.justificativa = justificativa
        self.data_pedido = data_pedido
        self.status = status
        self.id = id