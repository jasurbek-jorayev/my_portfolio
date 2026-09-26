from django.test import TestCase
from django.urls import reverse

from .models import Project


class ProjectModelTests(TestCase):
    def test_slug_is_auto_generated_from_title(self):
        project = Project.objects.create(
            title="ExamFluent", summary="Sum", description="Desc", tech_stack="Python"
        )
        self.assertEqual(project.slug, "examfluent")

    def test_duplicate_titles_get_unique_slugs(self):
        first = Project.objects.create(
            title="Bot", summary="Sum", description="Desc", tech_stack="Python"
        )
        second = Project.objects.create(
            title="Bot", summary="Sum", description="Desc", tech_stack="Python"
        )
        self.assertNotEqual(first.slug, second.slug)

    def test_tech_list_splits_on_comma(self):
        project = Project.objects.create(
            title="X", summary="Sum", description="Desc", tech_stack="Python, Django,  aiogram"
        )
        self.assertEqual(project.tech_list, ["Python", "Django", "aiogram"])


class ProjectViewTests(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            title="JasurMath", summary="Sum", description="Desc", tech_stack="Next.js"
        )

    def test_project_list_view(self):
        response = self.client.get(reverse("projects:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "JasurMath")

    def test_project_detail_view(self):
        response = self.client.get(reverse("projects:detail", args=[self.project.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "JasurMath")

    def test_unknown_slug_returns_404(self):
        response = self.client.get(reverse("projects:detail", args=["does-not-exist"]))
        self.assertEqual(response.status_code, 404)
