from fastapi import FastAPI
from database import engine, Base
import models
from routers import jogos, plataformas, avaliacoes
from tags import tags_metadata

app = FastAPI(
    title="Lion Games 🦁",
    description="Compre os jogos que vão aumentar a sua coleção e suas aventuras, e registre as suas avaliações.",
    version="1.0.0",
    openapi_tags=tags_metadata
)

Base.metadata.create_all(bind=engine)

app.include_router(jogos.router)
app.include_router(plataformas.router)
app.include_router(avaliacoes.router)

@app.get("/")
def raiz():
    return {"mensagem": "Lion Game está on!"}