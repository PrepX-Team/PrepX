# PrepX deployment handoff

Phase 8 configuration is prepared, but a live deployment has NOT been verified.

1. Provision PostgreSQL (Railway or Neon) and a Python web service.
2. Configure `DJANGO_DEBUG=false`, a newly generated `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, `DJANGO_CSRF_TRUSTED_ORIGINS`, and `DATABASE_URL` in the hosting dashboard. Never commit real secrets.
3. `pip install -r requirements.txt`
4. `python manage.py migrate --noinput`
5. `python manage.py collectstatic --noinput`
6. Start `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT` (Procfile included).
7. Run `python manage.py check --deploy` in the production environment, review output and smoke-test all roles, practice, conducted exams, reports, analytics and certificate PDF/verification.
8. Local SQLite and its backups stay on the user's computer; never upload them to the hosting repository.

## Local setup

Activate your existing virtual environment; `pip install -r requirements.txt`; `python manage.py migrate`; `python manage.py test`; `python manage.py runserver`. Login is at `/accounts/login/` (root `/` is not configured).

## Certificate behavior

All ten distinct completed practice tests for the same topic issue one certificate per student/topic. The certificate has a public verification URL and PDF download, and uses a faint vector graduation-cap watermark. This is a PrepX achievement, not a Microsoft credential.
