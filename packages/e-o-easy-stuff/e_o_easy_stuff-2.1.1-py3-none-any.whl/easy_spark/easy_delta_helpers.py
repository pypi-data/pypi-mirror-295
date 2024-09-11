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
