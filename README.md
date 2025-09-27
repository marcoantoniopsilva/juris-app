# Assessor Jurídico - Poder Judiciário

Sistema completo de geração de minutas jurídicas com RAG (Retrieval Augmented Generation) para o Poder Judiciário brasileiro.

## 🚀 Funcionalidades

- **RAG Jurídico**: Busca híbrida em documentos do usuário, modelos da unidade e jurisprudência
- **Scraping de Jurisprudência**: STF, STJ, TRF1-TRF6 com Playwright
- **Geração de Minutas**: Despachos, decisões e sentenças com citações rastreáveis
- **Multi-tenant**: Isolamento por unidade judicial e usuário
- **RBAC**: Controle de acesso por cargo (juiz, assessor, secretaria, estagiário)
- **Upload de Documentos**: PDF, DOCX, TXT, CSV, XLSX, imagens, áudio/vídeo
- **OCR/ASR**: Extração de texto com PaddleOCR e Whisper
- **Exportação**: DOCX e PDF com templates por tribunal

## 🏗️ Arquitetura

### Frontend
- **Next.js 14** com App Router
- **TypeScript** para type safety
- **Tailwind CSS** com shadcn/ui
- **Zustand** para gerenciamento de estado
- **React Hook Form** + **Zod** para formulários

### Backend
- **FastAPI** com Python 3.11
- **PostgreSQL 15** com pgvector para embeddings
- **Celery** + **Redis** para tarefas assíncronas
- **MinIO** para armazenamento de arquivos
- **Playwright** para scraping de jurisprudência

### IA/ML
- **LLM Principal**: GPT-4.1 (com opção para modelos on-prem)
- **Embeddings**: text-embedding-3-large
- **Reranking**: bge-reranker-v2-m3
- **OCR**: PaddleOCR + docTR
- **ASR**: Whisper large-v3

## 🛠️ Instalação

### Pré-requisitos
- Docker e Docker Compose
- Python 3.11+
- Node.js 18+

### 1. Clone o repositório
```bash
git clone <repository-url>
cd juridico-assessor
```

### 2. Configure as variáveis de ambiente
```bash
cp .env.example .env
# Edite o .env com suas configurações
```

### 3. Inicie os serviços
```bash
docker compose up -d
```

### 4. Execute as migrações (opcional)
```bash
cd api
alembic upgrade head
```

### 5. Popule dados iniciais
```bash
python scripts/seed_data.py
```

### 6. Acesse a aplicação
- Frontend: http://localhost:3000
- API: http://localhost:8000
- MinIO Console: http://localhost:9001
- PGAdmin: http://localhost:5050 (se configurado)

## 📦 Estrutura do Projeto

```
.
├── api/                 # Backend FastAPI
│   ├── app/
│   │   ├── core/       # Configurações
│   │   ├── db/         # Database
│   │   ├── models/     # SQLAlchemy models
│   │   ├── schemas/    # Pydantic schemas
│   │   ├── services/   # Business logic
│   │   ├── utils/      # Utilitários
│   │   └── worker/     # Celery tasks
│   └── requirements.txt
├── frontend/            # Next.js frontend
│   ├── src/
│   │   ├── app/        # App Router pages
│   │   ├── components/ # UI components
│   │   ├── lib/       # Utilitários
│   │   └── stores/    # Zustand stores
│   └── package.json
├── infra/               # Configurações de infra
├── scripts/            # Scripts auxiliares
└── docker-compose.yml
```

## 🔐 Segurança

- **Isolamento de dados**: Filtros por unit_id em todas as queries
- **RBAC**: Permissões granulars por cargo
- **Criptografia**: AES-256 at rest, TLS in transit
- **Auditoria**: Logs completos de todas as operações
- **Sem telemetria**: DATA_USAGE_OPT_OUT=true por padrão

## 🧪 Testes

```bash
# Backend
cd api
pytest

# Frontend
cd frontend
npm test
```

## 📊 Monitoramento

- **Prometheus** + **Grafana** para métricas
- **Logs estruturados** em JSON
- **Health checks** automatizados

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📝 Licença

Este projeto é destinado ao uso no Poder Judiciário brasileiro.

## 🆘 Suporte

Para dúvidas e suporte:
- Consulte a documentação em `/docs`
- Abra uma issue no repositório
- Contate a equipe de desenvolvimento

## 🚨 Importante

Este sistema lida com dados sensíveis do Poder Judiciário. Certifique-se de:
- Configurar corretamente as chaves de criptografia
- Manter o sistema atualizado com patches de segurança
- Realizar backups regulares
- Seguir as normas de segurança da informação do seu tribunal