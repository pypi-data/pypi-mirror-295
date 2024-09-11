import logging
from queue import Queue
from threading import Thread
from concurrent_log_handler import ConcurrentRotatingFileHandler


class AsyncConcurrentRotatingFileHandler(ConcurrentRotatingFileHandler):
    """多进程异步、加锁写入日志文件，在工程关闭时，可能会丢失日志"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._queue = Queue()
        self._thread = Thread(target=self._monitor)
        self._thread.daemon = True
        self._thread.start()

    def emit(self, record: logging.LogRecord):
        try:
            self._queue.put_nowait(record)
        except Exception:
            self.handleError(record)

    def _monitor(self):
        while True:
            record = self._queue.get()
            try:
                super().emit(record)
            except:  # noqa
                pass
