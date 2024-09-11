from dataclasses import dataclass, field
from typing import List

from dataclasses_json import dataclass_json

from tenyks_sdk.file_providers.config import StorageLocationType
from tenyks_sdk.file_providers.data_classes import FileSelectorDefinition


@dataclass_json
@dataclass
class AWSS3Credentials:
    aws_access_key_id: str
    aws_secret_access_key: str
    region_name: str


@dataclass_json
@dataclass
class AWSLocation:
    s3_uri: str
    credentials: AWSS3Credentials
    type: StorageLocationType
    selectors: List[FileSelectorDefinition] = field(default_factory=list)
    write_permission: bool = False


@dataclass_json
@dataclass
class AWSVideoLocation:
    type: StorageLocationType
    s3_uri: str
    credentials: AWSS3Credentials
