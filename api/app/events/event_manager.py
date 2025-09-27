from typing import Dict, Any, List, Callable, Optional
from datetime import datetime
import asyncio
from collections import defaultdict
import json
from enum import Enum

class EventType(Enum):
    """Tipos de eventos do sistema"""
    USER_CREATED = "user_created"
    USER_UPDATED = "user_updated"
    DOCUMENT_UPLOADED = "document_uploaded"
    DOCUMENT_PROCESSED = "document_processed"
    MINUTA_GENERATED = "minuta_generated"
    MINUTA_APPROVED = "minuta_approved"
    JURISPRUDENCE_FOUND = "jurisprudence_found"
    SEARCH_PERFORMED = "search_performed"
    BACKUP_COMPLETED = "backup_completed"
    ERROR_OCCURRED = "error_occurred"
    SYSTEM_ALERT = "system_alert"

class EventManager:
    def __init__(self):
        self.event_handlers = defaultdict(list)
        self.event_history = []
        self.max_history_size = 1000
    
    def subscribe(self, event_type: EventType, handler: Callable) -> bool:
        """Inscreve handler para um tipo de evento"""
        self.event_handlers[event_type].append(handler)
        return True
    
    def unsubscribe(self, event_type: EventType, handler: Callable) -> bool:
        """Remove inscrição de handler"""
        if handler in self.event_handlers[event_type]:
            self.event_handlers[event_type].remove(handler)
            return True
        return False
    
    async def publish(self, event_type: EventType, data: Dict[str, Any]) -> Dict[str, Any]:
        """Publica um evento"""
        event = {
            "id": self._generate_event_id(),
            "type": event_type.value,
            "data": data,
            "timestamp": datetime.utcnow().isoformat(),
            "handlers_called": 0,
            "handlers_failed": 0
        }
        
        # Adicionar ao histórico
        self._add_to_history(event)
        
        # Executar handlers
        handlers = self.event_handlers.get(event_type, [])
        event["total_handlers"] = len(handlers)
        
        for handler in handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(event)
                else:
                    handler(event)
                event["handlers_called"] += 1
            except Exception as e:
                event["handlers_failed"] += 1
                print(f"Erro no handler {handler.__name__} para evento {event_type}: {e}")
        
        return event
    
    def _add_to_history(self, event: Dict[str, Any]):
        """Adiciona evento ao histórico"""
        self.event_history.append(event)
        
        # Manter histórico dentro do limite
        if len(self.event_history) > self.max_history_size:
            self.event_history = self.event_history[-self.max_history_size:]
    
    def _generate_event_id(self) -> str:
        """Gera ID único para evento"""
        import uuid
        return str(uuid.uuid4())
    
    def get_event_history(self, 
                         event_type: Optional[EventType] = None,
                         limit: int = 100) -> List[Dict[str, Any]]:
        """Retorna histórico de eventos"""
        history = self.event_history
        
        if event_type:
            history = [event for event in history if event["type"] == event_type.value]
        
        return history[-limit:]
    
    def get_event_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas de eventos"""
        stats = {
            "total_events": len(self.event_history),
            "events_by_type": {},
            "handlers_by_type": {},
            "success_rate": 0
        }
        
        total_handlers_called = 0
        total_handlers_failed = 0
        
        for event in self.event_history:
            event_type = event["type"]
            stats["events_by_type"][event_type] = stats["events_by_type"].get(event_type, 0) + 1
            
            total_handlers_called += event.get("handlers_called", 0)
            total_handlers_failed += event.get("handlers_failed", 0)
            
            if event_type not in stats["handlers_by_type"]:
                stats["handlers_by_type"][event_type] = {
                    "called": 0,
                    "failed": 0
                }
            
            stats["handlers_by_type"][event_type]["called"] += event.get("handlers_called", 0)
            stats["handlers_by_type"][event_type]["failed"] += event.get("handlers_failed", 0)
        
        if total_handlers_called > 0:
            stats["success_rate"] = (total_handlers_called - total_handlers_failed) / total_handlers_called
        
        return stats
    
    def clear_history(self):
        """Limpa histórico de eventos"""
        self.event_history = []

# Handlers de evento comuns
async def log_event_handler(event: Dict[str, Any]):
    """Handler para logar eventos"""
    print(f"Evento {event['type']} publicado em {event['timestamp']}")
    print(f"Dados: {json.dumps(event['data'], indent=2)}")

async def notify_users_handler(event: Dict[str, Any]):
    """Handler para notificar usuários sobre eventos"""
    # Em produção, integrar com sistema de notificações
    event_type = event["type"]
    if event_type in [EventType.MINUTA_APPROVED.value, EventType.DOCUMENT_PROCESSED.value]:
        print(f"Notificando usuários sobre {event_type}")

async def update_metrics_handler(event: Dict[str, Any]):
    """Handler para atualizar métricas baseadas em eventos"""
    # Em produção, atualizar sistema de métricas
    event_type = event["type"]
    if event_type == EventType.SEARCH_PERFORMED.value:
        print("Atualizando métricas de busca")

async def trigger_workflows_handler(event: Dict[str, Any]):
    """Handler para acionar workflows baseados em eventos"""
    event_type = event["type"]
    data = event["data"]
    
    if event_type == EventType.DOCUMENT_UPLOADED.value:
        # Acionar processamento do documento
        print(f"Iniciando processamento do documento {data.get('document_id')}")

# Decorador para publicar eventos automaticamente
def event_publisher(event_type: EventType):
    """Decorador para publicar eventos automaticamente"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)
            
            # Publicar evento
            event_manager = EventManager()
            await event_manager.publish(event_type, {
                "function": func.__name__,
                "result": result,
                "timestamp": datetime.utcnow().isoformat()
            })
            
            return result
        return wrapper
    return decorator

# Inicialização do gerenciador de eventos
def initialize_event_manager() -> EventManager:
    """Inicializa e retorna gerenciador de eventos"""
    event_manager = EventManager()
    
    # Registrar handlers padrão
    event_manager.subscribe(EventType.USER_CREATED, log_event_handler)
    event_manager.subscribe(EventType.DOCUMENT_UPLOADED, log_event_handler)
    event_manager.subscribe(EventType.MINUTA_GENERATED, log_event_handler)
    event_manager.subscribe(EventType.SEARCH_PERFORMED, log_event_handler)
    
    event_manager.subscribe(EventType.MINUTA_APPROVED, notify_users_handler)
    event_manager.subscribe(EventType.DOCUMENT_PROCESSED, notify_users_handler)
    
    event_manager.subscribe(EventType.SEARCH_PERFORMED, update_metrics_handler)
    
    event_manager.subscribe(EventType.DOCUMENT_UPLOADED, trigger_workflows_handler)
    
    return event_manager

# Função para criar eventos de erro
async def publish_error_event(error: Exception, context: Dict[str, Any] = None):
    """Publica evento de erro"""
    event_manager = EventManager()
    
    await event_manager.publish(EventType.ERROR_OCCURRED, {
        "error_type": error.__class__.__name__,
        "error_message": str(error),
        "context": context or {},
        "timestamp": datetime.utcnow().isoformat()
    })

# Função para criar eventos de sistema
async def publish_system_event(event_type: EventType, message: str, details: Dict[str, Any] = None):
    """Publica evento de sistema"""
    event_manager = EventManager()
    
    await event_manager.publish(event_type, {
        "message": message,
        "details": details or {},
        "timestamp": datetime.utcnow().isoformat()
    })