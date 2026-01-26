import asyncio
import logging
import subprocess
import os
from datetime import datetime

INTERVALO = 30 * 60  # 30 minutos

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(__name__)


async def run_tests():
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
            ],
            check=True,
        )

        if os.path.exists("allure-results"):
            subprocess.run(
                [
                    "allure",
                    "generate",
                    "allure-results",
                    "-o",
                    "allure-report",
                    "--clean",
                ],
                check=True,
            )
            logger.info(f"[{datetime.now()}] Relatório Allure gerado com sucesso ✅")

        logger.info(f"[{datetime.now()}] Testes finalizados com sucesso ✅")

    except subprocess.CalledProcessError as e:
        logger.error(f"[{datetime.now()}] Testes falharam ❌ Código: {e.returncode}")

    except Exception as e:
        logger.error(f"[{datetime.now()}] Erro ao rodar testes: {e}")

async def test_execution_routine():
    subprocess.Popen(
        ["allure", "open", "allure-report", "-p", "8080", "-h", "0.0.0.0"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    while True:
        await run_tests()
        logger.info(f"[{datetime.now()}] Aguardando 30 minutos...\n")
        await asyncio.sleep(INTERVALO)


if __name__ == "__main__":
    asyncio.run(test_execution_routine())
