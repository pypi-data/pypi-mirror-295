from fastapi import APIRouter, FastAPI
from fastapi.responses import JSONResponse

from endmapper import endpoint_handlers
from endmapper.mappers.base_mapper import BaseEndpointMapper


router = APIRouter()
main_app = None


def connect_app(app: FastAPI):
    global main_app

    if not isinstance(main_app, FastAPI):
        raise Exception(f"FastAPI app has incorrect type: current={type(app)} | need=FastAPI")

    main_app = app
    main_app.include_router(router)


@router.get('/api/endpoints/')
def get_endpoints():
    global main_app
    """
    ATTENTION: include "router" to main FastAPI app

    This will add new endpoint "api/endpoints/" to your project
    """
    if main_app is None:
        return JSONResponse({"error": "FastAPI app not connected"}, status_code=401)

    config = BaseEndpointMapper.config()
    result = endpoint_handlers.FastAPIEndpointHandler(main_app, **config.options).result



    return JSONResponse(result, status_code=200)
