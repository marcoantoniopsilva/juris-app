#!/usr/bin/env python3
"""
Script de inicialização do Assessor Jurídico
"""
import asyncio
import uvicorn
from app.core.app_manager import app_manager, initialize_application, graceful_shutdown
from app.main import app  # Importar app FastAPI
import signal
import sys

async def start_application():
    """Inicia a aplicação completa"""
    print("🚀 Iniciando Assessor Jurídico - Poder Judiciário")
    print("=" * 50)
    
    try:
        # Inicializar gerenciador de aplicação
        await initialize_application()
        
        # Obter status da aplicação
        status = await app_manager.get_status()
        print("✅ Aplicação inicializada com sucesso")
        print(f"📊 Status: {status}")
        
        # Iniciar servidor FastAPI
        config = uvicorn.Config(
            app=app,
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
        
        server = uvicorn.Server(config)
        
        print("🌐 Servidor FastAPI iniciando...")
        print(f"📡 Endereço: http://{config.host}:{config.port}")
        print("=" * 50)
        
        await server.serve()
        
    except Exception as e:
        print(f"❌ Erro na inicialização: {e}")
        await graceful_shutdown()
        sys.exit(1)

async def handle_shutdown(signal_name):
    """Manipula sinal de desligamento"""
    print(f"\n🛑 Recebido sinal {signal_name}. Desligando graciosamente...")
    await graceful_shutdown()
    sys.exit(0)

def register_signal_handlers():
    """Registra handlers de sinal"""
    signals = {
        signal.SIGINT: "SIGINT",
        signal.SIGTERM: "SIGTERM"
    }
    
    for sig, name in signals.items():
        signal.signal(sig, lambda s, f: asyncio.create_task(handle_shutdown(name)))

if __name__ == "__main__":
    # Registrar handlers de sinal
    register_signal_handlers()
    
    # Iniciar aplicação
    try:
        asyncio.run(start_application())
    except KeyboardInterrupt:
        print("\n👋 Aplicação interrompida pelo usuário")
        sys.exit(0)