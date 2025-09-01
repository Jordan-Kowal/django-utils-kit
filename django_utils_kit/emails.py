"""Classes to easily send sync and async emails through Django."""

from threading import Thread
from typing import Any

from django.conf import settings
from django.core.mail import EmailMessage
from django.template import loader


class Email:
    """Class to send async/sync emails through Django using templates and contexts."""

    def __init__(
        self,
        default_subject: str,
        template_path: str,
    ) -> None:
        """
        Initializes the Email class with a template and a default subject.

        Args:
            default_subject (str): The default subject of the email (can be overridden in `send`).
            template_path (str): The path to the template to use for the email.
        """
        self.default_subject = default_subject
        self.template_path = template_path

    def send(
        self,
        context: dict[str, Any],
        subject: str | None = None,
        to: list[str] | None = None,
        cc: list[str] | None = None,
        bcc: list[str] | None = None,
        from_email: str | None = None,
    ) -> None:
        """
        Sends an email using the current template and the provided context.
        Does nothing if no recipients are provided.

        Args:
            context (dict[str, Any]): The context to render the template with.
            subject (str | None, optional): The subject of the email. Defaults to None.
            to (list[str] | None, optional): The list of recipients. Defaults to None.
            cc (list[str] | None, optional): The list of CC recipients. Defaults to None.
            bcc (list[str] | None, optional): The list of BCC recipients. Defaults to None.
            from_email (Optional[str], optional): The sender email address. Defaults to None.
        """
        to = to or []
        cc = cc or []
        bcc = bcc or []
        # Skip if no recipients
        if not to and not cc and not bcc:
            return
        email = EmailMessage(
            subject=subject or self.default_subject,
            body=self._render_template(self.template_path, context),
            to=to,
            cc=cc,
            bcc=bcc,
            from_email=from_email or settings.DEFAULT_FROM_EMAIL,
        )
        email.content_subtype = "html"
        email.send()

    def send_async(
        self,
        context: dict[str, Any],
        subject: str | None = None,
        to: list[str] | None = None,
        cc: list[str] | None = None,
        bcc: list[str] | None = None,
        from_email: str | None = None,
    ) -> Thread:
        """
        Sends an email asynchronously using the current template and the provided context.
        Exactly the same as `send` but returns a `Thread` object.

        Args:
            context (dict[str, Any]): The context to render the template with.
            subject (str | None, optional): The subject of the email. Defaults to None.
            to (list[str] | None, optional): The list of recipients. Defaults to None.
            cc (list[str] | None, optional): The list of CC recipients. Defaults to None.
            bcc (list[str] | None, optional): The list of BCC recipients. Defaults to None.
            from_email (str | None, optional): The sender email address. Defaults to None.

        Returns:
            Thread: The started thread in charge of sending the email.
        """
        thread = Thread(
            target=self.send, args=(context, subject, to, cc, bcc, from_email)
        )
        thread.start()
        return thread

    @staticmethod
    def _render_template(template_path: str, context: dict[str, Any]) -> str:
        """Renders a template with the given context."""
        template = loader.get_template(template_path)
        rendered = template.render(context)
        return rendered
