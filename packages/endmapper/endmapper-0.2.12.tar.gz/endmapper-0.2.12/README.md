# Endmapper

Endmapper is a library for mapping endpoints.

## Installation

```bash
pip install endmapper
```

## Config file "cmapcfg.json"

```yaml
{
  //This keywords must be in path
  "path_white_list": [],
  //This keywords could not be in path
  "path_black_list": [],
  //This keywords must be in endpoint name 
  "name_white_list": [],
  //This keywords could not be in endpoint name
  "name_black_list": [],
  //Services use with proxy endpoints
  //Service what you want to connect must use endmapper too
  "services": {
    "endpoint_name": "hostname or ip"
  }
}
```

## How to use with django/drf

- add new path to main project urls
```python
from django.urls import path, include

urlpatterns = [
    # another paths
    path('', include('endmapper.urls'))
]
```

## How to use with fastAPI