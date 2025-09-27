from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
import hashlib

from app.db.session import get_db
from app.models import Jurisprudence
from app.schemas import JurisprudenceResponse, JurisprudenceCreate, JurisSearchRequest
from app.api.auth import get_current_user

router = APIRouter()

def generate_juris_hash(juris_data: dict) -> str:
    """Gerar hash único para jurisprudência baseado em dados essenciais"""
    hash_data = f"{juris_data['tribunal']}_{juris_data['processo']}_{juris_data['data']}"
    return hashlib.sha256(hash_data.encode()).hexdigest()

@router.post("/scrape", response_model=JurisprudenceResponse)
async def scrape_jurisprudence(
    juris_data: JurisprudenceCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Verificar se já existe pelo hash
    hash_value = generate_juris_hash(juris_data.dict())
    
    result = await db.execute(select(Jurisprudence).where(Jurisprudence.hash == hash_value))
    existing_juris = result.scalars().first()
    if existing_juris:
        return existing_juris
    
    # Criar nova entrada de jurisprudência
    juris = Jurisprudence(
        **juris_data.dict(),
        hash=hash_value
    )
    
    db.add(juris)
    await db.commit()
    await db.refresh(juris)
    
    return juris

@router.get("/", response_model=List[JurisprudenceResponse])
async def list_jurisprudence(
    tribunal: Optional[str] = None,
    limit: int = 50,
    db: AsyncSession = Depends(get_db)
):
    query = select(Jurisprudence)
    
    if tribunal:
        query = query.where(Jurisprudence.tribunal == tribunal)
    
    query = query.limit(limit)
    
    result = await db.execute(query)
    juris_list = result.scalars().all()
    return juris_list

@router.post("/search", response_model=List[JurisprudenceResponse])
async def search_jurisprudence(
    search_request: JurisSearchRequest,
    db: AsyncSession = Depends(get_db)
):
    query = select(Jurisprudence)
    
    if search_request.tribunais:
        query = query.where(Jurisprudence.tribunal.in_(search_request.tribunais))
    
    if search_request.classes:
        # Assumindo que classes estão no metadata
        query = query.where(Jurisprudence.metadata["classe"].astext.in_(search_request.classes))
    
    if search_request.assuntos:
        query = query.where(Jurisprudence.metadata["assunto"].astext.in_(search_request.assuntos))
    
    if search_request.data_inicio:
        query = query.where(Jurisprudence.data >= search_request.data_inicio)
    
    if search_request.data_fim:
        query = query.where(Jurisprudence.data <= search_request.data_fim)
    
    query = query.limit(search_request.limit)
    
    result = await db.execute(query)
    juris_list = result.scalars().all()
    return juris_list

@router.get("/{juris_id}", response_model=JurisprudenceResponse)
async def get_jurisprudence(juris_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Jurisprudence).where(Jurisprudence.id == juris_id))
    juris = result.scalars().first()
    if not juris:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Jurisprudence not found"
        )
    return juris

@router.get("/tribunais/disponiveis")
async def get_available_tribunals(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Jurisprudence.tribunal).distinct())
    tribunais = result.scalars().all()
    return tribunais