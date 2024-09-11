from pyspark.sql import SparkSession
from py4j.java_gateway import java_import


class EasyDeltaFS:
    _spark: SparkSession = None

    def __init__(self, spark: SparkSession = None, path: str = None, must_java_import=False):
        EasyDeltaFS._spark = spark

        self.hadoop_conf = None
        self.fs = None
        self.file_path = None
        self.path: str = path

        if spark:
            if must_java_import:
                java_import(EasyDeltaFS._spark._jvm, 'org.apache.hadoop.fs.FileSystem')
                java_import(EasyDeltaFS._spark._jvm, 'org.apache.hadoop.conf.Configuration')
                java_import(EasyDeltaFS._spark._jvm, 'org.apache.hadoop.fs.Path')

            self.hadoop_conf = EasyDeltaFS._spark._jsc.hadoopConfiguration()
            self.fs = EasyDeltaFS._spark._jvm.FileSystem.get(self.hadoop_conf)

        if self.path and EasyDeltaFS._spark:
            self.file_path = EasyDeltaFS._spark._jvm.Path(self.path)

    def from_path(self, path: str) -> 'EasyDeltaFS':
        self.path = path
        self.file_path = EasyDeltaFS._spark._jvm.Path(self.path)
        return self

    def file_exists(self) -> bool:
        return self.fs.exists(self.file_path)

    def delete_file(self) -> bool:
        return self.fs.delete(self.file_path, True)

    def write_file_content(self, content: any, delete_if_exists: bool = False) -> bool:

        if delete_if_exists:
            if self.file_exists():
                self.delete_file()
        elif self.file_exists():
            return False

        output_stream = self.fs.create(self.file_path)
        try:
            output_stream.write(content)
        finally:
            output_stream.close()

        return True
