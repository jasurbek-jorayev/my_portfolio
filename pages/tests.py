from django.test import TestCase
from django.urls import reverse

from .models import Profile, Skill


class HomeViewTests(TestCase):
    def setUp(self):
        self.profile = Profile.objects.create(full_name="Test User", email="test@example.com")
        Skill.objects.create(name="Python", category=Skill.Category.LANGUAGE)

    def test_home_page_loads(self):
        response = self.client.get(reverse("pages:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test User")

    def test_contact_form_submission_creates_message(self):
        response = self.client.post(
            reverse("pages:home"),
            {
                "name": "Jane Doe",
                "email": "jane@example.com",
                "subject": "Hello",
                "message": "I'd like to work together.",
            },
        )
        self.assertRedirects(
            response, reverse("pages:home") + "#contact", fetch_redirect_response=False
        )
        from contact.models import ContactMessage

        self.assertEqual(ContactMessage.objects.count(), 1)

    def test_invalid_contact_form_does_not_create_message(self):
        response = self.client.post(reverse("pages:home"), {"name": "", "email": "", "message": ""})
        self.assertEqual(response.status_code, 200)
        from contact.models import ContactMessage

        self.assertEqual(ContactMessage.objects.count(), 0)
