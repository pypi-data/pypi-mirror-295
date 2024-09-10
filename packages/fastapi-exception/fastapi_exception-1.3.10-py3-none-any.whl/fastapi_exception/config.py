from typing import Any, Optional

from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi_global_variable import GlobalVariable
from keycloak import KeycloakAuthenticationError, KeycloakPostError
from requests import RequestException

from .exceptions.direct_response import DirectResponseException
from .handlers.global_exception_handler import http_global_exception_handler
from .handlers.http_exception_handler import http_direct_response_handler, http_exception_handler
from .handlers.key_cloak_exception_handler import keycloak_exception_handler, keycloak_post_exception_handler
from .handlers.request_exception_handler import request_exception_handler
from .handlers.validation_exception_handler import validation_exception_handler
from .translators.base_translator_service import BaseTranslatorService


class FastApiException:
  i18n_service: Any = None

  @staticmethod
  def config(translator_service: Optional[BaseTranslatorService] = None):
    return FastApiException(translator_service)

  def __init__(self, translator_service: Optional[BaseTranslatorService] = None):
    GlobalVariable.set('translator_service', translator_service)
    app = GlobalVariable.get_or_fail('app')

    app.exception_handler(Exception)(http_global_exception_handler)
    app.exception_handler(HTTPException)(http_exception_handler)
    app.exception_handler(DirectResponseException)(http_direct_response_handler)
    app.exception_handler(RequestValidationError)(validation_exception_handler)
    app.exception_handler(RequestException)(request_exception_handler)
    app.exception_handler(KeycloakAuthenticationError)(keycloak_exception_handler)
    app.exception_handler(KeycloakPostError)(keycloak_post_exception_handler)
