from fastapi import APIRouter, HTTPException
from datetime import date, datetime, timedelta

import jwt
from pydantic import BaseModel

from src.database.database import Database
from src.database.tables import Tabela

from src.schemas import *

from src.domain.usuarios import Usuario
from src.domain.pessoasFisica import PessoaFisica
from src.domain.pessoasJuridica import PessoaJuridica
from src.domain.beneficiarios import Beneficiario
from src.domain.itensCategoria import ItemCategoria
from src.domain.itens import Item
from src.domain.doacoes import Doacao
from src.domain.doacoesItem import DoacaoItem
from src.domain.rastreios import Rastreio
from src.domain.pedidosAuxilio import PedidoAuxilio
from src.domain.distribuicoes import Distribuicao
from src.domain.distribuicoesItens import DistribuicaoItem
from src.domain.vagasVoluntariado import VagaVoluntariado
from src.domain.inscricoes import Inscricao

from src.repositories.repository_usuarios import RepoUsuario
from src.repositories.repository_pessoasFisica import RepoPessoaFisica
from src.repositories.repository_pessoasJuridica import RepoPessoaJuridica
from src.repositories.repository_beneficiarios import RepoBeneficiario
from src.repositories.repository_itensCategoria import RepoItemCategoria
from src.repositories.repository_itens import RepoItens
from src.repositories.repository_doacoes import RepoDoacao
from src.repositories.repository_doacoesItem import RepoDoacoesItem
from src.repositories.repository_rastreios import RepoRastreio
from src.repositories.repository_pedidosAuxilio import RepoPedidoAuxilio
from src.repositories.repository_distribuicoes import RepoDistribuicao
from src.repositories.repository_distribuicoesItens import RepoDistribuicaoItem
from src.repositories.repository_vagasVoluntariado import RepoVagaVoluntariado
from src.repositories.repository_inscricoes import RepoInscricoes

router = APIRouter()
db = Database()
tb = Tabela()

repo_usuario = RepoUsuario(db, tb)
repo_pf = RepoPessoaFisica(db, tb)
repo_pj = RepoPessoaJuridica(db, tb)
repo_benef = RepoBeneficiario(db, tb)
repo_categoria = RepoItemCategoria(db, tb)
repo_item = RepoItens(db, tb)
repo_doacao = RepoDoacao(db, tb)
repo_doacao_item = RepoDoacoesItem(db, tb)
repo_rastreio = RepoRastreio(db, tb)
repo_pedido = RepoPedidoAuxilio(db, tb)
repo_dist = RepoDistribuicao(db, tb)
repo_dist_item = RepoDistribuicaoItem(db, tb)
repo_vaga = RepoVagaVoluntariado(db, tb)
repo_inscricao = RepoInscricoes(db, tb)

SECRET_KEY = "chave_secreta"
ALGORITHM = "HS256"

class LoginRequest(BaseModel):
    login: str
    senha: str

@router.post("/login/", tags=["0. Autenticação"])
def fazer_login(dados_login: LoginRequest):
    usuario = repo_usuario.read_by_login(dados_login.login)
    
    if not usuario or usuario.senha != dados_login.senha:
        raise HTTPException(status_code=401, detail="Login ou senha incorretos")

    dados_token = {
        "sub": usuario.login, 
        "exp": datetime.utcnow() + timedelta(hours=2)
    }
    
    token = jwt.encode(dados_token, SECRET_KEY, algorithm=ALGORITHM)
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario": {
            "nome": usuario.nome,
            "login": usuario.login
        }
    }

@router.post("/usuarios/", status_code=201, tags=["1. Atores - Usuários"])
def cadastrar_usuario(usuario_in: UsuarioCreate):
    novo_usuario = Usuario(
        nome=usuario_in.nome, email=usuario_in.email, senha=usuario_in.senha, 
        login=usuario_in.login, data_cadastro=date.today().strftime("%Y-%m-%d")
    )
    res = repo_usuario.create(novo_usuario)
    if "Não foi possível" in str(res): raise HTTPException(status_code=500, detail=str(res))
    return {"mensagem": "Usuário criado!"}

@router.get("/usuarios/", response_model=list[UsuarioResponse], tags=["1. Atores - Usuários"])
def listar_usuarios():
    return repo_usuario.get_all()

@router.get("/usuarios/{id_usuario}", response_model=UsuarioResponse, tags=["1. Atores - Usuários"])
def buscar_usuario(id_usuario: int):
    user = repo_usuario.read(id_usuario)
    if not user or "Não foi possível" in str(user): raise HTTPException(status_code=404, detail="Não encontrado")
    return user

@router.post("/pessoas-fisica/", status_code=201, tags=["1. Atores - Perfis"])
def vincular_pf(pf_in: PessoaFisicaCreate):
    data_nasc = pf_in.data_nascimento.strftime("%Y-%m-%d") if pf_in.data_nascimento else None
    nova_pf = PessoaFisica(id_usuario=pf_in.id_usuario, user_cpf=pf_in.user_cpf, data_nascimento=data_nasc)
    res = repo_pf.create(nova_pf)
    if "Não foi possível" in str(res): raise HTTPException(status_code=500, detail=str(res))
    return {"mensagem": "Pessoa Física vinculada!"}

@router.post("/pessoas-juridica/", status_code=201, tags=["1. Atores - Perfis"])
def vincular_pj(pj_in: PessoaJuridicaCreate):
    nova_pj = PessoaJuridica(id_usuario=pj_in.id_usuario, user_cnpj=pj_in.user_cnpj, razao_social=pj_in.razao_social)
    res = repo_pj.create(nova_pj)
    if "Não foi possível" in str(res): raise HTTPException(status_code=500, detail=str(res))
    return {"mensagem": "Pessoa Jurídica vinculada!"}

@router.post("/beneficiarios/", status_code=201, tags=["1. Atores - Perfis"])
def vincular_beneficiario(ben_in: BeneficiarioCreate):
    novo_ben = Beneficiario(id_usuario=ben_in.id_usuario, data_cadastro_beneficiario=ben_in.data_cadastro_beneficiario.strftime("%Y-%m-%d"))
    res = repo_benef.create(novo_ben)
    if "Não foi possível" in str(res): raise HTTPException(status_code=500, detail=str(res))
    return {"mensagem": "Beneficiário cadastrado!"}


# 2. INVENTÁRIO (CATEGORIAS E ITENS)

@router.post("/categorias/", status_code=201, tags=["2. Inventário"])
def criar_categoria(cat_in: ItensCategoriaCreate):
    nova_cat = ItemCategoria(nome_categoria=cat_in.nome_categoria, descricao=cat_in.descricao)
    res = repo_categoria.create(nova_cat)
    if "Não foi" in str(res): raise HTTPException(status_code=500, detail=str(res))
    return {"mensagem": "Categoria criada!"}

@router.get("/categorias/", response_model=list[ItensCategoriaResponse], tags=["2. Inventário"])
def listar_categorias():
    return repo_categoria.get_all()

@router.post("/itens/", status_code=201, tags=["2. Inventário"])
def criar_item(item_in: ItemCreate):
    novo_item = Item(id_categoria_item=item_in.id_categoria_item, descricao=item_in.descricao, nome=item_in.nome, unidade_medida=item_in.unidade_medida)
    res = repo_item.create(novo_item)
    if "Não foi" in str(res): raise HTTPException(status_code=500, detail=str(res))
    return {"mensagem": "Item criado!"}

@router.get("/itens/", response_model=list[ItemResponse], tags=["2. Inventário"])
def listar_itens():
    return repo_item.get_all()


# 3. DOAÇÕES E RASTREIO

@router.post("/doacoes/", status_code=201, tags=["3. Doações"])
def registrar_doacao(doacao_in: DoacaoCreate):
    nova_doacao = Doacao(id_usuario=doacao_in.id_usuario, data_doacao=doacao_in.data_doacao.strftime("%Y-%m-%d"), descricao=doacao_in.descricao, status_doacao=doacao_in.status_doacao)
    res = repo_doacao.create(nova_doacao)
    if "Não foi" in str(res): raise HTTPException(status_code=500, detail=str(res))
    return {"mensagem": "Doação iniciada!"}

@router.get("/doacoes/", response_model=list[DoacaoResponse], tags=["3. Doações"])
def listar_doacoes():
    return repo_doacao.get_all()

@router.post("/doacoes-item/", status_code=201, tags=["3. Doações"])
def adicionar_item_doacao(doacao_item_in: DoacaoItemCreate):
    novo_di = DoacaoItem(id_doacao=doacao_item_in.id_doacao, id_item=doacao_item_in.id_item, quantidade_utilizada=doacao_item_in.quantidade_utilizada)
    res = repo_doacao_item.create(novo_di)
    if "Não foi" in str(res): raise HTTPException(status_code=500, detail=str(res))
    return {"mensagem": "Item adicionado à doação!"}

@router.get("/doacoes/relatorio", tags=["3. Doações"])
def relatorio_por_categoria():
    return repo_doacao_item.get_total_donated_by_category()

@router.post("/rastreios/", status_code=201, tags=["3. Doações"])
def registrar_rastreio(rastreio_in: RastreioCreate):
    novo_rastreio = Rastreio(id_doacao_item=rastreio_in.id_doacao_item, data_movimentacao=rastreio_in.data_movimentacao.strftime("%Y-%m-%d"), tipo_movimentacao=rastreio_in.tipo_movimentacao, localizacao=rastreio_in.localizacao)
    res = repo_rastreio.create(novo_rastreio)
    if "Não foi" in str(res): raise HTTPException(status_code=500, detail=str(res))
    return {"mensagem": "Etapa de rastreio registrada!"}


# 4. PEDIDOS E DISTRIBUIÇÃO

@router.post("/pedidos-auxilio/", status_code=201, tags=["4. Saída e Distribuição"])
def criar_pedido(pedido_in: PedidoAuxilioCreate):
    novo_pedido = PedidoAuxilio(id_usuario=pedido_in.id_usuario, justificativa=pedido_in.justificativa, data_pedido=pedido_in.data_pedido.strftime("%Y-%m-%d"), status=pedido_in.status)
    res = repo_pedido.create(novo_pedido)
    if "Não foi" in str(res): raise HTTPException(status_code=500, detail=str(res))
    return {"mensagem": "Pedido registrado!"}

@router.get("/pedidos-auxilio/", response_model=list[PedidoAuxilioResponse], tags=["4. Saída e Distribuição"])
def listar_pedidos():
    return repo_pedido.get_all()

@router.post("/distribuicoes/", status_code=201, tags=["4. Saída e Distribuição"])
def registrar_distribuicao(dist_in: DistribuicaoCreate):
    nova_dist = Distribuicao(id_pedido_auxilio=dist_in.id_pedido_auxilio, status=dist_in.status, data_distribuicao=dist_in.data_distribuicao.strftime("%Y-%m-%d"))
    res = repo_dist.create(nova_dist)
    if "Não foi" in str(res): raise HTTPException(status_code=500, detail=str(res))
    return {"mensagem": "Distribuição registada!"}

@router.post("/distribuicoes-item/", status_code=201, tags=["4. Saída e Distribuição"])
def adicionar_item_distribuido(di_in: DistribuicaoItemCreate):
    novo_di = DistribuicaoItem(id_distribuicao=di_in.id_distribuicao, id_item=di_in.id_item, quantidade_utilizada=di_in.quantidade_utilizada)
    res = repo_dist_item.create(novo_di)
    if "Não foi" in str(res): raise HTTPException(status_code=500, detail=str(res))
    return {"mensagem": "Item adicionado à distribuição!"}

@router.get("/distribuicoes/relatorio/{id}", tags=["4. Saída e Distribuição"])
def relatorio_distribuicao_detalhado(id: int):
    return repo_dist.get_full_distribution_report(id)


# 5. VOLUNTARIADO

@router.post("/vagas-voluntario/", status_code=201, tags=["5. Voluntariado"])
def criar_vaga(vaga_in: VagasVoluntarioCreate):
    nova_vaga = VagaVoluntariado(id_usuario=vaga_in.id_usuario, titulo=vaga_in.titulo, descricao=vaga_in.descricao, data_inicio=vaga_in.data_inicio.strftime("%Y-%m-%d"), data_fim=vaga_in.data_fim.strftime("%Y-%m-%d"), carga_horaria=vaga_in.carga_horaria, quantidade_vagas=vaga_in.quantidade_vagas)
    res = repo_vaga.create(nova_vaga)
    if "Não foi" in str(res): raise HTTPException(status_code=500, detail=str(res))
    return {"mensagem": "Vaga criada!"}

@router.get("/vagas-voluntario/", response_model=list[VagasVoluntarioResponse], tags=["5. Voluntariado"])
def listar_vagas():
    return repo_vaga.get_all()

@router.post("/inscricoes/", status_code=201, tags=["5. Voluntariado"])
def inscrever_voluntario(inscricao_in: InscricaoCreate):
    nova_insc = Inscricao(id_vaga=inscricao_in.id_vaga, id_usuario=inscricao_in.id_usuario, status=inscricao_in.status, data_inscricao=inscricao_in.data_inscricao.strftime("%Y-%m-%d"))
    res = repo_inscricao.create(nova_insc)
    if "Não foi" in str(res): raise HTTPException(status_code=500, detail=str(res))
    return {"mensagem": "Inscrição realizada!"}

@router.get("/inscricoes/", response_model=list[InscricaoResponse], tags=["5. Voluntariado"])
def listar_inscricoes():
    return repo_inscricao.get_all()