import pickle
from multiprocessing import Queue


_SHARED_QUEUE = None


def init_pool(queue: Queue):
    global _SHARED_QUEUE
    _SHARED_QUEUE = queue


def get_queue() -> Queue:
    return _SHARED_QUEUE


def send_to_queue(n: int, fig):

    if _SHARED_QUEUE is not None:
        _SHARED_QUEUE.put((n, pickle.dumps(fig)))
    else:
        raise RuntimeError("Queue not initialized in worker process")
