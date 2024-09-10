""" Module for handling storage configurations. """

import base64
from urllib.parse import quote
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional
from azure.storage.blob import BlobServiceClient, ContainerClient, generate_blob_sas, BlobSasPermissions
from loguru import logger
from tqdm import tqdm
from aimmocore import config as conf
from aimmocore.core import utils


class StorageType(Enum):
    """Enum class for storage types."""

    AZURE = "blob"
    AWS = "s3"
    GCP = "gs"
    LOCAL = "local"


class StorageConfig:
    """Base storage configuration class."""

    def __init__(self, storage_type: StorageType):
        """
        Initializes the StorageConfig.

        Args:
            storage_type (StorageType): The type of storage service.
        """
        self.storage_type = storage_type
        self.credentials: Optional[dict] = None

    def generate_image_properties(self) -> list:
        """
        Generates file properties like signed url, size, ... for the storage service.
        [{"url": "https://example.com/image.jpg", "size": 1024}]
        """
        properties = []
        return properties

    def get_dataset_source(self) -> str:
        """
        Returns the dataset source string.
        """
        return str(self.storage_type.value)


class AzureStorageConfig(StorageConfig):
    """Azure storage configuration class."""

    def __init__(self, account_name: str, container_name: str, account_key: str):
        """
        Initializes the AzureStorageConfig.

        Args:
            account_name (str): The Azure storage account name.
            container_name (str): The Azure storage container name.
            account_key (str): The Azure storage account key.
        """
        super().__init__(StorageType.AZURE)
        self.account_name = account_name
        self.container_name = container_name
        self._is_valid_account_key(account_key)
        self.account_key = account_key

    def get_dataset_source(self):
        """Returns the dataset source."""
        return self.storage_type.value + f"://{self.account_name}/{self.container_name}"

    def _get_total_files_in_blobs(self, container_client):
        """Get the total number of files in the container.

        Calculates the total number of files in the specified Azure Blob Storage container,
        excluding those that are considered directories.

        Args:
            container_client: The client object for accessing the Azure Blob Storage container.

        Returns:
            int: The total count of non-directory blobs (files) in the container.
        """
        blob_list = container_client.list_blobs()
        return sum(1 for blob in blob_list if "/" not in blob.name or not blob.name.endswith("/"))

    def list_valid_image_blobs(self, container_client):
        """List and filter valid images based on the extension.

        Args:
            container_client: The client object for accessing the Azure Blob Storage container.

        Returns:
            list: A list of blobs that are valid images as per the supported file extensions.
        """
        logger.info("Check and filter valid images from the blobs.")
        total_files = self._get_total_files_in_blobs(container_client)
        blob_list = container_client.list_blobs()
        valid_images = [blob for blob in blob_list if utils.is_supported_ext(blob.name, conf.SUPPORT_IMAGE_EXTENSIONS)]
        if len(valid_images) < conf.CURATION_MINIMUM_SIZE:
            raise ValueError(f"The number of images is less than the minimum size({conf.CURATION_MINIMUM_SIZE}).")
        ignored_files = total_files - len(valid_images)
        if len(valid_images) != total_files:
            logger.warning(f"Some files({ignored_files}) are not supported and will be ignored.")
            logger.warning(f"Supported extensions: {conf.SUPPORT_IMAGE_EXTENSIONS}")
        logger.info(f"Checked {len(valid_images)} valid images from {total_files} files.")
        return valid_images

    def get_container_client(self) -> ContainerClient:
        """
        Creates and returns a ContainerClient object for the specified container.

        Returns:
            ContainerClient: A client object that can be used to interact with the specified Azure Blob Storage container.
        """
        blob_service_client = BlobServiceClient(
            account_url=f"https://{self.account_name}.blob.core.windows.net", credential=self.account_key
        )
        return blob_service_client.get_container_client(self.container_name)

    def generate_image_properties(self) -> list:
        """
        Generates a list of properties for each image file stored in Azure Blob Storage.

        Returns:
            list of dict: A list where each dictionary contains the 'url' and 'size' of an image.
                        The 'url' includes a SAS token allowing read access for 30 days, and
                        'size' is the size of the image in bytes.

        """
        properties = []
        container_client = self.get_container_client()
        image_blobs = self.list_valid_image_blobs(container_client)
        for blob in tqdm(image_blobs, desc="Generating sas url from blobs"):
            enc_blob_name = quote(blob.name)  # Encode the blob name for the URL
            sas_token = generate_blob_sas(
                account_name=self.account_name,
                container_name=self.container_name,
                blob_name=blob.name,
                account_key=self.account_key,
                permission=BlobSasPermissions(read=True),
                expiry=datetime.utcnow() + timedelta(hours=24 * 30),  # Set the expiry time as needed
            )
            sas_url = (
                f"https://{self.account_name}.blob.core.windows.net/{self.container_name}/{enc_blob_name}?{sas_token}"
            )
            blob_properties = container_client.get_blob_client(blob).get_blob_properties()
            properties.append({"url": sas_url, "size": blob_properties.size})
        return properties

    def _is_valid_account_key(self, account_key: str):
        """
        Check if the given Azure Blob Storage account key is valid.

        Args:
            account_key (str): The account key to validate.

        Returns:
            bool: True if the account key is valid, False otherwise.
        """
        try:
            decoded_key = base64.b64decode(account_key)
            if len(decoded_key) != 64:
                raise ValueError("Invalid Azure Blob Storage account key.")
        except (base64.binascii.Error, TypeError):
            raise ValueError("Invalid Azure Blob Storage account key.")
