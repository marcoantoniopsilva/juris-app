from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from uuid import UUID

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class JudicialUnitBase(BaseModel):
    tribunal: str
    nome: str
    codigo: str
    cidade: str
    uf: str

class JudicialUnitCreate(JudicialUnitBase):
    pass

class JudicialUnitResponse(JudicialUnitBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

class MembershipBase(BaseModel):
    user_id: UUID
    unit_id: UUID
    role: str
    is_admin: bool = False

class MembershipCreate(MembershipBase):
    pass

class MembershipResponse(MembershipBase):
    created_at: datetime

    class Config:
        from_attributes = True

class DocumentBase(BaseModel):
    filename: str
    content_type: str
    source_type: str
    pages: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None

class DocumentCreate(DocumentBase):
    owner_scope: str
    owner_id: UUID

class DocumentResponse(DocumentBase):
    id: UUID
    storage_path: str
    sha256: str
    created_at: datetime

    class Config:
        from_attributes = True

class CaseBase(BaseModel):
    numero: str
    classe: Optional[str] = None
    assunto: Optional[str] = None
    fase: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class CaseCreate(CaseBase):
    unit_id: UUID

class CaseResponse(CaseBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

class TemplateBase(BaseModel):
    titulo: str
    tipo_ato: str
    content_md: str
    variables: Optional[Dict[str, Any]] = None
    ativo: bool = True

class TemplateCreate(TemplateBase):
    unit_id: UUID

class TemplateResponse(TemplateBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class JurisprudenceBase(BaseModel):
    tribunal: str
    processo: str
    relator: Optional[str] = None
    orgao: Optional[str] = None
    data: Optional[date] = None
    tema: Optional[str] = None
    sumula: Optional[str] = None
    ementa: Optional[str] = None
    tese: Optional[str] = None
    url: Optional[str] = None
    html_text: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class JurisprudenceCreate(JurisprudenceBase):
    hash: str

class JurisprudenceResponse(JurisprudenceBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

class MinutaBase(BaseModel):
    tipo_ato: str
    status: str = "draft"
    content_md: str
    citations: Optional[Dict[str, Any]] = None

class MinutaCreate(MinutaBase):
    case_id: UUID

class MinutaResponse(MinutaBase):
    id: UUID
    docx_path: Optional[str] = None
    pdf_path: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[str] = None
    email: Optional[str] = None

class RAGSearchRequest(BaseModel):
    query: str
    scope: str = "user"  # user, unit, case
    case_id: Optional[UUID] = None
    unit_id: Optional[UUID] = None
    limit: int = 10

class RAGSearchResult(BaseModel):
    text: str
    score: float
    metadata: Dict[str, Any]
    source_type: str  # document, jurisprudence, template

class JurisSearchRequest(BaseModel):
    query: str
    tribunais: List[str] = []
    classes: List[str] = []
    assuntos: List[str] = []
    data_inicio: Optional[date] = None
    data_fim: Optional[date] = None
    limit: int = 20

class ProcessAnalysisRequest(BaseModel):
    case_id: UUID
    document_ids: List[UUID]

class ProcessAnalysisResponse(BaseModel):
    fase: str
    ultimos_pedidos: List[str]
    controversias: List[str]
    prazos: List[str]
    fundamentos_relevantes: List[str]

class MinutaGenerationRequest(BaseModel):
    case_id: UUID
    tipo_ato: str
    instrucoes: Optional[str] = None
    usar_modelos_unidade: bool = True
    buscar_jurisprudencia: bool = True

class MinutaGenerationResponse(BaseModel):
    minuta_id: UUID
    status: str
    content_md: Optional[str] = None
    citacoes: Optional[Dict[str, Any]] = None
    alertas: List[str] = []