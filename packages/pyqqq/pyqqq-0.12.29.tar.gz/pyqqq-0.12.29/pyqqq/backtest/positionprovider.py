import os
import datetime as dtm
import requests
import logging
from decimal import Decimal

import pyqqq
from pyqqq.utils.market_schedule import get_last_trading_day
from pyqqq.datatypes import StockPosition
from pyqqq.brokerage.kis.simple import KISSimpleDomesticStock
from pyqqq.utils.logger import get_logger
from typing import List


class BasePositionProvider:

    def __init__(
        self,
        brokerage: str = 'kis',
        api_key: str = None,
        account_no: str = None,
    ):
        self.brokerage = brokerage
        self.api_key = api_key or pyqqq.get_api_key()
        # ebest는 account_no가 api를 통해 얻어올 수 있으므로 따로 env로 관리하지 않음. 따라서 직접 기입해야 함.
        self.account_no = account_no or (os.getenv('KIS_CANO') + os.getenv('KIS_ACNT_PRDT_CD')) if brokerage == 'kis' else None

    def get_positions(self, date: dtm.date) -> List[StockPosition]:
        return []


class KISPositionProvider(BasePositionProvider):
    def __init__(
        self,
        api_key: str = None,
        account_no: str = None,
    ):
        super().__init__(brokerage='kis', api_key=api_key, account_no=account_no)

    def get_positions(self, date: dtm.date) -> List[StockPosition]:
        broker = KISSimpleDomesticStock(api_key=self.api_key, account_no=self.account_no)
        positions = broker.get_positions()
        return positions


class ManualPositionProvider(BasePositionProvider):
    """
    백테스팅용 포지션 정보를 직접 업데이트 하는 클래스
    """
    def __init__(
        self,
        positions: List[StockPosition]
    ):
        self.positions = positions or []

    def update_positions(self, positions: List[StockPosition]):
        self.positions = positions

    def get_positions(self, date: dtm.date) -> List[StockPosition]:
        return self.positions or []


class BackPositionProvider(BasePositionProvider):
    """
    DB에 저장된 포지션 정보를 가져오는 클래스
    """
    def __init__(
        self,
        brokerage: str = 'kis',
        api_key: str = None,
        account_no: str = None,
    ):
        super().__init__(brokerage=brokerage, api_key=api_key, account_no=account_no)
        self.logger = get_logger("BackPositionProvider")
        self.logger.setLevel(logging.DEBUG)

    def get_positions(self, date: dtm.date) -> List[StockPosition]:
        target_date = get_last_trading_day(date)
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }
        params = {
            "date": target_date.strftime("%Y%m%d"),
            "brokerage": self.brokerage,
            "account_no": self.account_no,
        }
        r = requests.get("https://pyqqq.net/api/analytics/positions", headers=headers, params=params)
        if r.status_code == 404:
            self.logger.debug(f"404 request error: {r.text}")
            return []

        r.raise_for_status()

        data = r.json()
        positions = []
        for p in data['positions']:
            pos = StockPosition(
                asset_code=p["asset_code"],
                asset_name=p["asset_name"],
                quantity=p["quantity"],
                sell_possible_quantity=p["sell_possible_quantity"],
                average_purchase_price=Decimal(p["average_purchase_price"]),
                current_price=p["current_price"],
                current_value=p["current_value"],
                current_pnl=Decimal(p["current_pnl"]),
                current_pnl_value=p["current_pnl_value"],
            )
            positions.append(pos)

        return positions
