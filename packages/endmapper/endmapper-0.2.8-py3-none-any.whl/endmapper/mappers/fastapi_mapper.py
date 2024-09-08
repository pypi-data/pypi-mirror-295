from fastapi import APIRouter

from endmapper import endpoint_handlers
from endmapper.mappers.base_mapper import BaseEndpointMapper


router = APIRouter()


@router.get('api/endpoints/')
def get(response):
    """
    ATTENTION: include "router" to main FastAPI app

    This will add new endpoint "api/endpoints/" to your project
    """
    config = BaseEndpointMapper.config()
    result = endpoint_handlers.FastAPIEndpointHandler(**config.options).result
    return result
