from sqlalchemy import Column, Integer, String, Float, ForeignKey
from database import Base

# # Colunas
class Plataforma(Base):
    __tablename__ = "plataformas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)

class Jogo(Base):
    __tablename__ = "jogos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    genero = Column(String(100), nullable=False)
    preco = Column(Float, nullable=False, default=0.0)
    plataforma_id = Column(Integer, ForeignKey("plataformas.id"))
    avaliacao_id = Column(Integer, ForeignKey("avaliacoes.id"))


class Avaliacao(Base):
    __tablename__ = "avaliacoes"

    id = Column(Integer, primary_key=True, index=True)
    nota = Column(Float, min_length=0.0, max_length=5.0)
    comentario = Column(String(300))
    jogo_id = Column(Integer, ForeignKey("jogos.id"))
