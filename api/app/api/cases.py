from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.db.session import get_db
from app.models import Case, CaseFile, Document
from app.schemas import CaseResponse, CaseCreate
from app.api.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=CaseResponse)
async def create_case(
    case_data: CaseCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Verificar se número de processo já existe na unidade
    result = await db.execute(
        select(Case).where(
            Case.unit_id == case_data.unit_id,
            Case.numero == case_data.numero
        )
    )
    existing_case = result.scalars().first()
    if existing_case:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Case number already exists in this unit"
        )
    
    case = Case(**case_data.dict())
    db.add(case)
    await db.commit()
    await db.refresh(case)
    
    return case

@router.get("/", response_model=List[CaseResponse])
async def list_cases(
    unit_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    query = select(Case)
    
    if unit_id:
        query = query.where(Case.unit_id == unit_id)
    
    result = await db.execute(query)
    cases = result.scalars().all()
    return cases

@router.get("/{case_id}", response_model=CaseResponse)
async def get_case(case_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Case).where(Case.id == case_id))
    case = result.scalars().first()
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found"
        )
    return case

@router.post("/{case_id}/files")
async def add_file_to_case(
    case_id: str,
    document_id: str,
    file_type: str,
    ordem: int = 0,
    db: AsyncSession = Depends(get_db)
):
    # Verificar se caso existe
    result = await db.execute(select(Case).where(Case.id == case_id))
    case = result.scalars().first()
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found"
        )
    
    # Verificar se documento existe
    result = await db.execute(select(Document).where(Document.id == document_id))
    document = result.scalars().first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # Criar relação caso-arquivo
    case_file = CaseFile(
        case_id=case_id,
        document_id=document_id,
        tipo=file_type,
        ordem=ordem
    )
    
    db.add(case_file)
    await db.commit()
    
    return {"message": "File added to case successfully"}