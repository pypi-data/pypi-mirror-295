from pyspark.sql import SparkSession
from easy_spark.easy_delta_fs import EasyDeltaFS
from easy_spark.easy_delta_helpers import EasyDeltaHelpers
from easy_spark.easy_df import EasyDF
from easy_spark.table_path import TablePath
from pyspark.sql.functions import *
from delta.tables import *
from pyspark.sql import Row


# TODO: Add Enums
# TODO: Use with
# TODO: Delta Table Can ne null
# TODO: Adding from dict is shit
# TODO: Add Combine
# TODO: Add replace none

class EasyDeltaPath:
    _spark: SparkSession = None

    def __init__(self, path: str = None, spark: SparkSession = None, create_table_if_not_exists: bool = False,
                 create_schema: StructType = None):
        EasyDeltaPath._spark = spark
        self._delta_path = None
        self.path: str = path

        if EasyDeltaPath._spark and self.path:
            self.from_path(self.path, False)

            if create_table_if_not_exists:
                self.create_empty_if_not_exists(create_schema)

            self.init_delta()

    @property
    def delta_path(self):
        return self._delta_path

    def to_easy_df(self) -> EasyDF:
        return EasyDF(self._delta_path.toDF(), EasyDeltaPath._spark)

    def to_fs(self, must_java_import=False) -> EasyDeltaFS:
        return EasyDeltaFS(EasyDeltaPath._spark, self.path, must_java_import)

    @staticmethod
    def table_exists(table_name: str, db_name: str) -> bool:
        return EasyDeltaPath._spark.catalog._jcatalog.tableExists(table_name, db_name)

    @staticmethod
    def file_exists(path: str, must_java_import=False) -> bool:
        return EasyDeltaFS(EasyDeltaPath._spark, path, must_java_import).file_exists()

    def from_path(self, path: str, init_delta: bool = True) -> 'EasyDeltaPath':
        self.path = path

        if init_delta:
            self.init_delta()

        return self

    def from_table_path(self, path: TablePath, init_delta: bool = True) -> 'EasyDeltaPath':
        return self.from_path(path.path, init_delta)

    def init_delta(self) -> 'EasyDeltaPath':
        self._delta_path = DeltaTable.forPath(EasyDeltaPath._spark, self.path)

        return self

    def create_empty_if_not_exists(self, schema: StructType = None, df_format="delta") -> 'EasyDeltaPath':
        if not EasyDeltaPath.file_exists(self.path):
            self.create_empty(schema, df_format)

        return self

    def create_empty(self, schema: StructType = None, df_format="delta") -> 'EasyDeltaPath':
        easy_df = EasyDF(None, EasyDeltaPath._spark)
        easy_df.empty(schema)
        easy_df.save_from_path(self.path, df_format=df_format)

        return self

    def get_dict(self, keys: dict[str, any]) -> dict[str, any] | None:
        df = self.to_easy_df().filter(keys).df
        if df is None or df.count() == 0:
            return None

        rows = df.collect()
        return rows[0].asDict()

    def get_dict_using_filter(self, keys: dict[str, any]) -> dict[str, any] | None:
        df = self.to_easy_df().filter_using_filter(keys).df
        if df is None or df.count() == 0:
            return None

        rows = df.collect()
        return rows[0].asDict()

    def get_dict_by_filter(self, condition: str) -> dict[str, any] | None:
        df = self.to_easy_df().filter_by_filter(condition).df
        if df is None or df.count() == 0:
            return None

        rows = df.collect()
        return rows[0].asDict()

    def get_rows_using_filter(self, keys: dict[str, any] = None) -> list[Row]:
        return self.to_easy_df().filter_using_filter(keys).df.collect()

    def get_rows_by_filter(self, condition: str = None) -> list[Row]:
        return self.to_easy_df().filter_by_filter(condition).df.collect()

    def get_rows(self, keys: dict[str, any] = None) -> list[Row]:
        return self.to_easy_df().filter(keys).df.collect()

    def get_list(self, keys: dict[str, any] = None) -> list[dict[str, any]]:
        rows = self.get_rows(keys)
        return [row.asDict() for row in rows]

    def get_list_by_filter(self, condition: str = None) -> list[dict[str, any]]:
        rows = self.get_rows_by_filter(condition)
        return [row.asDict() for row in rows]

    def add_from_dict(self, record: dict, df_format="delta") -> 'EasyDeltaPath':
        easy_df = self.to_easy_df()
        easy_df.append_from_dict(record)
        easy_df.save_from_path(self.path, df_format=df_format)
        return self

    def add_from_df(self, df: DataFrame, df_format="delta", type: str = 'unionByName',
                    allowMissingColumns: bool = True) -> 'EasyDeltaPath':
        easy_df = self.to_easy_df()
        easy_df.combine_from_df(df, type, allowMissingColumns)
        easy_df.save_from_path(self.path, df_format=df_format)
        return self

    def update(self, keys: dict[str, any], values: dict[str, any]) -> 'EasyDeltaPath':
        conditions = EasyDeltaPath._build_condition(keys)

        sets = {k: lit(v) for k, v in values.items()}

        self._delta_path.update(
            condition=conditions,
            set=sets
        )
        return self

    def update_by_condition(self, condition: str, values: dict[str, any]) -> 'EasyDeltaPath':
        sets = {k: lit(v) for k, v in values.items()}
        self._delta_path.update(
            condition=condition,
            set=sets
        )
        return self

    def delete(self, keys: dict[str, any] = None,
               multiple_keys: list[tuple[str, list]] = None) -> 'EasyDeltaPath':
        conditions = ""

        if keys:
            conditions = EasyDeltaPath._build_condition(keys)

        if multiple_keys:
            for key in multiple_keys:
                if conditions == "":
                    conditions += f"{key[0]} in {tuple(key[1])}"
                else:
                    conditions += f" and {key[0]} in {tuple(key[1])}"

        self._delta_path.delete(condition=conditions)
        return self

    def delete_by_multiple_keys(self, key: str, key_values: list) -> 'EasyDeltaPath':
        self._delta_path.delete(f"{key} in {tuple(key_values)}")
        return self

    def delete_by_condition(self, condition: str) -> 'EasyDeltaPath':
        self._delta_path.delete(condition)
        return self

    def delete_all(self, df_format="delta") -> 'EasyDeltaPath':
        df = EasyDeltaPath._spark.createDataFrame([], StructType([]))
        EasyDF(df, EasyDeltaPath._spark).save_from_path(self.path, df_format=df_format, mode="overwrite")
        return self

    def merge_from_list(self, keys: list[str], records: list[dict], schema: StructType = None,
                        add_missing_coloumns=True,
                        add_missing_coloumns_to_current=False, df_format="delta") -> 'EasyDeltaPath':

        df = EasyDeltaPath._spark.createDataFrame(records, schema)
        return self.merge_from_df(keys, df, add_missing_coloumns, add_missing_coloumns_to_current, df_format)

    def merge_from_df(self, keys: list[str], df: DataFrame, add_missing_coloumns=True,
                      add_missing_coloumns_to_current=False, df_format="delta") -> 'EasyDeltaPath':
        current_df = self._delta_path.toDF()
        df_coloumns = df.columns
        current_coloumns = current_df.columns

        if add_missing_coloumns:
            for current_coloumn in current_coloumns:
                if current_coloumn not in df_coloumns:
                    df = df.withColumn(current_coloumn, lit(None).cast(current_df.schema[current_coloumn].dataType))

        if add_missing_coloumns_to_current:
            current_df_has_new_columns = False
            for df_colomn in df_coloumns:
                if df_colomn not in current_coloumns:
                    current_df = current_df.withColumn(df_colomn, lit(None).cast(df.schema[df_colomn].dataType))
                    current_df_has_new_columns = True

            if current_df_has_new_columns:
                # TODO: Fix this
                EasyDF(current_df, EasyDeltaPath._spark).save_from_path(self.path, df_format=df_format,
                                                                        mode="overwrite",
                                                                        merge_option="overwriteSchema")

                # TODO: Fix this
                self._delta_path = DeltaTable.forPath(EasyDeltaPath._spark, self.path)

        merge_relationships = [f"A.`{key}` = B.`{key}` and " for key in keys]
        merge_relationships = "".join(merge_relationships)[:-4]
        self._delta_path.alias('A').merge(
            df.alias('B'),
            merge_relationships
        ).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()

        return self

    # Private Method
    @staticmethod
    def _build_condition(keys: dict[str, any]):
        return EasyDeltaHelpers.build_condition(keys)
