
import datetime as dtm
import logging
import os

from pyqqq.utils.logger import get_logger
from pyqqq.brokerage.ebest.oauth import EBestAuth
from pyqqq.brokerage.ebest.domestic_stock import EBestDomesticStock
from pyqqq.brokerage.ebest.simple import EBestSimpleDomesticStock
from pyqqq.brokerage.kis.oauth import KISAuth
from pyqqq.brokerage.kis.domestic_stock import KISDomesticStock
from pyqqq.brokerage.kis.simple import KISSimpleDomesticStock
from pyqqq.datatypes import OrderType
from pyqqq.backtest.wallclock import WallClock
from pyqqq.backtest.broker import MockBroker


class BaseStrategy:
    def __init__(
        self,
        backtest=False,
        brokerage='kis',
        paper_trading=False,
        position_provider=None,
        start_datetime=dtm.datetime.combine(dtm.date.today(), dtm.time(9, 0)),
        end_datetime=dtm.datetime.combine(dtm.date.today(), dtm.time(9, 0))
    ):
        """
        Args:
            backtest (bool, optional): 백테스트 모드 여부
            brokerage (str, optional): 거래소. kis, ebest.
            paper_trading (bool, optional): kis일 경우에만 유효.
            start_time (dtm.datetime, optional): 백테스트 시작 시간. 백테스트에서만 유효
            end_time (dtm.datetime, optional): 백테스트 종료 시간. 백테스트에서만 유효
        """

        self.logger = get_logger("Strategy")
        self.logger.setLevel(logging.DEBUG)
        self.position_provider = position_provider
        self.clock = WallClock(live_mode=not backtest, start_time=start_datetime, end_time=end_datetime)
        self.paper_broker_simple = None

        # auth
        if brokerage == 'kis':
            app_key = os.getenv("KIS_APP_KEY")
            app_secret = os.getenv("KIS_APP_SECRET")
            account_no = os.getenv("KIS_CANO")
            account_product_code = os.getenv("KIS_ACNT_PRDT_CD")

            self.auth = KISAuth(app_key, app_secret)
            self.broker = KISDomesticStock(self.auth)
            self.broker_simple = KISSimpleDomesticStock(self.auth, account_no, account_product_code)

            if paper_trading:
                paper_app_key = os.getenv("PAPER_KIS_APP_KEY")
                paper_app_secret = os.getenv("PAPER_KIS_APP_SECRET")
                paper_account_no = os.getenv("PAPER_KIS_CANO")
                paper_account_product_code = os.getenv("PAPER_KIS_ACNT_PRDT_CD")

                self.paper_auth = KISAuth(paper_app_key, paper_app_secret, paper_trading=True)
                self.paper_broker_simple = KISSimpleDomesticStock(self.paper_auth, paper_account_no, paper_account_product_code)

        elif brokerage == 'ebest':
            app_key = os.getenv("EBEST_APP_KEY")
            app_secret = os.getenv("EBEST_APP_SECRET")
            self.auth = EBestAuth(app_key, app_secret, paper_trading=paper_trading)
            self.broker = EBestDomesticStock(self.auth)
            self.broker_simple = EBestSimpleDomesticStock(self.auth)
            if paper_trading:
                self.paper_broker_simple = self.broker_simple

        self.use_mock_broker = backtest is True
        self.mock_broker = MockBroker(self.clock, self.broker_simple, self.position_provider)

    async def run(self):
        raise NotImplementedError

    def buy(self, code: str, order_type: OrderType, quantity: int, price: int):
        raise NotImplementedError

    def sell(self, code: str, quantity: int, price: int):
        raise NotImplementedError

    @property
    def order_broker(self):
        """ 주문에 사용할 Broker 반환 """
        if self.use_mock_broker:
            return self.mock_broker
        elif self.paper_broker_simple is not None:
            return self.paper_broker_simple
        else:
            return self.broker_simple

    def get_pending_orders(self):
        """미체결 주문 조회"""
        return self.order_broker.get_pending_orders()

    def get_positions(self):
        return self.order_broker.get_positions()

    def create_order(self, *args, **kwargs):
        return self.order_broker.create_order(*args, **kwargs)

    def update_order(self, *args, **kwargs):
        return self.order_broker.update_order(*args, **kwargs)

    def cancel_order(self, *args, **kwargs):
        return self.order_broker.cancel_order(*args, **kwargs)

    def debug(self, s):
        if self.clock.live_mode:
            self.logger.debug(s)
        else:
            print(f'{self.clock.now().strftime("%Y-%m-%d %H:%M:%S")} D {s}')
            pass

    def info(self, s):
        if self.clock.live_mode:
            self.logger.info(s)
        else:
            print(f'{self.clock.now().strftime("%Y-%m-%d %H:%M:%S")} I {s}')
