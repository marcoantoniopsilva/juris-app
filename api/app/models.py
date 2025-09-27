from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, JSON, Date, Text, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class JudicialUnit(Base):
    __tablename__ = "judicial_units"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tribunal = Column(String(100), nullable=False)
    nome = Column(String(255), nullable=False)
    codigo = Column(String(50), unique=True, nullable=False)
    cidade = Column(String(100), nullable=False)
    uf = Column(String(2), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Membership(Base):
    __tablename__ = "memberships"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    unit_id = Column(UUID(as_uuid=True), ForeignKey("judicial_units.id"), primary_key=True)
    role = Column(SQLEnum("juiz", "assessor", "secretaria", "estagiario", name="role_enum"), nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User")
    unit = relationship("JudicialUnit")

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_scope = Column(SQLEnum("user", "unit", name="owner_scope_enum"), nullable=False)
    owner_id = Column(UUID(as_uuid=True), nullable=False)
    filename = Column(String(255), nullable=False)
    content_type = Column(String(100), nullable=False)
    storage_path = Column(String(500), nullable=False)
    sha256 = Column(String(64), unique=True, nullable=False)
    source_type = Column(SQLEnum("pdf", "docx", "txt", "csv", "xlsx", "image", "audio", "video", name="source_type_enum"), nullable=False)
    pages = Column(Integer)
    metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False)
    chunk_index = Column(Integer, nullable=False)
    text = Column(Text, nullable=False)
    section = Column(String(100))
    page_start = Column(Integer)
    page_end = Column(Integer)
    metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    document = relationship("Document")

class Case(Base):
    __tablename__ = "cases"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    unit_id = Column(UUID(as_uuid=True), ForeignKey("judicial_units.id"), nullable=False)
    numero = Column(String(100), nullable=False)
    classe = Column(String(100))
    assunto = Column(String(200))
    fase = Column(String(50))
    metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    unit = relationship("JudicialUnit")

class CaseFile(Base):
    __tablename__ = "case_files"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id = Column(UUID(as_uuid=True), ForeignKey("cases.id"), nullable=False)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False)
    tipo = Column(SQLEnum("peticao", "despacho", "decisao", "sentenca", "outro", name="file_type_enum"), nullable=False)
    ordem = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    case = relationship("Case")
    document = relationship("Document")

class Template(Base):
    __tablename__ = "templates"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    unit_id = Column(UUID(as_uuid=True), ForeignKey("judicial_units.id"), nullable=False)
    titulo = Column(String(255), nullable=False)
    tipo_ato = Column(SQLEnum("despacho", "decisao", "sentenca", name="act_type_enum"), nullable=False)
    content_md = Column(Text, nullable=False)
    variables = Column(JSON)
    ativo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    unit = relationship("JudicialUnit")

class Jurisprudence(Base):
    __tablename__ = "jurisprudence"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tribunal = Column(String(50), nullable=False)
    processo = Column(String(100), nullable=False)
    relator = Column(String(200))
    orgao = Column(String(200))
    data = Column(Date)
    tema = Column(String(500))
    sumula = Column(String(500))
    ementa = Column(Text)
    tese = Column(Text)
    url = Column(String(500))
    html_text = Column(Text)
    metadata = Column(JSON)
    hash = Column(String(64), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Minuta(Base):
    __tablename__ = "minutas"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id = Column(UUID(as_uuid=True), ForeignKey("cases.id"), nullable=False)
    author_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    tipo_ato = Column(SQLEnum("despacho", "decisao", "sentenca", name="act_type_enum"), nullable=False)
    status = Column(SQLEnum("draft", "final", name="status_enum"), nullable=False)
    content_md = Column(Text, nullable=False)
    citations = Column(JSON)
    docx_path = Column(String(500))
    pdf_path = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    case = relationship("Case")
    author = relationship("User")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    unit_id = Column(UUID(as_uuid=True), ForeignKey("judicial_units.id"))
    action = Column(String(100), nullable=False)
    target_type = Column(String(50))
    target_id = Column(UUID(as_uuid=True))
    ip = Column(String(45))
    metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User")
    unit = relationship("JudicialUnit")

class Checklist(Base):
    __tablename__ = "checklists"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    unit_id = Column(UUID(as_uuid=True), ForeignKey("judicial_units.id"), nullable=False)
    tipo_ato = Column(SQLEnum("despacho", "decisao", "sentenca", name="act_type_enum"), nullable=False)
    items = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    unit = relationship("JudicialUnit")