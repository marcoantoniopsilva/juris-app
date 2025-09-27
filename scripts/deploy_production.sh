#!/bin/bash
# Script de deploy para produção

set -e

echo "🚀 Iniciando deploy do Assessor Jurídico para produção"
echo "======================================================"

# Variáveis
ENV_FILE=".env.production"
DOCKER_COMPOSE_FILE="docker-compose.production.yml"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="backups/production_$TIMESTAMP"

# Verificar se o arquivo .env existe
if [ ! -f "$ENV_FILE" ]; then
    echo "❌ Arquivo $ENV_FILE não encontrado"
    exit 1
fi

# Criar backup
echo "📦 Criando backup..."
mkdir -p "$BACKUP_DIR"
docker compose -f "$DOCKER_COMPOSE_FILE" exec -T postgres pg_dump -U postgres juridico > "$BACKUP_DIR/database.sql"
tar -czf "$BACKUP_DIR/app_backup.tar.gz" api/ frontend/ scripts/

echo "✅ Backup criado em $BACKUP_DIR"

# Parar serviços atuais
echo "🛑 Parando serviços..."
docker compose -f "$DOCKER_COMPOSE_FILE" down

# Atualizar código
echo "🔄 Atualizando código..."
git pull origin main

# Construir novas imagens
echo "🏗️ Construindo imagens..."
docker compose -f "$DOCKER_COMPOSE_FILE" build

# Iniciar serviços
echo "🚀 Iniciando serviços..."
docker compose -f "$DOCKER_COMPOSE_FILE" up -d

# Executar migrações
echo "📋 Executando migrações..."
docker compose -f "$DOCKER_COMPOSE_FILE" exec -T api alembic upgrade head

# Popular dados iniciais se necessário
echo "🌱 Populando dados iniciais..."
docker compose -f "$DOCKER_COMPOSE_FILE" exec -T api python scripts/seed_data.py

# Verificar saúde
echo "🏥 Verificando saúde dos serviços..."
sleep 10
docker compose -f "$DOCKER_COMPOSE_FILE" ps

# Testar endpoints
echo "🧪 Testando endpoints..."
curl -f http://localhost:8000/health || echo "❌ Health check falhou"
curl -f http://localhost:8000/docs || echo "❌ API docs falhou"

echo "======================================================"
echo "✅ Deploy concluído com sucesso!"
echo "🌐 Frontend: http://localhost:3000"
echo "📡 API: http://localhost:8000"
echo "📊 Monitoramento: http://localhost:5555"
echo "======================================================"