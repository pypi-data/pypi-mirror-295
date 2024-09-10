from datetime import datetime
import time
from typing import AsyncIterable, Iterator
import sys
import asyncio
from fastapi import APIRouter

router = APIRouter()
test_router = router


class SlowSyncIterator:
    iter_time: int = 0
    max: int
    order: int

    def __init__(self, order, loop: int = 3):
        self.max = loop
        self.order = order

    def __iter__(self):
        return self

    def __next__(self):
        time.sleep(1)  # Simulating a time-consuming operation
        self.iter_time += 1
        print('slow_iter:', self.order, '-',  self.iter_time)
        print(datetime.now())
        if self.iter_time > self.max:
            print('__next__ raise StopIteration')
            raise StopIteration
        return self.iter_time


def next_item(sync_iter: Iterator):
    try:
        return next(sync_iter)
    except StopIteration:
        return StopIteration


async def iterator_to_async_iterable(sync_iter: Iterator) -> AsyncIterable:
    loop = asyncio.get_running_loop()
    while True:
        item = await asyncio.to_thread(next_item, sync_iter)
        if item is StopIteration:
            break
        yield item
        await asyncio.sleep(0)  # Allow other tasks to run


class TestService:
    @staticmethod
    def sleep(order: int = 0, t: int = 2):
        time.sleep(t)  # 模拟一个耗时操作
        print('sleep', order, '-', t)
        print(datetime.now())
        return order

    @staticmethod
    async def async_slow_iter(order: int, loop: int = 3):
        sync_iter = SlowSyncIterator(order, loop)
        async_iter = iterator_to_async_iterable(iter(sync_iter))
        final: int
        async for item in async_iter:
            print('async', datetime.now())
            final = item
        return final

    @staticmethod
    def slow_iter(order: int, loop: int = 3):
        sync_iter = SlowSyncIterator(order, loop)
        final: int
        for item in sync_iter:
            final = item
        return final

    @staticmethod
    async def async_sleep(order: int = 0, t: int = 2) -> int:
        def run():
            return TestService.sleep(order, t)
        return await asyncio.to_thread(run)


async def main() -> int:
    """主函数，测试各种同步和异步操作"""
    # TestService.slow_iter(7, 3)
    await asyncio.gather(
        TestService.async_sleep(0),
        TestService.async_sleep(1),
        TestService.async_sleep(2),
        TestService.async_sleep(3),
        TestService.async_sleep(4),
        TestService.async_sleep(5),
        TestService.async_sleep(6),
        TestService.async_sleep(7),
        # TestService.async_slow_iter(8, 3),
        # TestService.async_slow_iter(9, 3)
    )
    return 0

if __name__ == '__main__':
    # 运行主函数
    asyncio.run(main())
