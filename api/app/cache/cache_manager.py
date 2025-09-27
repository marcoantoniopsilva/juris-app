from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import json
import redis
from app.core.config import settings

class CacheManager:
    def __init__(self):
        self.redis_client = None
        self.local_cache = {}
        self.cache_enabled = True
        
    def connect_redis(self):
        """Conecta ao Redis"""
        try:
            self.redis_client = redis.Redis.from_url(settings.REDIS_URL)
            self.redis_client.ping()
            print("Conectado ao Redis com sucesso")
            return True
        except Exception as e:
            print(f"Erro ao conectar ao Redis: {e}")
            self.cache_enabled = False
            return False
    
    def set(self, key: str, value: Any, expire_seconds: int = 3600) -> bool:
        """Armazena valor no cache"""
        if not self.cache_enabled:
            return False
        
        try:
            serialized_value = json.dumps(value)
            
            if self.redis_client:
                self.redis_client.setex(key, expire_seconds, serialized_value)
            else:
                # Fallback para cache local
                self.local_cache[key] = {
                    "value": serialized_value,
                    "expires_at": datetime.utcnow() + timedelta(seconds=expire_seconds)
                }
            return True
        except Exception as e:
            print(f"Erro ao armazenar no cache: {e}")
            return False
    
    def get(self, key: str) -> Optional[Any]:
        """Obtém valor do cache"""
        if not self.cache_enabled:
            return None
        
        try:
            if self.redis_client:
                cached_value = self.redis_client.get(key)
                if cached_value:
                    return json.loads(cached_value)
            else:
                # Fallback para cache local
                cached_item = self.local_cache.get(key)
                if cached_item and datetime.utcnow() < cached_item["expires_at"]:
                    return json.loads(cached_item["value"])
            return None
        except Exception as e:
            print(f"Erro ao obter do cache: {e}")
            return None
    
    def delete(self, key: str) -> bool:
        """Remove valor do cache"""
        if not self.cache_enabled:
            return False
        
        try:
            if self.redis_client:
                self.redis_client.delete(key)
            else:
                self.local_cache.pop(key, None)
            return True
        except Exception as e:
            print(f"Erro ao remover do cache: {e}")
            return False
    
    def clear(self) -> bool:
        """Limpa todo o cache"""
        if not self.cache_enabled:
            return False
        
        try:
            if self.redis_client:
                self.redis_client.flushdb()
            else:
                self.local_cache.clear()
            return True
        except Exception as e:
            print(f"Erro ao limpar cache: {e}")
            return False
    
    def get_with_fallback(self, key: str, fallback_func: callable, expire_seconds: int = 3600, *args, **kwargs) -> Any:
        """Obtém do cache ou executa função de fallback"""
        cached_value = self.get(key)
        if cached_value is not None:
            return cached_value
        
        # Executar função de fallback
        result = fallback_func(*args, **kwargs)
        
        # Armazenar no cache
        if result is not None:
            self.set(key, result, expire_seconds)
        
        return result
    
    def increment(self, key: str, amount: int = 1) -> Optional[int]:
        """Incrementa valor numérico no cache"""
        if not self.cache_enabled:
            return None
        
        try:
            if self.redis_client:
                return self.redis_client.incrby(key, amount)
            else:
                current = self.get(key) or 0
                new_value = current + amount
                self.set(key, new_value)
                return new_value
        except Exception as e:
            print(f"Erro ao incrementar no cache: {e}")
            return None
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do cache"""
        if self.redis_client:
            try:
                info = self.redis_client.info()
                return {
                    "used_memory": info.get("used_memory_human", "N/A"),
                    "keys": info.get("db0", {}).get("keys", 0),
                    "hits": info.get("keyspace_hits", 0),
                    "misses": info.get("keyspace_misses", 0),
                    "hit_rate": info.get("keyspace_hits", 0) / max(info.get("keyspace_misses", 1) + info.get("keyspace_hits", 1), 1)
                }
            except:
                return {"error": "Não foi possível obter estatísticas do Redis"}
        else:
            return {
                "local_cache_size": len(self.local_cache),
                "cache_enabled": self.cache_enabled
            }

# Decorador para cache automático
def cached(expire_seconds: int = 3600, key_prefix: str = ""):
    """Decorador para cache automático de funções"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            cache_manager = CacheManager()
            
            # Gerar chave única baseada na função e argumentos
            cache_key = f"{key_prefix}{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # Tentar obter do cache
            cached_result = cache_manager.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Executar função e armazenar resultado
            result = func(*args, **kwargs)
            if result is not None:
                cache_manager.set(cache_key, result, expire_seconds)
            
            return result
        return wrapper
    return decorator

# Context manager para operações em lote
class CacheBatch:
    """Context manager para operações em lote no cache"""
    def __init__(self, cache_manager: CacheManager):
        self.cache_manager = cache_manager
        self.batch_operations = []
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if not exc_type:
            self._execute_batch()
    
    def add_set(self, key: str, value: Any, expire_seconds: int = 3600):
        """Adiciona operação SET ao lote"""
        self.batch_operations.append(("set", key, value, expire_seconds))
    
    def add_delete(self, key: str):
        """Adiciona operação DELETE ao lote"""
        self.batch_operations.append(("delete", key))
    
    def _execute_batch(self):
        """Executa todas as operações em lote"""
        for operation in self.batch_operations:
            op_type, *args = operation
            if op_type == "set":
                self.cache_manager.set(*args)
            elif op_type == "delete":
                self.cache_manager.delete(*args)

# Função para gerar chaves de cache consistentes
def generate_cache_key(prefix: str, *args, **kwargs) -> str:
    """Gera chave de cache consistente"""
    key_parts = [prefix]
    
    # Adicionar argumentos posicionais
    for arg in args:
        if hasattr(arg, '__str__'):
            key_parts.append(str(arg))
        else:
            key_parts.append(repr(arg))
    
    # Adicionar argumentos nomeados
    for k, v in sorted(kwargs.items()):
        key_parts.append(f"{k}={v}")
    
    return ":".join(key_parts)

# Inicialização do gerenciador de cache
def initialize_cache() -> CacheManager:
    """Inicializa e retorna gerenciador de cache"""
    cache_manager = CacheManager()
    cache_manager.connect_redis()
    return cache_manager