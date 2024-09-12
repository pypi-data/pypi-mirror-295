from typing import List, Union

from gable.api.client import GableAPIClient
from gable.openapi import ErrorResponse


class GableDataAsset:
    def __init__(self, api_endpoint, api_key) -> None:
        self.api_client = GableAPIClient(api_endpoint, api_key)

    def get_full_darns(self, partial_darn: str) -> Union[List[str], ErrorResponse]:
        return self.api_client.get_full_darns(partial_darn)
