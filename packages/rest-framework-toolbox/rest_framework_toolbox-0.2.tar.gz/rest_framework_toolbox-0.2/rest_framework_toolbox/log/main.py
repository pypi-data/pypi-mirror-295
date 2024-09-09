import threading
import logging
import queue

class LoggingService(threading.Thread):
    def __init__(self):
        super().__init__()
        self.log_queue = queue.Queue()
        self.daemon = True
        #self.start()
    
    def run(self):
        while True:
            record = self.log_queue.get()
            if record is None:
                break
            logger = logging.getLogger(record.name)
            logger.handle(record)
            self.log_queue.task_done()
    
    def log(self, level, msg, *args, **kwargs):
        self.log_queue.put(logging.LogRecord(level, msg, *args, **kwargs))