from sqlalchemy import Table, String, Column, MetaData, Integer, Date, ForeignKey, Boolean
from datetime import date
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
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('id_usuario', Integer, ForeignKey('usuarios.id'), nullable=False),
            Column('data_doacao', Date, nullable=False),
            Column('descricao', String(255)),
            Column('status_doacao', String(40), nullable=False)
        )

        self.doacoesItem = Table('doacoesItem', self.metadata,
            Column('id', Integer, primary_key=True),
            Column('id_doacao', Integer, ForeignKey('doacoes.id')),
            Column('id_item', Integer, ForeignKey('itens.id')),
            Column('quantidade_utilizada', Integer, nullable=False)
        ) 

            # Usuários
        self.usuarios = Table('usuarios', self.metadata,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('nome', String(70)),
            Column('email', String(70), unique=True),
            Column('senha', String(70)),
            Column('login', String(70), unique=True),
            Column('data_cadastro', String(40)),
        )

        self.pessoasFisica = Table('pessoaFisica', self.metadata,
            Column('id_usuario', Integer, ForeignKey('usuarios.id'), primary_key=True),
            Column('user_cpf', String(11), unique=True, nullable=False),
            Column('data_nascimento', Date)
        )

        self.pessoasJuridica = Table('pessoasJuridica', self.metadata,
            Column('id_usuario', Integer, ForeignKey('usuarios.id'), primary_key=True),
            Column('user_cnpj', String(14), unique=True, nullable=False),
            Column('razao_social', String(100), nullable=False)
        )

            # Categoria
        self.itensCategoria = Table('itensCategoria', self.metadata,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('nome_categoria', String(50), unique=True, nullable=False),
            Column('descricao', String(50), unique=True, nullable=False)
        )

            # Itens
        self.itens = Table('itens', self.metadata,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('id_categoria_item', Integer, ForeignKey('itensCategoria.id')),
            Column('descricao', String(255)),
            Column('nome', String(255)),
            Column('unidade_medida', String(50))
        ) 

            # Distribuição
        self.distribuicoes = Table('distribuicoes', self.metadata,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('id_pedido_auxilio', Integer, ForeignKey('pedidosAuxilio.id')),
            Column('status', String(50)),
            Column('data_distribuicao', Date, nullable=False)
        )
        
        self.distribuicoesItem = Table('distribuicoesItem', self.metadata,
            Column('id_distribuicao', Integer, ForeignKey('distribuicoes.id'), primary_key=True),
            Column('id_item', Integer, ForeignKey('itens.id'), primary_key=True),
            Column('quantidade_utlizada', Integer, nullable=False)
        )

        self.rastreios = Table('rastreios', self.metadata,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('id_doacao_item', Integer, ForeignKey('doacoesItem.id'), nullable=False),
            Column('data_movimentacao', Date, nullable=False),
            Column('tipo_movimentação', String(100), nullable=False),
            Column('localizacao', String(100)) 
        )   
           
            # Pedido de auxílio
        self.pedidosAuxilio = Table('pedidosAuxilio', self.metadata,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('id_usuario', Integer, ForeignKey('usuarios.id'), nullable=False),
            Column('justificativa', String(500), nullable=False),
            Column('data_pedido', Date, nullable=False),
            Column('status', String(40), nullable=False)
        )

            # Voluntariado
        self.vagasVoluntario = Table('vagasVoluntario', self.metadata,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('id_usuario', Integer, ForeignKey('usuarios.id'), nullable=False),
            Column('titulo', String(100), nullable=False),
            Column('descricao', String(500), nullable=False),
            Column('data_inicio', Date, nullable=False),
            Column('data_fim', Date, nullable=False),
            Column('carga_horaria', String(50)),
            Column('quantidade_vagas', Integer),
        )
        
        self.inscricoes = Table('inscricoes', self.metadata,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('id_vaga', Integer, ForeignKey('vagasVoluntario.id'), nullable=False),
            Column('id_usuario', Integer, ForeignKey('usuarios.id'), nullable=False),
            Column('status', String(40), nullable=False),
            Column('data_inscricao', Date, nullable=False)
        )

        self.beneficiarios = Table('beneficiarios', self.metadata,
            Column('id_usuario', Integer, ForeignKey('usuarios.id'), nullable=False),
            Column('data_cadastro_beneficiario', Date, nullable=False)
        )

        
    def criar_tabelas(self, database):
        '''
        Cria as tabelas no banco de dados.
        '''

        self.metadata.create_all(database.session)