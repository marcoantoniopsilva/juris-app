# Assessor Jurídico - Poder Judiciário

Sistema completo de geração de minutas jurídicas com RAG (Retrieval Augmented Generation) para o Poder Judiciário brasileiro.

## 🚀 Funcionalidades Principais

- **🤖 RAG Jurídico**: Busca inteligente em documentos, jurisprudência e modelos
- **📄 Processamento de Documentos**: Suporte a PDF, DOCX, imagens, áudio e vídeo com OCR/ASR
- **⚖️ Scraping de Jurisprudência**: Integração com STF, STJ, TRFs
- **📝 Geração de Minutas**: Despachos, decisões e sentenças automatizadas
- **👥 Colaboração**: Comentários, sugestões e revisão em tempo real
- **🔒 Segurança**: RBAC, LGPD, auditoria completa
- **📊 Monitoramento**: Métricas, alertas e relatórios

## 🏗️ Arquitetura

### Frontend (Next.js 14)
- **Framework**: Next.js 14 com App Router
- **Estilo**: Tailwind CSS + shadcn/ui
- **Estado**: Zustand
- **Formulários**: React Hook Form + Zod
- **API Client**: Axios

### Backend (FastAPI)
- **Framework**: FastAPI com Python 3.11
- **Banco**: PostgreSQL 15 + pgvector
- **Cache**: Redis
- **Armazenamento**: MinIO (S3 compatível)
- **Filas**: Celery + Redis
- **Monitoramento**: Prometheus, Flower

### IA/ML
- **LLM**: OpenAI GPT-4/GPT-3.5 (compatível com modelos locais)
- **Embeddings**: Sentence Transformers
- **OCR**: PaddleOCR
- **ASR**: Whisper
- **Scraping**: Playwright

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

### 4. Inicialize o banco de dados
```bash
python scripts/init_database.py
```

### 5. Execute as migrações
```bash
cd api
alembic upgrade head
```

### 6. Acesse a aplicação
- **Frontend**: http://localhost:3000
- **API**: http://localhost:8000
- **MinIO Console**: http://localhost:9001
- **Flower (Celery)**: http://localhost:5555
- **Documentação API**: http://localhost:8000/docs

## 📦 Estrutura do Projeto

```
juridico-assessor/
├── api/                 # Backend FastAPI
│   ├── app/
│   │   ├── core/       # Configurações principais
│   │   ├── models/     # Modelos de banco
│   │   ├── api/        # Rotas da API
│   │   ├── services/   # Lógica de negócio
│   │   ├── utils/      # Utilitários
│   │   └── worker/     # Tarefas Celery
│   ├── alembic/        # Migrações de banco
│   └── requirements.txt
├── frontend/            # Next.js frontend
│   ├── src/
│   │   ├── app/        # App Router
│   │   ├── components/ # Componentes UI
│   │   ├── lib/       # Utilitários
│   │   └── stores/    # Gerenciamento de estado
│   └── package.json
├── scripts/            # Scripts auxiliares
├── docker-compose.yml
└── README.md
```

## 🔧 Configuração

### Variáveis de Ambiente Principais

```env
# Banco de dados
POSTGRES_URL=postgresql://postgres:postgres@postgres:5432/juridico

# Redis
REDIS_URL=redis://redis:6379/0

# MinIO/S3
S3_ENDPOINT=http://minio:9000
S3_BUCKET=juridico-files
S3_ACCESS_KEY=minioadmin
S3_SECRET_KEY=minioadmin

# Segurança
SECRET_KEY=your-super-secret-key
ALGORITHM=HS256

# Celery
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

## 🚀 Uso Rápido

### 1. Login
Acesse http://localhost:3000 e faça login com:
- Email: admin@example.com
- Senha: admin123

### 2. Upload de Documentos
- Navegue para "Upload"
- Arraste documentos ou clique para selecionar
- Documentos serão processados automaticamente

### 3. Busca Jurisprudência
- Acesse "Jurisprudência"
- Digite termos de busca
- Selecione tribunais e filtros
- Clique em "Buscar"

### 4. Gerar Minuta
- Acesse "Minutas"
- Selecione o tipo de ato
- Configure as opções
- Clique em "Gerar Minuta"

### 5. Colaboração
- Adicione comentários em documentos
- Faça sugestões de edição
- Revise minutas com colegas

## 🧪 Desenvolvimento

### Executando em modo desenvolvimento
```bash
# Backend
cd api
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend
cd frontend
npm run dev
```

### Testes
```bash
# Backend
cd api
pytest

# Frontend
cd frontend
npm test
```

### Linting e Formatação
```bash
# Backend
cd api
black .
flake8 .
mypy .

# Frontend
cd frontend
npm run lint
```

## 📊 Monitoramento

### Métricas da Aplicação
- **Health Checks**: http://localhost:8000/health
- **Métricas Prometheus**: http://localhost:8000/metrics
- **Monitor Celery**: http://localhost:5555

### Logs
```bash
# Ver logs dos containers
docker compose logs -f

# Logs da aplicação
tail -f api/logs/app.log
```

## 🔒 Segurança

### Autenticação
- JWT tokens com expiração configurável
- Refresh tokens
- Validação de escopos e permissões

### RBAC (Role-Based Access Control)
- **Juiz**: Acesso completo
- **Assessor**: Criação e edição de minutas
- **Secretaria**: Upload e organização
- **Estagiário**: Acesso limitado

### LGPD
- Pseudonimização de dados sensíveis
- Logs de auditoria
- Controle de consentimento

## 🚨 Troubleshooting

### Problemas Comuns

1. **Erro de conexão com banco**
   ```bash
   docker compose restart postgres
   ```

2. **Redis não responde**
   ```bash
   docker compose restart redis
   ```

3. **Migrações falham**
   ```bash
   cd api
   alembic upgrade head
   ```

4. **Arquivos não são processados**
   ```bash
   docker compose restart worker
   ```

### Logs de Depuração
```bash
# Logs detalhados
docker compose logs --tail=100 -f api

# Logs de erro
docker compose logs | grep -i error
```

## 📞 Suporte

Para issues e dúvidas:
1. Consulte a documentação em `/docs`
2. Verifique os logs da aplicação
3. Abra uma issue no repositório
4. Contate a equipe de desenvolvimento

## 📝 Licença

Este projeto é destinado ao uso no Poder Judiciário brasileiro.

## 🎯 Próximos Passos

- [ ] Integração com sistemas tribunais
- [ ] Modelos de IA customizados
- [ ] Mobile app
- [ ] Analytics avançado
- [ ] Integração com PJe

---

**Desenvolvido para o Poder Judiciário Brasileiro** 🎖️