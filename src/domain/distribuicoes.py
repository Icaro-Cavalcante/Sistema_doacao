class Distribuicao():
    """
    Classe responsável pelo mode de Distribuição dos itens.
    """

def __init__(self, id_pedido, id_doacao, user_cnpj, data_entrega, validacao_recebimento, id=None):
    self.id_pedido = id_pedido
    self.id_doacao = id_doacao
    self.user_cnpj = user_cnpj
    self.data_entrega = data_entrega
    self.validacao_recebimento = validacao_recebimento
    self.id = id