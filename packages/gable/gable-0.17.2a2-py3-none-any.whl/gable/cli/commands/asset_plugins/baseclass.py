from abc import ABC, abstractmethod
from typing import Callable, List, Mapping, NamedTuple, Optional

from gable.api.client import GableAPIClient
from gable.openapi import (
    DataAssetFieldsToProfilesMapping,
    GableSchemaField,
    SourceType,
    StructuredDataAssetResourceName,
)


class ExtractedAsset(NamedTuple):
    darn: StructuredDataAssetResourceName
    fields: List[GableSchemaField]
    dataProfileMapping: Optional[DataAssetFieldsToProfilesMapping]


class AssetPluginAbstract(ABC):
    @abstractmethod
    def source_type(self) -> SourceType:
        """Source type of the asset plugin"""

    @abstractmethod
    def click_options_decorator(self) -> Callable:
        """Decorator for click options for the asset plugin"""

    @abstractmethod
    def click_options_keys(self) -> set[str]:
        """Key names for the click options the asset plugin offers. This should be generated from a TypedDict that the plugin implementation uses
        to access the options. For example:
            return set(TypeScriptConfig.__annotations__.keys())
        """

    @abstractmethod
    def pre_validation(self, config: Mapping) -> None:
        """Validation for the asset plugin's inputs before asset extraction. This is intended
        for validity checks that cannot be done with click's validation and occurs after that validation.
        Should raise a click error like UsageError or MissingParameter.
        """

    @abstractmethod
    def extract_assets(
        self, client: GableAPIClient, config: Mapping
    ) -> List[ExtractedAsset]:
        """Extract assets from the source."""

    @abstractmethod
    def checked_when_registered(self) -> bool:
        pass
