import os
import time
import anthropic
from datetime import datetime
from dotenv import load_dotenv

# Set agent name BEFORE tokenjam bootstrap
os.environ["OTEL_SERVICE_NAME"] = "daily-briefing-agent-v2"

from tokenjam.sdk import watch
from tokenjam.sdk.integrations.anthropic import patch_anthropic
from agents.daily_briefing.fetchers import (
    fetch_weather, fetch_news, fetch_calendar, fetch_tasks
)
from agents.daily_briefing.validator import validate_briefing

load_dotenv()
patch_anthropic()
client = anthropic.Anthropic()

SYSTEM_PROMPT = """You are a personal morning briefing assistant.
Given weather, news, calendar, and tasks — produce a concise,
well-structured daily briefing.

Format:
## Good Morning — [Date]

### 🌤 Weather
### 📰 Top News
### 📅 Today's Schedule
### ✅ Priority Tasks
### 💡 Focus for Today (one sentence)

Keep it tight — readable in under 2 minutes."""


def generate_briefing(weather, news, calendar, tasks) -> str:
    user_content = f"""
    Date: {datetime.now().strftime("%A, %B %d, %Y")}

    Weather in {os.getenv('CITY', 'Washougal')}:
    - Temperature: {weather['temp']}°F (feels like {weather['feels_like']}°F)
    - Conditions: {weather['description']}
    - Humidity: {weather['humidity']}%

    Top Headlines:
    {chr(10).join(f"- {h}" for h in news)}

    Calendar:
    {chr(10).join(f"- {e['time']}: {e['title']} ({e['duration']})" for e in calendar)}

    Tasks:
    {chr(10).join(f"- {t}" for t in tasks)}
    """

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1000,
        system=[
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"}
            }
        ],
        messages=[{"role": "user", "content": user_content}]
    )
    return response.content[0].text


@watch(agent_id="daily-briefing-agent-v2")
def run_briefing_agent():
    print(f"\n{'='*50}")
    print(f"Daily Briefing v2 (cached) — {datetime.now().strftime('%I:%M %p')}")
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
