import datetime as dtm
import pandas as pd
import numpy as np
import logging
from dataclasses import asdict
from decimal import Decimal
from functools import lru_cache
from typing import Optional
from pyqqq.backtest.wallclock import WallClock
from pyqqq.data.daily import get_ohlcv_by_codes_for_period
from pyqqq.data.domestic import get_ticker_info
from pyqqq.data.minutes import get_all_day_data
from pyqqq.data.realtime import get_all_last_trades
from pyqqq.datatypes import OrderSide, OrderType, TradingHistory, StockOrder, StockPosition
from pyqqq.utils.logger import get_logger
from pyqqq.utils.market_schedule import get_trading_day_with_offset


class BaseBroker:
    def __init__(self, clock, simple_api, position_provider):
        pass

    def get_minute_price(self, code) -> pd.DataFrame:
        raise NotImplementedError

    def get_price(self, code):
        raise NotImplementedError

    def get_pending_orders(self):
        raise NotImplementedError

    def get_positions(self):
        raise NotImplementedError

    def create_order(self, asset_code: str, side: OrderSide, quantity: int, order_type: OrderType = OrderType.MARKET, price: int = 0):
        raise NotImplementedError

    def update_order(self, org_order_no: str, order_type: OrderType, price: int, quantity: int = 0):
        raise NotImplementedError

    def cancel_order(self, order_no: str, quantity: int = 0):
        raise NotImplementedError


# 모의 계좌나 실제 계좌로 트레이딩 할때 사용되는 브로커
class TradingBroker(BaseBroker):
    def __init__(self, clock: WallClock, simple_api, position_provider):
        super().__init__(clock, simple_api, position_provider)
        self.logger = get_logger('TradingBroker')
        self.logger.setLevel(logging.DEBUG)
        self.clock = clock
        self.clock.on_time_change = self.on_time_change

        self.simple_api = simple_api
        self.next_order_no = 1000
        account = simple_api.get_account()
        self.cash = account["total_balance"] - account["evaluated_amount"]
        self.pending_orders = []
        self.trading_history = []
        self.position_provider = position_provider
        self.positions = position_provider.get_positions(self.clock.today()) if position_provider else []

    def get_minute_price(self, code) -> pd.DataFrame:
        return self.simple_api.get_today_minute_data(code)

    def get_price(self, code):
        return self.simple_api.get_price(code)

    def get_pending_orders(self):
        return self.simple_api.pending_orders

    def get_positions(self):
        return self.simple_api.get_positions()

    def create_order(self, asset_code: str, side: OrderSide, quantity: int, order_type: OrderType = OrderType.MARKET, price: int = 0):
        return self.simple_api.create_order(asset_code, side, quantity, order_type, price)

    def update_order(self, org_order_no: str, order_type: OrderType, price: int, quantity: int = 0):
        return self.simple_api.update_order(org_order_no, order_type, price, quantity)

    def cancel_order(self, order_no: str, quantity: int = 0):
        return self.simple_api.cancel_order(order_no, quantity)


# 백테스팅 할때 사용되는 브로커
class MockBroker(BaseBroker):
    DBG_POSTFIX = ""

    def __init__(self, clock: WallClock, simple_api, position_provider, time_unit="minutes"):
        self.logger = get_logger('MockBroker')
        self.logger.setLevel(logging.DEBUG)
        self.clock = clock
        self.clock.on_time_change = self.on_time_change

        self.simple_api = simple_api
        self.next_order_no = 1000
        self.cash = 1_000_000_000
        self.pending_orders = []
        self.trading_history = []
        self.position_provider = position_provider
        self.positions = position_provider.get_positions(self.clock.today()) if position_provider else []
        self.time_unit = time_unit

        self.logger.debug(f"positions: {self.positions}")

    def set_initial_cash(self, cash):
        self.cash = cash

    def increase_cash(self, amount):
        self.cash += amount

    def decrease_cash(self, amount):
        self.cash -= amount

    def get_daily_price(self, code: str, from_date: Optional[dtm.date] = None, end_date: Optional[dtm.date] = None):

        if from_date is None:
            from_date = get_trading_day_with_offset(self.clock.today(), -10)
        if end_date is None:
            end_date = self.clock.today()

        if self.clock.live_mode:
            df = self.simple_api.get_historical_daily_data(code, from_date, end_date, adjusted_price=True)
        else:
            dfs = get_ohlcv_by_codes_for_period([code], from_date, end_date, adjusted=True)
            df = dfs[code]

        return df.iloc[::-1].copy()

    def get_minute_price(self, code) -> pd.DataFrame:
        if self.clock.live_mode:
            df = self._get_today_minute_price(code)
        else:
            df = self._get_minute_price_with_cache(self.clock.today(), code)

        return df[df['time'] <= self.clock.now()].copy()

    @lru_cache(maxsize=40)
    def _get_minute_price_with_cache(self, date, code) -> pd.DataFrame:
        if dtm.datetime.now().date() == date:
            return self._get_today_minute_price(code)
        else:
            dfs = get_all_day_data(date, [code], dtm.timedelta(minutes=1))
            df = dfs[code]
            df = df[['open', 'high', 'low', 'close', 'volume']].copy()
            df.reset_index(inplace=True)

            return df

    def _get_today_minute_price(self, code) -> pd.DataFrame:
        broker = self.simple_api.stock_api

        """
        분봉 데이터 조회

        Args:
            code (str): 종목코드

        Returns:
            pd.DataFrame: 분봉 데이터
        """
        now = dtm.datetime.now()
        time = now.time()
        minute_data = []

        while True:
            result = broker.inquire_time_itemchartprice(code, time, fid_pw_data_incu_yn="N")
            if len(result["output2"]) == 0:
                break

            for data in result["output2"]:
                minute_data.append(
                    {
                        "time": dtm.datetime.combine(data["stck_bsop_date"], data["stck_cntg_hour"]),
                        "open": data["stck_oprc"],
                        "high": data["stck_hgpr"],
                        "low": data["stck_lwpr"],
                        "close": data["stck_prpr"],
                        "volume": data["cntg_vol"],
                    }
                )
            last_item_time = minute_data[-1]["time"]
            request_time = last_item_time - dtm.timedelta(minutes=1)
            if request_time.time() < dtm.time(9, 0):
                break

            time = request_time.time()

        minute_data.reverse()

        df = pd.DataFrame(minute_data)
        return df

    def get_price(self, code):
        if self.clock.live_mode:
            cache_key = self.clock.now().replace(second=0, microsecond=0)
            df = self._get_live_price_with_cache(cache_key)
            return df.loc[code, 'price']
        else:
            if self.time_unit == "minutes":
                df = self.get_minute_price(code)
                return int(df["open"].iloc[-1])
            elif self.time_unit == "days":
                df = self.get_daily_price(code, self.clock.today(), self.clock.today())
                return int(df["close"].iloc[-1])
            else:
                raise ValueError(f"Invalid time unit: {self.time_unit}")

    @lru_cache(maxsize=2)
    def _get_live_price_with_cache(self, cache_key):
        trades = get_all_last_trades()
        df = pd.DataFrame(trades)
        df.set_index('shcode', inplace=True)
        return df

    def get_pending_orders(self):
        return self.pending_orders

    def get_positions(self):
        for p in self.positions:
            price = self.get_price(p.asset_code)
            p.current_price = price
            p.current_value = price * p.quantity
            p.current_pnl_value = int((price - p.average_purchase_price) * p.quantity)
            p.current_pnl = Decimal(0) if p.quantity == 0 else Decimal((p.current_pnl_value / (p.average_purchase_price * p.quantity)) * 100).quantize(Decimal("0.00"))

            print(f"code={p.asset_code} price={price} buy_price={p.average_purchase_price:.1f} quantity={p.quantity} current_value={p.current_value} current_pnl={p.current_pnl}")

        positions = [p for p in self.positions if p.quantity > 0]
        return positions

    def create_order(self, asset_code: str, side: OrderSide, quantity: int, order_type: OrderType = OrderType.MARKET, price: int = 0):
        price = self.get_price(asset_code) if order_type == OrderType.MARKET else price
        order_no = str(self.next_order_no)
        self.next_order_no += 1

        if side is OrderSide.BUY:
            total_amount = int(price * quantity * 1.00015)
            if self.cash < total_amount:
                raise ValueError("not enough cash")
            else:
                self.decrease_cash(total_amount)

        if isinstance(price, np.int64):
            raise ValueError(f"price must be int, not np.int64: {price} {type(price)}")

        order = StockOrder(
            order_no=order_no,
            asset_code=asset_code,
            side=side,
            price=price,
            quantity=quantity,
            filled_quantity=0,
            pending_quantity=quantity,
            order_type=order_type,
            order_time=self.clock.now(),
        )

        self.pending_orders.append(order)

        return order_no

    def update_order(self, org_order_no: str, order_type: OrderType, price: int, quantity: int = 0):
        order = next((order for order in self.pending_orders if order.order_no == org_order_no), None)
        if order is None:
            raise Exception(f"order not found: {org_order_no}")

        if quantity > order.pending_quantity:
            raise ValueError("quantity must be less than pending quantity")

        if quantity == 0:
            quantity = order.pending_quantity

        if order.side == OrderSide.BUY:
            price_diff = price - order.price
            # 0.015% 수수료
            diff_value = int(price_diff * quantity * 1.00015)
            if self.cash < diff_value:
                raise ValueError("not enough cash")
            else:
                self.decrease_cash(diff_value)

        new_order_no = str(self.next_order_no)
        self.next_order_no += 1

        new_order = StockOrder(
            org_order_no=order.order_no,
            order_no=new_order_no,
            asset_code=order.asset_code,
            side=order.side,
            price=price,
            quantity=quantity,
            filled_quantity=0,
            pending_quantity=quantity,
            order_type=order_type,
            order_time=self.clock.now(),
        )

        order.pending_quantity -= quantity
        self.pending_orders = [o for o in self.pending_orders if o.pending_quantity > 0]
        self.pending_orders.append(new_order)

    def cancel_order(self, order_no: str, quantity: int = 0):
        order = next((order for order in self.pending_orders if order.order_no == order_no), None)
        if order is None:
            raise Exception(f"order not found: {order_no}")

        if quantity == 0:
            self.pending_orders = [o for o in self.pending_orders if o.order_no != order_no]
        else:
            order.pending_quantity -= quantity
            if order.pending_quantity == 0:
                self.pending_orders = [o for o in self.pending_orders if o.order_no != order_no]

        if order.side == OrderSide.BUY:
            if quantity == 0:
                quantity = order.pending_quantity
            self.increase_cash(int(order.price * quantity * 1.00015))

    def on_time_change(self, current_time, before_time):
        for order in self.pending_orders:
            if self.time_unit == "minutes":
                df = self.get_minute_price(order.asset_code)
                df = df[(df["time"] >= before_time) & (df["time"] < current_time)].copy()
                if len(df) == 0:
                    continue

                df.set_index("time", inplace=True)
            elif self.time_unit == "days":
                from_date = before_time.date()
                to_date = current_time.date()

                df = self.get_daily_price(order.asset_code, from_date, to_date)
                if len(df) == 0:
                    continue

            else:
                raise ValueError(f"Invalid time unit: {self.time_unit}")

            if order.order_type == OrderType.MARKET or (order.order_type == OrderType.LIMIT_CONDITIONAL and current_time.time() >= dtm.time(15, 30)):
                # 시장가 주문의 경우 주문이 제출된 시간대의 종가로 체결
                if order.order_type == OrderType.MARKET:
                    filled_price = int(df['close'].iloc[0])
                else:
                    # 조건부지정가의 미경우 미체결시 동시호가(시장종가)로 체결
                    filled_price = int(df['close'].iloc[-1])

                if order.side == OrderSide.BUY:
                    self._buy_position(order.order_no, order.asset_code, order.quantity, filled_price)
                else:
                    self._sell_position(order.order_no, order.asset_code, order.quantity, filled_price)

            else:
                high = int(df['high'].max())
                low = int(df['low'].min())
                close = int(df['close'].iloc[-1])

                filled_price = None

                if order.side == OrderSide.BUY:
                    if order.price > high:
                        filled_price = close
                    elif order.price < low:
                        # not fill
                        self.logger.info(f"BUY ORDER NOT FILLED: {self._get_asset_name(order.asset_code)} price:{order.price} low:{low}")
                        pass
                    else:
                        filled_price = order.price

                elif order.side == OrderSide.SELL:
                    if order.price > high:
                        # not fill
                        self.logger.info(f"SELL ORDER NOT FILLED: {self._get_asset_name(order.asset_code)} price:{order.price} high:{high}")
                        pass
                    elif order.price < low:
                        filled_price = close
                    else:
                        filled_price = order.price

                if filled_price:
                    if order.side == OrderSide.BUY:
                        self._buy_position(order.order_no, order.asset_code, order.quantity, filled_price)
                    elif order.side == OrderSide.SELL:
                        self._sell_position(order.order_no, order.asset_code, order.quantity, filled_price)

    def _sell_position(self, order_no: str, asset_code: str, quantity: int, price: int):
        for pos in self.positions:
            if pos.asset_code == asset_code:
                pos.quantity -= quantity
                pos.current_value = pos.current_price * pos.quantity
                pos.current_pnl_value = (pos.current_price - pos.average_purchase_price) * pos.quantity
                pos.current_pnl = pos.current_pnl_value / pos.average_purchase_price * 100

                sell_value = price * quantity
                tax = sell_value * Decimal(0.003)
                fee = sell_value * Decimal(0.00015)
                buy_value = pos.average_purchase_price * quantity
                buy_fee = buy_value * Decimal(0.00015)
                pnl = sell_value - buy_value - fee - tax - buy_fee
                pnl_rate = pnl / buy_value * 100 if buy_value != 0 else 0

                self.add_trading_history(TradingHistory(
                    date=self.clock.today().strftime("%Y%m%d"),
                    order_no=order_no,
                    side=OrderSide.SELL,
                    asset_code=asset_code,
                    quantity=quantity,
                    filled_price=price,
                    average_purchase_price=pos.average_purchase_price,
                    tax=tax,
                    fee=fee,
                    pnl=pnl,
                    pnl_rate=pnl_rate,
                    executed_time=int(self.clock.now().timestamp() * 1000),
                ))

                # 실제로 팔렸을때 계산
                self.increase_cash(sell_value - fee - tax)

        self.pending_orders = [o for o in self.pending_orders if o.order_no != order_no]

    def _buy_position(self, order_no: str, asset_code: str, quantity: int, price: int):
        found = False
        for pos in self.positions:
            if pos.asset_code == asset_code:
                pos.average_purchase_price = (pos.average_purchase_price * pos.quantity + price * quantity) / (pos.quantity + quantity)

                pos.quantity += quantity
                pos.sell_possible_quantity += quantity
                pos.current_value = pos.current_price * pos.quantity
                pos.current_pnl_value = (pos.current_price - pos.average_purchase_price) * pos.quantity
                pos.current_pnl = pos.current_pnl_value / pos.average_purchase_price * 100
                found = True
                break

        if not found:
            pos = StockPosition(
                asset_code=asset_code,
                asset_name=self._get_asset_name(asset_code),
                quantity=quantity,
                sell_possible_quantity=quantity,
                average_purchase_price=Decimal(price),
                current_price=price,
                current_value=price * quantity,
                current_pnl=Decimal(0),
                current_pnl_value=0,
            )
            self.positions.append(pos)

        order = next((order for order in self.pending_orders if order.order_no == order_no), None)
        order_buy_value = order.price * order.pending_quantity

        buy_value = price * quantity
        fee = buy_value * 0.00015

        # 주문가와 체결가가 다를 수 있음
        if order_buy_value != buy_value:
            diff_amount = order_buy_value - buy_value
            self.increase_cash(int(diff_amount * 1.00015))

        self.add_trading_history(TradingHistory(
            date=self.clock.today().strftime("%Y%m%d"),
            order_no=order_no,
            side=OrderSide.BUY,
            asset_code=asset_code,
            quantity=quantity,
            filled_price=price,
            average_purchase_price=Decimal(price),
            fee=fee,
            tax=0,
            pnl=0,
            pnl_rate=0,
            executed_time=int(self.clock.now().timestamp() * 1000),
        ))

        self.pending_orders = [o for o in self.pending_orders if o.order_no != order_no]

    def add_trading_history(self, history):
        self.trading_history.append(history)

    def show_trading_history_report(self, make_file: bool = True, filter_side: OrderSide = None):

        empty_ret = {
            'count': 0,
            'total_pnl': 0,
            'avg_pnl': 0,
            'buy_sum': 0,
            'earn_sum': 0,
            'roi': 0,
        }
        if len(self.trading_history) == 0:
            return empty_ret

        dict_list = []
        for trade in self.trading_history:
            d = asdict(trade)

            if filter_side and d['side'] != filter_side:
                continue

            d['side'] = 'BUY' if d['side'] == OrderSide.BUY else 'SELL'
            d['name'] = self._get_asset_name(d['asset_code'])
            d['time'] = dtm.datetime.fromtimestamp(d['executed_time'] / 1000).strftime("%Y-%m-%d %H:%M:%S")
            d['buy_value'] = d['average_purchase_price'] * d['quantity']

            d.pop('executed_time')
            d.pop('date')
            d.pop('partial')

            d["average_purchase_price"] = d["average_purchase_price"].quantize(Decimal("0.00"))
            d["buy_value"] = int(d["buy_value"]) if d["buy_value"] else 0
            d["tax"] = int(d["tax"]) if d["tax"] else 0
            d["fee"] = int(d["fee"]) if d["fee"] else 0
            d["pnl"] = int(d["pnl"]) if d["pnl"] else 0
            d["pnl_rate"] = d["pnl_rate"].quantize(Decimal("0.00")) if d["pnl_rate"] else Decimal("0.00")

            minute_data = self.get_minute_price(d['asset_code'])
            d['max_price'] = minute_data['high'].max()
            d['max_time'] = minute_data.loc[minute_data['high'].idxmax(), 'time']
            d['max_buy_rate'] = (d['max_price'] - d['average_purchase_price']) / d['average_purchase_price'] * 100
            d['max_buy_rate'] = d['max_buy_rate'].quantize(Decimal("0.00"))
            d['min_price'] = minute_data['low'].min()
            d['min_time'] = minute_data.loc[minute_data['low'].idxmin(), 'time']
            dict_list.append(d)

        df = pd.DataFrame(dict_list)
        if df.empty:
            return empty_ret

        df.set_index('time', inplace=True)

        if make_file:
            df = df.sort_values(by='max_buy_rate', ascending=False)
            filename = f"debug/trading_history_{self.clock.today().strftime('%Y%m%d')}_{int(dtm.datetime.now().timestamp())}_{self.DBG_POSTFIX}.csv"
            df.to_csv(filename)

        pd.set_option('display.max_rows', None)
        print(df[["order_no", "side", "asset_code", "quantity", "average_purchase_price", "buy_value", "filled_price", "tax", "fee", "pnl", "pnl_rate", "name"]])
        pd.reset_option('display.max_rows')

        df.rename(columns={
            'order_no': '주문번호',
            'asset_code': '종목코드',
            'name': '종목명',
            'side': '매매구분',
            'quantity': '수량',
            'filled_price': '체결가',
            'average_purchase_price': '평단가',
            'buy_value': '매수금액',
            'tax': '세금',
            'fee': '수수료',
            'pnl': '손익',
            'pnl_rate': '손익률',
        }, inplace=True)
        df.index.name = '체결시간'

        # 컬럼 순서 변경
        df = df[['주문번호', '종목코드', '종목명', '매매구분', '수량', '체결가', '평단가', '매수금액', '세금', '수수료', '손익', '손익률']]

        count = len(df)
        total_pnl = df['손익률'].sum()
        avg_pnl = df['손익률'].mean()
        buy_sum = df['매수금액'].sum()
        earn_sum = df['손익'].sum()
        roi_pnl = earn_sum / buy_sum * 100 if buy_sum != 0 else 0
        print(f"Total {count} trades, Total PnL: {total_pnl:.2f}%, Avg PnL: {avg_pnl:.2f}% ROI: {roi_pnl:>7.2f}%")
        return {
            'count': count,
            'total_pnl': total_pnl,
            'avg_pnl': avg_pnl,
            'buy_sum': buy_sum,
            'earn_sum': earn_sum,
            'roi': roi_pnl / 100,
        }

    def show_pnl_timeline(self):
        df = pd.DataFrame()

        for pos in self.position_provider.get_positions(self.clock.today()):
            print('Fetch minute price for', pos.asset_code)

            minute_price_df = self._get_minute_price_with_cache(self.clock.today(), pos.asset_code)
            minute_price_df.set_index('time', inplace=True)
            minute_price_df = minute_price_df.loc[:self.clock.now().replace(hour=15, minute=20, second=0, microsecond=0)].copy()

            df2 = pd.DataFrame()

            df2[f"{pos.asset_code}_current_price"] = minute_price_df['close']
            df2[f"{pos.asset_code}_purchase_price"] = pos.average_purchase_price
            df2[f"{pos.asset_code}_quantity"] = pos.quantity
            df2[f"{pos.asset_code}_current_value"] = df2[f"{pos.asset_code}_current_price"] * pos.quantity
            df2[f"{pos.asset_code}_purchase_value"] = int(pos.average_purchase_price * pos.quantity)
            df2[f"{pos.asset_code}_pnl_value"] = df2[f"{pos.asset_code}_current_value"] - df2[f"{pos.asset_code}_purchase_value"]

            df = pd.concat([df, df2], axis=1)

        df['total_current_value'] = df.filter(like='_current_value').sum(axis=1)
        df['total_purchase_value'] = df.filter(like='_purchase_value').sum(axis=1)
        df['total_pnl_value'] = df.filter(like='_pnl_value').sum(axis=1)
        df['total_pnl_rate'] = df['total_pnl_value'] / df['total_purchase_value'] * 100

        df = df[['total_current_value', 'total_purchase_value', 'total_pnl_value', 'total_pnl_rate']].copy()

        if len(df) > 0:
            pd.set_option('display.max_rows', None)
            print(df)
            pd.reset_option('display.max_rows')

            print(f"- Max Pnl Time: {df['total_pnl_value'].idxmax()} {df['total_pnl_value'].max()} ({df['total_pnl_rate'].max()}%)")
            print(f"- Min Pnl Time: {df['total_pnl_value'].idxmin()} {df['total_pnl_value'].min()} ({df['total_pnl_rate'].min()}%)")

    def show_positions(self):
        positions = [p for p in self.positions if p.quantity > 0]
        data = []
        buy_value = 0
        pnl_value = 0
        current_value = 0
        pnl = 0

        for pos in positions:
            d = asdict(pos)
            d['average_purchase_price'] = round(float(pos.average_purchase_price), 2) if pos.average_purchase_price else 0
            d['pnl_rate'] = round(float(pos.current_pnl), 2) if pos.current_pnl else 0
            d['current_pnl_value'] = int(pos.current_pnl_value)
            data.append(d)

            buy_value += (d['average_purchase_price'] * d['quantity'])
            pnl_value += d['current_pnl_value']
            current_value += d["current_value"]

        df = pd.DataFrame(data)

        if len(df) > 0:
            pnl = pnl_value / buy_value * 100 if buy_value != 0 else 0
            print(df[["asset_code", "quantity", "sell_possible_quantity", "average_purchase_price", "current_price", "current_value", "current_pnl", "current_pnl_value", "pnl_rate", "asset_name"]])
            print(f"Total Buy Value: {buy_value} Total PnL: {pnl_value} ({pnl}%)")

        return {
            'buy_value': buy_value,
            'pnl_value': pnl_value,
            'pnl': pnl,
            'current_value': current_value
        }

    @lru_cache
    def _get_asset_name(self, code: str):
        df = get_ticker_info(code)
        return df['name'].iloc[-1]
