import shutil
import pytest
import pandas as pd
from datetime import datetime
from partitioneer.core import (
    PartitionFilter,
    read_data_from_partitions,
    write_data_to_partitions,
    get_latest_partition_date,
    get_first_partition_date
)


@pytest.fixture
def test_data():
    return pd.DataFrame({
        'year': [2023, 2023, 2022],
        'month': [10, 11, 12],
        'day': [1, 2, 31],
        'category': ['A', 'B', 'C'],
        'value': [100, 200, 300]
    })


@pytest.fixture
def base_path():
    path = './test_data'
    yield path
    shutil.rmtree(path)


def test_write_and_read_data(test_data, base_path):
    write_data_to_partitions(test_data, base_path, ['year', 'month', 'day'])
    result_df = read_data_from_partitions(base_path)
    pd.testing.assert_frame_equal(
        test_data.sort_values(by=['year', 'month', 'day'], ascending=False).reset_index(drop=True),
        result_df.sort_values(by=['year', 'month', 'day'], ascending=False).reset_index(drop=True)
    )

def test_read_data_with_filters(test_data, base_path):
    write_data_to_partitions(test_data, base_path, ['year', 'month', 'day'])

    filters = [
        PartitionFilter("year", "equals", 2023),  # Use integer instead of string
        PartitionFilter("month", "greater_than", 10)  # Use integer instead of string
    ]
    result_df = read_data_from_partitions(base_path, filters=filters)
    expected_df = test_data[(test_data['year'] == 2023) & (test_data['month'] > 10)]
    pd.testing.assert_frame_equal(expected_df.reset_index(drop=True), result_df.reset_index(drop=True))

def test_read_data_with_partition_date(test_data, base_path):
    write_data_to_partitions(test_data, base_path, ['year', 'month', 'day'])
    result_df = read_data_from_partitions(base_path, add_partition_date=True)
    assert 'partition_date' in result_df.columns


def test_write_data_with_date_col(base_path):
    df = pd.DataFrame({
        'date': ['2023-10-01', '2023-10-02', '2022-12-31'],
        'value': [100, 200, 300]
    })
    write_data_to_partitions(df, base_path, date_col='date')
    result_df = read_data_from_partitions(base_path)
    assert set(result_df.columns) == {'date', 'value', 'year', 'month', 'day'}
    assert result_df['year'].tolist() == [2023, 2023, 2022]
    assert result_df['month'].tolist() == [10, 10, 12]
    assert result_df['day'].tolist() == [2, 1, 31]

def test_write_data_override_existing(test_data, base_path):
    write_data_to_partitions(test_data, base_path, ['year', 'month', 'day'])
    new_data = pd.DataFrame({
        'year': [2023],
        'month': [10],
        'day': [1],
        'category': ['D'],
        'value': [400]
    })
    write_data_to_partitions(new_data, base_path, ['year', 'month', 'day'], override_existing=True)
    result_df = read_data_from_partitions(base_path)
    expected_df = pd.concat([test_data[test_data['day'] != 1], new_data], ignore_index=True)
    pd.testing.assert_frame_equal(
        expected_df.sort_values(by=['year', 'month', 'day']).reset_index(drop=True),
        result_df.sort_values(by=['year', 'month', 'day']).reset_index(drop=True)
    )

def test_get_latest_partition_date(test_data, base_path):
    write_data_to_partitions(test_data, base_path, ['year', 'month', 'day'])
    latest_date = get_latest_partition_date(base_path)
    assert latest_date == datetime(2023, 11, 2)


def test_get_first_partition_date(test_data, base_path):
    write_data_to_partitions(test_data, base_path, ['year', 'month', 'day'])
    first_date = get_first_partition_date(base_path)
    assert first_date == datetime(2022, 12, 31)


def test_invalid_filter_type():
    with pytest.raises(ValueError):
        read_data_from_partitions('./dummy_path', filters=[PartitionFilter("col", "invalid_type", "value")])


def test_invalid_partition_args():
    df = pd.DataFrame({'col': [1, 2, 3]})
    with pytest.raises(ValueError):
        write_data_to_partitions(df, './dummy_path')
    with pytest.raises(ValueError):
        write_data_to_partitions(df, './dummy_path', partition_cols=['col'], date_col='date')
