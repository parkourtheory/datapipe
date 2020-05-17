'''

API for sanitizing graph data

Author: Justin Chen
Date: 5/9/2020
'''

import networkx as nx
import numpy as np
from pandas import isnull

class DataCheck(object):
    def __init__(self):
        pass


    '''
    Create adjacency matrix from pandas dataframe

    inputs:
    df (DataFrame)

    outputs:
    adj (ndarray)
    '''
    def get_adjacency(self, df):
        d = len(df)
        adj = np.zeros([d, d], dtype=int)

        for i, row in df.iterrows():
            a = int(row['id']) - 1

            # iterate over every edge
            # if prereq or nextmove is not a string, it's NaN
            if isinstance(row['prereq'], str):
                for j in row['prereq'].split(', '):
                    b = int(df.loc[df['moveName'] == j]['id']) - 1
                    adj[a, b] += 1

            if isinstance(row['nextmove'], str):
                for j in row['nextmove'].split(', '):
                    b = int(df.loc[df['moveName'] == j]['id']) - 1
                    adj[a, b] += 1

        return adj


    '''
    Check symmetry of
    '''
    def check_symmetry(self, m):
        if not (m == m.T).all():
            return np.argwhere((m+m.T) == 1)+1


    '''
    Find duplicate rows

    inputs:  df (pd.DataFrame)
    outputs: series
    '''
    def duplicated(self, df):
        return df[df.duplicated('moveName', False)]


    '''
    Check that ids contain entire range of values

    inputs: df (pd.DataFrame)
    outputs: bool
    '''
    def valid_ids(self, df):
        ids = df['id'].tolist()
        return ids == list(range(1, len(ids)+1))


    '''
    Find cells with missing values

    inputs:
    df (pd.DataFrame) Dataframe
    col (str)         Column name

    outputs:
    list of row indices with missing values for column
    '''
    def find_empty(self, df, col):
        return [i+1 for i in df[df[col].isnull()].index.tolist()]
