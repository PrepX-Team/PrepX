# QA + LR practice-question bank

The project includes 6 topics (3 QA and 3 LR), 10 tests per topic, and a target of **25 approved/global/active questions per test**. Each practice attempt randomly draws **20 questions** from its level (see `core/constants.py`).

Run from the project directory, with your virtual environment active:

```powershell
python manage.py check
python seed_questions.py
python manage.py test questions.test_seed_bank
```

The seeder requires the six existing active topics and an active superuser; it **does not** create student attempts, results or certificates. It preserves existing questions and only fills levels with fewer than 25 eligible questions. It can be run again safely. The seed bank is deterministic and its correct options/explanations are calculated or based on explicit relationships.

Existing topic names:
- QA: Average; Profit & Loss; Ratio & Proportion
- LR: Blood Relations; Coding-Decoding; Number/Letter Series

After seeding, students must complete Test 1 through Test 10 through the normal practice UI, unlocking the next test by meeting the configured accuracy threshold. Certificates are issued for genuine submitted practice tests, not by seeding questions.

**Before running:** keep a backup of `db.sqlite3`. The ZIP intentionally excludes your local database, `.env`, `.git`, and virtual environment.
