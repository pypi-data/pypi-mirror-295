from pyspark.sql import Row
from pyspark.sql.functions import *

from easy_spark.easy_sql_builder import EasySQLSelectBuilder
from easy_spark.lh_path import LHPath
from easy_spark.table_path import TablePath
from pyspark.sql import SparkSession

from easy_spark.wh_path import WHPath


class EasyDF:
    _spark: SparkSession = None

    # Constructor
    def __init__(self, df: DataFrame = None, spark: SparkSession = None):
        self._df: DataFrame = df
        if spark is not None:
            EasyDF._spark = spark

    @property
    def df(self) -> DataFrame:
        return self._df

    def from_table_path(self, path: TablePath, df_format="delta") -> 'EasyDF':
        self._df = EasyDF._spark.read.format(df_format).load(path.path)
        return self

    def from_path(self, path: str, df_format="delta") -> 'EasyDF':
        self._df = EasyDF._spark.read.format(df_format).load(path)
        return self

    def from_sql_builder(self, sql_builder: EasySQLSelectBuilder) -> 'EasyDF':
        self._df = EasyDF._spark.sql(sql_builder.sql)
        return self

    def from_lh_flat_path(self, path: tuple[str, str, str, str], df_format="delta") -> 'EasyDF':
        from easy_spark.path import Path
        return self.from_table_path(LHPath(Path(path[0], path[1]), path[2], path[3]), df_format)

    def from_wh_flat_path(self, path: tuple[str, str, str, str], df_format="delta") -> 'EasyDF':
        from easy_spark.path import Path
        return self.from_table_path(WHPath(Path(path[0], path[1]), path[2], path[3]), df_format)

    def from_dict(self, records: dict, schema: StructType = None) -> 'EasyDF':
        self._df = EasyDF._spark.createDataFrame([Row(**records)], schema)
        return self

    def from_list(self, records: list[dict], schema: StructType = None) -> 'EasyDF':
        self._df = EasyDF._spark.createDataFrame(records, schema)
        return self

    def from_sql(self, sql: str) -> 'EasyDF':
        self._df = EasyDF._spark.sql(sql)
        return self

    def from_lh_name_path(self, name: str, table_name: str, limt: int = None) -> 'EasyDF':
        if limt:
            self._df = EasyDF._spark.sql(f"SELECT * FROM {name}.{table_name} LIMIT {limt}")
        else:
            self._df = EasyDF._spark.sql(f"SELECT * FROM {name}.{table_name}")

        return self

    def append_from_dict(self, record: dict) -> 'EasyDF':
        self._df = self._df.union(EasyDF._spark.createDataFrame([Row(**record)], self._df.schema))
        return self

    def append_from_row(self, row: Row) -> 'EasyDF':
        self._df = self._df.union(EasyDF._spark.createDataFrame([row], self._df.schema))
        return self

    def save_from_table_path(self, path: TablePath, df_format="delta", mode="overwrite",
                             merge_option: str = "overwriteSchema") -> 'EasyDF':
        self._df.write.format(df_format).mode(mode).option(merge_option, "true").save(path.path)
        return self

    def save_as_table(self, path: str, df_format="delta", mode="overwrite",
                      merge_option: str = "overwriteSchema") -> 'EasyDF':
        self._df.write.format(df_format).mode(mode).option(merge_option, "true").saveAsTable(path)
        return self

    def save_from_path(self, path: str, df_format="delta", mode="overwrite",
                       merge_option: str = "overwriteSchema") -> 'EasyDF':
        self._df.write.format(df_format).mode(mode).option(merge_option, "true").save(path)
        return self
