from typing import Any, Dict, List, Callable, Tuple, Optional
import threading
import time
from queue import Queue
from app.models.stage import StageResult

telemetry_log: List[Dict[str, Any]] = []
current_plan: Dict[str, Any] = {"tasks": []}

# internal queue for scheduled tasks
_task_queue: "Queue[Tuple[Callable[[], Any], float]]" = Queue()
_worker_thread: Optional[threading.Thread] = None


def telemetry(data: Dict[str, Any]) -> StageResult:
    telemetry_log.append(data)
    return StageResult(stage=8, status="telemetry received", data={"count": len(telemetry_log)})


def plan() -> StageResult:
    return StageResult(stage=8, status="current plan", data=current_plan)


def scheduler(task: Callable[[], Any], delay: float = 0.0) -> None:
    """Schedule a task to be executed after an optional delay.

    Tasks are enqueued and processed by a background worker thread in the
    order they are received.

    Args:
        task: Callable with no arguments to execute.
        delay: Seconds to wait before executing the task.
    """
    _task_queue.put((task, delay))
    _start_worker()


def _start_worker() -> None:
    global _worker_thread
    if _worker_thread is None or not _worker_thread.is_alive():
        _worker_thread = threading.Thread(target=_process_queue, daemon=True)
        _worker_thread.start()


def _process_queue() -> None:
    while not _task_queue.empty():
        func, delay = _task_queue.get()
        if delay > 0:
            time.sleep(delay)
        func()
        _task_queue.task_done()


def wait_for_all(timeout: Optional[float] = None) -> None:
    """Block until all scheduled tasks have been processed."""
    _task_queue.join()
    if _worker_thread is not None:
        _worker_thread.join(timeout=timeout)
