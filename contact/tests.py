from django.test import TestCase

from .forms import ContactForm
from .models import ContactMessage


class ContactFormTests(TestCase):
    def test_subject_is_optional(self):
        form = ContactForm(data={"name": "A", "email": "a@example.com", "message": "Hi"})
        self.assertTrue(form.is_valid())

    def test_missing_required_fields_invalid(self):
        form = ContactForm(data={"name": "", "email": "", "message": ""})
        self.assertFalse(form.is_valid())


class ContactMessageModelTests(TestCase):
    def test_str_representation(self):
        message = ContactMessage.objects.create(
            name="Jane", email="jane@example.com", subject="Hi", message="Hello there"
        )
        self.assertIn("Jane", str(message))
        self.assertIn("jane@example.com", str(message))
