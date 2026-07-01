from pydantic import BaseModel
from typing import Optional, List
from model.novel import Novel


class NovelSchema(BaseModel):
    """ Define como uma nova novel a ser inserida deve ser representada """
    titulo: str = "Sword Art Online"
    autor: str = "Reki Kawahara"
    genero: Optional[str] = "Ação"
    sinopse: Optional[str] = "Jogadores presos num RPG virtual."
    score: Optional[float] = 8.5
    ultimo_capitulo: Optional[int] = 143


class NovelBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca """
    titulo: Optional[str] = None
    autor: Optional[str] = None


class ListagemNovelsSchema(BaseModel):
    """ Define como uma listagem de novels será retornada """
    novels: List[NovelSchema]


class NovelDeleteSchema(BaseModel):
    """ Define como deve ser a estrutura para deletar uma novel """
    id: int


class NovelDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após remoção """
    message: str
    titulo: str


class NovelUpdateSchema(BaseModel):
    """ Define como deve ser a estrutura para atualização parcial de uma novel """
    id: int
    score: Optional[float] = None
    ultimo_capitulo: Optional[int] = None


class NovelViewSchema(BaseModel):
    """ Define como uma novel será retornada """
    id: int = 1
    titulo: str = "Sword Art Online"
    autor: str = "Reki Kawahara"
    genero: Optional[str] = "Ação"
    sinopse: Optional[str] = "Jogadores presos num RPG virtual."
    score: Optional[float] = 8.5
    ultimo_capitulo: Optional[int] = 143
    data_insercao: str = "2024-01-01 00:00:00"


def apresenta_novels(novels: List[Novel]):
    """ Retorna uma representação da listagem de novels """
    result = []
    for novel in novels:
        result.append({
            "id": novel.id,
            "titulo": novel.titulo,
            "autor": novel.autor,
            "genero": novel.genero,
            "sinopse": novel.sinopse,
            "score": novel.score,
            "ultimo_capitulo": novel.ultimo_capitulo,
            "data_insercao": novel.data_insercao.strftime("%Y-%m-%d %H:%M:%S") if novel.data_insercao else None,
        })
    return {"novels": result}


def apresenta_novel(novel: Novel):
    """ Retorna uma representação de uma novel """
    return {
        "id": novel.id,
        "titulo": novel.titulo,
        "autor": novel.autor,
        "genero": novel.genero,
        "sinopse": novel.sinopse,
        "score": novel.score,
        "ultimo_capitulo": novel.ultimo_capitulo,
        "data_insercao": novel.data_insercao.strftime("%Y-%m-%d %H:%M:%S") if novel.data_insercao else None,
    }
