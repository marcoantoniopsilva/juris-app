from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.db.session import get_db
from app.models import JudicialUnit, Membership, User
from app.schemas import JudicialUnitResponse, JudicialUnitCreate, MembershipResponse, MembershipCreate
from app.api.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[JudicialUnitResponse])
async def list_units(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(JudicialUnit))
    units = result.scalars().all()
    return units

@router.post("/", response_model=JudicialUnitResponse)
async def create_unit(unit_data: JudicialUnitCreate, db: AsyncSession = Depends(get_db)):
    # Verificar se código já existe
    result = await db.execute(select(JudicialUnit).where(JudicialUnit.codigo == unit_data.codigo))
    existing_unit = result.scalars().first()
    if existing_unit:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unit code already exists"
        )
    
    unit = JudicialUnit(**unit_data.dict())
    db.add(unit)
    await db.commit()
    await db.refresh(unit)
    
    return unit

@router.get("/{unit_id}", response_model=JudicialUnitResponse)
async def get_unit(unit_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(JudicialUnit).where(JudicialUnit.id == unit_id))
    unit = result.scalars().first()
    if not unit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unit not found"
        )
    return unit

@router.post("/{unit_id}/members", response_model=MembershipResponse)
async def add_member(
    unit_id: str, 
    membership_data: MembershipCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Verificar se a unidade existe
    result = await db.execute(select(JudicialUnit).where(JudicialUnit.id == unit_id))
    unit = result.scalars().first()
    if not unit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unit not found"
        )
    
    # Verificar se usuário existe
    result = await db.execute(select(User).where(User.id == membership_data.user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Verificar se membro já existe
    result = await db.execute(
        select(Membership).where(
            Membership.user_id == membership_data.user_id,
            Membership.unit_id == unit_id
        )
    )
    existing_member = result.scalars().first()
    if existing_member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already a member of this unit"
        )
    
    membership = Membership(**membership_data.dict())
    db.add(membership)
    await db.commit()
    await db.refresh(membership)
    
    return membership

@router.get("/{unit_id}/members", response_model=List[MembershipResponse])
async def list_members(unit_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Membership).where(Membership.unit_id == unit_id)
    )
    members = result.scalars().all()
    return members