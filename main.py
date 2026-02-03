import asyncio
import logging
import subprocess
import os
from datetime import datetime
from subprocess import Popen
from typing import Optional

INTERVALO = 30 * 60  # 30 minutos

allure_process: Optional[Popen] = None

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(__name__)


async def run_tests():
    global allure_process
    logger.info(f"\n[{datetime.now()}] Iniciando testes Playwright...")

    try:
        subprocess.run(
            [
                "pytest",
                "tests/test_initial.py",
                "tests/web/test_single_orders.py",
                "tests/web/test_order_management.py",
                "tests/web/test_table_operations.py",
                "--alluredir=allure-results"
            ]
        )

        if os.path.exists("allure-results"):
            subprocess.run(
                [
                    "npx",
                    "allure",
                    "generate",
                    "allure-results"
                ]
            )
            logger.info(f"[{datetime.now()}] Relatório Allure gerado com sucesso ✅")
            if allure_process is not None:
                        if allure_process.poll() is None:
                            logger.info("Encerrando servidor Allure antigo...")
                            allure_process.terminate()
                            allure_process.wait()

            if os.path.exists("allure-report"):
                allure_process = subprocess.Popen(
                    ["npx", "allure", "open", "allure-report", "--port", "8080"]
                )

        logger.info(f"[{datetime.now()}] Testes finalizados com sucesso ✅")

    except subprocess.CalledProcessError as e:
        logger.error(f"[{datetime.now()}] Testes falharam ❌ Código: {e.returncode}")

    except Exception as e:
        logger.error(f"[{datetime.now()}] Erro ao rodar testes: {e}")

async def test_execution_routine():
    while True:
        await run_tests()
        logger.info(f"[{datetime.now()}] Aguardando 30 minutos...\n")
        await asyncio.sleep(INTERVALO)


if __name__ == "__main__":
    asyncio.run(test_execution_routine())
