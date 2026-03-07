from sqlalchemy import Table, String, Column, MetaData, Integer, Date, ForeignKey
from src.database.database import Database
database = Database()

class Tabela():
    '''
    A classe que organiza e cria as tabelas do banco de dados
    '''

    def __init__(self):
        self.metadata = MetaData() # Função para criar as tabelas

# <--------------------------------------------------Tabelas-------------------------------------------------->
             
            # Doações
        self.doacoes = Table('doacoes', self.metadata,
            Column('id', Integer, primary_key=True),
            Column('id_usuario', Integer, ForeignKey('usuarios.id'), nullable=False, unique=True),
            Column('data_registro', Date),
            Column('status', String(40)),
            Column('motivo_recusa', String(40))
        )

        self.doacaoItem = Table('doacaoItem', self.metadata,
            Column('id', Integer, primary_key=True),     
            Column('id_doacao', Integer, ForeignKey('doacoes.id'), nullable=False, unique=True),
            Column('')                                       
        )
            # Usuários
        self.usuarios = Table('usuarios', self.metadata,
            Column('id', Integer, primary_key=True),
            Column('nome', String(70)),
            Column('email', String(70)),
            Column('senha', String(70)),
            Column('endereco', String(70)),
            Column('status', String(40)),
            Column('identificador', String(40)), # CPF ou CNPJ
            Column('tipo_perfil', String(40))
        )

        self.pessoaJuridica = Table('PessoaJuridica', self.metadata,
            Column('id_usuario', Integer, primary_key=True),
            Column('identificador', Integer, ForeignKey('identificador.identificador'), nullable=False, unique=True),
            Column('razao_social', String(70))     
        )
            # Categoria
        self.categoriaItem = Table('pessoaFisica', self.metadata,
                                  
        )

        self.categoria = Table('categoria', self.metadata,
                                  
        )

            # Distribuição
        self.distribuicao = Table('distribuicao', self.metadata,
                                  
        )
        
        self.distribuicaoItem = Table('distribuicaoItem', self.metadata,
                                  
        )

        self.rastreio = Table('rastreio', self.metadata,
                                  
        )
           
            # Pedido de auxílio
        self.pedidoAuxilio = Table('categoria', self.metadata,
                                  
        )

            # Voluntariado
        self.vagaVoluntariado = Table('vagaVoluntariado', self.metadata,

        )
        
        self.inscricao = Table('inscricao', self.metadata,
                                  
        )

        
    def criar_tabelas(self, database):
        '''
        Cria as tabelas no banco de dados.
        '''

        self.metadata.create_all(database.session)