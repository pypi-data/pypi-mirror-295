from typing import Any, Optional

from fastapi_global_variable import GlobalVariable
from pydantic import ValidationError
from requests import Request
from starlette import status
from starlette.responses import JSONResponse

from fastapi_exception.constants.error import CUSTOM_ERROR_TYPE
from fastapi_exception.custom_errors.validation_error_detail import ValidationErrorDetail

from ..translators.base_translator_service import BaseTranslatorService


class ErrorResponse:
  def __init__(self, translator_service: BaseTranslatorService, error: ValidationErrorDetail):
    self.translator_service = translator_service

    if isinstance(error, dict):
      self.type = error.get('type')
      self.loc = error.get('loc')
      self.ctx = error.get('ctx')
      self.msg = error.get('msg')
      self.property = error.get('property')
      self.custom_msg = error.get('custom_msg')
    else:
      self.type = error.type
      self.loc = error.loc
      self.ctx = error.ctx
      self.msg = error.msg
      self.property = error.property
      self.custom_msg = error.custom_msg

  """
       {
           "message": "Validation error",
           "errors": [
               {
                   "type": "string_too_short",
                   "loc": [
                       "body",
                       "hashtags",
                       1
                   ],
                   "msg": "hashtags[1] should have at least 1 characters"
               }
           ]
        }
    """

  def build_constrains(self, loc: tuple[int | str, ...], ctx: Optional[dict[str, Any]]):
    error_property = self.property or loc[-1]
    constraints: dict[str, Any] = {}

    if isinstance(error_property, int):
      error_index = error_property
      error_property = loc[-2]
      constraints['property'] = f'{error_property}[{error_index}]'
    else:
      constraints = {'property': error_property}

    if ctx:
      constraints.update(ctx)

    return constraints

  def translate_message(self):
    if self.type == CUSTOM_ERROR_TYPE or not self.translator_service:
      return self.msg

    constraints = self.build_constrains(self.loc, self.ctx)
    return self.translator_service.translate(f'validation.{self.type}', **constraints)

  def generate(self):
    return {
      'type': self.type,
      'loc': self.loc,
      'msg': self.custom_msg or self.translate_message(),
    }


async def validation_exception_handler(request: Request, error: ValidationError):  # pylint: disable=unused-argument
  response = {'message': 'Validation error', 'errors': translate_errors(error.errors())}
  return JSONResponse(response, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


def translate_errors(errors: list[ValidationErrorDetail]) -> list[ValidationErrorDetail]:
  translator_service: BaseTranslatorService = GlobalVariable.get('translator_service')

  return [ErrorResponse(translator_service, error).generate() for error in errors]
