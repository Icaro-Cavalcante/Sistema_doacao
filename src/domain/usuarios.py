class Usuario():
    '''
    Classe que representa o usuário no sistema.
    '''
    def __init__(self, nome, email, senha, login, data_cadastro, id=None):
            self.id = id
            self.nome = nome
            self.email = email
            self.senha = senha
            self.login = login
            self.data_cadastro = data_cadastro