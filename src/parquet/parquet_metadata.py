"""Script for testing and printing parquet file metadata and schema.

This script read a csv-file with pandas, pyarrow and polars and store it in
a parquet files, using different storage options. Then the parquet files are read
and their metadata and schema are printed.
"""

from pathlib import Path

import pandas as pd
import polars as pl
import pyarrow.csv as csv
import pyarrow.parquet as pq


def create_files() -> None:
    """Create parquet file stored with different index options."""
    print("Running create_files")
    data_dir = Path(__file__).parent / "dataset"
    csv_file = data_dir / "customers.csv"
    pandas_df = pd.read_csv(csv_file, parse_dates=["RegistrationDate"])
    pandas_df.to_parquet(data_dir / "pandas-no-index.parquet", index=False)
    pandas_df.to_parquet(data_dir / "pandas-with-index.parquet", index=True)
    pandas_df.to_parquet(data_dir / "pandas-def-index.parquet", index=None)  # Default

    pyarrow_table = csv.read_csv(csv_file)
    pq.write_table(pyarrow_table, data_dir / "pyarrow-def-index.parquet")

    polars_df = pl.read_csv(csv_file)
    polars_df.write_parquet(data_dir / "polars-def-index.parquet")

    # Pandas dataframe with monthly PeriodIndex from January 2020 to December 2020
    monthly_period_index = pd.period_range(start="2020-01", end="2020-12", freq="M")
    temp_oslo = [-1.6, -2.2, 1.8, 5.7, 11.4, 15.8, 16.4, 16.0, 11.3, 6.3, 0.5, -1.3]
    pandas_df_p = pd.DataFrame(
        data={"Average Temperature (°C)": temp_oslo}, index=monthly_period_index
    )
    pandas_df_p.to_parquet(data_dir / "pandas-period-index.parquet")

    # Pandas with categorical data
    pandas_df_cat = pd.DataFrame(
        {"A": list("abca"), "B": list("bccd")}, dtype="category"
    )
    pandas_df_cat.to_parquet(data_dir / "pandas-categorical-data.parquet")


def load_file_pyarrow(name: str) -> pq.ParquetFile:
    """Read the given dataset from a parquet file.

    Args:
        name: Name of the file without the .parquet suffix
    """
    print("Running load_file_pyarrow")
    data_dir = Path(__file__).parent / "dataset"
    file_path = data_dir / f"{name}.parquet"
    print(f"Loading file: {file_path.name}")
    return pq.ParquetFile(file_path)


def load_file_polars(name: str) -> pl.DataFrame:
    """Read the given dataset from a parquet file.

    Args:
        name: Name of the file without the .parquet suffix
    """
    data_dir = Path(__file__).parent / "dataset"
    file_path = data_dir / f"{name}.parquet"
    print(f"Loading file: {file_path.name}")
    return pl.read_parquet(file_path)


def print_metadata(parquet_file: pq.ParquetFile) -> None:
    """Print metadata and schema for a given parquet file."""
    print(parquet_file.schema)
    print(parquet_file.metadata)
    if custom_metadata := parquet_file.metadata.metadata:
        print("\nCustom Metadata:")
        for key, value in custom_metadata.items():
            print(f"{key.decode('utf-8')}: {value.decode('utf-8')}")
    else:
        print("\nNo custom metadata found.")


if __name__ == "__main__":
    create_files()
    file_names = [
        "pandas-def-index",
        "pandas-with-index",
        "pandas-no-index",
        "pyarrow-def-index",
        "polars-def-index",
        "pandas-categorical-data",
        "pandas-period-index",
    ]
    for file_name in file_names:
        print_metadata(load_file_pyarrow(file_name))

    # Try to read all files with polars. Some have reported problems
    # with pandas index columns.
    for file_name in file_names:
        load_file_polars(file_name)
