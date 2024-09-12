import pandas as pd
from ..base import Base

class CycleCutter(Base):
    """
    Processes a DataFrame to extract cycles of values (such as temperature, pressure)
    based on UUID identifiers for start, stop, and optional marker points. Provides
    raw cycle data and cycle-level statistics where values are identified by UUIDs
    and stored in a single value column (e.g., 'value_integer').
    """
    
    def __init__(self, dataframe: pd.DataFrame, time_column: str = 'systime', 
                 uuid_column: str = 'uuid', value_column: str = 'value_integer') -> None:
        """Initializes the CycleCutter with a DataFrame and relevant column names."""
        super().__init__(dataframe, column_name=time_column)
        self.time_column = time_column
        self.uuid_column = uuid_column
        self.value_column = value_column

    def get_raw_cycle_data(self, start_uuids: list, value_mappings: dict,
                       stop_uuids: list = None, marker_uuids: list = None) -> pd.DataFrame:
        """
        Extracts raw cycles from the DataFrame based on the start and (optional) stop UUIDs,
        normalizes time by seconds after the cycle start, and returns a concatenated DataFrame 
        where values (e.g., temperature, pressure) are identified by UUIDs and stored in a single 
        value column (e.g., 'value_integer').

        Args:
                start_uuids (list): List of UUIDs indicating where each cycle starts.
                value_mappings (dict): A dictionary where keys are sensor types (e.g., 'temperature', 'pressure')
                                    and values are the UUIDs corresponding to those sensors.
                stop_uuids (list, optional): List of UUIDs indicating where each cycle ends. If not provided,
                                        cycles will be cut from start to start.
            marker_uuids (list, optional): List of marker UUIDs to be added. Defaults to None.

        Returns:
            pd.DataFrame: A concatenated DataFrame where all cycles are combined.
        """
        if stop_uuids and len(start_uuids) != len(stop_uuids):
            raise ValueError("The number of start UUIDs must match the number of stop UUIDs.")

        all_cycles = []  # This will store all the DataFrames for each cycle

        # Iterate over the list of start UUIDs and process each cycle
        for idx, start_uuid in enumerate(start_uuids):
            # Get the start time for the current cycle
            start_row = self.dataframe[self.dataframe[self.uuid_column] == start_uuid]
            if start_row.empty:
                print(f"Start UUID not found: {start_uuid}")
                continue

            cycle_start_time = start_row[self.time_column].iloc[0]

            # Determine the stop time based on the next start or the stop UUIDs
            if stop_uuids:  # If explicit stop UUIDs are provided
                stop_uuid = stop_uuids[idx]
                stop_row = self.dataframe[self.dataframe[self.uuid_column] == stop_uuid]
                cycle_stop_time = stop_row[self.time_column].iloc[0] if not stop_row.empty else None
            else:  # If stop UUIDs are not provided, use the next start UUID or the end of the data
                if idx + 1 < len(start_uuids):
                    next_start_uuid = start_uuids[idx + 1]
                    next_start_row = self.dataframe[self.dataframe[self.uuid_column] == next_start_uuid]
                    cycle_stop_time = next_start_row[self.time_column].iloc[0] if not next_start_row.empty else None
                else:
                    cycle_stop_time = None  # For the last cycle, take all remaining data

            # Extract cycle data based on the start and stop times
            cycle_data = self._get_cycle_data(start_uuid, cycle_start_time, cycle_stop_time, value_mappings, marker_uuids, idx)
            if cycle_data is not None:
                all_cycles.append(cycle_data)  # Append the cycle DataFrame to the list

        # Concatenate all the cycles into a single DataFrame
        if all_cycles:
            return pd.concat(all_cycles, ignore_index=True)  # Concatenate and return as one DataFrame
        else:
            return pd.DataFrame()  # Return an empty DataFrame if no cycles were processed


    def get_cycle_statistics(self, start_uuids: list, value_mappings: dict, stop_uuids: list = None) -> pd.DataFrame:
        """
        Extracts and computes cycle-level statistics (duration, mean, max, min, std dev)
        for each cycle based on the start and (optional) stop UUIDs.

        Args:
            start_uuids (list): List of UUIDs indicating where each cycle starts.
            stop_uuids (list, optional): List of UUIDs indicating where each cycle ends. If not provided,
                                         cycles will be cut from start to start.
            value_mappings (dict): A dictionary where keys are sensor types (e.g., 'temperature', 'pressure')
                                   and values are the UUIDs corresponding to those sensors.

        Returns:
            pd.DataFrame: A DataFrame containing the cycle-level statistics.
        """
        if stop_uuids and len(start_uuids) != len(stop_uuids):
            raise ValueError("The number of start UUIDs must match the number of stop UUIDs.")

        cycle_stats = []

        # Iterate over the list of start UUIDs
        for idx, start_uuid in enumerate(start_uuids):
            start_row = self.dataframe[self.dataframe[self.uuid_column] == start_uuid]
            if start_row.empty:
                print(f"Start UUID not found: {start_uuid}")
                continue

            cycle_start_time = start_row[self.time_column].iloc[0]

            # Determine the stop time based on the next start or the stop UUIDs
            if stop_uuids:  # If explicit stop UUIDs are provided
                stop_uuid = stop_uuids[idx]
                stop_row = self.dataframe[self.dataframe[self.uuid_column] == stop_uuid]
                cycle_stop_time = stop_row[self.time_column].iloc[0] if not stop_row.empty else None
            else:  # If stop UUIDs are not provided, use the next start UUID or the end of the data
                if idx + 1 < len(start_uuids):
                    next_start_uuid = start_uuids[idx + 1]
                    next_start_row = self.dataframe[self.dataframe[self.uuid_column] == next_start_uuid]
                    cycle_stop_time = next_start_row[self.time_column].iloc[0] if not next_start_row.empty else None
                else:
                    cycle_stop_time = None  # For the last cycle, take all remaining data

            cycle_data = self._get_cycle_data(start_uuid, cycle_start_time, cycle_stop_time, value_mappings, None, idx)
            if cycle_data is not None:
                cycle_stats.append(self._calculate_cycle_statistics(cycle_data, value_mappings, idx))

        return pd.DataFrame(cycle_stats)

    def _get_cycle_data(self, start_uuid, cycle_start_time, cycle_stop_time, value_mappings, marker_uuids, cycle_id) -> pd.DataFrame:
        """
        Extracts the data for a single cycle based on the start time and stop time (or next cycle start),
        normalizes the time column, and returns the cycle DataFrame. If marker UUIDs are provided,
        they are added as a separate column with normalized times.

        Args:
            start_uuid (str): The UUID marking the start of the cycle.
            cycle_start_time (Timestamp): The start time of the cycle.
            cycle_stop_time (Timestamp): The stop time of the cycle (or None for all remaining data).
            value_mappings (dict): A dictionary of sensor types and their corresponding UUIDs.
            marker_uuids (list): List of marker UUIDs to add to the cycle.
            cycle_id (int): The unique identifier for the cycle.
        
        Returns:
            pd.DataFrame: A DataFrame for the cycle with normalized time and markers, or None if UUIDs are not found.
        """
        # Filter data between cycle start and stop times (or end of DataFrame if no stop time)
        if cycle_stop_time:
            cycle_df = self.dataframe[(self.dataframe[self.time_column] >= cycle_start_time) &
                                      (self.dataframe[self.time_column] < cycle_stop_time)]
        else:
            cycle_df = self.dataframe[self.dataframe[self.time_column] >= cycle_start_time]

        # Initialize an empty DataFrame to store the merged cycle data
        processed_cycle_df = pd.DataFrame()

        # Extract data for each sensor (e.g., temperature, pressure) based on UUID mappings
        for sensor_type, sensor_uuid in value_mappings.items():
            value_data = cycle_df[cycle_df[self.uuid_column] == sensor_uuid]
            if not value_data.empty:
                value_data['time_normalized'] = (value_data[self.time_column] - cycle_start_time).dt.total_seconds()
                value_data = value_data[[self.time_column, 'time_normalized', self.value_column]].rename(
                    columns={self.value_column: sensor_type})
                processed_cycle_df = pd.concat([processed_cycle_df, value_data.set_index(self.time_column)], axis=1, join='outer') if not processed_cycle_df.empty else value_data.set_index(self.time_column)

        # Add marker column if marker_uuids are provided
        if marker_uuids:
            processed_cycle_df['marker_time'] = processed_cycle_df[self.uuid_column].apply(
                lambda uuid: self._get_marker_time(uuid, marker_uuids, cycle_start_time) if uuid in marker_uuids else float('nan')
            )

        # Add cycle-specific information
        processed_cycle_df['cycle_id'] = cycle_id
        processed_cycle_df['start_time'] = cycle_start_time
        processed_cycle_df['stop_time'] = cycle_stop_time if cycle_stop_time else cycle_df[self.time_column].max()

        return processed_cycle_df.reset_index(drop=True)

    def _get_marker_time(self, uuid, marker_uuids, cycle_start_time) -> float:
        """
        Returns the normalized time for a marker UUID if it exists in the list of marker_uuids.

        Args:
            uuid (str): The UUID to check for in the marker list.
            marker_uuids (list): The list of marker UUIDs.
            cycle_start_time (Timestamp): The cycle start time to normalize against.
        
        Returns:
            float: The normalized time for the marker, or NaN if the UUID is not a marker.
        """
        if uuid in marker_uuids:
            marker_row = self.dataframe[self.dataframe[self.uuid_column] == uuid]
            if not marker_row.empty:
                marker_time = marker_row[self.time_column].iloc[0]
                return (marker_time - cycle_start_time).total_seconds()
        return float('nan')

    def _calculate_cycle_statistics(self, cycle_df: pd.DataFrame, value_mappings: dict, cycle_id: int) -> dict:
        """
        Calculate cycle-level statistics (duration, mean, max, min, std dev) for a given cycle.

        Args:
            cycle_df (pd.DataFrame): The DataFrame of a single cycle's data.
            value_mappings (dict): A dictionary of sensor types and their corresponding UUIDs.
            cycle_id (int): The unique identifier for the cycle.

        Returns:
            dict: A dictionary of cycle-level statistics.
        """
        # Calculate the duration of the cycle
        cycle_duration = (cycle_df['stop_time'].iloc[0] - cycle_df['start_time'].iloc[0]).total_seconds()

        # Initialize stats dictionary with general cycle info
        stats = {
            'cycle_id': cycle_id,
            'cycle_duration': cycle_duration,
            'start_time': cycle_df['start_time'].iloc[0],
            'stop_time': cycle_df['stop_time'].iloc[0]
        }

        # For each value type (e.g., temperature, pressure), calculate statistics
        for sensor_type in value_mappings.keys():
            if sensor_type in cycle_df.columns:
                stats[f'{sensor_type}_mean'] = cycle_df[sensor_type].mean()
                stats[f'{sensor_type}_max'] = cycle_df[sensor_type].max()
                stats[f'{sensor_type}_min'] = cycle_df[sensor_type].min()
                stats[f'{sensor_type}_std'] = cycle_df[sensor_type].std()
            else:
                # If the column is missing, store NaN
                stats[f'{sensor_type}_mean'] = float('nan')
                stats[f'{sensor_type}_max'] = float('nan')
                stats[f'{sensor_type}_min'] = float('nan')
                stats[f'{sensor_type}_std'] = float('nan')

        return stats