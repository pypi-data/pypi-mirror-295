from fastapi import APIRouter, FastAPI
from fastapi.responses import JSONResponse

from endmapper import endpoint_handlers
from endmapper.mappers.base_mapper import BaseEndpointMapper


router = APIRouter()
main_app = None


def connect_app(app: FastAPI):
    global main_app
    main_app = app


@router.get('/api/endpoints/')
def get_endpoints():
    global main_app
    """
    ATTENTION: include "router" to main FastAPI app

    This will add new endpoint "api/endpoints/" to your project
    """
    if main_app is None:
        return JSONResponse({"error": "No app not connected"}, status_code=200)

    config = BaseEndpointMapper.config()
    result = endpoint_handlers.FastAPIEndpointHandler(**config.options).result
    return JSONResponse(result, status_code=200)
