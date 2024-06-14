import pyarrow.parquet as pq

from parquet.parquet_metadata import create_files
from parquet.parquet_metadata import load_file_pyarrow


def test_load_file_pyarrow():
    create_files()
    parquet_file = load_file_pyarrow("pyarrow-def-index")
    assert isinstance(parquet_file, pq.ParquetFile)
    assert parquet_file.metadata.num_rows == 3
