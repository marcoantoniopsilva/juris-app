from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.db.session import get_db
from app.models import Template, JudicialUnit
from app.schemas import TemplateResponse, TemplateCreate
from app.api.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[TemplateResponse])
async def list_templates(
    unit_id: Optional[str] = None,
    tipo_ato: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    query = select(Template).where(Template.ativo == True)
    
    if unit_id:
        query = query.where(Template.unit_id == unit_id)
    
    if tipo_ato:
        query = query.where(Template.tipo_ato == tipo_ato)
    
    result = await db.execute(query)
    templates = result.scalars().all()
    return templates

@router.post("/", response_model=TemplateResponse)
async def create_template(
    template_data: TemplateCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Verificar se unidade existe
    result = await db.execute(select(JudicialUnit).where(JudicialUnit.id == template_data.unit_id))
    unit = result.scalars().first()
    if not unit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unit not found"
        )
    
    template = Template(**template_data.dict())
    db.add(template)
    await db.commit()
    await db.refresh(template)
    
    return template

@router.get("/{template_id}", response_model=TemplateResponse)
async def get_template(template_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Template).where(Template.id == template_id))
    template = result.scalars().first()
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    return template

@router.put("/{template_id}", response_model=TemplateResponse)
async def update_template(
    template_id: str,
    template_data: TemplateCreate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Template).where(Template.id == template_id))
    template = result.scalars().first()
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    # Atualizar template
    template.titulo = template_data.titulo
    template.tipo_ato = template_data.tipo_ato
    template.content_md = template_data.content_md
    template.variables = template_data.variables
    
    await db.commit()
    await db.refresh(template)
    
    return template

@router.delete("/{template_id}")
async def delete_template(template_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Template).where(Template.id == template_id))
    template = result.scalars().first()
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    # Marcar como inativo em vez de deletar
    template.ativo = False
    await db.commit()
    
    return {"message": "Template deleted successfully"}