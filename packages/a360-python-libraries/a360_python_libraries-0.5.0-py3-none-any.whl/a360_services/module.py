from fastapi import Depends

from .services import DictionaryService
from .utils.service_provider import ServiceProvider, get_service_provider


def get_dictionary_service(service_provider: ServiceProvider = Depends(
        get_service_provider)) -> DictionaryService:
    return DictionaryService(service_provider=service_provider)
