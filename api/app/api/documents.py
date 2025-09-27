from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
import magic
import hashlib
import os
from datetime import datetime

from app.db.session import get_db
from app.models import Document, DocumentChunk
from app.schemas import DocumentResponse, DocumentCreate
from app.api.auth import get_current_user
from app.core.config import settings

router = APIRouter()

async def detect_file_type(file: UploadFile) -> str:
    # Ler os primeiros bytes para detecção do tipo
    content = await file.read(2048)
    await file.seek(0)
    
    mime = magic.from_buffer(content, mime=True)
    
    if mime.startswith('application/pdf'):
        return 'pdf'
    elif mime in ['application/vnd.openxmlformats-officedocument.wordprocessingml.document', 
                 'application/msword']:
        return 'docx'
    elif mime.startswith('text/'):
        return 'txt'
    elif mime in ['application/vnd.ms-excel', 
                 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']:
        return 'xlsx'
    elif mime.startswith('image/'):
        return 'image'
    elif mime.startswith('audio/'):
        return 'audio'
    elif mime.startswith('video/'):
        return 'video'
    else:
        return 'other'

async def calculate_sha256(file: UploadFile) -> str:
    sha256 = hashlib.sha256()
    while chunk := await file.read(8192):
        sha256.update(chunk)
    await file.seek(0)
    return sha256.hexdigest()

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    owner_scope: str = Form(...),
    owner_id: str = Form(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Verificar se arquivo já existe pelo hash
    sha256_hash = await calculate_sha256(file)
    
    result = await db.execute(select(Document).where(Document.sha256 == sha256_hash))
    existing_doc = result.scalars().first()
    if existing_doc:
        return existing_doc
    
    # Detectar tipo do arquivo
    source_type = await detect_file_type(file)
    
    # Criar nome único para armazenamento
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    storage_path = f"documents/{filename}"
    
    # Aqui você implementaria o upload para MinIO/S3
    # Por enquanto, apenas simulamos
    
    document = Document(
        owner_scope=owner_scope,
        owner_id=owner_id,
        filename=file.filename,
        content_type=file.content_type,
        storage_path=storage_path,
        sha256=sha256_hash,
        source_type=source_type,
        metadata={
            "original_filename": file.filename,
            "uploaded_by": str(current_user.id),
            "uploaded_at": datetime.now().isoformat()
        }
    )
    
    db.add(document)
    await db.commit()
    await db.refresh(document)
    
    # Aqui você iniciaria o processamento assíncrono (OCR, chunking, etc.)
    
    return document

@router.get("/", response_model=List[DocumentResponse])
async def list_documents(
    owner_scope: Optional[str] = None,
    owner_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    query = select(Document)
    
    if owner_scope and owner_id:
        query = query.where(
            Document.owner_scope == owner_scope,
            Document.owner_id == owner_id
        )
    
    result = await db.execute(query)
    documents = result.scalars().all()
    return documents

@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(document_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Document).where(Document.id == document_id))
    document = result.scalars().first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    return document

@router.delete("/{document_id}")
async def delete_document(document_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Document).where(Document.id == document_id))
    document = result.scalars().first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # Aqui você removeria o arquivo do storage também
    await db.delete(document)
    await db.commit()
    
    return {"message": "Document deleted successfully"}