class PessoaJuridca():
    '''
    Classe de modelo para pessoa juridica.
    '''
def __init__(self, user_cnpj,razao_social, id=None):
    self.user_cnpj = user_cnpj
    self.razao_social = razao_social
    self.id = id