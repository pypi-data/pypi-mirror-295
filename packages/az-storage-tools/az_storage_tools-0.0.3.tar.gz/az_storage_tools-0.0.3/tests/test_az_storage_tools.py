import unittest

from unittest.mock import patch, MagicMock
from src.az_storage_tools import AZStorageTools


class TestAZStorageTools(unittest.TestCase):

    @patch("src.az_storage_tools.BlobServiceClient")
    def setUp(self, MockBlobServiceClient):
        self.mock_blob_service_client = MockBlobServiceClient.return_value
        self.mock_container_client = self.mock_blob_service_client.get_container_client.return_value
        self.az_storage_tools = AZStorageTools(
            container_name="test-container", account_name="test-account", account_key="test-key"
        )

    def test_false_init(self):
        with self.assertRaises(ValueError):
            AZStorageTools()

    @patch("src.az_storage_tools.BlobServiceClient")
    def test_init_with_conn_str(self, MockBlobServiceClient):

        conn_str = "DefaultEndpointsProtocol=https;AccountName={your-storage};AccountKey={your-access-key};EndpointSuffix=core.windows.net"

        AZStorageTools(
            container_name="test",
            conn_str=conn_str,
        )

        MockBlobServiceClient.from_connection_string.called_once_with(conn_str=conn_str)

    @patch("src.az_storage_tools.BlobServiceClient")
    def test_init_with_account_and_key(self, MockBlobServiceClient):

        AZStorageTools(
            container_name="test",
            account_name="test-account",
            account_key="test-key",
        )

        MockBlobServiceClient.called_once_with(
            account_url="https://test-account.blob.core.windows.net", credential="test-key"
        )

    def test_generate_blob_url_with_sas(self):
        sas_token = "test-sas-token"
        blob_name = "test-blob"
        expected_url = f"https://test-account.blob.core.windows.net/test-container/{blob_name}?{sas_token}"
        url = self.az_storage_tools.generate_blob_url_with_sas(blob_name, sas_token)
        self.assertEqual(url, expected_url)

    @patch("src.az_storage_tools.generate_container_sas")
    def test_generate_container_sas_token(self, mock_generate_container_sas):
        mock_generate_container_sas.return_value = "test-sas-token"
        sas_token = self.az_storage_tools.generate_container_sas_token()
        self.assertEqual(sas_token, "test-sas-token")

    @patch("src.az_storage_tools.generate_blob_sas")
    def test_generate_blob_sas_token(self, mock_generate_blob_sas):
        mock_generate_blob_sas.return_value = "test-blob-sas-token"
        sas_token = self.az_storage_tools.generate_blob_sas_token(blob_name="test-blob")
        self.assertEqual(sas_token, "test-blob-sas-token")

    def test_list_blobs(self):
        mock_blob = MagicMock()
        mock_blob.name = "test-blob"
        self.mock_container_client.list_blobs.return_value = [mock_blob]
        with patch("builtins.print") as mocked_print:
            self.az_storage_tools.list_blobs()
            mocked_print.assert_called_with("test-blob")

    def test_delete_blob(self):
        self.az_storage_tools.delete_blob("test-blob")
        self.mock_container_client.delete_blob.assert_called_with("test-blob", recursive=True)

    def test_upload_blob(self):
        data = b"test data"
        self.az_storage_tools.upload_blob("test.txt", data)
        _, args, kwargs = self.mock_container_client.upload_blob.mock_calls[0]

        assert args[0] == "test.txt"
        assert args[1] == data
        assert kwargs["content_settings"]["content_type"] == "text/plain"

    def test_download_blobs_by_type(self):
        blob_paths = {"test-blob": {}}
        mock_blob_client = MagicMock()
        mock_blob_client.get_blob_properties.return_value.content_settings.content_type = "application/pdf"
        mock_blob_client.download_blob.return_value.readall.return_value = b"test data"
        self.mock_container_client.get_blob_client.return_value = mock_blob_client

        with patch("src.az_storage_tools.CONTENT_TYPES", {"pdf": "application/pdf"}):
            result = self.az_storage_tools.download_blobs_by_type(blob_paths, "pdf")
            self.assertEqual(result, (b"test data", "test-blob", {}))


if __name__ == "__main__":

    unittest.main()
