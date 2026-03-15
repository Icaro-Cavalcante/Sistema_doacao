class Item():
    '''
    Classe que representa um item da categoria.
    '''
    def __init__(self, id_categoria_item, nome, descricao=None, unidade_medida=None, id=None):
        self.id_categoria_item = id_categoria_item
        self.nome = nome
        self.descricao = descricao
        self.unidade_medida = unidade_medida
        self.id = id
    