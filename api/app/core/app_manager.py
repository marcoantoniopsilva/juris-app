from typing import Dict, Any, List
import asyncio
from datetime import datetime
from app.cache.cache_manager import CacheManager, initialize_cache
from app.error.error_handler import ErrorHandler, initialize_error_handler
from app.events.event_manager import EventManager, initialize_event_manager
from app.queue.queue_manager import QueueManager, initialize_queue_manager
from app.scheduler.task_scheduler import TaskScheduler, initialize_scheduler
from app.logging.log_manager import LogManager
from app.monitoring.metrics_manager import MetricsManager

class AppManager:
    def __init__(self):
        self.cache_manager = None
        self.error_handler = None
        self.event_manager = None
        self.queue_manager = None
        self.task_scheduler = None
        self.log_manager = None
        self.metrics_manager = None
        self.initialized = False
    
    async def initialize(self):
        """Inicializa todos os componentes da aplicação"""
        if self.initialized:
            return
        
        print("Inicializando gerenciador de aplicação...")
        
        try:
            # Inicializar componentes
            self.cache_manager = initialize_cache()
            self.error_handler = initialize_error_handler()
            self.event_manager = initialize_event_manager()
            self.queue_manager = initialize_queue_manager()
            self.task_scheduler = initialize_scheduler()
            self.log_manager = LogManager()
            self.metrics_manager = MetricsManager()
            
            # Iniciar componentes assíncronos
            await self._start_async_components()
            
            self.initialized = True
            print("Gerenciador de aplicação inicializado com sucesso")
            
            # Publicar evento de inicialização
            await self.event_manager.publish(
                "system_initialized",
                {"timestamp": datetime.utcnow().isoformat()}
            )
            
        except Exception as e:
            print(f"Erro na inicialização da aplicação: {e}")
            raise
    
    async def _start_async_components(self):
        """Inicia componentes assíncronos"""
        # Iniciar agendador de tarefas
        asyncio.create_task(self.task_scheduler.start_scheduler())
        
        # Iniciar monitoramento de métricas
        asyncio.create_task(self.metrics_manager.start_monitoring())
        
        # Iniciar workers de fila
        await start_queue_workers()
        
        print("Componentes assíncronos iniciados")
    
    async def shutdown(self):
        """Desliga a aplicação graciosamente"""
        print("Desligando aplicação...")
        
        try:
            # Parar componentes assíncronos
            self.task_scheduler.stop_scheduler()
            
            # Publicar evento de desligamento
            await self.event_manager.publish(
                "system_shutdown",
                {"timestamp": datetime.utcnow().isoformat()}
            )
            
            print("Aplicação desligada com sucesso")
            
        except Exception as e:
            print(f"Erro no desligamento da aplicação: {e}")
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status da aplicação"""
        return {
            "initialized": self.initialized,
            "timestamp": datetime.utcnow().isoformat(),
            "components": {
                "cache": self.cache_manager is not None,
                "error_handler": self.error_handler is not None,
                "event_manager": self.event_manager is not None,
                "queue_manager": self.queue_manager is not None,
                "task_scheduler": self.task_scheduler is not None,
                "log_manager": self.log_manager is not None,
                "metrics_manager": self.metrics_manager is not None
            }
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """Verifica saúde da aplicação"""
        health_status = {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "components": {}
        }
        
        # Verificar cache
        if self.cache_manager:
            cache_stats = self.cache_manager.get_stats()
            health_status["components"]["cache"] = {
                "status": "healthy" if self.cache_manager.cache_enabled else "disabled",
                "details": cache_stats
            }
        
        # Verificar filas
        if self.queue_manager:
            queue_stats = self.queue_manager.get_queue_stats("documents")
            health_status["components"]["queue"] = {
                "status": "healthy" if self.queue_manager.queue_enabled else "disabled",
                "details": queue_stats
            }
        
        # Verificar agendador
        if self.task_scheduler:
            tasks = self.task_scheduler.get_scheduled_tasks()
            health_status["components"]["scheduler"] = {
                "status": "healthy",
                "scheduled_tasks": len(tasks)
            }
        
        # Verificar se há componentes com problemas
        for component, status in health_status["components"].items():
            if status["status"] != "healthy":
                health_status["status"] = "degraded"
        
        return health_status

# Instância global do gerenciador de aplicação
app_manager = AppManager()

# Handlers de evento para o gerenciador
async def handle_system_events(event: Dict[str, Any]):
    """Manipula eventos do sistema"""
    event_type = event["type"]
    data = event["data"]
    
    if event_type == "error_occurred":
        print(f"Erro do sistema: {data.get('error_message')}")
    elif event_type == "system_alert":
        print(f"Alerta do sistema: {data.get('message')}")

# Função para inicialização rápida
async def initialize_application():
    """Inicializa a aplicação rapidamente"""
    global app_manager
    await app_manager.initialize()
    
    # Inscrever handlers de evento
    app_manager.event_manager.subscribe("error_occurred", handle_system_events)
    app_manager.event_manager.subscribe("system_alert", handle_system_events)
    
    return app_manager

# Decorador para garantir que a aplicação está inicializada
def require_initialized(func):
    """Decorador que verifica se a aplicação está inicializada"""
    async def wrapper(*args, **kwargs):
        global app_manager
        if not app_manager.initialized:
            await app_manager.initialize()
        return await func(*args, **kwargs)
    return wrapper

# Funções de utilidade
async def get_app_status():
    """Retorna status da aplicação"""
    global app_manager
    return await app_manager.get_status()

async def perform_health_check():
    """Executa verificação de saúde"""
    global app_manager
    return await app_manager.health_check()

async def graceful_shutdown():
    """Desliga a aplicação graciosamente"""
    global app_manager
    await app_manager.shutdown()

# Inicialização automática quando o módulo é importado
async def auto_initialize():
    """Inicialização automática"""
    try:
        await initialize_application()
    except Exception as e:
        print(f"Falha na inicialização automática: {e}")

# Iniciar inicialização automática em background
asyncio.create_task(auto_initialize())