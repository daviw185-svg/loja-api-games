from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models import Plataforma as PlataformaModel
from tags import tags_metadata


router = APIRouter(prefix="/plataformas", tags=["Plataformas"])

class Plataforma(BaseModel):
    id: int
    nome: str

class PlataformaCreate(BaseModel):
    id: int
    nome: str

def get_or_404(plataforma_id: int, db: Session) -> Plataforma:
    p = db.query(Plataforma).filter(Plataforma.id == plataforma_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Plataforma não encontrada")
    return p

# Rota GET /plataforma
@router.get("/", 
            tags=['Plataformas'],
            summary='Todas os videogames listados.',
            description='Listar todas as plataformas registradas.', 
            responses={
                200: {'description': 'Busca concluída'},
            })
def listar(db: Session = Depends(get_db)):
    return db.query(PlataformaModel).all()

# Rota POST /auth/login
@router.post("/", 
            status_code=201, 
            tags=['Plataformas'],
            summary='Criação de plataforma',
            description='Criar uma plataforma de videogame', 
            responses={
                201: {'description': 'Plataforma criada'},
            })
def criar(dados: PlataformaCreate, db: Session = Depends(get_db)):
    novo = Plataforma(**dados.model_dump())
    dados_plataforma = novo.model_dump() 
    nova_plataforma_db = PlataformaModel(**dados_plataforma)
    db.add(nova_plataforma_db)
    db.commit()
    db.refresh(nova_plataforma_db)
    return nova_plataforma_db