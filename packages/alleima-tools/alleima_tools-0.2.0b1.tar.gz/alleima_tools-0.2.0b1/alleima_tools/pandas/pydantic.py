from typing import Any

from pandas import DataFrame
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema


class _DataFrameAnnotation:
    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type: Any, _handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        def validate_from_dataframe(value: DataFrame) -> DataFrame:
            return value

        from_dataframe_schema = core_schema.chain_schema(
            [core_schema.no_info_plain_validator_function(validate_from_dataframe)]
        )
