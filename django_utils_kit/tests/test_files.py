from django_utils_kit.test_utils import APITestCase


class FilesTestCase(APITestCase):
    def test_download_file(self) -> None:
        response = self.api_client.get("/download-file/")
        self.assertDownloadFile(response, "file.txt")

    def test_download_files_as_zip(self) -> None:
        response = self.api_client.get("/download-zip/")
        self.assertDownloadZipFile(response, "output.zip", ["file1.txt", "file2.txt"])
