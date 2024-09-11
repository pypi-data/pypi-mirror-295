import pandas as pd


def gen_lags(df: pd.DataFrame, target: str = 'value', n_lags: int = 1, lag_list: list = None):
    """
    Generates the autoregressive features (lags) given an input DataFrame and a target col name.
    Providing n_lags generates all the lags within 1 -> n_lags. lag_list provides more control on the specific lag value
    to generate.
    :param df: the time series DataFrame
    :param target: the target column name
    :param n_lags: to generate 1 -> n_lags lags
    :param lag_list: [1, 7, 14] to create autoregressive features at specific lag values
    :return: the DataFrame with the autoregressive features
    """
    target_type = df[target].dtype
    kept_cols = [col for col in df.columns if col != target]
    dt_df = df[kept_cols]
    tmp_df = df[target]

    if lag_list is None:
        for i in range(1, n_lags+1):
            lag_df = gen_lag(df, lag=i, target=target)
            tmp_df = pd.concat([lag_df, tmp_df], axis=1)
    else:
        for l in lag_list:
            lag_df = gen_lag(df, lag=l, target=target)
            tmp_df = pd.concat([lag_df, tmp_df], axis=1)

    tmp_df = pd.concat([dt_df, tmp_df], axis=1).dropna()

    return tmp_df.astype({col: target_type for col in tmp_df.columns if col not in kept_cols})


def gen_lag(df: pd.DataFrame, lag: int, target: str = 'value'):
    """
    Generate a shifted column given the lag value
    :param df: input DataFrame
    :param lag: lag value
    :param target: the target column name
    :return: the shifted column by lag value.
    """
    target_df = df[target]
    return target_df.shift(lag).rename(f'lag-{lag}')
