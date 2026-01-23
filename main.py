import asyncio
import subprocess
from datetime import datetime

INTERVALO = 30 * 60  # 30 minutos


async def rodar_testes():
    print(f"\n[{datetime.now()}] Iniciando testes Playwright...")

    try:
        processo = subprocess.run(
            [
                "pytest", 
                "tests/test_initial.py",
                "tests/web/test_single_orders.py",
                "tests/web/test_order_management.py",
                "tests/web/test_table_operations.py",
                "--html=reports/report.html", 
                "--self-contained-html"
            ],
            check=True,
        )
        print(f"[{datetime.now()}] Testes finalizados com sucesso ✅")

    except subprocess.CalledProcessError as e:
        print(f"[{datetime.now()}] Testes falharam ❌ Código: {e.returncode}")

    except Exception as e:
        print(f"[{datetime.now()}] Erro ao rodar testes: {e}")


async def loop_infinito():
    while True:
        await rodar_testes()
        print(f"[{datetime.now()}] Aguardando 30 minutos...\n")
        await asyncio.sleep(INTERVALO)


if __name__ == "__main__":
    asyncio.run(loop_infinito())
