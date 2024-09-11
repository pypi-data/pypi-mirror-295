from typing import Union
from urllib.parse import urlencode

from a360_services.utils.service_provider import ServiceProvider
from a360_services.utils.services_list import Services


class DictionaryService:
    def __init__(self, service_provider: ServiceProvider):
        self.service_provider = service_provider

    def get_allergies(self, icd10_codes: list[str]) -> dict:
        query_params = {'icd10_code': icd10_codes}
        request_path = f"/allergies?{urlencode(query_params, doseq=True)}"
        return self.service_provider.fetch_data(
            service=Services.dict,
            request_path=request_path
        ).get('items')

    def get_medical_conditions(self, icd10_codes: list[str]) -> dict:
        query_params = {'icd10_code': icd10_codes}
        request_path = f"/medical_conditions?{urlencode(query_params, doseq=True)}"
        return self.service_provider.fetch_data(
            service=Services.dict,
            request_path=request_path
        ).get('items')

    def get_countries(self, iso_codes: list[str]) -> dict:
        query_params = {'iso_code': iso_codes}
        request_path = f"/countries?{urlencode(query_params, doseq=True)}"
        return self.service_provider.fetch_data(
            service=Services.dict,
            request_path=request_path
        ).get('items')

    def get_states(self,
                   iso_codes: list[str],
                   country_iso_code: Union[None,
                                           str] = None) -> dict:
        query_params = {'iso_code': iso_codes}
        request_path = f"/states?{urlencode(query_params, doseq=True)}"
        if country_iso_code:
            request_path = f"/countries/{country_iso_code}/states?{urlencode(query_params, doseq=True)}"
        return self.service_provider.fetch_data(
            service=Services.dict,
            request_path=request_path
        ).get('items')

    def get_cities(self, city_ids: list[str]) -> dict:
        query_params = {'id': city_ids}
        request_path = f"/cities?{urlencode(query_params, doseq=True)}"
        return self.service_provider.fetch_data(
            service=Services.dict,
            request_path=request_path
        ).get('items')
