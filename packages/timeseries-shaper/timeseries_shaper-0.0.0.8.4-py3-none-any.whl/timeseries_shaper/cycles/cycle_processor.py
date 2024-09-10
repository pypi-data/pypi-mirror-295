from typing import Dict, List
import pandas as pd
from ..base import Base


class CycleDataProcessor:
    """
    A class to process cycle-based data and values. It allows for splitting and merging DataFrames based on cycles,
    and grouping data by cycle UUIDs.
    """

    def __init__(self, cycles_df: pd.DataFrame, values_df: pd.DataFrame):
        """
        Initializes the CycleDataProcessor with cycles and values DataFrames.

        :param cycles_df: DataFrame containing columns 'cycle_start', 'cycle_end', and 'cycle_uuid'.
        :param values_df: DataFrame containing the values and timestamps in the 'systime' column.
        """
        self.cycles_df = cycles_df.copy()
        super().__init__(values_df)

        # Ensure proper datetime format
        self.cycles_df['cycle_start'] = pd.to_datetime(self.cycles_df['cycle_start'])
        self.cycles_df['cycle_end'] = pd.to_datetime(self.cycles_df['cycle_end'])
        self.values_df['systime'] = pd.to_datetime(self.values_df['systime'])

    def split_by_cycle(self) -> Dict[str, pd.DataFrame]:
        """
        Splits the values DataFrame by cycles defined in the cycles DataFrame. 
        Each cycle is defined by a start and end time, and the corresponding values are filtered accordingly.

        :return: Dictionary where keys are cycle_uuids and values are DataFrames with the corresponding cycle data.
        """
        result = {}
        for _, row in self.cycles_df.iterrows():
            mask = (self.values_df['systime'] >= row['cycle_start']) & (self.values_df['systime'] <= row['cycle_end'])
            result[row['cycle_uuid']] = self.values_df[mask].copy()
        return result

    def merge_dataframes_by_cycle(self) -> pd.DataFrame:
        """
        Merges values DataFrame with cycles DataFrame based on the cycle time intervals. 
        Appends the 'cycle_uuid' to the values DataFrame.

        :return: DataFrame with an added 'cycle_uuid' column.
        """
        self.values_df['cycle_uuid'] = None

        for _, row in self.cycles_df.iterrows():
            mask = (self.values_df['systime'] >= row['cycle_start']) & (self.values_df['systime'] <= row['cycle_end'])
            self.values_df.loc[mask, 'cycle_uuid'] = row['cycle_uuid']

        return self.values_df.dropna(subset=['cycle_uuid'])

    def group_by_cycle_uuid(self, data: pd.DataFrame) -> List[pd.DataFrame]:
        """
        Group the DataFrame by the cycle_uuid column, resulting in a list of DataFrames, each containing data for one cycle.

        :param data: DataFrame containing the data to be grouped by cycle_uuid.
        :return: List of DataFrames, each containing data for a unique cycle_uuid.
        """
        grouped_dataframes = [group for _, group in data.groupby('cycle_uuid')]
        return grouped_dataframes

    def split_dataframes_by_group(self, dfs: List[pd.DataFrame], column: str) -> List[pd.DataFrame]:
        """
        Splits a list of DataFrames by groups based on a specified column. 
        This function essentially performs a groupby operation on each DataFrame in the list and then flattens the result.

        :param dfs: List of DataFrames to be split.
        :param column: Column name to group by.
        :return: List of DataFrames, each corresponding to a group in the original DataFrames.
        """
        split_dfs = []
        for df in dfs:
            groups = df.groupby(column)
            for _, group in groups:
                split_dfs.append(group)
        return split_dfs
