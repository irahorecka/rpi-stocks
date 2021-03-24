import datetime
from pytz import timezone
from yahoo_fin import stock_info as si


def round_2(method):
    def wrapper(*args, **kwargs):
        return round(method(*args, **kwargs), 2)

    return wrapper


class Stock:
    def __init__(self, ticker, shares, cost_basis):
        self.ticker = ticker.upper()
        self.cost_basis = cost_basis
        self.shares = shares
        self._current_price = 0
        self._open_price = 0
        self._close_price = 0
        self._previous_close_price = 0
        self._datetime_cache = get_current_EST_datetime()

    # Perhaps I'm going overboard with the @property decorator.
    @property
    @round_2
    def current_price(self):
        if self._exceeds_cache or self._current_price == 0:
            self._current_price = si.get_live_price(self.ticker)

        return self._current_price

    @property
    @round_2
    def open_price(self):
        if self._exceeds_cache or self._open_price == 0:
            self._open_price = si.get_data(
                self.ticker, start_date=get_market_datetime(market="open")
            )["open"].iloc[0]

        return self._open_price

    @property
    @round_2
    def close_price(self):
        if self._exceeds_cache or self._close_price == 0:
            if get_current_EST_datetime().hour < 16:
                # market closes at 16:00 EST - get previous close price
                self._close_price = self.previous_close_price
            else:
                self._close_price = self.current_price

        return self._close_price

    @property
    @round_2
    def previous_close_price(self):
        if self._exceeds_cache or self._previous_close_price == 0:
            self._previous_close_price = si.get_data(
                self.ticker, end_date=get_market_datetime(market="close")
            )["close"].iloc[-1]

        return self._previous_close_price

    @property
    @round_2
    def total_value(self):
        return self.shares * self.current_price

    @property
    @round_2
    def total_cost_basis(self):
        return self.shares * self.cost_basis

    @property
    @round_2
    def total_gain(self):
        return self.shares * (self.current_price - self.cost_basis)

    @property
    @round_2
    def percent_gain(self):
        return 100 * (self.current_price - self.previous_close_price) / self.previous_close_price

    @property
    def _exceeds_cache(self, duration=10):
        current_datetime = get_current_EST_datetime()
        datetime_diff = current_datetime - self._datetime_cache
        if datetime_diff.seconds > duration:
            self._datetime_cache = get_current_EST_datetime()
            return True

        return False


def get_market_datetime(market="open"):
    current_datetime = get_current_EST_datetime()

    def market_open():
        # market opens at 6:30 EST
        if current_datetime.hour < 6 and current_datetime.minute < 30:
            # get previous open
            open_datetime = current_datetime - datetime.timedelta(days=1)
        else:
            open_datetime = current_datetime
        year = open_datetime.year
        month = open_datetime.month
        day = open_datetime.day

        return datetime.datetime(year, month, day)

    def market_close():
        # No need to manipulate time to get previous close from yahoo.finance
        year = current_datetime.year
        month = current_datetime.month
        day = current_datetime.day

        return datetime.datetime(year, month, day)

    def str_format(datetime_obj):
        return datetime_obj.strftime("%m-%d-%Y")

    if market == "open":
        return str_format(market_open())
    elif market == "close":
        return str_format(market_close())


def get_current_EST_datetime():
    """ Get current datetime object in eastern time. """
    return datetime.datetime.now(timezone("EST"))


if __name__ == "__main__":
    # dirty test env - remove once tests are built
    aapl = Stock("AMC", 2390, 3)
    print(aapl.previous_close_price)
    print(aapl.open_price)
    print(aapl.current_price)
    print(aapl.close_price)
    print(aapl.percent_gain)
    print(aapl.total_gain)
    print(aapl.total_cost_basis)
    print(aapl.total_value)
