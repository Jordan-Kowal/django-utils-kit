from io import BytesIO

from django.core.files.storage import Storage


class MockStorage(Storage):
    def open(self, path: str, mode: str = "rb") -> BytesIO:
        content = f"Example file content {path}"
        return BytesIO(content.encode())

    def exists(self, name: str) -> bool:
        return True
