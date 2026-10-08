import os
import time
from datetime import datetime
from dotenv import load_dotenv

# Set agent name BEFORE tokenjam bootstrap
os.environ["OTEL_SERVICE_NAME"] = "daily-briefing-agent-v3"

from tokenjam.sdk import watch
from agents.daily_briefing.fetchers import (
    fetch_weather, fetch_news, fetch_calendar, fetch_tasks
)
from agents.daily_briefing.validator import validate_briefing

load_dotenv()


def generate_briefing(weather, news, calendar, tasks) -> str:
    """Pure Python — no LLM needed."""
    news_items = chr(10).join(f"- {h}" for h in news)
    calendar_items = chr(10).join(
        f"| {e['time']} | {e['title']} ({e['duration']}) |"
        for e in calendar
    )
    task_items = chr(10).join(f"{i+1}. {t}" for i, t in enumerate(tasks))

    return f"""## Good Morning — {datetime.now().strftime("%A, %B %d, %Y")}

### 🌤 Weather
{weather['temp']}°F and {weather['description']} in Washougal. Humidity at {weather['humidity']}%.

### 📰 Top News
{news_items}

### 📅 Today's Schedule
| Time | Event |
|------|-------|
{calendar_items}

### ✅ Priority Tasks
{task_items}

### 💡 Focus for Today
Review your schedule and tackle the highest priority task first."""


@watch(agent_id="daily-briefing-agent-v3")
def run_briefing_agent():
    print(f"\n{'='*50}")
    print(f"Daily Briefing v3 (scripted) — {datetime.now().strftime('%I:%M %p')}")
    print('='*50)

    weather  = fetch_weather(os.getenv("CITY", "Washougal"))
    news     = fetch_news("technology")
    calendar = fetch_calendar()
    tasks    = fetch_tasks()

    briefing = generate_briefing(weather, news, calendar, tasks)
    valid    = validate_briefing(briefing)

    print(briefing)
    print(f"\n✅ Validation: {'passed' if valid else 'failed'}")
    return briefing


def run_for_tokenjam_testing(cycles: int = 10):
    print(f"Running {cycles} cycles for TokenJam analysis...")
    for i in range(cycles):
        print(f"\n--- Cycle {i+1}/{cycles} ---")
        run_briefing_agent()
        time.sleep(2)


if __name__ == "__main__":
    run_for_tokenjam_testing()
