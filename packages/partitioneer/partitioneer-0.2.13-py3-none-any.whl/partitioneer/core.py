import os
from typing import List, Union, Optional, Literal
from datetime import datetime, date
from dataclasses import dataclass
import pandas as pd
from tqdm import tqdm
from multiprocessing.dummy import Pool
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from .manual_parameters import DEFAULT_THREADS

FilterType = Literal[
    "equals",
    "not_equal",
    "greater_than",
    "less_than",
    "greater_than_or_equal",
    "less_than_or_equal",
    "in",
    "not_in",
]


@dataclass
class PartitionFilter:
    """
    Represents a filter to be applied on partitioned data.

    Attributes:
        column (str): The name of the column to filter on.
        filter_type (FilterType): The type of filter to apply.
        value (Union[str, List[str], int, List[int], float, List[float]]): The value(s) to compare against.

    Example:
        PartitionFilter("age", "greater_than", 18)
        PartitionFilter("category", "in", ["A", "B", "C"])
    """
    column: str
    filter_type: FilterType
    value: Union[str, List[str], int, List[int], float, List[float]]


def write_partition(args):
    df, base_path, partition_cols, data_file_name, override_existing, duplicate_existing = args
    path = base_path
    for col in partition_cols:
        path = os.path.join(path, f"{col}={df[col].iloc[0]}")

    os.makedirs(path, exist_ok=True)
    file_path = os.path.join(path, data_file_name)

    if os.path.exists(file_path):
        if override_existing:
            df.to_parquet(file_path, index=False)
        elif duplicate_existing:
            existing_df = pd.read_parquet(file_path)
            new_df = pd.concat([existing_df, df], ignore_index=True)
            new_df.to_parquet(file_path, index=False)
    else:
        df.to_parquet(file_path, index=False)


def get_threads_given_iterable(iterable_to_process):
    min_sensible = min(len(iterable_to_process), DEFAULT_THREADS)
    return max(min_sensible, 1)


def find_parquet_files(path):
    files = []
    try:
        for entry in os.scandir(path):
            if entry.is_file() and entry.name.endswith('.parquet'):
                files.append(entry.path)
            elif entry.is_dir():
                files.extend(find_parquet_files(entry.path))
    except (PermissionError, FileNotFoundError):
        print(f"Error accessing: {path}")
    return files

def find_parquet_files_parallel(base_path, num_threads=None):
    if num_threads is None:
        num_threads = DEFAULT_THREADS

    if not os.path.exists(base_path):
        print(f"Base path does not exist: {base_path}")
        return []

    if not os.path.isdir(base_path):
        print(f"Base path is not a directory: {base_path}")
        return []

    # Get year directories
    year_dirs = [os.path.join(base_path, d) for d in os.listdir(base_path)
                 if os.path.isdir(os.path.join(base_path, d)) and d.startswith('year=')]

    if not year_dirs:
        # If there are no year directories, search the base_path directly
        return find_parquet_files(base_path)

    # Get month directories for each year
    month_dirs = []
    for year_dir in year_dirs:
        month_dirs.extend([os.path.join(year_dir, m) for m in os.listdir(year_dir)
                           if os.path.isdir(os.path.join(year_dir, m)) and m.startswith('month=')])

    if not month_dirs:
        # If there are no month directories, use year directories
        search_dirs = year_dirs
    else:
        search_dirs = month_dirs

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        results = list(executor.map(find_parquet_files, search_dirs))

    all_files = [file for sublist in results for file in sublist]
    return all_files

def write_data_to_partitions(
        df: pd.DataFrame,
        base_path: str,
        partition_cols: Optional[List[str]] = None,
        date_col: Optional[str] = None,
        override_existing: bool = False,
        duplicate_existing: bool = False,
        data_file_name: str = "data.parquet",
        num_threads: Optional[int] = None
) -> None:
    """
    Write data to partitioned Parquet files.

    Args:
        df (pd.DataFrame): The DataFrame to write.
        base_path (str): The base path to write the partitioned data to.
        partition_cols (Optional[List[str]]): The columns to partition by.
        date_col (Optional[str]): The date column to use for partitioning.
        override_existing (bool): Whether to override existing files.
        data_file_name (str): The name of the data file in each partition.
        num_processes (int): The number of processes to use for multiprocessing.

    Raises:
        ValueError: If neither partition_cols nor date_col is provided, or if both are provided.
    """
    if (partition_cols is None and date_col is None) or (partition_cols is not None and date_col is not None):
        raise ValueError("Either partition_cols or date_col must be provided, but not both.")

    if len(df) == 0:
        print(f"INFO: Dataframe is empty. No data to be written to `{os.path.basename(base_path)}`.") # TODO: Use proper logging.
        return

    if date_col:
        df[date_col] = pd.to_datetime(df[date_col])
        partition_cols = ['year', 'month', 'day']
        df['year'] = df[date_col].dt.year
        df['month'] = df[date_col].dt.month
        df['day'] = df[date_col].dt.day

    df = df.sort_values(by=partition_cols)

    if not override_existing and not duplicate_existing:
        existing_dates = set()
        for root, _, files in os.walk(base_path):
            if all(f"{col}=" in root for col in partition_cols):
                parts = root.split(os.path.sep)
                date_parts = {col: int(next(part.split('=')[1] for part in parts if part.startswith(f"{col}="))) for col
                              in partition_cols}
                existing_dates.add(tuple(date_parts[col] for col in partition_cols))

        df = df[~df[partition_cols].apply(tuple, axis=1).isin(existing_dates)]

    grouped = df.groupby(partition_cols)

    if num_threads is None:
        num_threads = get_threads_given_iterable(grouped)

    with Pool(processes=num_threads) as pool:
        list(tqdm(pool.imap_unordered(
            write_partition,
            [(group, base_path, partition_cols, data_file_name, override_existing, duplicate_existing) for _, group in
             grouped]),
            total=len(grouped),
            desc=f"Writing data to `{os.path.basename(base_path)}`"
        ))


def convert_to_datetime(date_input: Optional[Union[str, datetime, date]]) -> Optional[datetime]:
    if date_input is None:
        return None
    if isinstance(date_input, datetime):
        return date_input
    if isinstance(date_input, date):
        return datetime(date_input.year, date_input.month, date_input.day)
    if isinstance(date_input, str):
        return datetime.strptime(date_input, "%Y-%m-%d")
    raise ValueError(f"Invalid date input: {date_input}")


def read_and_filter_partition(args):
    file_path, filters, start_date, end_date, add_partition_date = args
    df = pd.read_parquet(file_path)
    parts = file_path.split(os.path.sep)
    date_parts = {}
    for part in parts:
        if '=' in part:
            col, val = part.split('=')
            if col not in df.columns:
                df[col] = val
            if col in ['year', 'month', 'day']:
                date_parts[col] = int(val)

    if len(date_parts) == 3:
        partition_date = datetime(date_parts['year'], date_parts['month'], date_parts['day'])
        if start_date and partition_date < start_date:
            return None
        if end_date and partition_date > end_date:
            return None
        if add_partition_date:
            df['partition_date'] = partition_date

    if filters:
        for filter in filters:
            if filter.filter_type == "equals":
                df = df[df[filter.column] == filter.value]
            elif filter.filter_type == "not_equal":
                df = df[df[filter.column] != filter.value]
            elif filter.filter_type == "greater_than":
                df = df[df[filter.column] > filter.value]
            elif filter.filter_type == "less_than":
                df = df[df[filter.column] < filter.value]
            elif filter.filter_type == "greater_than_or_equal":
                df = df[df[filter.column] >= filter.value]
            elif filter.filter_type == "less_than_or_equal":
                df = df[df[filter.column] <= filter.value]
            elif filter.filter_type == "in":
                df = df[df[filter.column].isin(filter.value)]
            elif filter.filter_type == "not_in":
                df = df[~df[filter.column].isin(filter.value)]
            else:
                raise ValueError(f"Invalid filter type: {filter.filter_type}")

    return df if not df.empty else None


def read_data_from_partitions(
        base_path: str,
        filters: Optional[Union[PartitionFilter, List[PartitionFilter]]] = None,
        add_partition_date: bool = False,
        start_date: Optional[Union[str, datetime, date]] = None,
        end_date: Optional[Union[str, datetime, date]] = None,
        num_threads: Optional[int] = None
) -> pd.DataFrame:
    """
    Read data from partitioned Parquet files.

    Args:
        base_path (str): The base path containing partitioned Parquet files.
        filters (Optional[Union[PartitionFilter, List[PartitionFilter]]]): Filters to apply to the data.
        add_partition_date (bool): Whether to add a partition_date column to the result.
        start_date (Optional[Union[str, datetime, date]]): The start date for filtering (inclusive).
        end_date (Optional[Union[str, datetime, date]]): The end date for filtering (inclusive).

    Returns:
        pd.DataFrame: The combined and filtered data from all partitions.

    Raises:
        ValueError: If an invalid filter type is provided.
    """

    start_date = convert_to_datetime(start_date)
    end_date = convert_to_datetime(end_date)

    if isinstance(filters, PartitionFilter):
        filters = [filters]

    all_files = find_parquet_files_parallel(base_path, num_threads)

    if num_threads is None:
        num_threads = get_threads_given_iterable(all_files)

    with Pool(processes=num_threads) as pool:
        dfs = list(tqdm(
            pool.imap_unordered(
                read_and_filter_partition,
                [(file, filters, start_date, end_date, add_partition_date) for file in all_files]
            ),
            total=len(all_files),
            desc=f"Reading data from `{os.path.basename(base_path)}`"
        ))

    # Remove None values (filtered out partitions) and concatenate
    result = pd.concat([df for df in dfs if df is not None], ignore_index=True)

    if 'partition_date' in result.columns:
        return result.sort_values(by='partition_date', ascending=False)
    else:
        # If partition_date is not available, try to create it from year, month, day columns
        date_cols = ['year', 'month', 'day']
        if all(col in result.columns for col in date_cols) and add_partition_date:
            result['partition_date'] = pd.to_datetime(result[date_cols])
            return result.sort_values(by='partition_date', ascending=False)
        else:
            # If we can't create a partition_date, just return the result unsorted
            return result.sort_values(by=date_cols, ascending=False)


def get_latest_partition_date(base_path: str) -> Optional[datetime]:
    """
    Get the latest partition date from the directory structure.

    Args:
        base_path (str): The base path containing partitioned Parquet files.

    Returns:
        Optional[datetime]: The latest partition date, or None if no date partitions found.
    """
    latest_date = None
    for root, dirs, files in os.walk(base_path):
        if 'year=' in root and 'month=' in root and 'day=' in root:
            parts = root.split(os.path.sep)
            year = int(next(part.split('=')[1] for part in parts if part.startswith('year=')))
            month = int(next(part.split('=')[1] for part in parts if part.startswith('month=')))
            day = int(next(part.split('=')[1] for part in parts if part.startswith('day=')))
            current_date = datetime(year, month, day)
            if latest_date is None or current_date > latest_date:
                latest_date = current_date
    return latest_date


def read_latest_partition(base_path: str, *args, **kwargs) -> pd.DataFrame:
    latest_partition = get_latest_partition_date(base_path)
    df = read_data_from_partitions(
        base_path,
        *args,
        start_date=latest_partition,
        end_date=latest_partition,
        **kwargs
    )
    return df


def read_first_partition(base_path: str, *args, **kwargs) -> pd.DataFrame:
    first_partition = get_first_partition_date(base_path)
    df = read_data_from_partitions(
        base_path,
        *args,
        start_date=first_partition,
        end_date=first_partition,
        **kwargs
    )
    return df


def get_first_partition_date(base_path: str) -> Optional[datetime]:
    """
    Get the first partition date from the directory structure.

    Args:
        base_path (str): The base path containing partitioned Parquet files.

    Returns:
        Optional[datetime]: The first partition date, or None if no date partitions found.
    """
    first_date = None
    for root, dirs, files in os.walk(base_path):
        if 'year=' in root and 'month=' in root and 'day=' in root:
            parts = root.split(os.path.sep)
            year = int(next(part.split('=')[1] for part in parts if part.startswith('year=')))
            month = int(next(part.split('=')[1] for part in parts if part.startswith('month=')))
            day = int(next(part.split('=')[1] for part in parts if part.startswith('day=')))
            current_date = datetime(year, month, day)
            if first_date is None or current_date < first_date:
                first_date = current_date
    return first_date
