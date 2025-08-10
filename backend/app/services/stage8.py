from typing import Any, Dict, List, Callable, Tuple, Optional
import threading
import time
from queue import Queue
from app.models.stage import StageResult


class Stage8Service:
    """Service layer for Stage 8 operations.

    Each request should create a fresh instance of this service to avoid
    leaking state between requests or tests.
    """

    def __init__(self) -> None:
        self.telemetry_log: List[Dict[str, Any]] = []
        self.current_plan: Dict[str, Any] = {"tasks": []}
        self._task_queue: "Queue[Tuple[Callable[[], Any], float]]" = Queue()
        self._worker_thread: Optional[threading.Thread] = None

    def telemetry(self, data: Dict[str, Any]) -> StageResult:
        self.telemetry_log.append(data)
        return StageResult(
            stage=8,
            status="telemetry received",
            data={"count": len(self.telemetry_log)},
        )

    def plan(self) -> StageResult:
        return StageResult(stage=8, status="current plan", data=self.current_plan)

    def scheduler(self, task: Callable[[], Any], delay: float = 0.0) -> None:
        """Schedule a task to be executed after an optional delay.

        Tasks are enqueued and processed by a background worker thread in the
        order they are received.

        Args:
            task: Callable with no arguments to execute.
            delay: Seconds to wait before executing the task.
        """
        self._task_queue.put((task, delay))
        self._start_worker()

    def _start_worker(self) -> None:
        if self._worker_thread is None or not self._worker_thread.is_alive():
            self._worker_thread = threading.Thread(
                target=self._process_queue, daemon=True
            )
            self._worker_thread.start()

    def _process_queue(self) -> None:
        while not self._task_queue.empty():
            func, delay = self._task_queue.get()
            if delay > 0:
                time.sleep(delay)
            func()
            self._task_queue.task_done()

    def wait_for_all(self, timeout: Optional[float] = None) -> None:
        """Block until all scheduled tasks have been processed."""
        self._task_queue.join()
        if self._worker_thread is not None:
            self._worker_thread.join(timeout=timeout)
