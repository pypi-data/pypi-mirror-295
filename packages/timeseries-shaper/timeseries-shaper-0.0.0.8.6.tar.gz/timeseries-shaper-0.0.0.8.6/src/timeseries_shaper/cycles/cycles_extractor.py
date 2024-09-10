from typing import Optional
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
        
        self.df = dataframe  # Use the provided DataFrame directly
        self.start_uuid = start_uuid
        self.end_uuid = end_uuid if end_uuid else start_uuid
        logging.info(f"CycleExtractor initialized with start_uuid: {self.start_uuid} and end_uuid: {self.end_uuid}")

    def process_persistent_cycle(self) -> pd.DataFrame:
        """Processes cycles where the value of the variable stays true during the cycle."""
        # Assuming dataframe is pre-filtered
        cycle_starts = self.df[self.df['value_bool'] == True]
        cycle_ends = self.df[self.df['value_bool'] == False]

        return self._generate_cycle_dataframe(cycle_starts, cycle_ends)

    def process_trigger_cycle(self) -> pd.DataFrame:
        """Processes cycles where the value of the variable goes from true to false during the cycle."""
        # Assuming dataframe is pre-filtered
        cycle_starts = self.df[self.df['value_bool'] == True]
        cycle_ends = self.df[self.df['value_bool'] == False].shift(-1)

        return self._generate_cycle_dataframe(cycle_starts, cycle_ends)

    def process_separate_start_end_cycle(self) -> pd.DataFrame:
        """Processes cycles where different variables indicate cycle start and end."""
        # Assuming dataframe is pre-filtered for both start_uuid and end_uuid
        cycle_starts = self.df[self.df['value_bool'] == True]
        cycle_ends = self.df[self.df['value_bool'] == True]

        return self._generate_cycle_dataframe(cycle_starts, cycle_ends)

    def process_step_sequence(self, start_step: int, end_step: int) -> pd.DataFrame:
        """Processes cycles based on a step sequence, where specific integer values denote cycle start and end."""
        # Assuming dataframe is pre-filtered
        cycle_starts = self.df[self.df['value_int'] == start_step]
        cycle_ends = self.df[self.df['value_int'] == end_step]

        return self._generate_cycle_dataframe(cycle_starts, cycle_ends)

    def process_state_change_cycle(self) -> pd.DataFrame:
        """Processes cycles where the start of a new cycle is the end of the previous cycle."""
        # Assuming dataframe is pre-filtered
        cycle_starts = self.df.copy()
        cycle_ends = self.df.shift(-1)

        return self._generate_cycle_dataframe(cycle_starts, cycle_ends)

    def process_value_change_cycle(self) -> pd.DataFrame:
        """Processes cycles where a change in the value indicates a new cycle."""
        # Assuming dataframe is pre-filtered
        self.df['value_change'] = (
            self.df[['value_double', 'value_bool', 'value_string', 'value_int']]
            .apply(lambda x: x.diff().ne(0).any(axis=1), axis=1)
        )

        cycle_starts = self.df[self.df['value_change'] == True]
        cycle_ends = self.df[self.df['value_change'] == True].shift(-1)

        return self._generate_cycle_dataframe(cycle_starts, cycle_ends)

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