from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database import get_db
from models import Jogo as JogoModel, Avaliacao, Plataforma
from tags import tags_metadata

router = APIRouter(prefix="/jogos", tags=["Jogos"])


class Jogo(BaseModel):
    nome: str
    genero: str
    preco: float 
    plataforma_id: int

class JogoCreate(BaseModel):
    nome: str
    genero: str
    preco: float 
    plataforma_id: int

class JogoUpdate(BaseModel):
    nome: Optional[str] = None
    genero: Optional[str] = None
    preco: Optional[float] = None
    plataforma_id: int

def get_or_404(produto_id: int, db: Session) -> Jogo:
    j = db.query(JogoModel).filter(JogoModel.id == produto_id).first()
    if not j:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")
    return j


@router.get("/", 
        tags=['Jogos'],
        summary='Lista de todos os jogos',
        description='Listar todos os jogos registrados', 
        responses={
            200: {'description': 'Listagem concluída'},
        })
def listar(db: Session = Depends(get_db)):
    return db.query(JogoModel).all()

@router.get("/{jogo_id}", 
            tags=['Jogos'],
            summary='Busca o jogo pelo ID',
            description='Digite o ID do jogo para encontrar suas informações', 
            responses={
                200: {'description': 'Busca concluída!'},
                404: {'description': 'Jogo não encontrado. Verifique se o ID está correto'},
            })
def buscar(jogo_id: int, db: Session = Depends(get_db)):
    return get_or_404(jogo_id, db)

@router.post("/", 
            status_code=201,
            tags=['Jogos'],
            summary='Registrar de Jogo',
            description='Registre um jogo com seu nome, gênero, preço e plataforma', 
            responses={
                201: {'description': 'Jogo criado e adicionado!'},
            })
def criar(dados: JogoCreate, db: Session = Depends(get_db)):
    novo = Jogo(**dados.model_dump())
    dados_jogo = novo.model_dump() 
    novo_jogo_db = JogoModel(**dados_jogo)
    if not Plataforma:
        raise HTTPException(status_code=404, detail='Plataforma não encontrada')
    db.add(novo_jogo_db)
    db.commit()
    db.refresh(novo_jogo_db)
    return novo_jogo_db


@router.put("/{jogo_id}",
            tags=['Jogos'],
            summary='Atualizar jogo',
            description='Atualize o jogo por inteiro', 
            responses={
                200: {'description': 'Atualização feita'},
                404: {'description': 'Jogo não encontrado. Verifique se o ID está correto'},
            })
def atualizar(jogo_id: int, dados: JogoUpdate, db: Session = Depends(get_db)):
    j = get_or_404(jogo_id, db)
    if dados.nome is not None: j.nome = dados.nome
    if dados.genero is not None: j.genero = dados.genero
    if dados.preco is not None: j.preco = dados.preco
    if dados.plataforma_id is not None: j.plataforma_id = dados.plataforma_id
    db.commit()
    db.refresh(j)
    return j

@router.delete("/{jogo_id}",
               tags=['Jogos'],
                summary='Excluir jogo',
                description='Digite o ID correto do jogo e confirme a exclusão', 
                responses={
                    200: {'description': 'Jogo excluído'},
                    404: {'description': 'Jogo não encontrado. Verifique se o ID está correto'},
                })
def deletar(jogo_id: int, db: Session = Depends(get_db)):
    j = get_or_404(jogo_id, db)
    db.delete(j)
    db.commit()
    return {"mensagem": f"Jogo {jogo_id} removido"}

@router.get("/{jogo_id}/avaliacoes",
            tags=['Avaliações'],
            summary='Avaliação do Jogo',
            description='Busca a avaliação registrado do jogo', 
            responses={
                200: {'description': 'Busca concluída'},
                404: {'description': 'Avaliação não encontrada. Verifique se o ID do jogo está correto'},
            })
def listar_notas(jogo_id: int, db: Session = Depends(get_db)):
    jogo = get_or_404 (jogo_id, db)
    return jogo.avaliacoes