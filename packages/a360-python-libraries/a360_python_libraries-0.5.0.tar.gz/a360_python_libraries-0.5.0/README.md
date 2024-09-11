# a360-python-libraries

Python shared libraries for a360 applications

## License
This software is proprietary and is intended solely for use by Aesthetics-360 Inc.. Unauthorized use, distribution, or modification of this software outside of Aesthetics-360 Inc. is strictly prohibited.

## Add package into your project

```bash
poetry add a360-python-libraries
```

## Usage

### Role based access control

```python
from fastapi import APIRouter, Depends

from a360_security.depends import require_role
from a360_security.enums import Role

router = APIRouter()

@router.get(
    ...,
    dependencies=[Depends(require_role(Role.ADMIN))]
)
def get() -> dict:
    ...
```


### User dependency

```python
from fastapi import APIRouter, Depends

from a360_security.depends import require_user
from a360_security.dto import UserDTO

router = APIRouter()

@router.get(
    ...,
)
def get(user: UserDTO = Depends(require_user)) -> dict:
    ...
```


### Client platform

```python
from fastapi import APIRouter, Depends

from a360_security.depends import require_client_platform
from a360_security.enums import ClientPlatform

router = APIRouter()

@router.get(
    ...,
)
def get(client_platform: ClientPlatform = Depends(require_client_platform)) -> dict:
    ...
```

### Internal services

```python
from fastapi import APIRouter, Depends

from a360_services import get_dictionary_service
from a360_services.services import DictionaryService

router = APIRouter()

@router.get(
    ...,
)
def get(dict_service: DictionaryService = Depends(get_dictionary_service)) -> dict:
    medical_conditions = dict_service.get_medical_conditions()
```