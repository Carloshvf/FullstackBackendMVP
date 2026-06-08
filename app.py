from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Novel
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Novels API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(
    name="Documentação",
    description="Seleção de documentação: Swagger, Redoc ou RapiDoc",
)
novel_tag = Tag(
    name="Novel", description="Adição, visualização e remoção de novels à base"
)


@app.get("/", tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
    return redirect("/openapi")


@app.post(
    "/novel",
    tags=[novel_tag],
    responses={"200": NovelViewSchema, "409": ErrorSchema, "400": ErrorSchema},
)
def add_novel(body: NovelSchema):
    """Adiciona uma nova Novel à base de dados.

    Retorna uma representação da novel criada.
    """
    novel = Novel(
        titulo=body.titulo,
        autor=body.autor,
        genero=body.genero,
        sinopse=body.sinopse,
        score=body.score,
        ultimo_capitulo=body.ultimo_capitulo,
    )
    logger.debug(f"Adicionando novel de título: '{novel.titulo}'")
    try:
        session = Session()
        session.add(novel)
        session.commit()
        logger.debug(f"Adicionada novel de título: '{novel.titulo}'")
        return apresenta_novel(novel), 200

    except IntegrityError as e:
        error_msg = "Novel com mesmo título já salva na base :/"
        logger.warning(
            f"Erro ao adicionar novel '{novel.titulo}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        error_msg = "Não foi possível salvar nova novel :/"
        logger.warning(
            f"Erro ao adicionar novel '{novel.titulo}', {error_msg}")
        return {"message": error_msg}, 400


@app.get(
    "/novels",
    tags=[novel_tag],
    responses={"200": ListagemNovelsSchema, "404": ErrorSchema},
)
def get_novels():
    """Faz a busca por todas as Novels cadastradas.

    Retorna uma representação da listagem de novels.
    """
    logger.debug("Coletando novels")
    session = Session()
    novels = session.query(Novel).all()

    if not novels:
        return {"novels": []}, 200
    else:
        logger.debug(f"%d novels encontradas" % len(novels))
        return apresenta_novels(novels), 200


@app.get(
    "/novel", tags=[novel_tag], responses={"200": NovelViewSchema, "404": ErrorSchema}
)
def get_novel(query: NovelBuscaSchema):
    """Faz a busca por uma Novel a partir do título ou autor.

    Retorna uma representação da novel encontrada.
    """
    session = Session()

    if query.titulo:
        logger.debug(f"Coletando novel pelo título: '{query.titulo}'")
        novel = session.query(Novel).filter(
            Novel.titulo.ilike(f"%{query.titulo}%")).first()
    elif query.autor:
        logger.debug(f"Coletando novel pelo autor: '{query.autor}'")
        novel = session.query(Novel).filter(
            Novel.autor.ilike(f"%{query.autor}%")).first()
    else:
        return {"message": "Informe título ou autor para busca :/"}, 400

    if not novel:
        error_msg = "Novel não encontrada na base :/"
        logger.warning(f"Erro ao buscar novel, {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Novel encontrada: '{novel.titulo}'")
        return apresenta_novel(novel), 200


@app.delete(
    "/novel", tags=[novel_tag], responses={"200": NovelDelSchema, "404": ErrorSchema}
)
def del_novel(query: NovelBuscaSchema):
    """Deleta uma Novel a partir do id informado.

    Retorna uma mensagem de confirmação da remoção.
    """
    novel_id = query.id
    logger.debug(f"Deletando novel de id: '{novel_id}'")
    session = Session()

    novel = session.query(Novel).filter(Novel.id == novel_id).first()

    if not novel:
        error_msg = "Novel não encontrada na base :/"
        logger.warning(
            f"Erro ao deletar novel de id '{novel_id}', {error_msg}")
        return {"message": error_msg}, 404

    titulo = novel.titulo
    session.delete(novel)
    session.commit()

    logger.debug(f"Deletada novel '{titulo}'")
    return {"message": "Novel removida", "titulo": titulo}, 200


@app.patch('/novel', tags=[novel_tag], responses={"200": NovelViewSchema, "404": ErrorSchema, "400": ErrorSchema})
def update_novel(body: NovelUpdateSchema):
    """Atualiza o score e/ou último capítulo de uma novel.

    Retorna a representação da novel atualizada.
    """
    logger.debug(f"Atualizando novel de id: '{body.id}'")
    session = Session()

    novel = session.query(Novel).filter(Novel.id == body.id).first()

    if not novel:
        error_msg = "Novel não encontrada na base :/"
        logger.warning(
            f"Erro ao atualizar novel de id '{body.id}', {error_msg}")
        return {"message": error_msg}, 404

    if body.score is None and body.ultimo_capitulo is None:
        error_msg = "Informe score ou último capítulo para atualizar :/"
        logger.warning(
            f"Erro ao atualizar novel de id '{body.id}', {error_msg}")
        return {"message": error_msg}, 400

    if body.score is not None:
        novel.score = body.score
    if body.ultimo_capitulo is not None:
        novel.ultimo_capitulo = body.ultimo_capitulo

    session.commit()
    logger.debug(f"Novel '{novel.titulo}' atualizada com sucesso")
    return apresenta_novel(novel), 200
