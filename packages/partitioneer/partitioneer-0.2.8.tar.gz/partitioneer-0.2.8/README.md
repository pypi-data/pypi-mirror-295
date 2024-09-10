# Partitioneer

Partitioneer is a Python library that provides utilities for managing data files in a date-partitioned format. It offers functions for writing data to partitions, reading data from partitions with filtering capabilities, and retrieving partition date information.

## Installation

You can install Partitioneer using pip:

```sh
pip install partitioneer
```

## Usage

### Writing Data to Partitions

To write data to partitioned Parquet files:

```python
from partitioneer import write_data_to_partitions
import pandas as pd

df = pd.DataFrame(...)  # Your data
write_data_to_partitions(
    df,
    base_path="/path/to/data",
    date_col="date_column",
    override_existing=False
)
```

### Reading Data from Partitions

To read data from partitioned Parquet files:

```python
from partitioneer import read_data_from_partitions, PartitionFilter

df = read_data_from_partitions(
    base_path="/path/to/data",
    filters=[
        PartitionFilter("category", "in", ["A", "B"]),
        PartitionFilter("value", "greater_than", 100)
    ],
    add_partition_date=True,
    start_date="2024-01-01",
    end_date="2024-12-31"
)
```

### Getting Partition Date Information

To get the latest or first partition date:

```python
from partitioneer import get_latest_partition_date, get_first_partition_date

latest_date = get_latest_partition_date("/path/to/data")
first_date = get_first_partition_date("/path/to/data")
```

## Build Instructions

To build the package:

```sh
python setup.py sdist bdist_wheel
```

To upload to PyPI:

```sh
pip install twine
twine upload dist/*
```

Automated build and publish script:

```shell
python setup.py sdist bdist_wheel
pip install twine
twine upload dist/* --password <add_pypi_token_here>
rm -r ./build
rm -r ./dist
rm -r ./partitioneer.egg-info
```

## License

[MIT License](LICENSE)