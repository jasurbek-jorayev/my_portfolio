# Jasurbek Jo'rayev — Developer Portfolio

A Django-powered personal portfolio: a fast, database-backed single-page site with a
full project showcase, a working contact form, an admin panel for editing content,
and SEO basics (sitemap, robots.txt, OG tags) — all served without a frontend
framework, so it stays lightweight and fast.

## Stack

- **Backend:** Django 6, Python 3.12
- **Database:** SQLite (dev) / PostgreSQL (production-ready via `DATABASE_URL`-style env vars)
- **Static/media:** WhiteNoise (compressed, cache-busted static files)
- **Frontend:** hand-written HTML templates + a single custom CSS file (no framework), vanilla JS for theme toggle / mobile nav / scroll reveal
- **Deployment:** Gunicorn + Docker

## Apps

| App        | Responsibility                                                       |
|------------|------------------------------------------------------------------------|
| `pages`    | Site owner's `Profile`, `Skill` list, homepage view, context processor, sitemap, robots.txt |
| `projects` | `Project` model (auto-slugging, tech tags), list + detail views       |
| `contact`  | `ContactMessage` model, `ContactForm`, stores + emails submissions    |

## Local setup

```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux

pip install -r requirements.txt

copy .env.example .env         # Windows: copy, macOS/Linux: cp
python manage.py migrate
python manage.py seed_data     # populates Profile, Skills and Projects with real data
python manage.py createsuperuser
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` for the site and `http://127.0.0.1:8000/admin/` to edit
content (profile bio, skills, projects, contact messages) without touching code.

## Running tests

```bash
python manage.py test
```

## Environment variables

See `.env.example`. Key ones:

- `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS` — standard Django config.
- `DJANGO_EMAIL_BACKEND` / `EMAIL_*` — contact form email delivery. Defaults to printing to
  the console in development.
- `CONTACT_RECIPIENT_EMAIL` — where contact form notifications are sent.

## Deployment (Render)

This is a standard Django app (WSGI + a database + media/static files), so it fits
naturally on **Render** (free tier, native PostgreSQL, persistent storage) rather than
a serverless platform like Vercel — serverless functions don't keep a writable
filesystem, which the admin's media uploads and WhiteNoise's static manifest rely on.

The repo includes a `render.yaml` Blueprint, so deploying is one click:

1. Go to [dashboard.render.com](https://dashboard.render.com), sign in with GitHub.
2. **New +** → **Blueprint** → select this repo. Render reads `render.yaml` and
   provisions both the web service and a free PostgreSQL database automatically.
3. Click **Apply**. `DJANGO_SECRET_KEY` is generated for you, `DATABASE_URL` is wired
   to the new database, migrations run and the site is seeded on first deploy.
4. Once live, note the assigned `https://<name>.onrender.com` URL — Django picks it up
   automatically via the `RENDER_EXTERNAL_HOSTNAME` env var Render injects.

To deploy manually instead (or on Railway):

1. Create a Web Service + PostgreSQL database, connect this repo.
2. Set env vars from `.env.example`, `DJANGO_DEBUG=False`, a real `DJANGO_SECRET_KEY`,
   and `DATABASE_URL` from the database instance.
3. Build command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
4. Start command: `gunicorn config.wsgi:application`

### Docker

```bash
docker compose up --build
```

## Project structure

```
config/          # settings, root urls, wsgi/asgi
pages/           # profile + skills + homepage
projects/        # project showcase
contact/         # contact form + message storage
templates/       # base.html, includes, per-app templates
static/          # css/, js/, images/
```
