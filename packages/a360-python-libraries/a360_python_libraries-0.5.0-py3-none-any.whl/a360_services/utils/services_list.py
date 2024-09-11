from enum import Enum

from ..settings import settings


class Services(str, Enum):
    dict = settings.PROJECT_HOST_SERVICE_DICT
    patient = settings.PROJECT_HOST_SERVICE_PATIENTS
    practice = settings.PROJECT_HOST_SERVICE_PRACTICES
    consultation = settings.PROJECT_HOST_SERVICE_CONSULTATIONS
    product = settings.PROJECT_HOST_SERVICE_PRODUCTS
    ml = settings.PROJECT_HOST_SERVICE_ML
    cms = settings.PROJECT_HOST_SERVICE_CMS
