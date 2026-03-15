class ItemCategoria:
    '''
    Classe que representa um item de categoria.
    '''
    def __init__(self, nome_categoria, descricao, id=None):
        self.nome_categoria = nome_categoria
        self.descricao = descricao
        self.id = id