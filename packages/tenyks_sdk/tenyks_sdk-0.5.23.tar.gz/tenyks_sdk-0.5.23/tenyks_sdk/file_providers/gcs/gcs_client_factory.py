from typing import Dict

from google.cloud.storage import Client

from tenyks_sdk.file_providers.gcs.gcs_client import GCSClient


class GCSClientFactory:
    @staticmethod
    def create_client(
        gcs_credentials: Dict[str, str],
    ) -> GCSClient:
        gcs_client = GCSClient(Client.from_service_account_info(gcs_credentials))

        return gcs_client
