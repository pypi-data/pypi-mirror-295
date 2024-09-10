import json
from urllib.error import HTTPError

from fastapi import Request
from starlette.responses import JSONResponse


async def request_exception_handler(request: Request, error: HTTPError):  # pylint: disable=unused-argument
  error = json.loads(error.response.text).get('error')
  response = {'message': error.get('message')}
  return JSONResponse(response, status_code=error.get('code'))
