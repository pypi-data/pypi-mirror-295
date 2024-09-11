import pandas as pd
import holidays

from useful_ts_tools.utils.periods import Periods
from useful_ts_tools.utils import constants


def add_date_time_features(df: pd.DataFrame, date_col_name: str = 'date', period=Periods.DAILY):
    """
    Add all date & time features to the input DataFrame
    :param df: the time series DataFrame
    :param date_col_name: the date column name
    :param period: the ts period (hourly, daily, weekly, ...)
    :return: the time series dataframe with all the date & time features that fit the period.
    """
    if period in [Periods.HOURLY, Periods.DAILY, Periods.WEEKLY, Periods.MONTHLY, Periods.YEARLY]:
        df.loc[:, 'year'] = add_year(df, date_col_name)

    if period in [Periods.HOURLY, Periods.DAILY, Periods.WEEKLY, Periods.MONTHLY]:
        df.loc[:, 'month'] = add_month(df, date_col_name)
        df.loc[:, 'quarter'] = add_quarter(df, date_col_name)

    if period in [Periods.HOURLY, Periods.DAILY, Periods.WEEKLY]:
        df.loc[:, 'weekofyear'] = add_weekofyear(df, date_col_name)

    if period in [Periods.HOURLY, Periods.DAILY]:
        df.loc[:, 'dayofyear'] = add_dayofyear(df, date_col_name)
        df.loc[:, 'dayofmonth'] = add_day(df, date_col_name)
        df.loc[:, 'dayofweek'] = add_dayofweek(df, date_col_name)

    if period == Periods.HOURLY:
        df.loc[:, 'hour'] = add_hour(df, date_col_name)

    return df


def add_season(df: pd.DataFrame, date_col_name: str = 'date', hemisphere = 'north'):
    """
    Add season to the DataFrame
    :param df: the input DataFrame
    :param date_col_name: the date column name
    :param hemisphere: north or south (default to north)
    :return: the DataFrame with a valued season column
    """
    df[date_col_name] = pd.to_datetime(df[date_col_name])
    if hemisphere == 'north':
        df['season'] = df[date_col_name].apply(lambda v: get_north_season(v))
    else:
        df['season'] = df[date_col_name].apply(lambda v: get_south_season(v))

    return df


def add_holiday(df: pd.DataFrame, date_col_name: str = 'date', country = 'FR'):
    """
    Add holidays as a new DataFrame column given a country code (holidays package country code)
    :param df: the input DataFrame
    :param date_col_name: the date column name
    :param country: the country code (@see the holidays package)
    :return: the DataFRame with a boolean holiday column
    """
    country_holidays = holidays.country_holidays(country)

    df['holiday'] = df[date_col_name].apply(lambda v: v in country_holidays)

    return df


def get_north_season(date):
    if ((date.month == 3) & (date.day >= 20)) | \
            (date.month in [4, 5]) | \
            ((date.month == 6) & (date.day < 21)):
        return constants.spring
    elif (date.month == 6) & (date.day >= 21) | \
            (date.month in [7, 8]) | \
            ((date.month == 9) & (date.day < 23)):
        return constants.summer
    elif (date.month == 9) & (date.day >= 23) | \
            (date.month in [10, 11]) | \
            ((date.month == 12) & (date.day < 21)):
        return constants.autumn
    elif ((date.month == 12) & (date.day >= 21)) | \
            (date.month in [1, 2]) | \
            ((date.month == 3) & (date.day < 20)):
        return constants.winter
    else:
        raise Exception('Incorrect date {}'.format(date))


def get_south_season(date):
    if ((date.month == 3) & (date.day >= 20)) | \
            (date.month in [4, 5]) | \
            ((date.month == 6) & (date.day < 21)):
        return constants.autumn
    elif (date.month == 6) & (date.day >= 21) | \
            (date.month in [7, 8]) | \
            ((date.month == 9) & (date.day < 23)):
        return constants.winter
    elif (date.month == 9) & (date.day >= 23) | \
            (date.month in [10, 11]) | \
            ((date.month == 12) & (date.day < 21)):
        return constants.spring
    elif ((date.month == 12) & (date.day >= 21)) | \
            (date.month in [1, 2]) | \
            ((date.month == 3) & (date.day < 20)):
        return constants.summer
    else:
        raise Exception('Incorrect date {}'.format(date))

def add_hour(df: pd.DataFrame, date_col_name: str = 'date'):
    """
    Adds the hour feature to the input DataFrame
    :param df: the time series DataFrame
    :param date_col_name: the date column name
    :return: the hour Series
    """
    return df[date_col_name].dt.hour


def add_day(df: pd.DataFrame, date_col_name: str = 'date'):
    """
    Adds the day feature to the input DataFrame
    :param df: the time series DataFrame
    :param date_col_name: the date column name
    :return: the day Series
    """
    return df[date_col_name].dt.day


def add_dayofweek(df: pd.DataFrame, date_col_name: str = 'date'):
    """
    Adds the dayofweek feature to the input DataFrame
    :param df: the time series DataFrame
    :param date_col_name: the date column name
    :return: the dayofweek Series
    """
    return df[date_col_name].dt.dayofweek


def add_weekofyear(df: pd.DataFrame, date_col_name: str = 'date'):
    """
    Adds the weekofyear feature to the input DataFrame
    :param df: the time series DataFrame
    :param date_col_name: the date column name
    :return: the weekofyear Series
    """
    return df[date_col_name].dt.isocalendar().week


def add_month(df: pd.DataFrame, date_col_name: str = 'date'):
    """
    Adds the month feature to the input DataFrame
    :param df: the time series DataFrame
    :param date_col_name: the date column name
    :return: the month Series
    """
    return df[date_col_name].dt.month


def add_quarter(df: pd.DataFrame, date_col_name: str = 'date'):
    """
    Adds the quarter feature to the input DataFrame
    :param df: the time series DataFrame
    :param date_col_name: the date column name
    :return: the quarter Series
    """
    return df[date_col_name].dt.quarter


def add_year(df: pd.DataFrame, date_col_name: str = 'date'):
    """
    Adds the year feature to the input DataFrame
    :param df: the time series DataFrame
    :param date_col_name: the date column name
    :return: the year Series
    """
    return df[date_col_name].dt.year


def add_dayofyear(df: pd.DataFrame, date_col_name: str = 'date'):
    """
    Adds the dayofyear feature to the input DataFrame
    :param df: the time series DataFrame
    :param date_col_name: the date column name
    :return: the dayofyear Series
    """
    return df[date_col_name].dt.dayofyear
