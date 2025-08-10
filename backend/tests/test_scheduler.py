import time

import pytest

from app.services.stage8 import Stage8Service


@pytest.fixture()
def stage8_service() -> Stage8Service:
    return Stage8Service()


def test_scheduler_executes_tasks_in_order_and_respects_delay(stage8_service):
    execution = []
    start = time.time()

    def task1():
        execution.append(("t1", time.time()))

    def task2():
        execution.append(("t2", time.time()))

    stage8_service.scheduler(task1, delay=0.1)
    stage8_service.scheduler(task2)
    stage8_service.wait_for_all()

    assert [name for name, _ in execution] == ["t1", "t2"]
    assert execution[0][1] - start >= 0.1
