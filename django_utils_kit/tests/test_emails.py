from django.core import mail

from django_utils_kit.emails import Email
from django_utils_kit.test_utils import ImprovedTestCase


class EmailTestCase(ImprovedTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.email = Email("Test subject", "email.html")

    def test_send_return_early(self) -> None:
        self.email.send({})
        self.assertEqual(len(mail.outbox), 0)

    def test_send_recipients(self) -> None:
        self.email.send(
            {},
            to=["to"],
            cc=["cc"],
            bcc=["bcc"],
            from_email="custom@localhost.com",
            subject="Custom subject",
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["to"])
        self.assertEqual(mail.outbox[0].cc, ["cc"])
        self.assertEqual(mail.outbox[0].bcc, ["bcc"])
        self.assertEqual(mail.outbox[0].from_email, "custom@localhost.com")
        self.assertEqual(mail.outbox[0].subject, "Custom subject")

    def test_send_defaults(self) -> None:
        self.email.send({}, to=["to"])
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Test subject")
        self.assertEqual(mail.outbox[0].from_email, "test@localhost.com")

    def test_send_template_rendering(self) -> None:
        self.email.send({"name": "John Doe"}, to=["to"])
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Test subject")
        self.assertIn("The name is John Doe", mail.outbox[0].body)

    def test_send_async(self) -> None:
        thread = self.email.send_async(
            {},
            to=["to"],
            cc=["cc"],
            bcc=["bcc"],
            from_email="custom@localhost.com",
            subject="Custom subject",
        )
        self.assertEqual(len(mail.outbox), 0)
        thread.join()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["to"])
        self.assertEqual(mail.outbox[0].cc, ["cc"])
        self.assertEqual(mail.outbox[0].bcc, ["bcc"])
        self.assertEqual(mail.outbox[0].from_email, "custom@localhost.com")
        self.assertEqual(mail.outbox[0].subject, "Custom subject")
