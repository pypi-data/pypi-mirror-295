# FastAPI Exception

## Installation

```shell
pip install fastapi-exception
```

## How to use


### fastapi_exception exposes exceptions

- FastApiException
- ForbiddenException
- NotFoundException
- GoneException
- BadRequestException
- DirectResponseException
- EntityNotFoundException
- UnauthorizedException

### fastapi_exception exposes errors

- DuplicateError
- StringTooLongError
- StringTooShortError
- MissingError


### Configuration

```python
# config/exception.py
from config.i18n import i18n_service
from fastapi_exception import FastApiException

FastApiException.init()
FastApiException.init(translator_service=i18n_service) # pass translator_service if we integrate with i18n
```

### Use exceptions with throw_validation

```python
from fastapi_exception import throw_validation

throw_validation(type='value_error', loc=('body', 'key'))
```

### Use errors with throw_validation_with_exception

```python

from fastapi_exception import throw_validation_with_exception, MissingError

raise throw_validation_with_exception(MissingError(('body', 'product media or galleries')))
```

### Customize Exception

```python
from fastapi_exception import ValidationErrorDetail

class InvalidDataTypeError(ValidationErrorDetail):
  error_type = 'datatype.invalid'

  def __init__(
    self,
    loc: tuple[int | str, ...],
    ctx: dict[str, dict[str, Any]] | None = {},
    input: dict[str, Any] = {},
  ):
    super().__init__(self.error_type, loc, '', input, ctx)

throw_validation_with_exception(InvalidDataTypeError(('body', 'value')))
```
