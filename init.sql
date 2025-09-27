CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Tabela de usuários
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de unidades judiciais
CREATE TABLE judicial_units (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tribunal VARCHAR(100) NOT NULL,
    nome VARCHAR(255) NOT NULL,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    uf CHAR(2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de membros (relação usuário-unidade)
CREATE TABLE memberships (
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    unit_id UUID REFERENCES judicial_units(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('juiz', 'assessor', 'secretaria', 'estagiario')),
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, unit_id)
);

-- Tabela de documentos
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    owner_scope VARCHAR(10) NOT NULL CHECK (owner_scope IN ('user', 'unit')),
    owner_id UUID NOT NULL,
    filename VARCHAR(255) NOT NULL,
    content_type VARCHAR(100) NOT NULL,
    storage_path VARCHAR(500) NOT NULL,
    sha256 CHAR(64) UNIQUE NOT NULL,
    source_type VARCHAR(20) NOT NULL CHECK (source_type IN ('pdf', 'docx', 'txt', 'csv', 'xlsx', 'image', 'audio', 'video')),
    pages INTEGER,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de chunks de documentos
CREATE TABLE document_chunks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    text TEXT NOT NULL,
    section VARCHAR(100),
    page_start INTEGER,
    page_end INTEGER,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de embeddings de documentos
CREATE TABLE document_embeddings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    chunk_id UUID REFERENCES document_chunks(id) ON DELETE CASCADE,
    vector vector(3072),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de casos
CREATE TABLE cases (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    unit_id UUID REFERENCES judicial_units(id) ON DELETE CASCADE,
    numero VARCHAR(100) NOT NULL,
    classe VARCHAR(100),
    assunto VARCHAR(200),
    fase VARCHAR(50),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de arquivos do caso
CREATE TABLE case_files (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    case_id UUID REFERENCES cases(id) ON DELETE CASCADE,
    document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    tipo VARCHAR(20) NOT NULL CHECK (tipo IN ('peticao', 'despacho', 'decisao', 'sentenca', 'outro')),
    ordem INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de templates
CREATE TABLE templates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    unit_id UUID REFERENCES judicial_units(id) ON DELETE CASCADE,
    titulo VARCHAR(255) NOT NULL,
    tipo_ato VARCHAR(20) NOT NULL CHECK (tipo_ato IN ('despacho', 'decisao', 'sentenca')),
    content_md TEXT NOT NULL,
    variables JSONB,
    ativo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de jurisprudência
CREATE TABLE jurisprudence (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tribunal VARCHAR(50) NOT NULL,
    processo VARCHAR(100) NOT NULL,
    relator VARCHAR(200),
    orgao VARCHAR(200),
    data DATE,
    tema VARCHAR(500),
    sumula VARCHAR(500),
    ementa TEXT,
    tese TEXT,
    url VARCHAR(500),
    html_text TEXT,
    metadata JSONB,
    hash VARCHAR(64) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de embeddings de jurisprudência
CREATE TABLE juris_embeddings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    juris_id UUID REFERENCES jurisprudence(id) ON DELETE CASCADE,
    vector vector(3072),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de minutas
CREATE TABLE minutas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    case_id UUID REFERENCES cases(id) ON DELETE CASCADE,
    author_user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    tipo_ato VARCHAR(20) NOT NULL CHECK (tipo_ato IN ('despacho', 'decisao', 'sentenca')),
    status VARCHAR(10) NOT NULL CHECK (status IN ('draft', 'final')),
    content_md TEXT NOT NULL,
    citations JSONB,
    docx_path VARCHAR(500),
    pdf_path VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de logs de auditoria
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    unit_id UUID REFERENCES judicial_units(id) ON DELETE CASCADE,
    action VARCHAR(100) NOT NULL,
    target_type VARCHAR(50),
    target_id UUID,
    ip VARCHAR(45),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de checklists
CREATE TABLE checklists (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    unit_id UUID REFERENCES judicial_units(id) ON DELETE CASCADE,
    tipo_ato VARCHAR(20) NOT NULL CHECK (tipo_ato IN ('despacho', 'decisao', 'sentenca')),
    items JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices
CREATE INDEX idx_documents_owner ON documents(owner_scope, owner_id);
CREATE INDEX idx_document_chunks_document ON document_chunks(document_id);
CREATE INDEX idx_cases_unit ON cases(unit_id);
CREATE INDEX idx_case_files_case ON case_files(case_id);
CREATE INDEX idx_templates_unit ON templates(unit_id);
CREATE INDEX idx_jurisprudence_tribunal ON jurisprudence(tribunal);
CREATE INDEX idx_jurisprudence_hash ON jurisprudence(hash);
CREATE INDEX idx_minutas_case ON minutas(case_id);
CREATE INDEX idx_audit_logs_user ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_unit ON audit_logs(unit_id);
CREATE INDEX idx_audit_logs_created ON audit_logs(created_at);