import pandas as pd
from models.models import GraphData
from typing import Callable, Dict

ALL_GRAPHS: Dict[int, GraphData] = {
    0: GraphData(
        id=0,
        title='IoC by indicator_type',
        type='bar',
        description='This graph shows how many IoC where collected grouped by indicator_type'
    ),
    1: GraphData(
        id=1,
        title='IoC by user',
        type='bar',
        description='This graph shows how many IoC where found by users'
    )
}

def ioc_by_indicatortype_data(full_df: pd.DataFrame) -> GraphData:
    df = full_df.groupby(['indicator_type'])['indicator'].count()
    graph_data = ALL_GRAPHS.get(0)
    graph_data.labels = list(df.index)
    graph_data.data = list(df)
    return graph_data

def ioc_by_user_data(full_df: pd.DataFrame) -> GraphData:
    df = full_df.groupby(['user'])['indicator'].count()
    graph_data = ALL_GRAPHS.get(1)
    graph_data.labels = list(df.index)
    graph_data.data = list(df)
    return graph_data

#TODO: Add other functions for other graphs here!

GRAPH_DICT: Dict[int, Callable[[pd.DataFrame], GraphData]] = {
    0: ioc_by_indicatortype_data,
    1: ioc_by_user_data
}

def get_graph_data(full_df: pd.DataFrame, graph_id: int) -> GraphData:
    try:
        res = GRAPH_DICT.get(graph_id)(full_df)
        return res
    except Exception as e:
        print(e)
        return None

def get_all_graphs_reducted() -> list[GraphData]:
    return list(ALL_GRAPHS.values())