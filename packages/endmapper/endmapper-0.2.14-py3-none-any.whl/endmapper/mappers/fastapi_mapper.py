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
        return JSONResponse({"error": "FastAPI app not connected"}, status_code=401)
    if not isinstance(main_app, FastAPI):
        return JSONResponse({"error": f"FastAPI app has incorrect type: current={type(main_app)} | need=FastAPI"}, status_code=401)

    config = BaseEndpointMapper.config()
    result = endpoint_handlers.FastAPIEndpointHandler(main_app, **config.options).result

    main_app.include_router(router)

    return JSONResponse(result, status_code=200)
