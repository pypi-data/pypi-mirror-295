from typing import Optional, Union
import pandas as pd
import uuid
import logging
from ..base import Base

class CycleExtractor(Base):
    """Class for processing cycles based on different criteria."""

    def __init__(self, dataframe: pd.DataFrame, start_uuid: str, end_uuid: Optional[str] = None):
        """Initializes the class with the data and the UUIDs for cycle start and end."""
        super().__init__(dataframe)
        
        # Validate input types
        if not isinstance(dataframe, pd.DataFrame):
            raise ValueError("dataframe must be a pandas DataFrame")
        if not isinstance(start_uuid, str):
            raise ValueError("start_uuid must be a string")
        
        self.start_uuid = start_uuid
        self.end_uuid = end_uuid if end_uuid else start_uuid
        logging.info(f"CycleExtractor initialized with start_uuid: {self.start_uuid} and end_uuid: {self.end_uuid}")

    def process_persistent_cycle(self) -> pd.DataFrame:
        """Processes cycles where the value of the variable stays true during the cycle."""
        df_filtered = self._filter_by_uuid_and_delta(self.start_uuid)
        cycle_starts = df_filtered[df_filtered['value_bool'] == True]
        cycle_ends = df_filtered[df_filtered['value_bool'] == False]

        return self._generate_cycle_dataframe(cycle_starts, cycle_ends)

    def process_trigger_cycle(self) -> pd.DataFrame:
        """Processes cycles where the value of the variable goes from true to false during the cycle."""
        df_filtered = self._filter_by_uuid_and_delta(self.start_uuid)
        cycle_starts = df_filtered[df_filtered['value_bool'] == True]
        cycle_ends = df_filtered[df_filtered['value_bool'] == False].shift(-1)

        return self._generate_cycle_dataframe(cycle_starts, cycle_ends)

    def process_separate_start_end_cycle(self) -> pd.DataFrame:
        """Processes cycles where different variables indicate cycle start and end."""
        df_start_filtered = self._filter_by_uuid_and_delta(self.start_uuid)
        df_end_filtered = self._filter_by_uuid_and_delta(self.end_uuid)

        cycle_starts = df_start_filtered[df_start_filtered['value_bool'] == True]
        cycle_ends = df_end_filtered[df_end_filtered['value_bool'] == True]

        return self._generate_cycle_dataframe(cycle_starts, cycle_ends)

    def process_step_sequence(self, start_step: int, end_step: int) -> pd.DataFrame:
        """Processes cycles based on a step sequence, where specific integer values denote cycle start and end."""
        df_filtered = self._filter_by_uuid_and_delta(self.start_uuid)
        cycle_starts = df_filtered[df_filtered['value_int'] == start_step]
        cycle_ends = df_filtered[df_filtered['value_int'] == end_step]

        return self._generate_cycle_dataframe(cycle_starts, cycle_ends)

    def process_state_change_cycle(self) -> pd.DataFrame:
        """Processes cycles where the start of a new cycle is the end of the previous cycle."""
        df_filtered = self._filter_by_uuid_and_delta(self.start_uuid)
        cycle_starts = df_filtered.copy()
        cycle_ends = df_filtered.shift(-1)

        return self._generate_cycle_dataframe(cycle_starts, cycle_ends)

    def process_value_change_cycle(self) -> pd.DataFrame:
        """Processes cycles where a change in the value indicates a new cycle."""
        df_filtered = self._filter_by_uuid_and_delta(self.start_uuid)
        df_filtered['value_change'] = (
            df_filtered[['value_double', 'value_bool', 'value_string', 'value_int']]
            .apply(lambda x: x.diff().ne(0).any(axis=1), axis=1)
        )

        cycle_starts = df_filtered[df_filtered['value_change'] == True]
        cycle_ends = df_filtered[df_filtered['value_change'] == True].shift(-1)

        return self._generate_cycle_dataframe(cycle_starts, cycle_ends)

    def _filter_by_uuid_and_delta(self, uuid_value: str) -> pd.DataFrame:
        """Filters the dataframe by UUID and ensures 'is_delta' is True."""
        df_filtered = self.df[self.df['uuid'] == uuid_value]
        df_filtered = df_filtered[df_filtered['is_delta'] == True]
        logging.info(f"Filtered dataframe for UUID: {uuid_value} with {len(df_filtered)} records")
        return df_filtered

    def _generate_cycle_dataframe(self, cycle_starts: pd.DataFrame, cycle_ends: pd.DataFrame) -> pd.DataFrame:
        """Generates a DataFrame with cycle start and end times."""
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
            logging.warning("Cycle end data ran out while generating cycles.")

        logging.info(f"Generated {len(cycle_df)} cycles.")
        return cycle_df