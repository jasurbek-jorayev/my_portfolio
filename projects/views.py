from django.shortcuts import get_object_or_404, render

from .models import Project


def project_list(request):
    projects = Project.objects.all()
    return render(request, "projects/project_list.html", {"projects": projects})


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    other_projects = Project.objects.exclude(pk=project.pk)[:2]
    return render(
        request,
        "projects/project_detail.html",
        {"project": project, "other_projects": other_projects},
    )
