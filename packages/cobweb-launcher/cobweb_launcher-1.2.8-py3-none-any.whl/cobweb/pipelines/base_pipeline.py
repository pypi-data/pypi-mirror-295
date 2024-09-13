import time
import threading

from abc import ABC, abstractmethod
from cobweb.base import BaseItem, Queue, logger


class Pipeline(threading.Thread, ABC):

    def __init__(
            self,
            done_queue: Queue,
            upload_queue: Queue,
            upload_queue_size: int,
            upload_wait_seconds: int
    ):
        super().__init__()
        self.done_queue = done_queue
        self.upload_queue = upload_queue
        self.upload_queue_size = upload_queue_size
        self.upload_wait_seconds = upload_wait_seconds

    @abstractmethod
    def build(self, item: BaseItem) -> dict:
        pass

    @abstractmethod
    def upload(self, table: str, data: list) -> bool:
        pass

    def run(self):
        while True:
            status = self.upload_queue.length < self.upload_queue_size
            if status:
                time.sleep(self.upload_wait_seconds)
            data_info, seeds = {}, []
            for _ in range(self.upload_queue_size):
                item = self.upload_queue.pop()
                if not item:
                    break
                data = self.build(item)
                seeds.append(item.seed)
                data_info.setdefault(item.table, []).append(data)
            for table, datas in data_info.items():
                try:
                    self.upload(table, datas)
                    status = True
                except Exception as e:
                    logger.info(e)
                    status = False
                if status:
                    self.done_queue.push(seeds)


