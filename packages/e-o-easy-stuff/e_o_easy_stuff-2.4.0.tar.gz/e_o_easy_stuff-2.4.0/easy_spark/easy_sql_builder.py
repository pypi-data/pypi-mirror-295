from easy_spark.easy_delta_helpers import EasyDeltaHelpers
from easy_spark.table_path import TablePath


class EasySQLSelectBuilder:
    def __init__(self):
        self.sql: str = "SELECT"
        pass;

    def select(self, columns: list[str]) -> 'EasySQLSelectBuilder':
        self.sql += " " + ", ".join(columns)
        return self

    def from_table(self, table: str) -> 'EasySQLSelectBuilder':
        self.sql += f" FROM {table}"
        return self

    def from_lh_table(self, name: str, table: str) -> 'EasySQLSelectBuilder':
        self.sql += f" FROM {name}.{table}"
        return self

    def from_path(self, path: str) -> 'EasySQLSelectBuilder':
        self.sql += f" FROM delta.`{path}`"
        return self

    def from_table_path(self, path: TablePath) -> 'EasySQLSelectBuilder':
        return self.from_path(path.path)

    def where(self, keys: dict[str, any]) -> 'EasySQLSelectBuilder':
        conditions = EasyDeltaHelpers.build_condition(keys)

        self.sql += f" WHERE {conditions}"
        return self

    def where_from_condition(self, condition: str) -> 'EasySQLSelectBuilder':
        self.sql += f" WHERE {condition}"
        return self

    @staticmethod
    def new() -> 'EasySQLSelectBuilder':
        return EasySQLSelectBuilder()
