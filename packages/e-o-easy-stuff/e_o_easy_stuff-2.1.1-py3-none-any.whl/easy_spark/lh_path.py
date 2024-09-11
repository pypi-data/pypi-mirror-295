from easy_spark.path import Path
from easy_spark.table_path import TablePath


class LHPath(TablePath):
    def __init__(self, path: Path, schema: str, table_name: str):
        super().__init__(path, schema, table_name, is_lh=True)
