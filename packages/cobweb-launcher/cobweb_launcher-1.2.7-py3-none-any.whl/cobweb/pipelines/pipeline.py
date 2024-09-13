import time
import threading

from abc import ABC, abstractmethod
from cobweb.base import BaseItem, Queue, logger


class Pipeline(threading.Thread, ABC):

    def __init__(
            self,
            stop: threading.Event,
            pause: threading.Event,
            upload: Queue, done: Queue,
            upload_size: int,
            wait_seconds: int
    ):
        super().__init__()
        self._stop = stop
        self._pause = pause
        self._upload = upload
        self._done = done

        self.upload_size = upload_size
        self.wait_seconds = wait_seconds

    @abstractmethod
    def build(self, item: BaseItem) -> dict:
        pass

    @abstractmethod
    def upload(self, table: str, data: list) -> bool:
        pass

    def run(self):
        while not self._stop.is_set():
            status = self._upload.length < self.upload_size
            if status:
                time.sleep(self.wait_seconds)
            data_info, seeds = {}, []
            for _ in range(self.upload_size):
                item = self._upload.pop()
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
                    self._done.push(seeds)

        logger.info("upload pipeline close!")


