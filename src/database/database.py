from sqlalchemy import create_engine
from src.config.db_config import DATABASE_URL, ECHO

class Database():
    '''
    A classe que estabelece a conexão com o banco de dados
    '''
    def __init__(self):
        self.session = create_engine(DATABASE_URL, echo=ECHO) # Conexão com o banco de dados

    def connect(self):
        '''Conectando com o banco de dados'''
        try:
            return self.session.connect()
        except Exception as erro:
            print(f"Não foi possível conectar ao Banco de dados\nErro: {erro}")
            return None