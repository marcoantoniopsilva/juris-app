from typing import Dict, Any, List, Optional
from datetime import datetime
import asyncio
from collections import deque
import json
import redis
from app.core.config import settings

class QueueManager:
    def __init__(self):
        self.redis_client = None
        self.local_queues = {}
        self.queue_enabled = True
        
    def connect_redis(self):
        """Conecta ao Redis"""
        try:
            self.redis_client = redis.Redis.from_url(settings.REDIS_URL)
            self.redis_client.ping()
            print("Conectado ao Redis para filas")
            return True
        except Exception as e:
            print(f"Erro ao conectar ao Redis: {e}")
            self.queue_enabled = False
            return False
    
    async def enqueue(self, queue_name: str, item: Any, priority: int = 0) -> bool:
        """Adiciona item à fila"""
        if not self.queue_enabled:
            return False
        
        try:
            serialized_item = json.dumps({
                "data": item,
                "priority": priority,
                "timestamp": datetime.utcnow().isoformat()
            })
            
            if self.redis_client:
                # Usar lista ordenada para prioridade
                self.redis_client.zadd(
                    f"queue:{queue_name}", 
                    {serialized_item: priority}
                )
            else:
                # Fallback para fila local
                if queue_name not in self.local_queues:
                    self.local_queues[queue_name] = deque()
                
                self.local_queues[queue_name].append({
                    "data": item,
                    "priority": priority,
                    "timestamp": datetime.utcnow().isoformat()
                })
            
            return True
        except Exception as e:
            print(f"Erro ao enfileirar: {e}")
            return False
    
    async def dequeue(self, queue_name: str, timeout: int = 0) -> Optional[Any]:
        """Remove e retorna item da fila"""
        if not self.queue_enabled:
            return None
        
        try:
            if self.redis_client:
                # Obter item com maior prioridade (menor score)
                items = self.redis_client.zrange(
                    f"queue:{queue_name}", 
                    0, 0, 
                    withscores=True
                )
                
                if not items:
                    if timeout > 0:
                        await asyncio.sleep(timeout)
                        return await self.dequeue(queue_name, 0)
                    return None
                
                serialized_item, _ = items[0]
                self.redis_client.zrem(f"queue:{queue_name}", serialized_item)
                
                item_data = json.loads(serialized_item)
                return item_data["data"]
            else:
                # Fallback para fila local
                if queue_name not in self.local_queues or not self.local_queues[queue_name]:
                    if timeout > 0:
                        await asyncio.sleep(timeout)
                        return await self.dequeue(queue_name, 0)
                    return None
                
                # Encontrar item com maior prioridade
                highest_priority_item = None
                highest_priority = float('-inf')
                
                for item in self.local_queues[queue_name]:
                    if item["priority"] > highest_priority:
                        highest_priority = item["priority"]
                        highest_priority_item = item
                
                if highest_priority_item:
                    self.local_queues[queue_name].remove(highest_priority_item)
                    return highest_priority_item["data"]
                
                return None
        except Exception as e:
            print(f"Erro ao desenfileirar: {e}")
            return None
    
    def get_queue_size(self, queue_name: str) -> int:
        """Retorna tamanho da fila"""
        if not self.queue_enabled:
            return 0
        
        try:
            if self.redis_client:
                return self.redis_client.zcard(f"queue:{queue_name}")
            else:
                return len(self.local_queues.get(queue_name, []))
        except Exception as e:
            print(f"Erro ao obter tamanho da fila: {e}")
            return 0
    
    def clear_queue(self, queue_name: str) -> bool:
        """Limpa toda a fila"""
        if not self.queue_enabled:
            return False
        
        try:
            if self.redis_client:
                self.redis_client.delete(f"queue:{queue_name}")
            else:
                self.local_queues[queue_name] = deque()
            return True
        except Exception as e:
            print(f"Erro ao limpar fila: {e}")
            return False
    
    def get_queue_stats(self, queue_name: str) -> Dict[str, Any]:
        """Retorna estatísticas da fila"""
        if not self.queue_enabled:
            return {"enabled": False}
        
        size = self.get_queue_size(queue_name)
        
        return {
            "queue_name": queue_name,
            "size": size,
            "enabled": self.queue_enabled,
            "backend": "redis" if self.redis_client else "local",
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def process_queue(self, 
                          queue_name: str, 
                          processor: callable,
                          max_items: int = None,
                          timeout: int = 1):
        """Processa itens da fila continuamente"""
        processed_count = 0
        
        while True:
            try:
                item = await self.dequeue(queue_name, timeout)
                if item is None:
                    if max_items and processed_count >= max_items:
                        break
                    continue
                
                # Processar item
                if asyncio.iscoroutinefunction(processor):
                    await processor(item)
                else:
                    processor(item)
                
                processed_count += 1
                
                if max_items and processed_count >= max_items:
                    break
                    
            except Exception as e:
                print(f"Erro ao processar item da fila {queue_name}: {e}")
                await asyncio.sleep(1)  # Esperar antes de tentar novamente

# Funções de processamento de fila comuns
async def process_document_queue(item: Dict[str, Any]):
    """Processa itens da fila de documentos"""
    print(f"Processando documento: {item.get('document_id')}")
    # Implementação real do processamento

async def process_minuta_queue(item: Dict[str, Any]):
    """Processa itens da fila de minutas"""
    print(f"Processando minuta: {item.get('minuta_id')}")
    # Implementação real do processamento

async def process_notification_queue(item: Dict[str, Any]):
    """Processa itens da fila de notificações"""
    print(f"Processando notificação: {item.get('user_id')}")
    # Implementação real do processamento

# Decorador para enfileirar automaticamente
def enqueue_after(queue_name: str, priority: int = 0):
    """Decorador para enfileirar resultado de função"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)
            
            # Enfileirar resultado
            queue_manager = QueueManager()
            await queue_manager.enqueue(queue_name, {
                "function": func.__name__,
                "result": result,
                "args": args,
                "kwargs": kwargs,
                "timestamp": datetime.utcnow().isoformat()
            }, priority)
            
            return result
        return wrapper
    return decorator

# Inicialização do gerenciador de filas
def initialize_queue_manager() -> QueueManager:
    """Inicializa e retorna gerenciador de filas"""
    queue_manager = QueueManager()
    queue_manager.connect_redis()
    return queue_manager

# Função para iniciar workers de fila
async def start_queue_workers():
    """Inicia workers para processar filas"""
    queue_manager = initialize_queue_manager()
    
    # Iniciar workers para diferentes filas
    workers = [
        asyncio.create_task(
            queue_manager.process_queue(
                "documents",
                process_document_queue,
                timeout=5
            )
        ),
        asyncio.create_task(
            queue_manager.process_queue(
                "minutas", 
                process_minuta_queue,
                timeout=3
            )
        ),
        asyncio.create_task(
            queue_manager.process_queue(
                "notifications",
                process_notification_queue,
                timeout=2
            )
        )
    ]
    
    return workers

# Context manager para operações em lote na fila
class QueueBatch:
    """Context manager para operações em lote na fila"""
    def __init__(self, queue_manager: QueueManager, queue_name: str):
        self.queue_manager = queue_manager
        self.queue_name = queue_name
        self.batch_items = []
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if not exc_type:
            self._execute_batch()
    
    def add_item(self, item: Any, priority: int = 0):
        """Adiciona item ao lote"""
        self.batch_items.append((item, priority))
    
    def _execute_batch(self):
        """Executa todas as operações em lote"""
        for item, priority in self.batch_items:
            asyncio.create_task(
                self.queue_manager.enqueue(self.queue_name, item, priority)
            )