from pyspark.sql.functions import *


class EasyDeltaHelpers:

    @staticmethod
    def build_condition(keys: dict[str, any]):
        conditions = ""
        if keys is None or len(keys) == 0:
            return conditions

        for key, value in keys.items():
            if conditions == "":
                conditions += f"{key} == '{value}'"
            else:
                conditions += f" & {key} == '{value}'"
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
