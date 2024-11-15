from django.http import HttpResponse, StreamingHttpResponse
from django.views import View
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from django_utils_kit.exceptions import Conflict, FailedPrecondition
from django_utils_kit.files import download_file, download_files_as_zip
from django_utils_kit.permissions import BlockAll, IsNotAuthenticated
from django_utils_kit.tests.fake_app.serializers import BasicSerializer
from django_utils_kit.tests.fake_app.storage import MockStorage
from django_utils_kit.viewsets import ImprovedViewSet


class ConflictExampleView(APIView):
    def get(self, _request: Request) -> Response:
        raise Conflict()


class FailedPreconditionExampleView(APIView):
    def get(self, _request: Request) -> Response:
        raise FailedPrecondition()


class DownloadFileView(View):
    def get(self, request: Request) -> StreamingHttpResponse:
        return download_file("path/to/file.txt", MockStorage())


class DownloadZipFileView(View):
    def get(self, request: Request) -> HttpResponse:
        return download_files_as_zip(
            ["path/to/file1.txt", "path/to/file2.txt"], "output.zip", MockStorage()
        )


class BlockAllViewSet(GenericViewSet):
    permission_classes = [BlockAll]

    def list(self, request: Request) -> Response:
        return Response()


class IsNotAuthenticatedViewSet(GenericViewSet):
    permission_classes = [IsNotAuthenticated]

    def list(self, request: Request) -> Response:
        return Response(data={"is_authenticated": False})


class ImprovedViewSetExample(ImprovedViewSet):
    default_permission_classes = [BlockAll]
    default_serializer_class = None
    permission_classes_per_action = {"list": [AllowAny]}
    serializer_class_per_action = {"list": BasicSerializer}

    def list(self, request: Request) -> Response:
        if request.query_params.get("error") == "true":
            self.get_valid_serializer(data={"id": "ok"})
        serializer = self.get_valid_serializer(data={"id": 1})
        data = {"name": serializer.__class__.__name__}
        return Response(data)

    def retrieve(self, request: Request, pk: int) -> Response:
        return Response()
