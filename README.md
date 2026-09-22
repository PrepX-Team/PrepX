# PrepX — MCQ Exam & Result System

Django-based student practice, teacher-conducted exams, results, analytics, reporting and certificates.

## Local development

1. Create/activate a Python virtual environment.
2. `pip install -r requirements.txt`
3. `python manage.py migrate`
4. `python manage.py test`
5. `python manage.py runserver`
6. Open `http://127.0.0.1:8000/accounts/login/`.

Certificates are earned after completing all ten distinct practice tests for a topic. Certificate PDFs include a faint PrepX logo watermark, unique ID and public verification link.

Deployment preparation: see [DEPLOYMENT.md](DEPLOYMENT.md). Never commit `.env`, SQLite databases or database backups.

## Viva-friendly code map

See [SIMPLE_CODE_GUIDE.md](SIMPLE_CODE_GUIDE.md) for a short explanation of the project flow and files.
