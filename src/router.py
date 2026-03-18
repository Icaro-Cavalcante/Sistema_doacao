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


# 1. ATORES - USUÁRIOS E PERFIS

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

@router.put("/usuarios/{id_usuario}", tags=["1. Atores - Usuários"])
def atualizar_usuario(id_usuario: int, usuario_in: UsuarioCreate):
    atualizado = Usuario(
        nome=usuario_in.nome, email=usuario_in.email, senha=usuario_in.senha, 
        login=usuario_in.login, data_cadastro=date.today().strftime("%Y-%m-%d")
    )
    res = repo_usuario.update(id_usuario, atualizado)
    if "Não foi" in str(res): raise HTTPException(status_code=500, detail=str(res))
    return {"mensagem": "Usuário atualizado!"}

@router.delete("/usuarios/{id_usuario}", tags=["1. Atores - Usuários"])
def deletar_usuario(id_usuario: int):
    res = repo_usuario.delete(id_usuario)
    if "Não foi" in str(res): raise HTTPException(status_code=500, detail=str(res))
    return {"mensagem": "Usuário deletado!"}

@router.post("/pessoas-fisica/", status_code=201, tags=["1. Atores - Perfis"])
def vincular_pf(pf_in: PessoaFisicaCreate):
    data_nasc = pf_in.data_nascimento.strftime("%Y-%m-%d") if pf_in.data_nascimento else None
    nova_pf = PessoaFisica(id_usuario=pf_in.id_usuario, user_cpf=pf_in.user_cpf, data_nascimento=data_nasc)
    res = repo_pf.create(nova_pf)
    if "Não foi possível" in str(res): raise HTTPException(status_code=500, detail=str(res))
    return {"mensagem": "Pessoa Física vinculada!"}

@router.get("/pessoas-fisica/", tags=["1. Atores - Perfis"])
def listar_pf():
    return repo_pf.get_all()

@router.get("/pessoas-fisica/{id_pf}", tags=["1. Atores - Perfis"])
def buscar_pf(id_pf: int):
    pf = repo_pf.read(id_pf)
    if not pf or "Não foi possível" in str(pf): raise HTTPException(status_code=404, detail="Não encontrado")
    return pf

@router.put("/pessoas-fisica/{id_pf}", tags=["1. Atores - Perfis"])
def atualizar_pf(id_pf: int, pf_in: PessoaFisicaCreate):
    data_nasc = pf_in.data_nascimento.strftime("%Y-%m-%d") if pf_in.data_nascimento else None
    atualizada = PessoaFisica(id_usuario=pf_in.id_usuario, user_cpf=pf_in.user_cpf, data_nascimento=data_nasc)
    res = repo_pf.update(id_pf, atualizada)
    if "Não foi" in str(res): raise HTTPException(status_code=500, detail=str(res))
    return {"mensagem": "Pessoa Física atualizada!"}

@router.delete("/pessoas-fisica/{id_pf}", tags=["1. Atores - Perfis"])
def deletar_pf(id_pf: int):
    res = repo_pf.delete(id_pf)
    if "Não foi" in str(res): raise HTTPException(status_code=500, detail=str(res))
    return {"mensagem": "Pessoa Física deletada!"}

@router.post("/pessoas-juridica/", status_code=201, tags=["1. Atores - Perfis"])
def vincular_pj(pj_in: PessoaJuridicaCreate):
    nova_pj = PessoaJuridica(id_usuario=pj_in.id_usuario, user_cnpj=pj_in.user_cnpj, razao_social=pj_in.razao_social)
    res = repo_pj.create(nova_pj)
    if "Não foi possível" in str(res): raise HTTPException(status_code=500, detail=str(res))
    return {"mensagem": "Pessoa Jurídica vinculada!"}

@router.get("/pessoas-juridica/", tags=["1. Atores - Perfis"])
def listar_pj():
    return repo_pj.get_all()

@router.get("/pessoas-juridica/{id_pj}", tags=["1. Atores - Perfis"])
def buscar_pj(id_pj: int):
    pj = repo_pj.read(id_pj)
    if not pj or "Não foi possível" in str(pj): raise HTTPException(status_code=404, detail="Não encontrado")
    return pj

@router.put("/pessoas-juridica/{id_pj}", tags=["1. Atores - Perfis"])
def atualizar_pj(id_pj: int, pj_in: PessoaJuridicaCreate):
    atualizada = PessoaJuridica(id_usuario=pj_in.id_usuario, user_cnpj=pj_in.user_cnpj, razao_social=pj_in.razao_social)
    res = repo_pj.update(id_pj, atualizada)
    if "Não foi" in str(res): raise HTTPException(status_code=500, detail=str(res))
    return {"mensagem": "Pessoa Jurídica atualizada!"}

@router.delete("/pessoas-juridica/{id_pj}", tags=["1. Atores - Perfis"])
def deletar_pj(id_pj: int):
    res = repo_pj.delete(id_pj)
    if "Não foi" in str(res): raise HTTPException(status_code=500, detail=str(res))
    return {"mensagem": "Pessoa Jurídica deletada!"}

@router.post("/beneficiarios/", status_code=201, tags=["1. Atores - Perfis"])
def vincular_beneficiario(ben_in: BeneficiarioCreate):
    novo_ben = Beneficiario(id_usuario=ben_in.id_usuario, data_cadastro_beneficiario=ben_in.data_cadastro_beneficiario.strftime("%Y-%m-%d"))
    res = repo_benef.create(novo_ben)
    if "Não foi possível" in str(res): raise HTTPException(status_code=500, detail=str(res))
    return {"mensagem": "Beneficiário cadastrado!"}

@router.get("/beneficiarios/", tags=["1. Atores - Perfis"])
def listar_beneficiarios():
    return repo_benef.get_all()

@router.get("/beneficiarios/{id_ben}", tags=["1. Atores - Perfis"])
def buscar_beneficiario(id_ben: int):
    ben = repo_benef.read(id_ben)
    if not ben or "Não foi possível" in str(ben): raise HTTPException(status_code=404, detail="Não encontrado")
    return ben

@router.put("/beneficiarios/{id_ben}", tags=["1. Atores - Perfis"])
def atualizar_beneficiario(id_ben: int, ben_in: BeneficiarioCreate):
    atualizado = Beneficiario(id_usuario=ben_in.id_usuario, data_cadastro_beneficiario=ben_in.data_cadastro_beneficiario.strftime("%Y-%m-%d"))
    res = repo_benef.update(id_ben, atualizado)
    if "Não foi" in str(res): raise HTTPException(status_code=500, detail=str(res))
    return {"mensagem": "Beneficiário atualizado!"}

@router.delete("/beneficiarios/{id_ben}", tags=["1. Atores - Perfis"])
def deletar_beneficiario(id_ben: int):
    res = repo_benef.delete(id_ben)
    if "Não foi" in str(res): raise HTTPException(status_code=500, detail=str(res))
    return {"mensagem": "Beneficiário deletado!"}


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

@router.get("/categorias/{id_cat}", tags=["2. Inventário"])
def buscar_categoria(id_cat: int):
    cat = repo_categoria.read(id_cat)
    if not cat or "Não foi" in str(cat): raise HTTPException(status_code=404, detail="Não encontrado")
    return cat

@router.put("/categorias/{id_cat}", tags=["2. Inventário"])
def atualizar_categoria(id_cat: int, cat_in: ItensCategoriaCreate):
    atualizada = ItemCategoria(nome_categoria=cat_in.nome_categoria, descricao=cat_in.descricao)
    res = repo_categoria.update(id_cat, atualizada)
    if "Não foi" in str(res): raise HTTPException(status_code=500, detail=str(res))
    return {"mensagem": "Categoria atualizada!"}

@router.delete("/categorias/{id_cat}", tags=["2. Inventário"])
def deletar_categoria(id_cat: int):
    res = repo_categoria.delete(id_cat)
    if "Não foi" in str(res): raise HTTPException(status_code=500, detail=str(res))
    return {"mensagem": "Categoria deletada!"}

@router.post("/itens/", status_code=201, tags=["2. Inventário"])
def criar_item(item_in: ItemCreate):
    novo_item = Item(id_categoria_item=item_in.id_categoria_item, descricao=item_in.descricao, nome=item_in.nome, unidade_medida=item_in.unidade_medida)
    res = repo_item.create(novo_item)
    if "Não foi" in str(res): raise HTTPException(status_code=500, detail=str(res))
    return {"mensagem": "Item criado!"}

@router.get("/itens/", response_model=list[ItemResponse], tags=["2. Inventário"])
def listar_itens():
    return repo_item.get_all()

@router.get("/itens/{id_item}", tags=["2. Inventário"])
def buscar_item(id_item: int):
    item = repo_item.read(id_item)
    if not item or "Não foi" in str(item): raise HTTPException(status_code=404, detail="Não encontrado")
    return item

@router.put("/itens/{id_item}", tags=["2. Inventário"])
def atualizar_item(id_item: int, item_in: ItemCreate):
    atualizado = Item(id_categoria_item=item_in.id_categoria_item, descricao=item_in.descricao, nome=item_in.nome, unidade_medida=item_in.unidade_medida)
    res = repo_item.update(id_item, atualizado)
    if "Não foi" in str(res): raise HTTPException(status_code=500, detail=str(res))
    return {"mensagem": "Item atualizado!"}

@router.delete("/itens/{id_item}", tags=["2. Inventário"])
def deletar_item(id_item: int):
    res = repo_item.delete(id_item)
    if "Não foi" in str(res): raise HTTPException(status_code=500, detail=str(res))
    return {"mensagem": "Item deletado!"}


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

@router.get("/doacoes/{id_doacao}", tags=["3. Doações"])
def buscar_doacao(id_doacao: int):
    doacao = repo_doacao.read(id_doacao)
    if not doacao or "Não foi" in str(doacao): raise HTTPException(status_code=404, detail="Não encontrado")
    return doacao

@router.put("/doacoes/{id_doacao}", tags=["3. Doações"])
def atualizar_doacao(id_doacao: int, doacao_in: DoacaoCreate):
    atualizada = Doacao(id_usuario=doacao_in.id_usuario, data_doacao=doacao_in.data_doacao.strftime("%Y-%m-%d"), descricao=doacao_in.descricao, status_doacao=doacao_in.status_doacao)
    res = repo_doacao.update(id_doacao, atualizada)
    if "Não foi" in str(res): raise HTTPException(status_code=500, detail=str(res))
    return {"mensagem": "Doação atualizada!"}

@router.delete("/doacoes/{id_doacao}", tags=["3. Doações"])
def deletar_doacao(id_doacao: int):
    res = repo_doacao.delete(id_doacao)
    if "Não foi" in str(res): raise HTTPException(status_code=500, detail=str(res))
    return {"mensagem": "Doação deletada!"}

@router.post("/doacoes-item/", status_code=201, tags=["3. Doações"])
def adicionar_item_doacao(doacao_item_in: DoacaoItemCreate):
    novo_di = DoacaoItem(id_doacao=doacao_item_in.id_doacao, id_item=doacao_item_in.id_item, quantidade_utilizada=doacao_item_in.quantidade_utilizada)
    res = repo_doacao_item.create(novo_di)
    if "Não foi" in str(res): raise HTTPException(status_code=500, detail=str(res))
    return {"mensagem": "Item adicionado à doação!"}

@router.get("/doacoes-item/", tags=["3. Doações"])
def listar_doacao_itens():
    return repo_doacao_item.get_all()

@router.get("/doacoes-item/{id_di}", tags=["3. Doações"])
def buscar_doacao_item(id_di: int):
    di = repo_doacao_item.read(id_di)
    if not di or "Não foi" in str(di): raise HTTPException(status_code=404, detail="Não encontrado")
    return di

@router.put("/doacoes-item/{id_di}", tags=["3. Doações"])
def atualizar_doacao_item(id_di: int, di_in: DoacaoItemCreate):
    atualizado = DoacaoItem(id_doacao=di_in.id_doacao, id_item=di_in.id_item, quantidade_utilizada=di_in.quantidade_utilizada)
    res = repo_doacao_item.update(id_di, atualizado)
    if "Não foi" in str(res): raise HTTPException(status_code=500, detail=str(res))
    return {"mensagem": "Item da doação atualizado!"}

@router.delete("/doacoes-item/{id_di}", tags=["3. Doações"])
def deletar_doacao_item(id_di: int):
    res = repo_doacao_item.delete(id_di)
    if "Não foi" in str(res): raise HTTPException(status_code=500, detail=str(res))
    return {"mensagem": "Item da doação deletado!"}

@router.get("/doacoes/{id_doacao}/itens", tags=["3. Doações"])
def listar_itens_por_doacao(id_doacao: int):
    return repo_doacao_item.get_items_by_doacao_details(id_doacao)

@router.get("/doacoes/relatorio", tags=["3. Doações"])
def relatorio_por_categoria():
    return repo_doacao_item.get_total_donated_by_category()

@router.post("/rastreios/", status_code=201, tags=["3. Doações"])
def registrar_rastreio(rastreio_in: RastreioCreate):
    novo_rastreio = Rastreio(id_doacao_item=rastreio_in.id_doacao_item, data_movimentacao=rastreio_in.data_movimentacao.strftime("%Y-%m-%d"), tipo_movimentacao=rastreio_in.tipo_movimentacao, localizacao=rastreio_in.localizacao)
    res = repo_rastreio.create(novo_rastreio)
    if "Não foi" in str(res): raise HTTPException(status_code=500, detail=str(res))
    return {"mensagem": "Etapa de rastreio registrada!"}

@router.get("/rastreios/", tags=["3. Doações"])
def listar_rastreios():
    return repo_rastreio.get_all()

@router.get("/rastreios/{id_rastreio}", tags=["3. Doações"])
def buscar_rastreio(id_rastreio: int):
    rastreio = repo_rastreio.read(id_rastreio)
    if not rastreio or "Não foi" in str(rastreio): raise HTTPException(status_code=404, detail="Não encontrado")
    return rastreio

@router.put("/rastreios/{id_rastreio}", tags=["3. Doações"])
def atualizar_rastreio(id_rastreio: int, rastreio_in: RastreioCreate):
    atualizado = Rastreio(id_doacao_item=rastreio_in.id_doacao_item, data_movimentacao=rastreio_in.data_movimentacao.strftime("%Y-%m-%d"), tipo_movimentacao=rastreio_in.tipo_movimentacao, localizacao=rastreio_in.localizacao)
    res = repo_rastreio.update(id_rastreio, atualizado)
    if "Não foi" in str(res): raise HTTPException(status_code=500, detail=str(res))
    return {"mensagem": "Rastreio atualizado!"}

@router.delete("/rastreios/{id_rastreio}", tags=["3. Doações"])
def deletar_rastreio(id_rastreio: int):
    res = repo_rastreio.delete(id_rastreio)
    if "Não foi" in str(res): raise HTTPException(status_code=500, detail=str(res))
    return {"mensagem": "Rastreio deletado!"}


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

@router.get("/pedidos-auxilio/{id_pedido}", tags=["4. Saída e Distribuição"])
def buscar_pedido(id_pedido: int):
    pedido = repo_pedido.read(id_pedido)
    if not pedido or "Não foi" in str(pedido): raise HTTPException(status_code=404, detail="Não encontrado")
    return pedido

@router.put("/pedidos-auxilio/{id_pedido}", tags=["4. Saída e Distribuição"])
def atualizar_pedido(id_pedido: int, pedido_in: PedidoAuxilioCreate):
    atualizado = PedidoAuxilio(id_usuario=pedido_in.id_usuario, justificativa=pedido_in.justificativa, data_pedido=pedido_in.data_pedido.strftime("%Y-%m-%d"), status=pedido_in.status)
    res = repo_pedido.update(id_pedido, atualizado)
    if "Não foi" in str(res): raise HTTPException(status_code=500, detail=str(res))
    return {"mensagem": "Pedido atualizado!"}

@router.delete("/pedidos-auxilio/{id_pedido}", tags=["4. Saída e Distribuição"])
def deletar_pedido(id_pedido: int):
    res = repo_pedido.delete(id_pedido)
    if "Não foi" in str(res): raise HTTPException(status_code=500, detail=str(res))
    return {"mensagem": "Pedido deletado!"}

@router.post("/distribuicoes/", status_code=201, tags=["4. Saída e Distribuição"])
def registrar_distribuicao(dist_in: DistribuicaoCreate):
    nova_dist = Distribuicao(id_pedido_auxilio=dist_in.id_pedido_auxilio, status=dist_in.status, data_distribuicao=dist_in.data_distribuicao.strftime("%Y-%m-%d"))
    res = repo_dist.create(nova_dist)
    if "Não foi" in str(res): raise HTTPException(status_code=500, detail=str(res))
    return {"mensagem": "Distribuição registada!"}

@router.get("/distribuicoes/", tags=["4. Saída e Distribuição"])
def listar_distribuicoes():
    return repo_dist.get_all()

@router.get("/distribuicoes/{id_dist}", tags=["4. Saída e Distribuição"])
def buscar_distribuicao(id_dist: int):
    dist = repo_dist.read(id_dist)
    if not dist or "Não foi" in str(dist): raise HTTPException(status_code=404, detail="Não encontrado")
    return dist

@router.put("/distribuicoes/{id_dist}", tags=["4. Saída e Distribuição"])
def atualizar_distribuicao(id_dist: int, dist_in: DistribuicaoCreate):
    atualizada = Distribuicao(id_pedido_auxilio=dist_in.id_pedido_auxilio, status=dist_in.status, data_distribuicao=dist_in.data_distribuicao.strftime("%Y-%m-%d"))
    res = repo_dist.update(id_dist, atualizada)
    if "Não foi" in str(res): raise HTTPException(status_code=500, detail=str(res))
    return {"mensagem": "Distribuição atualizada!"}

@router.delete("/distribuicoes/{id_dist}", tags=["4. Saída e Distribuição"])
def deletar_distribuicao(id_dist: int):
    res = repo_dist.delete(id_dist)
    if "Não foi" in str(res): raise HTTPException(status_code=500, detail=str(res))
    return {"mensagem": "Distribuição deletada!"}

@router.get("/distribuicoes-detalhadas/", tags=["4. Saída e Distribuição"])
def listar_distribuicoes_detalhadas():
    return repo_dist.get_all_distributions_with_details()

@router.post("/distribuicoes-item/", status_code=201, tags=["4. Saída e Distribuição"])
def adicionar_item_distribuido(di_in: DistribuicaoItemCreate):
    novo_di = DistribuicaoItem(id_distribuicao=di_in.id_distribuicao, id_item=di_in.id_item, quantidade_utilizada=di_in.quantidade_utilizada)
    res = repo_dist_item.create(novo_di)
    if "Não foi" in str(res): raise HTTPException(status_code=500, detail=str(res))
    return {"mensagem": "Item adicionado à distribuição!"}

@router.get("/distribuicoes-item/", tags=["4. Saída e Distribuição"])
def listar_distribuicoes_item():
    return repo_dist_item.get_all()

@router.get("/distribuicoes-item/{id_di}", tags=["4. Saída e Distribuição"])
def buscar_distribuicao_item(id_di: int):
    di = repo_dist_item.read(id_di)
    if not di or "Não foi" in str(di): raise HTTPException(status_code=404, detail="Não encontrado")
    return di

@router.put("/distribuicoes-item/{id_di}", tags=["4. Saída e Distribuição"])
def atualizar_distribuicao_item(id_di: int, di_in: DistribuicaoItemCreate):
    atualizado = DistribuicaoItem(id_distribuicao=di_in.id_distribuicao, id_item=di_in.id_item, quantidade_utilizada=di_in.quantidade_utilizada)
    res = repo_dist_item.update(id_di, atualizado)
    if "Não foi" in str(res): raise HTTPException(status_code=500, detail=str(res))
    return {"mensagem": "Item da distribuição atualizado!"}

@router.delete("/distribuicoes-item/{id_di}", tags=["4. Saída e Distribuição"])
def deletar_distribuicao_item(id_di: int):
    res = repo_dist_item.delete(id_di)
    if "Não foi" in str(res): raise HTTPException(status_code=500, detail=str(res))
    return {"mensagem": "Item da distribuição deletado!"}

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

@router.get("/vagas-voluntario/{id_vaga}", tags=["5. Voluntariado"])
def buscar_vaga(id_vaga: int):
    vaga = repo_vaga.read(id_vaga)
    if not vaga or "Não foi" in str(vaga): raise HTTPException(status_code=404, detail="Não encontrado")
    return vaga

@router.put("/vagas-voluntario/{id_vaga}", tags=["5. Voluntariado"])
def atualizar_vaga(id_vaga: int, vaga_in: VagasVoluntarioCreate):
    atualizada = VagaVoluntariado(id_usuario=vaga_in.id_usuario, titulo=vaga_in.titulo, descricao=vaga_in.descricao, data_inicio=vaga_in.data_inicio.strftime("%Y-%m-%d"), data_fim=vaga_in.data_fim.strftime("%Y-%m-%d"), carga_horaria=vaga_in.carga_horaria, quantidade_vagas=vaga_in.quantidade_vagas)
    res = repo_vaga.update(id_vaga, atualizada)
    if "Não foi" in str(res): raise HTTPException(status_code=500, detail=str(res))
    return {"mensagem": "Vaga atualizada!"}

@router.delete("/vagas-voluntario/{id_vaga}", tags=["5. Voluntariado"])
def deletar_vaga(id_vaga: int):
    res = repo_vaga.delete(id_vaga)
    if "Não foi" in str(res): raise HTTPException(status_code=500, detail=str(res))
    return {"mensagem": "Vaga deletada!"}

@router.post("/inscricoes/", status_code=201, tags=["5. Voluntariado"])
def inscrever_voluntario(inscricao_in: InscricaoCreate):
    nova_insc = Inscricao(id_vaga=inscricao_in.id_vaga, id_usuario=inscricao_in.id_usuario, status=inscricao_in.status, data_inscricao=inscricao_in.data_inscricao.strftime("%Y-%m-%d"))
    res = repo_inscricao.create(nova_insc)
    if "Não foi" in str(res): raise HTTPException(status_code=500, detail=str(res))
    return {"mensagem": "Inscrição realizada!"}

@router.get("/inscricoes/", response_model=list[InscricaoResponse], tags=["5. Voluntariado"])
def listar_inscricoes():
    return repo_inscricao.get_all()

@router.get("/inscricoes/{id_insc}", tags=["5. Voluntariado"])
def buscar_inscricao(id_insc: int):
    insc = repo_inscricao.read(id_insc)
    if not insc or "Não foi" in str(insc): raise HTTPException(status_code=404, detail="Não encontrado")
    return insc

@router.put("/inscricoes/{id_insc}", tags=["5. Voluntariado"])
def atualizar_inscricao(id_insc: int, insc_in: InscricaoCreate):
    atualizada = Inscricao(id_vaga=insc_in.id_vaga, id_usuario=insc_in.id_usuario, status=insc_in.status, data_inscricao=insc_in.data_inscricao.strftime("%Y-%m-%d"))
    res = repo_inscricao.update(id_insc, atualizada)
    if "Não foi" in str(res): raise HTTPException(status_code=500, detail=str(res))
    return {"mensagem": "Inscrição atualizada!"}

@router.delete("/inscricoes/{id_insc}", tags=["5. Voluntariado"])
def deletar_inscricao(id_insc: int):
    res = repo_inscricao.delete(id_insc)
    if "Não foi" in str(res): raise HTTPException(status_code=500, detail=str(res))
    return {"mensagem": "Inscrição deletada!"}
