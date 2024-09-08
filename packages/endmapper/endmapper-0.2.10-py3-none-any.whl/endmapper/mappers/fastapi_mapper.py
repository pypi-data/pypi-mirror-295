from fastapi import APIRouter, FastAPI

from endmapper import endpoint_handlers
from endmapper.mappers.base_mapper import BaseEndpointMapper


router = APIRouter()
main_app = None


def connect_app(app: FastAPI):
    global main_app
    main_app = app


@router.get('/api/endpoints/')
def get(response):
    global main_app
    """
    ATTENTION: include "router" to main FastAPI app

    This will add new endpoint "api/endpoints/" to your project
    """
    if main_app is None:
        return {"error": "No app not connected"}
    config = BaseEndpointMapper.config()
    result = endpoint_handlers.FastAPIEndpointHandler(**config.options).result
    return result
