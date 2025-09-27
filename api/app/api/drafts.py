from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
import uuid

from app.db.session import get_db
from app.models import Minuta, Case, User
from app.schemas import MinutaResponse, MinutaCreate, MinutaGenerationRequest, MinutaGenerationResponse
from app.api.auth import get_current_user
from app.api.rag import hybrid_search

router = APIRouter()

async def generate_minuta_content(case_id: str, tipo_ato: str, db: AsyncSession) -> str:
    """Gerar conteúdo da minuta usando RAG e modelos de IA"""
    # Buscar informações do caso
    result = await db.execute(select(Case).where(Case.id == case_id))
    case = result.scalars().first()
    
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found"
        )
    
    # Buscar informações relevantes usando RAG
    search_request = {
        "query": f"{case.classe} {case.assunto} {tipo_ato}",
        "scope": "case",
        "case_id": case_id,
        "limit": 10
    }
    
    relevant_info = await hybrid_search(search_request, None, db)
    
    # Simular geração de conteúdo com IA
    # Em produção, integraríamos com OpenAI ou outro provedor LLM
    content = f"""# {tipo_ato.upper()} - Processo {case.numero}

## RELATÓRIO

Processo: {case.numero}
Classe: {case.classe}
Assunto: {case.assunto}

## FUNDAMENTAÇÃO

Baseando-se na jurisprudência e doutrina relevantes:

"""
    
    # Adicionar citações relevantes
    for info in relevant_info[:3]:
        content += f"- {info.text}\n"
    
    content += """

## DISPOSITIVO

Diante do exposto, julgo:

"""
    
    return content

@router.post("/generate", response_model=MinutaGenerationResponse)
async def generate_minuta(
    generation_request: MinutaGenerationRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Verificar se caso existe
    result = await db.execute(select(Case).where(Case.id == generation_request.case_id))
    case = result.scalars().first()
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found"
        )
    
    # Gerar conteúdo da minuta
    content_md = await generate_minuta_content(
        generation_request.case_id,
        generation_request.tipo_ato,
        db
    )
    
    # Criar minuta
    minuta = Minuta(
        case_id=generation_request.case_id,
        author_user_id=current_user.id,
        tipo_ato=generation_request.tipo_ato,
        status="draft",
        content_md=content_md,
        citations={"sources": []}  # Seria preenchido com citações reais
    )
    
    db.add(minuta)
    await db.commit()
    await db.refresh(minuta)
    
    return MinutaGenerationResponse(
        minuta_id=minuta.id,
        status="success",
        content_md=content_md,
        citacoes=minuta.citations
    )

@router.get("/{minuta_id}", response_model=MinutaResponse)
async def get_minuta(minuta_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Minuta).where(Minuta.id == minuta_id))
    minuta = result.scalars().first()
    if not minuta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Minuta not found"
        )
    return minuta

@router.put("/{minuta_id}", response_model=MinutaResponse)
async def update_minuta(
    minuta_id: str,
    minuta_data: MinutaCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Minuta).where(Minuta.id == minuta_id))
    minuta = result.scalars().first()
    if not minuta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Minuta not found"
        )
    
    # Verificar se usuário é o autor
    if minuta.author_user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this minuta"
        )
    
    # Atualizar minuta
    minuta.content_md = minuta_data.content_md
    minuta.citations = minuta_data.citations
    minuta.status = minuta_data.status
    
    await db.commit()
    await db.refresh(minuta)
    
    return minuta

@router.get("/case/{case_id}", response_model=List[MinutaResponse])
async def list_case_minutas(case_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Minuta).where(Minuta.case_id == case_id))
    minutas = result.scalars().all()
    return minutas