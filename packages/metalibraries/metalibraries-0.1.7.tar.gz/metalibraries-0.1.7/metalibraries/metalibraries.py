import os
from itertools import groupby
from operator import itemgetter
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import pandas_market_calendars as mcal
import datetime as dt
import holidays
import time
import pytz
import yfinance as yf
import requests
import json

def delete_folders(names):
    """Delete folders specified in the 'names' list."""
    for name in names:
        if os.path.exists(name):
            os.rmdir(name)  # Only works if the directory is empty
        else:
            print(f"Directory {name} does not exist.")


def combine_number_letters(number_str, letter_str):
    """Combine number and letter strings into a single string."""
    return number_str + letter_str


def find_files_by_extension(extension: str, search_path: str):
    """Find all files with the specified extension in the search path."""
    result = []
    for root, _, files in os.walk(search_path):
        for file in files:
            if file.endswith(extension):
                result.append(os.path.join(root, file))
    return result


def time_series_summary(df, col_name):
    """Get summary statistics for a time series column."""
    return {
        'mean': df[col_name].mean(),
        'std': df[col_name].std(),
        'min': df[col_name].min(),
        'max': df[col_name].max()
    }


def format_percentage(value):
    """Format a numeric value as a percentage string."""
    if isinstance(value, (int, float)) and not np.isnan(value):
        return f"{round(value * 100, 2)} %"
    return None


def format_datetime(dt_obj):
    """Format a datetime object as a string."""
    return dt_obj.strftime('%Y-%m-%d %H:%M:%S') if dt_obj.hour or dt_obj.minute or dt_obj.second else dt_obj.strftime('%Y-%m-%d')


def replace_zero_time_index(df, time_zone='America/New_York'):
    """Replace zero-time index values in DataFrame."""
    if time_zone is None:
        return df
    new_index = []
    for idx in df.index:
        if idx.hour == 0 and idx.minute == 0 and idx.second == 0:
            if time_zone == 'America/New_York':
                new_index.append(idx.replace(hour=9, minute=30, second=0))
        else:
            new_index.append(idx)
    df.index = new_index
    return df


def create_lags(df, col_name, lags):
    """Create lag features for a DataFrame."""
    for lag in range(1, lags + 1):
        df[f'lag_{lag}'] = df[col_name].shift(lag)
    return df


def create_folders(names):
    # import os
    for name in names:
        os.makedirs(f'{name}', exist_ok=True)


def separate_number_letters(string):
    number_str, letter_str = '', ''
    for char in string:
        if char.isdigit():
            number_str += char
        else:
            letter_str += char
    return number_str + ' ' + letter_str  # CHANGE 0005 ORG (order of output)


def find_specific_file(filename: str, search_path: str, refresh=True):
    # import os
    # find_specific_file(f"{ticker}.csv", f"{dir_main}", update=False) # Example
    result = []
    if not refresh:
        for root, dir, files in os.walk(search_path):
            if filename in files:
                result.append(os.path.join(root, filename))
    return result


def find_files(ticker, dir_path, update=False):
    # import os
    files = []
    if not update:
        for path in os.listdir(dir_path):
            if os.path.isfile(os.path.join(dir_path, path)):  # Reason: check if current path is a file
                files.append(path)
        files = [file for file in files if ticker in file]
    return files


def consecutive_groups(iterable, ordering=lambda x: x):
    # from itertools import groupby
    # from operator import itemgetter
    for k, g in groupby(enumerate(iterable), key=lambda x: x[0] - ordering(x[1])):
        yield map(itemgetter(1), g)


def percentile_crop(df, percentile, mode, col_name):
    percentile_value = np.percentile(df.loc[:, col_name].dropna(), percentile)
    if mode == 'top':
        result = df[df.loc[:, col_name] >= percentile_value]
    elif df == 'bottom':
        result = df[df.loc[:, col_name] <= percentile_value]
    else:
        result = pd.concat([[df.loc[:, col_name] >= percentile_value], df[df.loc[:, col_name] <= percentile_value]],
                           axis=1)
    return result


def percentage_crop(df, percentage, mode):
    # Use only if it contains a single row; otherwise, col with nan will be dropped.
    if mode == 'top':
        result = df[df >= (1 - percentage)].dropna(axis=1)
    elif mode == 'bottom':
        result = df[df <= percentage].dropna(axis=1)
    else:
        result = pd.concat([df[df >= (1 - percentage)].dropna(axis=1), df[df <= percentage].dropna(axis=1)], axis=1)
    return result


def is_third_friday(date):
    # import datetime as dt
    d = dt.datetime.strptime(str(date).split()[0], '%Y-%m-%d')
    return d.weekday() == 4 and 15 <= d.day <= 21


def is_end_quarter(date):
    # import datetime as dt
    d = dt.datetime.strptime(str(date).split()[0], '%Y-%m-%d')
    return d.weekday() == 4 and 15 <= d.day <= 21 and d.month in (3, 6, 9, 12)


def is_end_month(date):
    # import datetime as dt
    tomorrows_month = (date + dt.timedelta(days=1)).month
    return tomorrows_month != date.month


def is_end_year(date):
    # import datetime as dt
    tomorrows_year = (date + dt.timedelta(days=1)).year
    return tomorrows_year != date.year


def is_working_day(date):
    return pd.Timestamp(date).isoweekday() in range(1, 6)


def next_US_business_day(date):
    # import datetime as dt
    # import holidays
    next_day = date + dt.timedelta(days=1)
    while next_day.weekday() in holidays.WEEKEND or next_day in holidays.US():  # Okay
        next_day += dt.timedelta(days=1)
    return next_day


def naive_from_to_timezone(time_date, from_zone='UTC', to_zone='America/New_York'):
    # import datetime as dt
    # import pytz

    # Ensure 'time_date' is a timezone-naive datetime object
    if time_date.tzinfo is not None:
        raise ValueError("The input datetime object should be timezone-naive.")

    # Get timezone objects
    from_zone = pytz.timezone(from_zone)
    to_zone = pytz.timezone(to_zone)

    # Localize the naive datetime to the 'from_zone'
    localized_time = from_zone.localize(time_date)

    # Convert to the target timezone
    to_time = localized_time.astimezone(to_zone)

    return to_time


def split_data(info, split_ratio):
    """ Split the data into training and test sets based on the split ratio."""
    split_index = int(len(info) * split_ratio)
    train_data = info.iloc[:split_index]
    test_data = info.iloc[split_index:]
    return train_data, test_data


def count_list_items(lst: list):
    count = 0
    for item in lst:
        if isinstance(item, list):
            count += count_list_items(item)
        else:
            count += 1
    return count


def string_percent(item_to_percent):
    if (isinstance(item_to_percent, float) and not np.isnan(item_to_percent)) and item_to_percent is not None:
        if item_to_percent == 0:
            return 0
        else:
            return str(round(item_to_percent * 100, 2)) + ' %'
    return None


def date_to_string(date):
    return date.strftime('%Y-%m-%d' if date.hour == date.minute == date.second == 0 else '%Y-%m-%d %H:%M:%S')


def replace_zero_time_index_for_timezone(df, time_zone='America/New_York'):
    if time_zone is None:
        return df
    new_index = []
    for idx in df.index:
        if idx.hour == 0 and idx.minute == 0 and idx.second == 0:
            if time_zone == 'America/New_York':
                new_index.append(idx.replace(hour=9, minute=30, second=0))
        else:
            return df
    df.index = new_index
    return df


def create_lags(info, col_name, lags):
    for lag in range(1, lags + 1):
        info[f'lag_{lag}'] = info[f'{col_name}'].shift(lag)
    return info


# ======================================================================================================================
# FINANCE

def financial_data_download(ticker, ticker_type, start_time, end_time, timeframe, data_source, useRTH, refresh, path,
                            time_zone='America/New_York', ib_bot=None, ratios=None):
    time1 = time.time()

    yahoo_to_csv(ticker, start_time, end_time, timeframe, True, path)
    original_data = pd.read_csv(f"{path}/{ticker}_{timeframe}.csv", index_col="Date", parse_dates=True, dayfirst=False)
    original_data = replace_zero_time_index_for_timezone(original_data, time_zone=time_zone)
    if not original_data.empty:
        original_data.index = original_data.index.tz_localize(time_zone)
        original_data.drop('Adj Close', axis=1, inplace=True)
        original_data = original_data[(original_data.index >= start_time) & (original_data.index <= end_time)]  # yahoo does not need this as it's always refresh=True.
        original_data = original_data.sort_index()
        original_data = original_data[~original_data.index.duplicated(keep='first')]

    print(f"Data got ready in {round(time.time() - time1, 2)} seconds.\n")
    if ratios is None:
        return original_data
    else:
        # Define the split ratios for training, validation, and final test sets
        initial_train_ratio, validation_ratio, final_test_ratio = ratios
        assert initial_train_ratio + validation_ratio + final_test_ratio == 1.0, "Ratios must sum up to 1.0"
        initial_train_data, temp_data = split_data(original_data, initial_train_ratio)
        validation_data, final_test_data = split_data(temp_data,
                                                      validation_ratio / (validation_ratio + final_test_ratio))
        return initial_train_data, validation_data, final_test_data


def filter_non_trading_days_from_list(data: list, exchange='NYSE'):
    # import pandas_market_calendars as mcal

    # Get the trading calendar for the specified exchange
    calendar = mcal.get_calendar(exchange)

    # Get the valid trading days in the date range of the data
    trading_days = calendar.valid_days(start_date=data[0], end_date=data[-1])

    # Filter the data to only include rows with dates in the trading_days
    filtered_data = [item for item in data if item in trading_days]

    return filtered_data


def next_trading_day(date: dt.datetime, exchange='NYSE'):
    tz_input = date.tzinfo
    time_input = date.time()
    date = date.replace(tzinfo=None, hour=0, minute=0, second=0, microsecond=0)
    calendar = mcal.get_calendar(exchange)
    next_days = calendar.valid_days(start_date=date, end_date=date + dt.timedelta(days=10))
    next_day = next_days[1] if next_days[0].date() == date.date() else next_days[0]
    next_day = next_day.replace(hour=time_input.hour, minute=time_input.minute, second=time_input.second, microsecond=time_input.microsecond)
    return next_day.replace(tzinfo=tz_input).to_pydatetime()


def get_exchange_rate(from_currency, to_currency):
    # import requests
    # import json
    try:
        response = requests.get(f"https://api.exchangerate-api.com/v4/latest/{from_currency}")
        data = json.loads(response.text)
        rate = data['rates'][to_currency]
    except Exception as e:
        rate = yf.download([from_currency + to_currency + '=X'], dt.datetime.now() - dt.timedelta(1), dt.datetime.now() + dt.timedelta(1), interval='1d').iloc[-1]['Close']
    return rate


def atr_calculator(data, period=14):
    # Calculate True Range (TR)
    high_low = data['High'] - data['Low']
    high_close = np.abs(data['High'] - data['Close'].shift())
    low_close = np.abs(data['Low'] - data['Close'].shift())
    tr = high_low.to_frame(name='TR')
    tr['High-Close'] = high_close
    tr['Low-Close'] = low_close
    tr['TrueRange'] = tr.max(axis=1)

    # Calculate ATR
    atr = tr['TrueRange'].rolling(window=period, min_periods=1).mean()

    return atr


def plot_equity_curve(info, ticker, strat_name, path, quiet=True):
    """ Plot the equity curve and drawdown of a trading strategy."""
    fig, ax1 = plt.subplots(1, 1, figsize=(10, 6))
    ax1.plot(info.index, info['equity_curve'], label='Equity Curve')
    ax1.set_ylabel('Equity ($)')
    ax1.legend(loc='upper left')
    plt.setp(ax1.get_xticklabels(), rotation=0, ha='right')

    ax2 = ax1.twinx()
    ax2.plot(info.index, info['drawdown'] * 100, label='Drawdown', color='red', alpha=0.3)
    ax2.set_ylabel('Drawdown (%)')
    ax2.legend(loc='upper right')

    plt.title(f'{strat_name}: Equity Curve and Drawdown for ${ticker}')
    plt.xlabel('Date')
    plt.grid()
    plt.savefig(path, dpi=1200)
    if not quiet:
        plt.show(block=True)


def is_market_open(time_zone='America/New_York', always_open=False, useRTH=True):
    # import pytz
    if always_open:
        return True
    else:
        now = None
        market_open = None
        market_close = None

        calendar = mcal.get_calendar('NYSE')  # Get the trading calendar for the specified exchange
        trading_days = calendar.valid_days(start_date=dt.datetime.now(dt.timezone.utc), end_date=dt.datetime.now(dt.timezone.utc))

        if time_zone == 'America/New_York':
            tz = pytz.timezone('America/New_York')
            now = dt.datetime.now(tz).time()
            if useRTH:
                market_open = dt.time(9, 30)
                market_close = dt.time(16, 0)
            else:
                market_open = dt.time(4, 0)
                market_close = dt.time(20, 0)

        return True if not trading_days.empty and market_open <= now < market_close else False


def is_extended_hours(current_time, time_zone='America/New_York'):
    """ Checks if the given time is within pre-market or after-hours trading sessions. """
    # import pytz
    # import pandas as pd
    # from datetime import datetime, time

    # Define the time zone for the market.
    if time_zone == 'America/New_York':
        market_tz = pytz.timezone('America/New_York')
        regular_open = dt.time(9, 30)
        regular_close = dt.time(16, 0)
        pre_market_open = dt.time(4, 0)
        after_hours_close = dt.time(20, 0)
    elif time_zone == 'Europe/London':
        market_tz = pytz.timezone('Europe/London')
        regular_open = dt.time(8, 0)
        regular_close = dt.time(16, 30)
        pre_market_open = dt.time(5, 0)
        after_hours_close = dt.time(20, 0)
    else:
        raise ValueError("Market not supported or incorrect market code provided.")

    # Ensure the current_time is timezone-aware and in the market's time zone
    if current_time.tzinfo is None:
        raise ValueError("The current_time must be timezone-aware.")

    current_time = current_time.astimezone(market_tz)
    current_time_only = current_time.time()

    if pre_market_open <= current_time_only < regular_open:
        return 'pre-market'
    elif regular_open <= current_time_only < regular_close:
        return 'regular'
    elif regular_close <= current_time_only < after_hours_close:
        return 'after-hours'
    else:
        return 'outside trading hours'


timeframe_info = {  # CHANGE 0003 ORG (order of output)
    # timeframe: (candle_duration, recommended_sometime, max_trading_dates_per_request_ib),
    '1sec': (dt.timedelta(seconds=1), dt.timedelta(seconds=0.1), dt.timedelta(hours=0.5)),
    '30sec': (dt.timedelta(seconds=30), dt.timedelta(seconds=1), dt.timedelta(hours=12)),
    '1min': (dt.timedelta(minutes=1), dt.timedelta(seconds=5), dt.timedelta(days=20)),
    '2min': (dt.timedelta(minutes=2), dt.timedelta(seconds=10), dt.timedelta(days=20)),
    '5min': (dt.timedelta(minutes=5), dt.timedelta(seconds=20), dt.timedelta(days=90)),
    '15min': (dt.timedelta(minutes=15), dt.timedelta(seconds=45), dt.timedelta(days=90)),
    '30min': (dt.timedelta(minutes=30), dt.timedelta(seconds=60), dt.timedelta(days=90)),
    '1hour': (dt.timedelta(hours=1), dt.timedelta(seconds=60), dt.timedelta(days=90)),
    '4hour': (dt.timedelta(hours=4), dt.timedelta(seconds=60), dt.timedelta(days=90)),
    '1d': (dt.timedelta(days=1), dt.timedelta(seconds=60), dt.timedelta(days=365)),
}


def candle_time_limits(now, timeframe, time_zone=None):
    candle_duration = timeframe_info[timeframe][0]

    if time_zone == 'America/New_York':
        today_SOD = now.replace(hour=9, minute=30, second=0, microsecond=0)
        today_EOD = now.replace(hour=16, minute=0, second=0, microsecond=0)
    else:
        tz = None
        now = dt.datetime.now(tz)
        today_SOD = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_EOD = now.replace(hour=23, minute=59, second=59, microsecond=999999)
    tomorrow_SOD = next_trading_day(today_SOD, exchange='NYSE')
    tomorrow_EOD = next_trading_day(today_EOD, exchange='NYSE')

    if timeframe in ['1d']:
        this_candle_open = today_SOD
        this_candle_close = today_EOD
        next_candle_open = tomorrow_SOD
        next_candle_close = tomorrow_EOD
    else:  # Test other timeframes: for now, 5min, 2min
        # Adjust the open time to the most recent candle's start time
        candle_seconds = int(candle_duration.total_seconds())
        current_seconds = int((now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds())
        seconds_from_start = current_seconds % candle_seconds
        this_candle_open = (now - dt.timedelta(seconds=seconds_from_start)).replace(microsecond=0)
        this_candle_close = this_candle_open + candle_duration
        next_candle_open = this_candle_close
        next_candle_close = next_candle_open + candle_duration
        # Although when AH finishes, intraday next_candle_open is at the start of PM and not this_candle_close, if lib.is_market_open(always_open=False), program will not run then.

    return this_candle_open, this_candle_close, next_candle_open, next_candle_close  # CHANGE 0004 ORG (order of output)  # Sensitive: Time output from candle_time_limits is timezone aware.


def wait_for_candle(timeframe, candle_open, candle_close, time_margin, trade_time, time_zone=None):
    # CHANGE 0008  # CHANGE 0010
    if 'anytime' in trade_time:
        return
    else:
        if time_zone == 'America/New_York':
            tz = pytz.timezone('America/New_York')
        else:
            tz = None
        sometime_candle = timeframe_info[timeframe][1]  # CHANGE 0003
        if 'open' in trade_time:
            if dt.datetime.now(tz) >= candle_close - time_margin:
                print(f"\nCONCLUSION: Too late to trade compared to execution_time ({trade_time}).\nNext revision if entry trade, or Aggressive exit if exit trade.")
                return True  # Revise again.
            elif candle_open <= dt.datetime.now(tz):
                return False  # Sent order.
            elif dt.datetime.now(tz) < candle_open - time_margin:
                print(f"\nCONCLUSION: Not ready to trade yet at {dt.datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')}: too far from execution_time ({trade_time}).\nNext revision.")
                return True  # Revise again.
            else:
                while dt.datetime.now(tz) < candle_open:
                    print(f'Holding off trading until {candle_open.strftime('%Y-%m-%d %H:%M:%S')}. '
                          f'Order will be sent in {int((candle_open - dt.datetime.now(tz)).total_seconds())} seconds ...')
                    time.sleep(1)
                return False  # Sent order.
        elif 'close' in trade_time:
            if dt.datetime.now(tz) < candle_open:
                return False  # Sent order.
                # timeframe='1d' orders with entry_time='close' can be sent before open of upcoming candle, which is this_candle_open on PM session.
                # For AH, these orders will be sent because they're still the last available data point.
            elif dt.datetime.now(tz) < candle_close - time_margin:  # CHANGE 0009 ORG (time until release)
                print(f"\nCONCLUSION: Not ready to trade yet: too far from execution_time ({trade_time}).\nNext revision.")
                return True  # Revise again.
            else:
                while dt.datetime.now(tz) < candle_close - sometime_candle:
                    # When we are closer than sometime_candle to the close of the candle, we send the order at observed price at that time, although it's not exactly this_candle_close.
                    print(f'Holding off trading until {(candle_close - sometime_candle).strftime('%Y-%m-%d %H:%M:%S')}. '
                          f'Order will be sent in {int((candle_close - sometime_candle - dt.datetime.now(tz)).total_seconds())} seconds ...')
                    time.sleep(1)
                return False  # Sent order after wait.
                # No check to orders/exit will be performed until hold-off orders sent. entry_price is not updated either.


def top_up_equity_curve(df, threshold_ratio):
    """
    Top up the equity curve when it falls below a certain threshold.
    """
    start_value = df['equity_curve'].iloc[0]
    threshold = start_value * threshold_ratio
    equity_curve = df['equity_curve'].copy()
    for i in range(1, len(equity_curve)):
        if equity_curve.iloc[i] < threshold:
            equity_curve.iloc[i] += start_value
    return equity_curve


def handling_returns_negative_equity(df, equity_curve_col_name='equity_curve', threshold_ratio=0.01):
    """
    Calculate the returns of an equity curve, with an optional threshold for topping up the equity curve when it falls below a certain level to prevent issues if equity curve falls below 0.
    """
    if equity_curve_col_name not in df.columns:
        raise ValueError(f"Column '{equity_curve_col_name}' not found in DataFrame")

    if any(df[equity_curve_col_name] < 0):
        df['topped_equity_curve'] = top_up_equity_curve(df, threshold_ratio)
        df['returns'] = df['topped_equity_curve'].pct_change(fill_method=None).dropna()
        condition_for_adj_return = df[equity_curve_col_name] < df[equity_curve_col_name].iloc[0] * threshold_ratio
        df['returns'] = np.where(condition_for_adj_return, df['returns'] * threshold_ratio - 1,
                                 df['returns'])  # Does not work as intended but could be fix if needed.
        returns = df['returns']
        df.drop(columns=['topped_equity_curve', 'returns'], inplace=True)
    else:
        returns = df[equity_curve_col_name].pct_change(fill_method=None).dropna()

    return returns


def find_swing_highs_lows(series, series_low=None, window=1):
    """
    Identify swing highs and swing lows.
    A swing high is when a point is higher than its neighbors (within a given window).
    A swing low is when a point is lower than its neighbors (within a given window).
    """
    swing_highs = (series.shift(window) < series) & (series.shift(-window) < series)
    if series_low is None:
        swing_lows = (series.shift(window) > series) & (series.shift(-window) > series)
    else:
        swing_lows = (series_low.shift(window) > series_low) & (series_low.shift(-window) > series_low)
    return swing_highs, swing_lows


def find_files_by_prefix(prefix: str, dir_path: str):
    """Find all files starting with the specified prefix in the directory."""
    files = []
    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)) and path.startswith(prefix):
            files.append(path)
    return files


def split_into_groups(iterable, size):
    """Split iterable into groups of the specified size."""
    for i in range(0, len(iterable), size):
        yield iterable[i:i + size]


def percentile_summary(df, col_name):
    """Get summary statistics of a column based on percentiles."""
    percentiles = [25, 50, 75]
    summary = {p: np.percentile(df[col_name].dropna(), p) for p in percentiles}
    return summary


def percentage_summary(df):
    """Get summary statistics for each column in the DataFrame based on percentage."""
    summary = {}
    for col in df.columns:
        non_nan_values = df[col].dropna()
        if not non_nan_values.empty:
            min_value = non_nan_values.min()
            max_value = non_nan_values.max()
            summary[col] = {'min': min_value, 'max': max_value}
    return summary


def is_business_day(date):
    """Check if a given date is a business day."""
    return pd.Timestamp(date).isoweekday() in range(1, 6)


def previous_trading_day(date: dt.datetime, exchange='NYSE'):
    """Find the previous trading day given a date."""
    calendar = mcal.get_calendar(exchange)
    prev_days = calendar.valid_days(start_date=date - dt.timedelta(days=10), end_date=date)
    return prev_days[-2] if len(prev_days) > 1 else None


def add_lags(df, col_name, lags):
    """Add lag features to a DataFrame."""
    for lag in range(1, lags + 1):
        df[f'lag_{lag}'] = df[col_name].shift(lag)
    return df

if __name__ == "__main__":
    pass
