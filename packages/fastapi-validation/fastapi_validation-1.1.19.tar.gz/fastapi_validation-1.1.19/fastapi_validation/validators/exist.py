from typing import Any, Callable, Optional

from fastapi_exception import EntityNotFoundException
from fastapi_global_variable import GlobalVariable
from pydantic import ValidationInfo

from ..constants.validator_constant import VALIDATOR_EXISTS
from ..enums.database_type_enum import DatabaseTypeEnum
from ..types.custom_condition_type import CustomCondition
from .nosql_exists import NosqlExists
from .sql_exist import SqlExists


class Exists:
  __name__ = VALIDATOR_EXISTS

  def __init__(
    self,
    table,
    column: Any,
    case_insensitive: bool = False,
    customs: Optional[list[CustomCondition]] = [],
    custom_error: Optional[Callable] | None = EntityNotFoundException,
  ):
    self.table = table
    self.column = column
    self.case_insensitive = case_insensitive
    self.customs = customs
    self.exist_validator = self.get_exist_validator()
    self.custom_error = custom_error

  def get_exist_validator(self):
    if GlobalVariable.get('database_type') == DatabaseTypeEnum.SQL:
      return SqlExists(self.table, self.column, self.case_insensitive, self.customs)

    return NosqlExists(self.table, self.column, self.case_insensitive, self.customs)

  def __call__(self, values: Optional[Any] | list[Optional[Any]], info: ValidationInfo) -> Optional[Any]:
    if not values:
      return values

    is_list = isinstance(values, list)
    if not is_list:
      values = [values]

    for value in values:
      criterion = self.exist_validator.init_criterion(value)

      self.exist_validator.build_custom_criterion(criterion, info.data)

      if not self.exist_validator.validate(*criterion):
        raise self.custom_error(self.table)

    return values if is_list else values[0]
