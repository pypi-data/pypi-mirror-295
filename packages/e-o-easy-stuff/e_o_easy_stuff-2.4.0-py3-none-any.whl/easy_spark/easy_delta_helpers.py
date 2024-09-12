from pyspark.sql.functions import *


class EasyDeltaHelpers:

    @staticmethod
    def build_condition(keys: dict[str, any], conditions=""):
        conditions = conditions

        if keys is None or len(keys) == 0:
            return conditions

        for key, value in keys.items():
            is_integer = isinstance(value, int) or isinstance(value, float)
            if not conditions == "":
                conditions += f" And "

            if is_integer:
                conditions += f"{key} == {value}"
            else:
                conditions += f"{key} == '{value}'"

        return conditions

    @staticmethod
    def build_condition_by_multiple_keys(multiple_keys: list[tuple[str, list]], conditions=""):
        conditions = conditions

        if multiple_keys is None or len(multiple_keys) == 0:
            return conditions

        for key in multiple_keys:
            if key[1] is None and len(key[1]) == 0:
                continue

            if not conditions == "":
                conditions += f" And "

            if len(key[1]) == 1:
                conditions = EasyDeltaHelpers.build_condition({key[0]: key[1][0]}, conditions)
            else:
                conditions += f"{key[0]} in {tuple(key[1])}"
        return conditions

    @staticmethod
    def combine_from_dfs(dfs: list[DataFrame], type: str = 'unionByName',
                         allowMissingColumns: bool = True) -> DataFrame:

        # Fid the index of df in dfs with the most number of columns
        index_df = 0
        for df in dfs:
            if len(df.columns) > len(dfs[index_df].columns):
                index_df = dfs.index(df)

        combine_df = dfs[index_df]

        if len(dfs) > 1:
            others_dfs = dfs[:index_df] + dfs[index_df + 1:]
            for other_df in others_dfs:
                if type == 'unionByName':
                    combine_df = combine_df.unionByName(other_df, allowMissingColumns=allowMissingColumns)
                else:
                    combine_df = combine_df.union(other_df)

                    # TODO: Move this
        # if replace_nan:
        #     combine_df = combine_df.replace({np.nan: None}).replace({"nan": None})

        return combine_df
