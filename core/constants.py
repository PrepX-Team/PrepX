MIN_TEST_NUMBER = 1
MAX_TEST_NUMBER = 10
QUESTIONS_PER_TEST = 20
UNLOCK_PERCENTAGE = 75  # reserved for Part 3 — not used yet in Part 1

DEFAULT_PRACTICE_DURATION_MINUTES = 30  # implementation default, not a formal SRS value

IDLE_THRESHOLD_SECONDS = 300          # 5 minutes — configurable default
RAPID_ANSWER_THRESHOLD_SECONDS = 2    # heuristic only, not proof of cheating
TIMER_WARNING_SECONDS = 300           # < 5 min → warning UI
TIMER_CRITICAL_SECONDS = 60            # < 1 min → critical UI
AUTOSAVE_SYNC_SECONDS = 30             # periodic timer re-sync interval