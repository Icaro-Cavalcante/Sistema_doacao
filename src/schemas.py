from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional


# 1. USUÁRIOS E PERFIS

class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    login: str

class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr
    login: str
    data_cadastro: date
    class Config:
        from_attributes = True

class PessoaFisicaCreate(BaseModel):
    id_usuario: int
    user_cpf: str
    data_nascimento: Optional[date] = None

class PessoaFisicaResponse(PessoaFisicaCreate):
    class Config:
        from_attributes = True

class PessoaJuridicaCreate(BaseModel):
    id_usuario: int
    user_cnpj: str
    razao_social: str

class PessoaJuridicaResponse(PessoaJuridicaCreate):
    class Config:
        from_attributes = True

class BeneficiarioCreate(BaseModel):
    id_usuario: int
    data_cadastro_beneficiario: date

class BeneficiarioResponse(BeneficiarioCreate):
    class Config:
        from_attributes = True


# 2. INVENTÁRIO (CATEGORIAS E ITENS)

class ItensCategoriaCreate(BaseModel):
    nome_categoria: str
    descricao: str

class ItensCategoriaResponse(ItensCategoriaCreate):
    id: int
    class Config:
        from_attributes = True

class ItemCreate(BaseModel):
    id_categoria_item: int
    descricao: Optional[str] = None
    nome: str
    unidade_medida: Optional[str] = None

class ItemResponse(ItemCreate):
    id: int
    class Config:
        from_attributes = True


# 3. DOAÇÕES E RASTREIO

class DoacaoCreate(BaseModel):
    id_usuario: int
    data_doacao: date
    descricao: Optional[str] = None
    status_doacao: str

class DoacaoResponse(DoacaoCreate):
    id: int
    class Config:
        from_attributes = True

class DoacaoItemCreate(BaseModel):
    id_doacao: int
    id_item: int
    quantidade_utilizada: int

class DoacaoItemResponse(DoacaoItemCreate):
    id: int
    class Config:
        from_attributes = True

class RastreioCreate(BaseModel):
    id_doacao_item: int
    data_movimentacao: date
    tipo_movimentacao: str
    localizacao: Optional[str] = None

class RastreioResponse(RastreioCreate):
    id: int
    class Config:
        from_attributes = True


# 4. PEDIDOS E DISTRIBUIÇÃO

class PedidoAuxilioCreate(BaseModel):
    id_usuario: int
    justificativa: str
    data_pedido: date
    status: str

class PedidoAuxilioResponse(PedidoAuxilioCreate):
    id: int
    class Config:
        from_attributes = True

class DistribuicaoCreate(BaseModel):
    id_pedido_auxilio: int
    status: Optional[str] = None
    data_distribuicao: date

class DistribuicaoResponse(DistribuicaoCreate):
    id: int
    class Config:
        from_attributes = True

class DistribuicaoItemCreate(BaseModel):
    id_distribuicao: int
    id_item: int
    quantidade_utilizada: int

class DistribuicaoItemResponse(DistribuicaoItemCreate):
    class Config:
        from_attributes = True


# 5. VOLUNTARIADO

class VagasVoluntarioCreate(BaseModel):
    id_usuario: int
    titulo: str
    descricao: str
    data_inicio: date
    data_fim: date
    carga_horaria: Optional[str] = None
    quantidade_vagas: Optional[int] = None

class VagasVoluntarioResponse(VagasVoluntarioCreate):
    id: int
    class Config:
        from_attributes = True

class InscricaoCreate(BaseModel):
    id_vaga: int
    id_usuario: int
    status: str
    data_inscricao: date

class InscricaoResponse(InscricaoCreate):
    id: int
    class Config:
        from_attributes = True