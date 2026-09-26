from django.db import models


class Profile(models.Model):
    """Singleton-style model holding the site owner's public profile data.

    Only one row is expected to exist; ``Profile.objects.first()`` is used
    everywhere instead of a hardcoded id so re-seeding stays simple.
    """

    full_name = models.CharField(max_length=120, default="Jasurbek Jo'rayev")
    role_title = models.CharField(max_length=150, default="Python Backend Developer")
    tagline = models.CharField(
        max_length=200,
        blank=True,
        help_text="Short one-line hook shown under your name in the hero section.",
    )
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True, default="Uzbekistan")

    email = models.EmailField(blank=True)
    telegram_username = models.CharField(
        max_length=50, blank=True, help_text="Without the @ sign, e.g. JORAYEV_0709"
    )
    github_url = models.URLField(blank=True)
    resume = models.FileField(upload_to="resume/", blank=True, null=True)

    education_place = models.CharField(max_length=120, blank=True, default="Najot Ta'lim")
    education_program = models.CharField(max_length=150, blank=True)
    education_period = models.CharField(max_length=60, blank=True)

    meta_description = models.CharField(
        max_length=160,
        blank=True,
        help_text="Used as the <meta name=description> for the homepage.",
    )

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profile"

    def __str__(self):
        return self.full_name

    @property
    def telegram_url(self):
        return f"https://t.me/{self.telegram_username}" if self.telegram_username else ""

    @property
    def telegram_display(self):
        return f"@{self.telegram_username}" if self.telegram_username else ""

    @property
    def initials(self):
        parts = self.full_name.split()
        return "".join(p[0] for p in parts[:2]).upper() if parts else "JJ"


class Skill(models.Model):
    class Category(models.TextChoices):
        LANGUAGE = "LANG", "Languages"
        BACKEND = "BACKEND", "Backend"
        FRONTEND = "FRONTEND", "Frontend"
        DATA = "DATA", "Databases & Data"
        AI = "AI", "AI & APIs"
        TOOLS = "TOOLS", "Tools & DevOps"

    name = models.CharField(max_length=60)
    category = models.CharField(max_length=10, choices=Category.choices)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["category", "order", "name"]

    def __str__(self):
        return self.name
