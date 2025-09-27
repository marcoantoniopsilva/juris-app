#!/usr/bin/env python3
import asyncio
import uuid
from datetime import datetime, date
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

async def seed_database():
    # Conectar ao banco
    engine = create_async_engine("postgresql+asyncpg://postgres:postgres@localhost:5432/juridico")
    
    async with engine.connect() as conn:
        # Inserir unidades judiciais de exemplo
        units_data = [
            {
                "id": str(uuid.uuid4()),
                "tribunal": "TRF1",
                "nome": "Vara Federal da Seção Judiciária do Rio de Janeiro",
                "codigo": "TRF1-RJ-001",
                "cidade": "Rio de Janeiro",
                "uf": "RJ",
                "created_at": datetime.now()
            },
            {
                "id": str(uuid.uuid4()),
                "tribunal": "TRF2",
                "nome": "Vara Federal de São Paulo",
                "codigo": "TRF2-SP-001",
                "cidade": "São Paulo",
                "uf": "SP",
                "created_at": datetime.now()
            }
        ]
        
        for unit in units_data:
            await conn.execute(
                text("""
                INSERT INTO judicial_units (id, tribunal, nome, codigo, cidade, uf, created_at)
                VALUES (:id, :tribunal, :nome, :codigo, :cidade, :uf, :created_at)
                ON CONFLICT DO NOTHING
                """),
                unit
            )
        
        # Inserir jurisprudência de exemplo
        juris_data = [
            {
                "id": str(uuid.uuid4()),
                "tribunal": "STJ",
                "processo": "REsp 1.000.000",
                "relator": "Ministro João Silva",
                "orgao": "Primeira Turma",
                "data": date(2023, 6, 15),
                "tema": "DIREITO CIVIL. CONSUMIDOR. VÍCIO DO PRODUTO.",
                "sumula": "A responsabilidade civil do fornecedor é objetiva.",
                "ementa": "A responsabilidade civil do fornecedor por vícios do produto é objetiva, independente de culpa.",
                "tese": "Responsabilidade objetiva do fornecedor por vícios do produto.",
                "url": "https://stj.jus.br/jurisprudencia",
                "html_text": "<p>Responsabilidade civil objetiva do fornecedor...</p>",
                "metadata": {"classe": "REsp", "assunto": "Direito do Consumidor"},
                "hash": "abc123def456",
                "created_at": datetime.now()
            }
        ]
        
        for juris in juris_data:
            await conn.execute(
                text("""
                INSERT INTO jurisprudence (id, tribunal, processo, relator, orgao, data, tema, 
                                         sumula, ementa, tese, url, html_text, metadata, hash, created_at)
                VALUES (:id, :tribunal, :processo, :relator, :orgao, :data, :tema, :sumula, 
                        :ementa, :tese, :url, :html_text, :metadata, :hash, :created_at)
                ON CONFLICT DO NOTHING
                """),
                juris
            )
        
        await conn.commit()
        print("Dados iniciais inseridos com sucesso!")

if __name__ == "__main__":
    asyncio.run(seed_database())