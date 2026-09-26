from django.contrib import messages
from django.core.mail import mail_admins
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from contact.forms import ContactForm
from projects.models import Project

from .models import Profile, Skill


def home(request):
    profile = Profile.objects.first()

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            try:
                mail_admins(
                    subject=f"Portfolio contact: {contact_message.subject or contact_message.name}",
                    message=(
                        f"From: {contact_message.name} <{contact_message.email}>\n\n"
                        f"{contact_message.message}"
                    ),
                    fail_silently=True,
                )
            except Exception:
                pass
            messages.success(
                request, "Thanks! Your message has been sent — I'll reply soon."
            )
            return redirect(reverse("pages:home") + "#contact")
        messages.error(request, "Please fix the errors below and try again.")
    else:
        form = ContactForm()

    context = {
        "profile": profile,
        "skills": Skill.objects.all(),
        "featured_projects": Project.objects.filter(is_featured=True)[:4]
        or Project.objects.all()[:4],
        "form": form,
    }
    return render(request, "pages/home.html", context)


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Allow: /",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
