from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from database import get_db
from models import Avaliacao, Jogo
from tags import tags_metadata

router = APIRouter(prefix="/avaliacoes", tags=["Avaliações"])


class AvaliacaoCreate(BaseModel):
    nota: float = Field(..., ge=0.0, le=5.0)
    comentario: str
    jogo_id: int

def get_or_404(avaliacao_id: int, db: Session) -> Avaliacao:
    a = db.query(Avaliacao).filter(Avaliacao.id == avaliacao_id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Avaliação não encontrada")
    return a

@router.post("/", status_code=201)
def criar(dados: AvaliacaoCreate, db: Session = Depends(get_db)):
    # Valida produto
    jogo = db.query(Jogo).filter(Jogo.id == dados.jogo_id).first()
    if not jogo:
        raise HTTPException(status_code=422, detail="Avalie o jogo com números entre 0.0 e 5.0.")
    nova = Avaliacao(**dados.model_dump())
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova

@router.delete("/{avaliacoes_id}")
def deletar(avaliacao_id: int, db: Session = Depends(get_db)):
    a = get_or_404(avaliacao_id, db)
    db.delete(a)
    db.commit()
    return {"mensagem": f"Avaliação {avaliacao_id} removido"}

