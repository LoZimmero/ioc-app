import pandas as pd
from typing import Callable, Dict

def ioc_by_indicatortype_data(full_df: pd.DataFrame) -> pd.Series:
    df2 = full_df.groupby(['indicator_type'])['indicator'].count()
    return df2

def ioc_by_user_data(full_df: pd.DataFrame) -> pd.Series:
    df2 = full_df.groupby(['user'])['indicator'].count()
    return df2

GRAPH_DICT: Dict[int, Callable[[pd.DataFrame], pd.Series]] = {
    0: ioc_by_indicatortype_data,
    1: ioc_by_user_data
}

def get_graph_data(full_df: pd.DataFrame, graph_id: int) -> pd.Series:
    return GRAPH_DICT.get(graph_id)(full_df)


