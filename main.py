import asyncio
import logging
import subprocess
from datetime import datetime

INTERVALO = 30 * 60  # 30 minutos

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(__name__)


async def run_tests():
    logger.info(f"\n[{datetime.now()}] Iniciando testes Playwright...")

    try:
        processo = subprocess.run(
            [
                "pytest",
                "tests/test_initial.py",
                # "tests/web/test_single_orders.py",
                # "tests/web/test_order_management.py",
                "tests/web/test_table_operations.py",
                "--html=reports/report.html",
                "--self-contained-html",
            ]
        )

        logger.info(f"STDOUT{processo.stdout}")

        # Erros, se houver
        logger.info(f"STDERR:{processo.stderr}")

        logger.info("Código de saída:", processo.returncode)
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
