"""Utilities for handling files with DRF."""

from io import BytesIO
from urllib.parse import urlparse
import zipfile

from django.core.files.storage import Storage
from django.http import HttpResponse, StreamingHttpResponse


def download_file(path: str, storage: Storage) -> StreamingHttpResponse:
    """
    Downloads a file from a storage backend.

    Args:
        path (str): path to the file
        storage (Storage): storage backend

    Returns:
        StreamingHttpResponse: the streaming response containing the file
    """
    filename = urlparse(path).path.split("/").pop()
    response = StreamingHttpResponse(streaming_content=storage.open(path))
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


def download_files_as_zip(
    paths: list[str], output_filename: str, storage: Storage
) -> HttpResponse:
    """
    Downloads a zip-file from a storage backend.

    Args:
        paths (list[str]): paths to the files
        output_filename (str): name of the generated and to-be-downloaded zip-file
        storage (Storage): storage backend

    Returns:
        HttpResponse: the response containing the zip-file
    """
    content = BytesIO()
    with zipfile.ZipFile(content, "w") as zf:
        for path in paths:
            filename = urlparse(path).path.split("/").pop()
            zf.writestr(filename, storage.open(path).read())
    response = HttpResponse(content.getvalue())
    response["Content-Disposition"] = f'attachment; filename="{output_filename}"'
    return response
