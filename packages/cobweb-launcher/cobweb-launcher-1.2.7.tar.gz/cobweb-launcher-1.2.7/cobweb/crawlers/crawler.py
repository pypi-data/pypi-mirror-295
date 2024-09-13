import json
import threading
import time
import traceback
from inspect import isgenerator
from typing import Union, Callable, Mapping

from cobweb.constant import DealModel, LogTemplate
from cobweb.base import (
    Queue, 
    Seed, 
    BaseItem, 
    Request, 
    Response, 
    ConsoleItem,
    logger
)


class Crawler(threading.Thread):

    def __init__(
            self,
            stop: threading.Event,
            pause: threading.Event,
            launcher_queue: Union[Mapping[str, Queue]],
            custom_func: Union[Mapping[str, Callable]],
            thread_num: int,
            max_retries: int
    ):
        super().__init__()

        self._stop = stop
        self._pause = pause
        self._new = launcher_queue["new"]
        self._todo = launcher_queue["todo"]
        self._done = launcher_queue["done"]
        self._upload = launcher_queue["upload"]

        for func_name, _callable in custom_func.items():
            if isinstance(_callable, Callable):
                self.__setattr__(func_name, _callable)

        self.thread_num = thread_num
        self.max_retries = max_retries

    @staticmethod
    def request(seed: Seed) -> Union[Request, BaseItem]:
        yield Request(seed.url, seed, timeout=5)

    @staticmethod
    def download(item: Request) -> Union[Seed, BaseItem, Response, str]:
        response = item.download()
        yield Response(item.seed, response, **item.to_dict)

    @staticmethod
    def parse(item: Response) -> BaseItem:
        upload_item = item.to_dict
        upload_item["text"] = item.response.text
        yield ConsoleItem(item.seed, data=json.dumps(upload_item, ensure_ascii=False))

    # def get_seed(self) -> Seed:
    #     return self._todo.pop()

    def distribute(self, item, seed):
        if isinstance(item, BaseItem):
            self._upload.push(item)
        elif isinstance(item, Seed):
            self._new.push(item)
        elif isinstance(item, str) and item == DealModel.poll:
            self._todo.push(seed)
        elif isinstance(item, str) and item == DealModel.done:
            self._done.push(seed)
        elif isinstance(item, str) and item == DealModel.fail:
            seed.params.seed_status = DealModel.fail
            self._done.push(seed)
        else:
            raise TypeError("yield value type error!")

    def spider(self):
        while not self._stop.is_set():

            seed = self._todo.pop()

            if not seed:
                time.sleep(1)
                continue

            elif seed.params.retry > self.max_retries:
                seed.params.seed_status = DealModel.fail
                self._done.push(seed)
                continue

            seed_detail_log_info = LogTemplate.log_info(seed.to_dict)

            try:
                request_iterators = self.request(seed)

                if not isgenerator(request_iterators):
                    raise TypeError("request function isn't a generator!")

                iterator_status = False

                for request_item in request_iterators:

                    iterator_status = True

                    if isinstance(request_item, Request):
                        iterator_status = False
                        download_iterators = self.download(request_item)
                        if not isgenerator(download_iterators):
                            raise TypeError("download function isn't a generator")

                        for download_item in download_iterators:
                            iterator_status = True
                            if isinstance(download_item, Response):
                                iterator_status = False
                                logger.info(LogTemplate.download_info.format(
                                    detail=seed_detail_log_info,
                                    retry=seed.params.retry,
                                    priority=seed.params.priority,
                                    seed_version=seed.params.seed_version,
                                    identifier=seed.identifier or "",
                                    status=download_item.response,
                                    response=LogTemplate.log_info(download_item.to_dict)
                                ))
                                parse_iterators = self.parse(download_item)
                                if not isgenerator(parse_iterators):
                                    raise TypeError("parse function isn't a generator")
                                for parse_item in parse_iterators:
                                    iterator_status = True
                                    if isinstance(parse_item, Response):
                                        raise TypeError("upload_item can't be a Response instance")
                                    self.distribute(parse_item, seed)
                            else:
                                self.distribute(download_item, seed)
                    else:
                        self.distribute(request_item, seed)

                if not iterator_status:
                    raise ValueError("request/download/parse function yield value error!")
            except Exception as e:
                logger.info(LogTemplate.download_exception.format(
                    detail=seed_detail_log_info,
                    retry=seed.params.retry,
                    priority=seed.params.priority,
                    seed_version=seed.params.seed_version,
                    identifier=seed.identifier or "",
                    exception=''.join(traceback.format_exception(type(e), e, e.__traceback__))
                ))
                seed.params.retry += 1
                self._todo.push(seed)
            finally:
                time.sleep(0.1)
        logger.info("spider thread close")

    def run(self):
        for index in range(self.thread_num):
            threading.Thread(name=f"spider_{index}", target=self.spider).start()

