import pandas as pd, numpy as np
from types import MethodType
from pandas.core.groupby import DataFrameGroupBy


class CustomGroupBy(DataFrameGroupBy):
    def __init__(self, *args, grouped_keys: list[str], **kwargs):
        super().__init__(*args, **kwargs)
        self.grouped_keys = grouped_keys

    def __iter__(self):
        for condition_values, group in super().__iter__():
            if not isinstance(condition_values, (tuple)):
                condition_values = (condition_values,)
            conditions = {key: value for key, value in zip(self.grouped_keys, condition_values)}
            yield conditions, group


@pd.api.extensions.register_dataframe_accessor("grp")
class GroupUtilsAccessor:
    def __init__(self, pandas_obj):
        self._validate(pandas_obj)
        self._obj = pandas_obj

    @staticmethod
    def _validate(obj):
        if not isinstance(obj, pd.DataFrame):
            raise TypeError("Cannot use grp on an accessor that is not a pandas DataFrame")

    def filter(self, **kwargs):
        index_names = self._obj.index.names
        dataframe = self._obj.reset_index()
        for key, value in kwargs.items():
            if isinstance(value, list):
                dataframe = dataframe[dataframe[key].isin(value)]
            else:
                dataframe = dataframe[dataframe[key] == value]
        return dataframe.set_index(index_names)

    def merged(self, merged_key, merged_value, extra_condition_keys=[]):
        # for the merged_key, i want the
        if merged_key in extra_condition_keys:
            raise ValueError(f"merged_key:{merged_key} cannot be in extra_condition_keys:{extra_condition_keys}")

        uniques_merged_values = self._obj[merged_key].unique()
        uniques_merged_values = np.delete(
            uniques_merged_values,
            np.where(uniques_merged_values == merged_value),
            axis=None,
        )

        for non_merged_value in uniques_merged_values:
            merged_group = self._obj[
                (self._obj[merged_key] == non_merged_value) | (self._obj[merged_key] == merged_value)
            ]
            conditions = {merged_key: non_merged_value}

            if extra_condition_keys:
                for condition_values, group in merged_group.groupby(extra_condition_keys):
                    conditions.update({key: value for key, value in zip(extra_condition_keys, condition_values)})

                    yield conditions.copy(), group  # copy to avoid inconsistency issues if the dict is changed outside
                    # between iterations
            else:
                yield conditions.copy(), merged_group

    def groupby(self, condition_keys: str | list[str], *args, **kwargs):

        if not isinstance(condition_keys, (list, tuple)):
            condition_keys = [condition_keys]

        grouped_object = self._obj.groupby(condition_keys, *args, **kwargs)
        custom_groupby_object = CustomGroupBy(
            grouped_object.obj, grouped_object.grouper, grouped_object.axis, grouped_keys=condition_keys
        )

        return custom_groupby_object

    def exclude(self, key, value):
        """_summary_

        Args:
            key (_type_): _description_
            value (_type_): _description_

        Returns:
            _type_: _description_
        """
        return self._obj[self._obj[key] != value]

    def apply_settings(self, settings_dict):
        """_summary_

        Args:
            settings_dict (_type_):
                example of filter dict :
                {"groupby": [
                    "in_target_barrel",
                    "nontarget_amplitude",
                    "target_whisker",
                ],
                "merged_key": "frequency_change",
                "merged_value": 0,
                "exclude" : {}
            }
        """
        dataframe = self._obj

        # excluding data that
        if (exclusions := settings_dict.get("exclude", None)) is not None:
            for key, value in exclusions.items():
                dataframe = dataframe.grp.exclude(key, value)

        groupby_settings = settings_dict.get("groupby", [])

        if ((merged_key_settings := settings_dict.get("merged_key", None)) is not None) and (
            (merged_value_settings := settings_dict.get("merged_value", None)) is not None
        ):
            yield from dataframe.grp.merged(
                merged_key_settings,
                merged_value_settings,
                groupby_settings,
            )

        elif len(groupby_settings):
            yield from dataframe.grp.groupby(groupby_settings)

        else:
            conditions = {}
            yield (
                conditions,
                dataframe,
            )  # mimick the output of groupby for compatibility, but grouped on no condition


# @pd.api.extensions.register_series_accessor("one")
# class OneAcessor:
#     def __init__(self, pandas_obj) -> None:
#         self._validate(pandas_obj)
#         self._obj = pandas_obj
#         self.project = self._obj.projects[0]

#     @staticmethod
#     def _validate(obj):
#         required_fields = ["path","alias","subject","date","number","json","qc","rel_path","admin_url","projects"]
#         missing_fields = []
#         for req_field in required_fields :
#             if not req_field in obj.index :
#                 missing_fields.append(req_field)
#         if len(missing_fields):
#             raise AttributeError(f"The series must have some fields to use one acessor.
#               This object is missing fields : {','.join(missing_fields)}")
