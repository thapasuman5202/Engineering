import os
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from app.services import stage8


def test_scheduler_executes_tasks_in_order_and_respects_delay():
    execution = []
    start = time.time()

    def task1():
        execution.append(("t1", time.time()))

    def task2():
        execution.append(("t2", time.time()))

    stage8.scheduler(task1, delay=0.1)
    stage8.scheduler(task2)
    stage8.wait_for_all()

    assert [name for name, _ in execution] == ["t1", "t2"]
    assert execution[0][1] - start >= 0.1
