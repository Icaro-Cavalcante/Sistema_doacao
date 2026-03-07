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
        return self.session.connect()