from typing import Dict, List, Any, Callable
from datetime import datetime, timedelta
import asyncio
import json
from pathlib import Path
import uuid

class TaskScheduler:
    def __init__(self, tasks_dir: str = "scheduled_tasks"):
        self.tasks_dir = Path(tasks_dir)
        self.tasks_dir.mkdir(exist_ok=True)
        self.scheduled_tasks = {}
        self.task_history = {}
        self.running = False
        self.registered_task_types = {}
    
    def register_task_type(self, task_type: str, task_function: Callable, description: str = ""):
        """Registra um tipo de tarefa"""
        self.registered_task_types[task_type] = {
            "function": task_function,
            "description": description,
            "registered_at": datetime.utcnow().isoformat()
        }
    
    def schedule_task(self, task_type: str, schedule: Dict[str, Any], parameters: Dict[str, Any] = None, task_name: str = None) -> str:
        """Agenda uma tarefa"""
        if task_type not in self.registered_task_types:
            raise ValueError(f"Tipo de tarefa não registrado: {task_type}")
        
        task_id = str(uuid.uuid4())
        
        task = {
            "task_id": task_id,
            "task_type": task_type,
            "task_name": task_name or f"Tarefa {task_type}",
            "schedule": schedule,
            "parameters": parameters or {},
            "created_at": datetime.utcnow().isoformat(),
            "status": "scheduled",
            "next_run": self._calculate_next_run(schedule),
            "last_run": None,
            "run_count": 0
        }
        
        self.scheduled_tasks[task_id] = task
        
        # Salvar tarefa em arquivo
        self._save_task(task)
        
        return task_id
    
    def _calculate_next_run(self, schedule: Dict[str, Any]) -> str:
        """Calcula próxima execução baseada no agendamento"""
        now = datetime.utcnow()
        
        if "interval_minutes" in schedule:
            interval = timedelta(minutes=schedule["interval_minutes"])
            next_run = now + interval
        elif "daily_at" in schedule:
            hour, minute = map(int, schedule["daily_at"].split(":"))
            next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            if next_run <= now:
                next_run += timedelta(days=1)
        elif "weekly_on" in schedule:
            next_run = now + timedelta(weeks=1)
        else:
            next_run = now + timedelta(hours=1)
        
        return next_run.isoformat()
    
    def _save_task(self, task: Dict[str, Any]):
        """Salva tarefa em arquivo"""
        task_file = self.tasks_dir / f"{task['task_id']}.json"
        with open(task_file, "w") as f:
            json.dump(task, f, indent=2)
    
    def load_tasks(self):
        """Carrega tarefas de arquivos"""
        for task_file in self.tasks_dir.glob("*.json"):
            try:
                with open(task_file, "r") as f:
                    task = json.load(f)
                self.scheduled_tasks[task["task_id"]] = task
            except Exception as e:
                print(f"Erro ao carregar tarefa {task_file}: {e}")
    
    def get_scheduled_tasks(self) -> List[Dict[str, Any]]:
        """Retorna tarefas agendadas"""
        return list(self.scheduled_tasks.values())
    
    def get_task(self, task_id: str) -> Dict[str, Any]:
        """Retorna uma tarefa específica"""
        return self.scheduled_tasks.get(task_id)
    
    def cancel_task(self, task_id: str) -> bool:
        """Cancela uma tarefa agendada"""
        if task_id in self.scheduled_tasks:
            task = self.scheduled_tasks[task_id]
            task["status"] = "cancelled"
            task["cancelled_at"] = datetime.utcnow().isoformat()
            self._save_task(task)
            return True
        return False
    
    def update_task_schedule(self, task_id: str, new_schedule: Dict[str, Any]) -> bool:
        """Atualiza agendamento de tarefa"""
        if task_id in self.scheduled_tasks:
            task = self.scheduled_tasks[task_id]
            task["schedule"] = new_schedule
            task["next_run"] = self._calculate_next_run(new_schedule)
            task["updated_at"] = datetime.utcnow().isoformat()
            self._save_task(task)
            return True
        return False
    
    async def start_scheduler(self):
        """Inicia o agendador"""
        self.running = True
        self.load_tasks()
        
        print("Agendador iniciado")
        
        while self.running:
            try:
                await self._check_and_run_tasks()
                await asyncio.sleep(60)
            except Exception as e:
                print(f"Erro no agendador: {e}")
                await asyncio.sleep(60)
    
    def stop_scheduler(self):
        """Para o agendador"""
        self.running = False
        print("Agendador parado")
    
    async def _check_and_run_tasks(self):
        """Verifica e executa tarefas agendadas"""
        now = datetime.utcnow()
        
        for task_id, task in self.scheduled_tasks.items():
            if task["status"] != "scheduled":
                continue
            
            next_run = datetime.fromisoformat(task["next_run"].replace("Z", "+00:00"))
            
            if now >= next_run:
                await self._run_task(task)
    
    async def _run_task(self, task: Dict[str, Any]):
        """Executa uma tarefa"""
        task_id = task["task_id"]
        task_type = task["task_type"]
        
        print(f"Executando tarefa {task_id} ({task_type})")
        
        task["status"] = "running"
        task["last_run"] = datetime.utcnow().isoformat()
        self._save_task(task)
        
        try:
            task_info = self.registered_task_types.get(task_type)
            if not task_info:
                raise ValueError(f"Função não encontrada para tipo {task_type}")
            
            task_function = task_info["function"]
            
            if asyncio.iscoroutinefunction(task_function):
                result = await task_function(**task["parameters"])
            else:
                result = task_function(**task["parameters"])
            
            task["status"] = "completed"
            task["last_result"] = result
            task["run_count"] += 1
            task["next_run"] = self._calculate_next_run(task["schedule"])
            
            print(f"Tarefa {task_id} concluída com sucesso")
            
        except Exception as e:
            task["status"] = "failed"
            task["last_error"] = str(e)
            print(f"Erro na tarefa {task_id}: {e}")
        
        self._save_task(task)
        self._add_to_history(task)
    
    def _add_to_history(self, task: Dict[str, Any]):
        """Adiciona tarefa ao histórico"""
        history_entry = {
            "task_id": task["task_id"],
            "task_type": task["task_type"],
            "status": task["status"],
            "run_at": task["last_run"],
            "result": task.get("last_result"),
            "error": task.get("last_error")
        }
        
        if task["task_id"] not in self.task_history:
            self.task_history[task["task_id"]] = []
        
        self.task_history[task["task_id"]].append(history_entry)
        
        # Manter apenas últimas 10 execuções
        if len(self.task_history[task["task_id"]]) > 10:
            self.task_history[task["task_id"]] = self.task_history[task["task_id"]][-10:]
    
    def get_task_history(self, task_id: str) -> List[Dict[str, Any]]:
        """Retorna histórico de uma tarefa"""
        return self.task_history.get(task_id, [])
    
    def run_task_now(self, task_id: str) -> bool:
        """Executa uma tarefa imediatamente"""
        task = self.scheduled_tasks.get(task_id)
        if not task:
            return False
        
        # Criar task assíncrona para execução
        asyncio.create_task(self._run_task(task))
        return True
    
    def get_task_types(self) -> List[Dict[str, Any]]:
        """Retorna tipos de tarefas registrados"""
        return [
            {
                "type": task_type,
                "description": info["description"],
                "registered_at": info["registered_at"]
            }
            for task_type, info in self.registered_task_types.items()
        ]

# Funções de tarefas comuns
async def backup_database_task(**kwargs):
    """Tarefa de backup do banco de dados"""
    print("Executando backup do banco de dados...")
    # Implementação real do backup
    return {"status": "success", "backup_size": "500MB"}

async def cleanup_temp_files_task(**kwargs):
    """Tarefa de limpeza de arquivos temporários"""
    print("Limpando arquivos temporários...")
    # Implementação real da limpeza
    return {"status": "success", "files_deleted": 42}

async def sync_external_data_task(**kwargs):
    """Tarefa de sincronização de dados externos"""
    print("Sincronizando dados externos...")
    # Implementação real da sincronização
    return {"status": "success", "records_synced": 150}

async def generate_reports_task(**kwargs):
    """Tarefa de geração de relatórios"""
    print("Gerando relatórios...")
    # Implementação real da geração de relatórios
    return {"status": "success", "reports_generated": 5}

# Inicialização do agendador
def initialize_scheduler():
    """Inicializa o agendador com tarefas padrão"""
    scheduler = TaskScheduler()
    
    # Registrar tipos de tarefas
    scheduler.register_task_type(
        "backup_database", 
        backup_database_task, 
        "Backup completo do banco de dados"
    )
    scheduler.register_task_type(
        "cleanup_temp_files", 
        cleanup_temp_files_task, 
        "Limpeza de arquivos temporários"
    )
    scheduler.register_task_type(
        "sync_external_data", 
        sync_external_data_task, 
        "Sincronização com sistemas externos"
    )
    scheduler.register_task_type(
        "generate_reports", 
        generate_reports_task, 
        "Geração de relatórios automáticos"
    )
    
    return scheduler