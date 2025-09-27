from typing import Dict, Any, Optional
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
import traceback
import logging
from datetime import datetime

class ErrorHandler:
    def __init__(self):
        self.logger = logging.getLogger("error_handler")
        self.error_codes = self._load_error_codes()
    
    def _load_error_codes(self) -> Dict[int, Dict[str, Any]]:
        """Carrega códigos de erro padrão"""
        return {
            400: {
                "message": "Requisição inválida",
                "description": "Os parâmetros fornecidos são inválidos ou estão faltando"
            },
            401: {
                "message": "Não autorizado",
                "description": "Autenticação necessária para acessar este recurso"
            },
            403: {
                "message": "Proibido",
                "description": "Você não tem permissão para acessar este recurso"
            },
            404: {
                "message": "Não encontrado",
                "description": "O recurso solicitado não foi encontrado"
            },
            500: {
                "message": "Erro interno do servidor",
                "description": "Ocorreu um erro interno no servidor"
            },
            503: {
                "message": "Serviço indisponível",
                "description": "O serviço está temporariamente indisponível"
            }
        }
    
    def create_error_response(self, 
                            status_code: int, 
                            message: Optional[str] = None,
                            details: Optional[Dict[str, Any]] = None,
                            error_code: Optional[str] = None) -> Dict[str, Any]:
        """Cria resposta de erro padronizada"""
        error_info = self.error_codes.get(status_code, {
            "message": "Erro desconhecido",
            "description": "Ocorreu um erro não especificado"
        })
        
        response = {
            "error": {
                "code": status_code,
                "message": message or error_info["message"],
                "description": error_info["description"],
                "timestamp": datetime.utcnow().isoformat(),
                "error_code": error_code or f"ERR_{status_code}"
            }
        }
        
        if details:
            response["error"]["details"] = details
        
        return response
    
    def handle_http_exception(self, request: Request, exc: HTTPException) -> JSONResponse:
        """Manipula exceções HTTP"""
        error_response = self.create_error_response(
            exc.status_code,
            exc.detail,
            {"path": request.url.path}
        )
        
        self.logger.warning(
            f"HTTP Error {exc.status_code}: {exc.detail} - Path: {request.url.path}"
        )
        
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response
        )
    
    def handle_generic_exception(self, request: Request, exc: Exception) -> JSONResponse:
        """Manipula exceções genéricas"""
        # Logar erro completo
        error_traceback = traceback.format_exc()
        self.logger.error(
            f"Unhandled exception: {str(exc)}\nTraceback:\n{error_traceback}"
        )
        
        error_response = self.create_error_response(
            500,
            "Erro interno do servidor",
            {
                "path": request.url.path,
                "exception_type": exc.__class__.__name__
            },
            "ERR_INTERNAL"
        )
        
        return JSONResponse(
            status_code=500,
            content=error_response
        )
    
    def log_error(self, 
                 error: Exception, 
                 context: Optional[Dict[str, Any]] = None,
                 level: str = "error"):
        """Registra erro com contexto"""
        error_info = {
            "exception_type": error.__class__.__name__,
            "error_message": str(error),
            "timestamp": datetime.utcnow().isoformat(),
            "traceback": traceback.format_exc()
        }
        
        if context:
            error_info["context"] = context
        
        log_message = f"Error: {error.__class__.__name__} - {str(error)}"
        
        if level == "warning":
            self.logger.warning(log_message, extra=error_info)
        else:
            self.logger.error(log_message, extra=error_info)
    
    def create_custom_error(self, 
                           error_code: str, 
                           message: str, 
                           status_code: int = 400,
                           details: Optional[Dict[str, Any]] = None) -> HTTPException:
        """Cria exceção HTTP personalizada"""
        error_data = self.create_error_response(status_code, message, details, error_code)
        return HTTPException(
            status_code=status_code,
            detail=error_data
        )
    
    def validate_request_data(self, data: Dict[str, Any], required_fields: list) -> Optional[Dict[str, Any]]:
        """Valida dados da requisição"""
        missing_fields = []
        invalid_fields = []
        
        for field in required_fields:
            if field not in data:
                missing_fields.append(field)
            elif data[field] is None or data[field] == "":
                invalid_fields.append(field)
        
        errors = {}
        if missing_fields:
            errors["missing_fields"] = missing_fields
        if invalid_fields:
            errors["invalid_fields"] = invalid_fields
        
        if errors:
            return self.create_error_response(
                400,
                "Dados da requisição inválidos",
                errors,
                "ERR_VALIDATION"
            )
        
        return None

# Decorador para tratamento de erros em funções
def error_handler(log_context: bool = True):
    """Decorador para tratamento automático de erros"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            handler = ErrorHandler()
            try:
                return func(*args, **kwargs)
            except HTTPException:
                raise
            except Exception as e:
                context = {}
                if log_context:
                    context = {
                        "function": func.__name__,
                        "args": str(args),
                        "kwargs": str(kwargs)
                    }
                handler.log_error(e, context)
                raise handler.create_custom_error(
                    "ERR_FUNCTION",
                    f"Erro na execução da função {func.__name__}",
                    500,
                    {"exception": str(e)}
                )
        return wrapper
    return decorator

# Context manager para blocos de código com tratamento de erro
class ErrorContext:
    """Context manager para tratamento de erros em blocos de código"""
    def __init__(self, context_name: str, raise_exception: bool = True):
        self.context_name = context_name
        self.raise_exception = raise_exception
        self.handler = ErrorHandler()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None and exc_type != HTTPException:
            self.handler.log_error(
                exc_val,
                {"context": self.context_name},
                "error" if self.raise_exception else "warning"
            )
            
            if self.raise_exception:
                raise self.handler.create_custom_error(
                    "ERR_CONTEXT",
                    f"Erro no contexto {self.context_name}",
                    500,
                    {"exception": str(exc_val)}
                )
        
        # Retornar True para indicar que a exceção foi tratada
        return True

# Função para registro de erros de validação
def log_validation_errors(errors: list, context: Dict[str, Any] = None):
    """Registra erros de validação"""
    handler = ErrorHandler()
    error_data = {
        "validation_errors": errors,
        "context": context or {}
    }
    handler.logger.warning("Validation errors occurred", extra=error_data)

# Inicialização do manipulador de erros
def initialize_error_handler() -> ErrorHandler:
    """Inicializa e retorna manipulador de erros"""
    return ErrorHandler()