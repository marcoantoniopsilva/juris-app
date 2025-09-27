from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
import numpy as np

from app.db.session import get_db
from app.models import DocumentChunk, Jurisprudence
from app.schemas import RAGSearchRequest, RAGSearchResult
from app.api.auth import get_current_user

router = APIRouter()

async def semantic_search(query: str, embeddings: List, chunks: List, limit: int = 10):
    # Simulação de busca semântica
    # Em produção, usaríamos um modelo de embeddings real
    results = []
    for i, chunk in enumerate(chunks):
        # Simular score de similaridade
        score = np.random.random()
        results.append({
            "text": chunk.text,
            "score": score,
            "metadata": chunk.metadata or {},
            "chunk_id": chunk.id
        })
    
    # Ordenar por score e limitar resultados
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:limit]

@router.post("/search", response_model=List[RAGSearchResult])
async def rag_search(
    search_request: RAGSearchRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Buscar chunks de documentos baseado no escopo
    if search_request.scope == "user":
        # Documentos do usuário
        query = select(DocumentChunk).join(Document).where(
            Document.owner_scope == "user",
            Document.owner_id == str(current_user.id)
        )
    elif search_request.scope == "unit" and search_request.unit_id:
        # Documentos da unidade
        query = select(DocumentChunk).join(Document).where(
            Document.owner_scope == "unit",
            Document.owner_id == search_request.unit_id
        )
    elif search_request.scope == "case" and search_request.case_id:
        # Documentos do caso específico
        # Esta é uma simplificação - na prática precisaríamos de joins mais complexos
        query = select(DocumentChunk)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid search scope or missing parameters"
        )
    
    result = await db.execute(query)
    chunks = result.scalars().all()
    
    # Buscar jurisprudência relevante
    juris_query = select(Jurisprudence).where(
        Jurisprudence.tribunal.in_(search_request.tribunais) if search_request.tribunais else True
    )
    juris_result = await db.execute(juris_query)
    juris_chunks = juris_result.scalars().all()
    
    # Converter jurisprudência para formato de chunks
    juris_as_chunks = []
    for juris in juris_chunks:
        juris_as_chunks.append({
            "text": f"{juris.tribunal} - {juris.processo}: {juris.ementa}",
            "metadata": {
                "tribunal": juris.tribunal,
                "processo": juris.processo,
                "relator": juris.relator,
                "data": juris.data.isoformat() if juris.data else None,
                "url": juris.url,
                "source_type": "jurisprudence"
            }
        })
    
    # Combinar todos os chunks
    all_chunks = []
    for chunk in chunks:
        all_chunks.append({
            "text": chunk.text,
            "metadata": {
                **chunk.metadata,
                "source_type": "document",
                "document_id": chunk.document_id,
                "section": chunk.section,
                "pages": f"{chunk.page_start}-{chunk.page_end}" if chunk.page_start and chunk.page_end else None
            }
        })
    
    all_chunks.extend(juris_as_chunks)
    
    # Realizar busca semântica (simulada)
    search_results = await semantic_search(search_request.query, [], all_chunks, search_request.limit)
    
    # Formatar resultados
    formatted_results = []
    for result in search_results:
        formatted_results.append(RAGSearchResult(
            text=result["text"],
            score=result["score"],
            metadata=result["metadata"],
            source_type=result["metadata"].get("source_type", "unknown")
        ))
    
    return formatted_results

@router.post("/hybrid-search", response_model=List[RAGSearchResult])
async def hybrid_search(
    search_request: RAGSearchRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Implementação de busca híbrida (semântica + lexical)
    # Esta é uma versão simplificada
    
    # 1. Busca semântica
    semantic_results = await rag_search(search_request, current_user, db)
    
    # 2. Busca lexical (BM25) - simplificada
    # Em produção, usaríamos pg_trgm ou full-text search do PostgreSQL
    lexical_results = []
    
    # Combinar e rerankear resultados
    all_results = semantic_results + lexical_results
    
    # Remover duplicatas e ordenar por score
    seen_texts = set()
    final_results = []
    
    for result in all_results:
        if result.text not in seen_texts:
            seen_texts.add(result.text)
            final_results.append(result)
    
    final_results.sort(key=lambda x: x.score, reverse=True)
    
    return final_results[:search_request.limit]