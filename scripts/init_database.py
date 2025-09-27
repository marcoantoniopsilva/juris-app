#!/usr/bin/env python3
"""
Script para inicialização do banco de dados
"""
import asyncio
import sys
from pathlib import Path

# Adicionar diretório pai ao path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import create_async_engine
from app.models import Base
from scripts.seed_data import seed_database

async def init_database():
    """Inicializa o banco de dados"""
    print("🔄 Inicializando banco de dados...")
    
    # URL do banco de dados
    database_url = "postgresql+asyncpg://postgres:postgres@localhost:5432/juridico"
    
    try:
        # Criar engine
        engine = create_async_engine(database_url)
        
        # Criar todas as tabelas
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        print("✅ Tabelas criadas com sucesso")
        
        # Popular com dados iniciais
        await seed_database()
        
        print("✅ Dados iniciais inseridos")
        
        await engine.dispose()
        
    except Exception as e:
        print(f"❌ Erro na inicialização do banco: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(init_database())