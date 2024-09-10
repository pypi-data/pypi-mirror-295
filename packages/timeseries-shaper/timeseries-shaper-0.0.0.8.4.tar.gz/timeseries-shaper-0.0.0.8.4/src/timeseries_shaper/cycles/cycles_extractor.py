from typing import Optional
import pandas as pd
import uuid
from ..base import Base


class CycleExtractor:
    """Class for processing cycles based on different criteria."""

    def __init__(self, dataframe: pd.DataFrame, start_uuid: str, end_uuid: Optional[str] = None):
        """Initializes the class with the data and the UUIDs for cycle start and end."""
        super().__init__(dataframe)
        self.start_uuid = start_uuid
        self.end_uuid = end_uuid if end_uuid else start_uuid

    def process_persistent_cycle(self) -> pd.DataFrame: 
        """Processes cycles where the value of the variable stays true during the cycle."""
        df_filtered = self.df[self.df['uuid'] == self.start_uuid]
        df_filtered = df_filtered[df_filtered['is_delta'] == True]
        cycle_starts = df_filtered[df_filtered['value_bool'] == True]
        cycle_ends = df_filtered[df_filtered['value_bool'] == False]

        return self._generate_cycle_dataframe(cycle_starts, cycle_ends)

    def process_trigger_cycle(self) -> pd.DataFrame: 
        """Processes cycles where the value of the variable goes from true to false during the cycle."""
        df_filtered = self.df[self.df['uuid'] == self.start_uuid]
        df_filtered = df_filtered[df_filtered['is_delta'] == True]
        cycle_starts = df_filtered[df_filtered['value_bool'] == True]
        cycle_ends = df_filtered[df_filtered['value_bool'] == False].shift(-1)

        return self._generate_cycle_dataframe(cycle_starts, cycle_ends)

    def process_separate_start_end_cycle(self) -> pd.DataFrame: 
        """Processes cycles where different variables indicate cycle start and end."""
        df_start_filtered = self.df[self.df['uuid'] == self.start_uuid]
        df_end_filtered = self.df[self.df['uuid'] == self.end_uuid]
        df_start_filtered = df_start_filtered[df_start_filtered['is_delta'] == True]
        df_end_filtered = df_end_filtered[df_end_filtered['is_delta'] == True]

        cycle_starts = df_start_filtered[df_start_filtered['value_bool'] == True]
        cycle_ends = df_end_filtered[df_end_filtered['value_bool'] == True]

        return self._generate_cycle_dataframe(cycle_starts, cycle_ends)

    def process_step_sequence(self, start_step: int, end_step: int) -> pd.DataFrame:
        """Processes cycles based on a step sequence, where specific integer values denote cycle start and end."""
        df_filtered = self.df[self.df['uuid'] == self.start_uuid]
        df_filtered = df_filtered[df_filtered['is_delta'] == True]
        cycle_starts = df_filtered[df_filtered['value_int'] == start_step]
        cycle_ends = df_filtered[df_filtered['value_int'] == end_step]

        return self._generate_cycle_dataframe(cycle_starts, cycle_ends)

    def process_state_change_cycle(self) -> pd.DataFrame:
        """Processes cycles where the start of a new cycle is the end of the previous cycle."""
        df_filtered = self.df[self.df['uuid'] == self.start_uuid]
        df_filtered = df_filtered[df_filtered['is_delta'] == True]
        cycle_starts = df_filtered.copy()
        cycle_ends = df_filtered.shift(-1)

        return self._generate_cycle_dataframe(cycle_starts, cycle_ends)

    def process_value_change_cycle(self) -> pd.DataFrame:
        """Processes cycles where a change in the value indicates a new cycle."""
        df_filtered = self.df[self.df['uuid'] == self.start_uuid]
        df_filtered['value_change'] = (df_filtered['value_double'].diff().ne(0) | 
                                       df_filtered['value_bool'].diff().ne(0) | 
                                       df_filtered['value_string'].shift().ne(df_filtered['value_string']) |
                                       df_filtered['value_int'].diff().ne(0))

        cycle_starts = df_filtered[df_filtered['value_change'] == True]
        cycle_ends = df_filtered[df_filtered['value_change'] == True].shift(-1)

        return self._generate_cycle_dataframe(cycle_starts, cycle_ends)

    def _generate_cycle_dataframe(self, cycle_starts: pd.DataFrame, cycle_ends: pd.DataFrame) -> pd.DataFrame:
        cycle_df = pd.DataFrame(columns=['cycle_start', 'cycle_end', 'cycle_uuid'])
        cycle_ends_iter = iter(cycle_ends['systime'])

        try:
            next_cycle_end = next(cycle_ends_iter)
            for _, start_row in cycle_starts.iterrows():
                start_time = start_row['systime']
                while next_cycle_end <= start_time:
                    next_cycle_end = next(cycle_ends_iter)
                cycle_df.loc[len(cycle_df)] = {
                    'cycle_start': start_time,
                    'cycle_end': next_cycle_end,
                    'cycle_uuid': str(uuid.uuid4())
                }
        except StopIteration:
            pass

        return cycle_df