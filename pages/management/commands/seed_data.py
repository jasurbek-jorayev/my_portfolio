from django.core.management.base import BaseCommand

from contact.models import ContactMessage  # noqa: F401  (imported for discoverability)
from pages.models import Profile, Skill
from projects.models import Project

PROJECTS = [
    dict(
        title="ExamFluent",
        summary="AI-powered CEFR/IELTS English practice platform with adaptive scoring.",
        description=(
            "ExamFluent is an AI English-learning platform built around CEFR (A1-C2) and "
            "IELTS scoring logic. Learners practice writing and speaking tasks, receive "
            "Gemini-generated feedback mapped to real band descriptors, and track their "
            "progress over time on a Recharts-powered dashboard. The app is built with "
            "Next.js and TypeScript on top of Supabase for auth, storage and Postgres, "
            "styled with Tailwind CSS."
        ),
        tech_stack="Next.js, TypeScript, Supabase, Google Gemini API, Tailwind CSS, Recharts",
        github_url="https://github.com/jasurbek-jorayev/examfluent",
        is_featured=True,
        order=1,
    ),
    dict(
        title="JasurMath",
        summary="Telegram Mini App math tutor that teaches from zero with Gemini streaming.",
        description=(
            "JasurMath is an AI math tutor that runs as a Telegram Mini App, designed to "
            "teach a complete beginner starting from zero. It streams step-by-step "
            "explanations from the Gemini API in real time so answers feel like a live "
            "tutor typing rather than a static wall of text. The Gemini API key never "
            "reaches the client — all model calls are proxied through server-side Next.js "
            "route handlers, keeping the app safe to embed inside Telegram's WebView."
        ),
        tech_stack="Next.js 15, TypeScript, Telegram Mini Apps SDK, Google Gemini API (@google/genai)",
        github_url="https://github.com/jasurbek-jorayev/jasurmath",
        is_featured=True,
        order=2,
    ),
    dict(
        title="MatUstoz",
        summary="Uzbek-language Telegram bot that works as a personal math tutor.",
        description=(
            "MatUstoz is a personal math-tutor Telegram bot for Uzbek-speaking students, "
            "built with aiogram 3 on top of async Python. It stores each student's goal, "
            "deadline, current level, personalized study plan and completed topics in "
            "PostgreSQL, then uses that history to automatically pick the next topic and "
            "adjust difficulty as the student progresses — turning a simple Q&A bot into "
            "an adaptive tutor that remembers where every student left off."
        ),
        tech_stack="Python, aiogram 3, PostgreSQL (asyncpg), APScheduler",
        github_url="https://github.com/jasurbek-jorayev/matustoz",
        is_featured=False,
        order=3,
    ),
]

SKILLS = [
    (Skill.Category.LANGUAGE, ["Python", "TypeScript", "SQL"]),
    (Skill.Category.BACKEND, ["Django", "aiogram 3", "aiohttp", "REST APIs"]),
    (Skill.Category.FRONTEND, ["Next.js", "React", "Tailwind CSS"]),
    (Skill.Category.DATA, ["PostgreSQL (asyncpg)", "Supabase", "SQLite"]),
    (Skill.Category.AI, ["Google Gemini API", "Anthropic Claude API"]),
    (Skill.Category.TOOLS, ["Docker", "Git", "Vercel", "Linux"]),
]


class Command(BaseCommand):
    help = "Seeds the database with the portfolio owner's profile, skills and projects."

    def handle(self, *args, **options):
        profile, created = Profile.objects.update_or_create(
            pk=1,
            defaults=dict(
                full_name="Jasurbek Jo'rayev",
                role_title="Python Backend Developer",
                tagline="Building AI-powered Telegram bots, Mini Apps and learning platforms.",
                bio=(
                    "I build Telegram bots, Mini Apps and AI-powered learning platforms for "
                    "Uzbek-speaking users — from English (CEFR/IELTS) practice to a math "
                    "tutor that teaches from zero. I care about clean architecture, async "
                    "Python and shipping real products people use."
                ),
                location="Uzbekistan",
                email="jjasurbek0009@gmail.com",
                telegram_username="JORAYEV_0709",
                github_url="https://github.com/jasurbek-jorayev",
                education_place="Najot Ta'lim",
                education_program="Python Backend Development",
                education_period="Graduate",
                meta_description=(
                    "Jasurbek Jo'rayev — Python backend developer building Telegram bots, "
                    "Mini Apps and AI-powered education platforms."
                ),
            ),
        )
        self.stdout.write(self.style.SUCCESS(f"Profile {'created' if created else 'updated'}."))

        Skill.objects.all().delete()
        for category, names in SKILLS:
            for order, name in enumerate(names):
                Skill.objects.create(name=name, category=category, order=order)
        self.stdout.write(self.style.SUCCESS(f"Seeded {Skill.objects.count()} skills."))

        for data in PROJECTS:
            Project.objects.update_or_create(
                title=data["title"],
                defaults={k: v for k, v in data.items() if k != "title"},
            )
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(PROJECTS)} projects."))
