from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator
import logging

from app.core.config import settings
from app.db.session import async_session
from app.api import auth, units, documents, cases, rag, juris, drafts, templates, checklists, audit

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Assessor Jurídico - Poder Judiciário",
    description="Sistema de geração de minutas jurídicas com RAG",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Dependency para sessão do banco
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

# Rotas
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(units.router, prefix="/units", tags=["units"])
app.include_router(documents.router, prefix="/documents", tags=["documents"])
app.include_router(cases.router, prefix="/cases", tags=["cases"])
app.include_router(rag.router, prefix="/rag", tags=["rag"])
app.include_router(juris.router, prefix="/juris", tags=["juris"])
app.include_router(drafts.router, prefix="/drafts", tags=["drafts"])
app.include_router(templates.router, prefix="/templates", tags=["templates"])
app.include_router(checklists.router, prefix="/checklists", tags=["checklists"])
app.include_router(audit.router, prefix="/audit", tags=["audit"])

@app.get("/")
async def root():
    return {"message": "Assessor Jurídico API - Poder Judiciário"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)