""" AZ Storage Ops module """

import os
from datetime import datetime, timedelta
from typing import Any, Dict, Tuple, Union

from azure.storage.blob import BlobServiceClient, generate_container_sas, generate_blob_sas, ContainerSasPermissions
from azure.storage.blob import ContentSettings

from constants import CONTENT_TYPES


class AZStorageTools:
    """Azure Storage Tools class"""

    def __init__(
        self,
        container_name: Union[str, None] = None,
        conn_str: Union[str, None] = None,
        account_name: Union[str, None] = None,
        account_key: Union[str, None] = None,
    ):

        self._blob_service_client = None
        # Get the container name
        if container_name is None:
            self._container_name = os.getenv("AZ_STORAGE_CONTAINER_NAME", None)
            if self._container_name is None:
                raise ValueError("Container name must be given via constructor or AZ_STORAGE_CONTAINER_NAME variable")
        else:
            self._container_name = container_name

        self._conn_str = conn_str

        # Get the connection string if available
        if self._conn_str is None:
            self._conn_str = os.getenv("AZ_STORAGE_CONNECTION_STRING", None)

        if self._conn_str is not None:
            self._blob_service_client = BlobServiceClient.from_connection_string(conn_str=self._conn_str)
            # Get a reference to the container
            self._container_client = self._blob_service_client.get_container_client(self._container_name)

            return
        # Get the account name and key if not using connection string
        if self._blob_service_client is None:
            if account_name is None:
                self._account_name = os.getenv("AZ_STORAGE_ACCOUNT_NAME", None)
            else:
                self._account_name = account_name
            if self._account_name is None:
                raise ValueError("Account name must be given via constructor or AZ_STORAGE_ACCOUNT_NAME variable")
            if account_key is None:
                self._account_key = os.getenv("AZ_STORAGE_ACCOUNT_KEY", None)
            else:
                self._account_key = account_key
            if self._account_key is None:
                raise ValueError("Account key must be given via constructor or AZ_STORAGE_ACCOUNT_KEY variable")

        self.account_url = f"https://{self._account_name}.blob.core.windows.net"

        # Create a BlobServiceClient using the account name and account key
        self._blob_service_client = BlobServiceClient(account_url=self.account_url, credential=self._account_key)

        # Get a reference to the container
        self._container_client = self._blob_service_client.get_container_client(self._container_name)

    def __generate_expiration_time(self, hours: int = 1) -> Tuple[datetime, datetime]:
        """
        Generate an expiration time

        Args:
            hours (int): The length of time period in hours. Defaults to 1.

        Returns:
            Tuple[datetime,datetime]: A tuple of start and end times
        """
        start_time = datetime.utcnow()
        expiry_time = start_time + timedelta(hours=hours)
        return start_time, expiry_time

    def generate_blob_url_with_sas(self, blob_name: str, sas_token: str) -> str:
        """
        Generate a URL for a blob with a SAS token

        Args:
            blob_name (str): Name of the blob
            sas_token (str): Token

        Returns:
            str: url with sas token
        """
        url = self.account_url + "/" + self._container_name + "/" + blob_name + "?" + sas_token

        return url

    def upload_blob_from_url(self, blob_name: str, url: str, **kwargs)-> Dict[str, Any]:
        """
        Upload a blob from a URL

        Args:
            blob_name (str): Name of the blob
            url (str): Url of the blob
        
        Returns:
            Dict[str, Any]: Response from the upload
        """
        return self._container_client.get_blob_client(blob=blob_name).upload_blob_from_url(url, **kwargs)

    def generate_container_sas_token(
        self, pread: bool = True, plist: bool = True, token_validity_hours: int = 1
    ) -> str:
        """
        Generate a SAS token for a container

        Args:
            pread (bool, optional): Read permission. Defaults to True.
            plist (bool, optional): List permission. Defaults to True.
            token_validity_hours (int, optional): Token validity length in hours. Defaults to 1.

        Returns:
            str: Token as a string
        """
        # Set SAS token expiry time
        start_time, expiry_time = self.__generate_expiration_time(hours=token_validity_hours)

        # Generate the SAS token for the container, with the intended
        # permissions for reads and listing.
        permissions = ContainerSasPermissions(read=pread, list=plist)
        sas_token = generate_container_sas(
            self._container_client.account_name,
            self._container_name,
            account_key=self._blob_service_client.credential.account_key,
            permission=permissions,
            start=start_time,
            expiry=expiry_time,
        )
        return sas_token

    def generate_blob_sas_token(
        self, blob_name: str, pread: bool = True, pwrite: bool = False, token_validity_hours: int = 1
    ) -> str:
        """
        Generate a SAS token for a blob

        Args:
            blob_name (str): Name of the blob
            pread (bool, optional): Read permission. Defaults to True.
            token_validity_hours (int, optional): Token validity length in hours. Defaults to 1.

        Returns:
            str: Token as a string
        """
        # Set SAS token expiry time
        start_time, expiry_time = self.__generate_expiration_time(hours=token_validity_hours)

        permissions = ContainerSasPermissions(read=pread, write=pwrite)
        sas_token = generate_blob_sas(
            self._container_client.account_name,
            self._container_name,
            blob_name,
            account_key=self._blob_service_client.credential.account_key,
            permission=permissions,
            start=start_time,
            expiry=expiry_time,
        )

        return sas_token

    def list_blobs(self, prefix: Union[None, str] = None):
        """
        List blobs in a container

        Args:
            prefix (Union[None, str], optional): The name prefix for blobs. Defaults to None.
        """
        blobs = self._container_client.list_blobs(name_starts_with=prefix)
        print("List of Blobs:")
        for blob in blobs:
            print(blob.name)

    def delete_blob(self, blob_name: str):
        """
        Delete a blob

        Args:
            blob_name (str): Name of the blob
        """
        self._container_client.delete_blob(blob_name, recursive=True)

    def upload_blob(self, name: str, data: bytes) -> None:
        """
        Upload data to Azure Blob Storage

        Args:
            name (str): Name of the file
            data (bytes): Data to be uploaded
        """
        filetype = name.split(".")[-1].lower()

        content_settings = ContentSettings()

        content_settings = ContentSettings(content_type=CONTENT_TYPES[filetype])
        self._container_client.upload_blob(name, data, overwrite=True, content_settings=content_settings, timeout=60)

    def download_blobs_by_type(self, blob_paths: dict, filetype: str):
        """
        Downloads blobs by type

        Args:
            blob_paths (dict): The paths of pdf files in Azure storage
            filetype (str): The type of the file

        Returns:
            Tuple [bytes, str, Dict[str,Any]]: Raw file, blob path and blob metadata
        """
        for blob_path, blob_dict in blob_paths.items():
            blob_client = self._container_client.get_blob_client(blob=blob_path)
            content_settings = blob_client.get_blob_properties().content_settings

            # Check the content type, then download the .pdf blob
            if content_settings.content_type == CONTENT_TYPES[filetype]:
                return blob_client.download_blob().readall(), blob_path, blob_dict
