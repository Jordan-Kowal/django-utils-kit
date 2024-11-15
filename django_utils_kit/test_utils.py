"""Additional TestCase classes for easier testing in Django."""

import datetime
from io import BytesIO
import json
from typing import (
    TYPE_CHECKING,
    Any,
    ByteString,
    Dict,
    Iterable,
    List,
    Mapping,
    Optional,
    OrderedDict,
    Type,
    Union,
)
from urllib.parse import urlencode
from zipfile import ZipFile

from django.contrib.sessions.models import Session
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
from django.db.models import FileField, ImageField, Model, QuerySet
from django.http import StreamingHttpResponse
from django.test import RequestFactory, TestCase
from django.test.client import BOUNDARY, MULTIPART_CONTENT, encode_multipart
from django.utils import timezone
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from django_utils_kit.images import image_to_base64

if TYPE_CHECKING:
    from django.contrib.auth.models import User as UserType

CONTENT_DISPOSITION = 'attachment; filename="{file_name}"'


class AssertionTestCase(TestCase):
    """Adds new assertions to TestCase."""

    def assertDictEqual(
        self,
        d1: Mapping[Any, object],
        d2: Mapping[Any, object],
        msg: Optional[str] = None,
    ) -> None:
        """
        Overrides `assertDictEqual` to handle `OrderedDict` instances.

        Args:
            d1 (Mapping[Any, object]): First dictionary
            d2 (Mapping[Any, object]): Second dictionary
            msg (Optional[str], optional): Error message to display. Defaults to None.
        """
        if isinstance(d1, OrderedDict):
            d1 = dict(d1)
        if isinstance(d2, OrderedDict):
            d2 = dict(d2)
        super().assertDictEqual(d1, d2, msg)

    def assertDateEqualsString(
        self,
        instance_date: Optional[Union[datetime.datetime, datetime.date]],
        string_date: Optional[str],
        format: Optional[str] = "%Y-%m-%dT%H:%M:%S.%fZ",
    ) -> None:
        """
        Compares a date instance with a string date to see if they are equal.

        Args:
            instance_date (Optional[Union[datetime.datetime, datetime.date]]): Optional date or datetime instance
            string_date (Optional[str]): Optional string representation of a date
            format (Optional[str]): The string format. Defaults to "%Y-%m-%dT%H:%M:%S.%fZ".
        """
        if not instance_date:
            self.assertIsNone(string_date)
        else:
            self.assertEqual(instance_date.strftime(format), string_date)

    def assertDownloadFile(self, response: Response, file_name: str) -> None:
        """
        Asserts that a file was downloaded using the `Content-Disposition` header.

        Args:
            response (Response): The HTTP/API response
            file_name (str): The expected filename available in the header
        """
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get("Content-Disposition"),
            CONTENT_DISPOSITION.format(file_name=file_name),
        )

    def assertDownloadZipFile(
        self, response: Response, file_name: str, zip_content: List[str]
    ) -> None:
        """
        Asserts that a zip file was downloaded using the `Content-Disposition` header
        and contains the expected files.

        Args:
            response (Response): The HTTP/API response
            file_name (str): The expected filename for the ZIP file
            zip_content (List[str]): The expected files in the ZIP file
        """
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get("Content-Disposition"),
            CONTENT_DISPOSITION.format(file_name=file_name),
        )
        # Check the zip content
        myzip = ZipFile(BytesIO(response.getvalue()))
        zipped_files = set(myzip.namelist())
        self.assertSetEqual(set(zip_content), zipped_files)

    def assertEmailWasSent(
        self,
        subject: str,
        to: Optional[List[str]] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
    ) -> None:
        """
        Asserts that an email was sent with the provided subject, to, cc, and bcc.

        Args:
            subject (str): The expected subject
            to (Optional[List[str]], optional): List of recipients. Defaults to None.
            cc (Optional[List[str]], optional): List of CC recipients. Defaults to None.
            bcc (Optional[List[str]], optional): List of BCC recipients. Defaults to None.
        """
        email = mail.outbox[-1]
        self.assertEqual(email.subject, subject)
        if to is not None:
            self.assertEqual(len(to), len(email.to))
            self.assertSetEqual(set(to), set(email.to))
        if cc is not None:
            self.assertEqual(len(cc), len(email.cc))
            self.assertSetEqual(set(cc), set(email.cc))
        if bcc is not None:
            self.assertEqual(len(bcc), len(email.bcc))
            self.assertSetEqual(set(bcc), set(email.bcc))

    def assertFieldsHaveError(
        self,
        response: Response,
        key_paths: List[str],
    ) -> None:
        """
        Asserts that the response contains errors for the provided key paths

        Args:
            response (Response): The HTTP/API response
            key_paths (List[str]): A list of paths to the fields
        """
        self.assertEqual(response.status_code, 400)
        for key_path in key_paths:
            # key_path example: "valves.0.description"
            value = response.data
            for key in key_path.split("."):
                if isinstance(value, list):
                    value = value[int(key)]
                else:
                    value = value.get(key)
            self.assertIsNotNone(value)

    def assertFileEqual(
        self,
        file_1: Union[FileField, SimpleUploadedFile],
        file_2: Union[FileField, SimpleUploadedFile],
    ) -> None:
        """
        Asserts that the contents of two files are equal.

        Args:
            file_1 (Union[FileField, SimpleUploadedFile]): The first file to compare
            file_2 (Union[FileField, SimpleUploadedFile]): The second file to compare
        """
        # Reset cursor position to make sure we compare the whole file
        file_1.seek(0)
        file_2.seek(0)
        # .read() must be stored within variable or it won't work
        content_1 = file_1.read()
        content_2 = file_2.read()
        self.assertEqual(content_1, content_2)

    def assertFileIsNone(self, file_field: FileField) -> None:
        """
        Shortcut to assert that a file field is empty.

        Args:
            file_field (FileField): The file field to check.
        """
        self.assertFalse(bool(file_field))

    def assertImageToBase64(
        self, img: ImageField, data: ByteString, resize_to: Optional[int] = None
    ) -> None:
        """
        Asserts that the provided data matches with the base64 representation of the image.

        Args:
            img (ImageField): The image to convert.
            data (ByteString): The expected base64 data.
            resize_to (Optional[int], optional): The size to resize the image to before converting to base 64. Defaults to None.
        """
        converted_image = image_to_base64(img, resize_to)
        self.assertEqual(converted_image, data)

    def assertIntegrityErrorOnSave(self, instance: Model) -> None:
        """
        Shortcut to assert that an integrity error is raised when saving a model instance.

        Args:
            instance (Model): The model instance to save.
        """
        with self.assertRaises(IntegrityError):
            instance.save()

    def assertQuerySetPks(
        self, queryset: QuerySet, expected_pks: Iterable[Any], pk: str = "id"
    ) -> None:
        """
        Shortcut to assert that a query set has the expected pks.

        Args:
            queryset (QuerySet): The query set to check.
            expected_pks (Iterable[Any]): The expected pks.
            pk (str, optional): The primary key field. Defaults to "id".
        """
        queryset_pks = {getattr(item, pk) for item in queryset}
        self.assertSetEqual(queryset_pks, set(expected_pks))


class ImprovedTestCase(AssertionTestCase):
    """Base TestCase with additional assertions and methods."""

    @staticmethod
    def build_fake_request(
        method: str = "get", path: str = "/", data: Dict = None
    ) -> Request:
        """
        Builds a fake request to simulate an HTTP or API call.

        Args:
            method (str, optional): The HTTP method. Defaults to "get".
            path (str, optional): The request path. Defaults to "/".
            data (Dict, optional): The request data. Defaults to None.

        Returns:
            Request: The built request.
        """
        factory = RequestFactory()
        factory_call = getattr(factory, method.lower())
        return factory_call(path, data=data)

    @staticmethod
    def generate_non_existing_id(model_class: Type[Model], pk_field: str = "id") -> Any:
        """
        Generates a new and not-already-existing pk for a model.
        Only works for integer primary keys.

        Args:
            model_class (Type[Model]): The model class.
            pk_field (str, optional): The primary key field. Defaults to "id".

        Returns:
            Any: _description_
        """
        instance = model_class.objects.all().order_by(f"-{pk_field}").first()
        return 1 if not instance else getattr(instance, pk_field) + 1

    @staticmethod
    def uploaded_file_from_path(
        filepath: str, upload_name: Optional[str] = None
    ) -> SimpleUploadedFile:
        """
        Creates a SimpleUploadedFile from a file path.

        Args:
            filepath (str): path to the file
            upload_name (Optional[str], optional): name of the file. Defaults to None.

        Returns:
            SimpleUploadedFile: The uploaded file
        """
        if upload_name is None:
            upload_name = filepath.split("/")[-1]
        with open(filepath, "rb") as f:
            binary_content = f.read()
        return SimpleUploadedFile(name=upload_name, content=binary_content)


class APITestCase(ImprovedTestCase):
    """Base TestCase for API tests."""

    api_client_class: Type[APIClient] = APIClient
    api_client: APIClient
    payload: Dict[str, Any]

    @classmethod
    def setUpClass(cls) -> None:
        """Instantiate the API client."""
        cls.api_client = cls.api_client_class()
        super().setUpClass()

    @staticmethod
    def build_url(
        name: str,
        kwargs: Optional[Dict] = None,
        query_kwargs: Optional[Dict] = None,
    ) -> str:
        """
        Builds a URL from a name and optional kwargs and query kwargs.

        Args:
            name (str): Name of the url (to use `reverse`)
            kwargs (Optional[Dict], optional): The kwargs to pass to `reverse`. Defaults to None.
            query_kwargs (Optional[Dict], optional): The query kwargs to add to the URL. Defaults to None.

        Returns:
            str: The computed URL
        """
        url = reverse(name, kwargs=kwargs)
        if query_kwargs is not None:
            url += f"?{urlencode(query_kwargs)}"
        return url

    @staticmethod
    def disconnect_user(user: "UserType") -> None:
        """
        Removes all active sessions for the user.

        Args:
            user (UserType): A user instance
        """
        user_active_session_ids = []
        all_active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
        for session in all_active_sessions:
            if session.get_decoded().get("_auth_user_id") == str(user.pk):
                user_active_session_ids.append(session.pk)
        if len(user_active_session_ids) > 0:
            Session.objects.filter(pk__in=user_active_session_ids).delete()

    @staticmethod
    def parse_streaming_response(response: StreamingHttpResponse) -> Union[Dict, List]:
        """
        Parses a streaming response into a JSON object.

        Args:
            response (StreamingHttpResponse): The streaming response to parse

        Returns:
            Union[Dict, List]: The parsed JSON object
        """
        return json.loads(b"".join(response.streaming_content).decode("utf-8"))

    def multipart_api_call(
        self,
        method: str,
        url: str,
        payload: Dict[str, Any],
        *args: Any,
        **kwargs: Any,
    ) -> Response:
        """
        Transforms a JSON payload into a flattened form-data and performs a multipart request.

        Args:
            method (str): The HTTP method to use (e.g., "POST", "GET", etc.)
            url (str): The URL to send the request to.
            payload (Dict[str, Any]): The JSON payload to transform into form-data.

        Returns:
            Response: The response from the API call.
        """
        flat_dict = self._dict_to_flat_dict(payload)
        data = encode_multipart(data=flat_dict, boundary=BOUNDARY)
        method = getattr(self.api_client, method.lower())
        return method(url, data=data, content_type=MULTIPART_CONTENT, *args, **kwargs)  # type: ignore

    @staticmethod
    def _dict_to_flat_dict(data: Dict[str, Any]) -> Dict[str, Union[str, int, bool]]:
        """
        Recursively flattens a dict. Keys for nested arrays or dicts might look like this:
        'key[0][subkey][3]'

        Args:
            data (Dict[str, Any]): The dict to flatten

        Returns:
            Dict[str, Union[str, int, bool]]: The flattened dict
        """
        flat_dict = {}

        def _convert_value(current_path: str, current_value: Any) -> None:
            # Undefined values are skipped
            if current_value is None or current_value == "":
                return
            # Array: Add index to path for each value and recurse
            if type(current_value) == list:  # noqa
                for i, sub_value in enumerate(current_value):
                    new_path = f"{current_path}[{i}]"
                    _convert_value(new_path, sub_value)
                return
            # Object: Add key to path for each value and recurse
            if type(current_value) == dict:  # noqa
                for sub_key, sub_value in current_value.items():
                    new_path = f"{current_path}[{str(sub_key)}]"
                    _convert_value(new_path, sub_value)
                return
            # All other cases: Set value
            flat_dict[current_path] = current_value

        for key, value in data.items():
            _convert_value(str(key), value)
        return flat_dict
