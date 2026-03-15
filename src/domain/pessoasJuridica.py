class PessoaJuridica():
    '''
    Classe de modelo para pessoa jurídica.
    '''
    def __init__(self, id_usuario, user_cnpj, razao_social):
        self.id_usuario = id_usuario
        self.user_cnpj = user_cnpj
        self.razao_social = razao_social