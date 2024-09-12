from typing import Any, List, Tuple, Union

from gable.api.client import GableAPIClient
from gable.openapi import GableSchemaContractField, PostContractRequest
from gable.sdk.converters.trino import (
    convert_trino_timestamp_to_spark_timestamp,
    trino_to_gable_type,
)

from .helpers import external_to_internal_contract_input
from .models import ContractPublishResponse, ExternalContractInput, TrinoDataType


class GableContract:
    def __init__(self, api_endpoint, api_key) -> None:
        self.api_client = GableAPIClient(api_endpoint, api_key)

    def publish(
        self,
        contracts: list[ExternalContractInput],
    ) -> List[ContractPublishResponse]:
        responses: List[ContractPublishResponse] = []  # List to store responses

        for contract in contracts:
            # Call the API for each contract
            api_response, success, _status_code = self.api_client.post_contract(
                PostContractRequest(
                    __root__=external_to_internal_contract_input(contract),
                )
            )

            if not success:
                response = ContractPublishResponse(
                    id=contract.contractSpec.id,
                    message=api_response["message"],  # type: ignore
                    success=False,
                )
            else:
                response = ContractPublishResponse(
                    id=contract.contractSpec.id, success=True, message=None
                )

            # Store the response in the list
            responses.append(response)

        return responses

    def trino_to_gable_schema(
        self,
        dict_schema: dict[
            str, Union[str, Union[TrinoDataType, Tuple[TrinoDataType, Tuple[Any, ...]]]]
        ],
        convert_to_spark_types: bool = False,
    ) -> List[GableSchemaContractField]:
        results = [
            trino_to_gable_type(key, value) for key, value in dict_schema.items()
        ]
        if convert_to_spark_types:
            results = [
                convert_trino_timestamp_to_spark_timestamp(result) for result in results
            ]
        return results
