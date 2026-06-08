from sqlalchemy import Column, String, Integer, Float, DateTime
from datetime import datetime
from typing import Union

from model import Base


class Novel(Base):
    __tablename__ = 'novels'

    id = Column("pk_novel", Integer, primary_key=True)
    titulo = Column(String(140), unique=True)
    autor = Column(String(140))
    genero = Column(String(80), nullable=True)
    sinopse = Column(String(4000), nullable=True)
    score = Column(Float, nullable=True)
    ultimo_capitulo = Column(Integer, nullable=True)
    data_insercao = Column(DateTime, default=datetime.now())

    def __init__(self, titulo: str, autor: str,
                 genero: Union[str, None] = None,
                 sinopse: Union[str, None] = None,
                 score: Union[float, None] = None,
                 ultimo_capitulo: Union[int, None] = None,
                 data_insercao: Union[DateTime, None] = None):
        """
        Cria uma Novel

        Arguments:
            titulo: título da novel.
            autor: autor da novel.
            genero: gênero da novel.
            sinopse: sinopse da novel.
            score: nota dada à novel.
            ultimo_capitulo: último capítulo lido.
            data_insercao: data de quando a novel foi inserida à base.
        """
        self.titulo = titulo
        self.autor = autor
        self.genero = genero
        self.sinopse = sinopse
        self.score = score
        self.ultimo_capitulo = ultimo_capitulo

        if data_insercao:
            self.data_insercao = data_insercao
