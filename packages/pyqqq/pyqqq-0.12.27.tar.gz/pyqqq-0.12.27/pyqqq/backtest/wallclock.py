import asyncio
import datetime as dtm
from typing import Optional


class WallClock:
    def __init__(self, live_mode: bool = True, start_time: Optional[dtm.datetime] = None, end_time: Optional[dtm.datetime] = None):
        self.live_mode = live_mode
        self.current_time = start_time
        self.end_time = end_time if end_time is not None else dtm.datetime.now()
        self.on_time_change = None

    def now(self) -> dtm.datetime:
        if self.live_mode:
            return dtm.datetime.now()
        else:
            if self.current_time > dtm.datetime.now():
                raise ValueError("backtesting time is must be less than current time")

            return self.current_time

    def today(self) -> dtm.date:
        return self.now().date()

    def is_alive(self) -> bool:
        if self.live_mode:
            return True
        else:
            return self.current_time <= self.end_time

    async def sleep(self, seconds: float):
        if self.live_mode:
            await asyncio.sleep(seconds)
        else:
            before = self.current_time
            self.current_time += dtm.timedelta(seconds=seconds)

            if self.on_time_change:
                self.on_time_change(self.current_time, before)
