class PessoaFisica:
    '''
    Classe que representa uma pessoa física.
    '''
    def __init__(self, id_usuario, user_cpf, data_nascimento=None):
        self.id_usuario = id_usuario
        self.user_cpf = user_cpf
        self.data_nascimento = data_nascimento