from fastapi import APIRouter
import psutil
import time
import threading

router = APIRouter(prefix="/blackrock/challenge/v1")


@router.get("/performance")
def performance():

    start = time.time()

    process = psutil.Process()
    mem = process.memory_info().rss / (1024 * 1024)

    duration = (time.time() - start) * 1000

    return {
        "time": f"{duration:.2f} ms",
        "memory": f"{mem:.2f} MB",
        "threads": threading.active_count(),
    }