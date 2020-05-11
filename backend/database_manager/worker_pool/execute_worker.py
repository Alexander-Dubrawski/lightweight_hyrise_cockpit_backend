"""Functions defining execute workers."""
from multiprocessing import Queue, Value
from multiprocessing.synchronize import Event as EventType
from queue import Empty
from time import sleep


def execute_queries(
    task_queue: Queue,
    continue_execution_flag: Value,
    i_am_done_event: EventType,
    worker_wait_for_exit_event: EventType,
) -> None:
    """Define workers work loop."""
    while True:
        if not continue_execution_flag.value:
            i_am_done_event.set()
            worker_wait_for_exit_event.wait()
        try:
            _ = task_queue.get(block=False)
            # Do some work
            sleep(0.001)
        except Empty:
            continue
