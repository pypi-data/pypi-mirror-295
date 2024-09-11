import datetime as dtm

from pyqqq.utils.market_schedule import is_full_day_closed


def print_invest_result(dataframe, initial_cash, risk_free_rate=0.02, save_csv=False, csv_path="invest_result.csv"):
    """
    dataframe: 일별 거래 결과가 담긴 데이터프레임
        ["earn_money"]: (필수 필드) 일별 수익 (매매 후 현금 + 보유 주식 가치 기준 계산)
        ["account_value"]: (옵션 필드) 일별 계좌 가치. 없으면 initail_cash와 earn_money로 계산
    initial_cash: 초기 현금
    risk_free_rate: 무위험 수익률 (연율)
    save_csv: 결과를 csv로 저장할지 여부
    csv_path: csv 저장 경로
    """
    print("====== invest result ======")
    df = dataframe.copy(deep=True)
    df["trading_date"] = ~df.index.to_series().apply(lambda x: is_full_day_closed(dtm.datetime.combine(x, dtm.time(10, 30))))
    df = df.loc[df["trading_date"]]
    if "account_value" not in df.columns:
        df["account_value"] = df["earn_money"].cumsum() + initial_cash
    df["daily_pnl"] = df["earn_money"] / df["account_value"]

    # cagr
    days = len(df)
    cagr = (df["account_value"].iloc[-1] / initial_cash) ** (252 / days) - 1
    print(f"cagr: {cagr * 100:.3f}%")

    # sharpe ratio
    daily_risk_free_rate = (1 + risk_free_rate) ** (1 / 252) - 1
    df["daily_excess_return"] = df["daily_pnl"] - daily_risk_free_rate
    mean_excess_return = df["daily_excess_return"].mean()
    std_excess_return = df["daily_excess_return"].std()
    sharpe_ratio = mean_excess_return / std_excess_return * (252 ** 0.5)
    print(f"sharpe ratio: {sharpe_ratio:.3f}")

    # max drawdown
    df["cummax"] = df["account_value"].cummax()
    df["drawdown"] = 1 - df["account_value"] / df["cummax"]
    max_drawdown = df["drawdown"].max()
    print(f"max drawdown: {max_drawdown*100:.3f}%")
    print("===========================")

    if save_csv:
        df.to_csv(csv_path)
