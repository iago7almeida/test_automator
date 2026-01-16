import time
import csv
import functools
from datetime import datetime
from contextlib import contextmanager

class PerformanceTracker:
    _records = []

    @classmethod
    def record(cls, action_name, duration, status="SUCCESS", error_msg=""):
        """
        Salva o registro com status e mensagem de erro (se houver).
        """
        cls._records.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "action": action_name,
            "duration_seconds": round(duration, 4),
            "status": status,
            "error_message": error_msg
        })

    @classmethod
    def generate_report(cls, filename="relatorio_performance_global.csv"):
        if not cls._records: return
        fieldnames = ["timestamp", "action", "duration_seconds", "status", "error_message"]
        
        with open(filename, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(cls._records)
        
        print(f"\n📊 Relatório salvo em: {filename}")

# --- Context Manager (Uso manual com 'with measure...') ---
@contextmanager
def measure(step_name: str):
    start = time.time()
    status = "SUCCESS"
    error_msg = ""
    try:
        yield
    except Exception as e:
        status = "ERROR"
        error_msg = str(e).split('\n')[0] 
        raise 
    finally:
        duration = time.time() - start
        PerformanceTracker.record(step_name, duration, status, error_msg)

# --- Decorador (Uso automático nas classes) ---
def auto_measure_func(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        class_name = args[0].__class__.__name__ if args else ""
        action_name = f"{class_name}.{func.__name__}"
        
        start = time.time()
        status = "SUCCESS"
        error_msg = ""
        
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            status = "ERROR"
            error_msg = str(e).replace("\n", " ")[:200] 
            raise
        finally:
            duration = time.time() - start
            PerformanceTracker.record(action_name, duration, status, error_msg)
            
    return wrapper