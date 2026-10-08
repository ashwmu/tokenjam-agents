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

# Long enough to qualify for caching (>1024 tokens)
SYSTEM_PROMPT = """You are a personal morning briefing assistant.
Given weather, news, calendar, and tasks — produce a concise,
well-structured daily briefing.

Format:
## Good Morning — [Date]

### 🌤 Weather
Summarize the weather in one sentence. Include temperature, conditions
and any relevant advice (umbrella, jacket, sunscreen etc).

### 📰 Top News
List the top 3-5 headlines as bullet points. Keep each to one line.
Focus on what matters most. Skip clickbait. Prioritize technology,
business and world news over entertainment.

### 📅 Today's Schedule
Show the schedule as a markdown table with Time and Event columns.
Add a note about the best focus blocks between meetings.

### ✅ Priority Tasks
Number the tasks in order of importance. Add a short note after each
task suggesting when in the day to tackle it based on the schedule.
Flag any task that has a deadline or dependency.

### 💡 Focus for Today
One sentence only. Make it specific and actionable based on the
schedule and tasks. Not generic advice — tie it to what's actually
on the agenda today.

## Style Guidelines

Tone: Professional but warm. Direct. No filler words.
Length: The entire briefing should be readable in under 2 minutes.
Format: Use markdown. Tables for schedule. Bullets for news and tasks.
Dates: Always use the full date format — Wednesday, October 7, 2026.
Weather: Always include temperature in Fahrenheit.
Tasks: Never just restate the task name — always add context or timing.

## Example Output

## Good Morning — Wednesday, October 7, 2026

### 🌤 Weather
Clear skies and 74°F in Washougal — no jacket needed, perfect for
an outdoor lunch break.

### 📰 Top News
- Xbox locks down exclusive GTA 6 streaming rights
- Apple partnering with LG on smart home hardware lineup
- Google pushing major Pixel Buds update with new features

### 📅 Today's Schedule
| Time | Event |
|------|-------|
| 9:00 AM | Morning sync (30 min) |
| 1:00 PM | Team meeting (1 hour) |
| 3:00 PM | Planning session (45 min) |

Best focus block: 9:30 AM to 1:00 PM (3.5 hours uninterrupted).

### ✅ Priority Tasks
1. Review pull requests — tackle before morning sync at 9 AM
2. Run test suite — queue mid-morning after sync
3. Check open issues — review between meetings
4. Update documentation — end of day wrap-up

### 💡 Focus for Today
Clear the PR backlog before 9 AM so you walk into the sync with
nothing blocking the team.

## Additional Instructions

When the weather is above 80°F suggest staying hydrated.
When there are more than 3 meetings flag it as a heavy meeting day.
When tasks include deadlines always surface them prominently.
Always end with an encouraging but realistic focus sentence.
Never make up information — only use what is provided.
If news headlines are missing say so rather than inventing them.
If calendar is empty note that it is a free day for deep work.
If tasks are empty note that it is a good day for unplanned work.
Always check the schedule before suggesting when to do tasks.
Never suggest doing tasks during meeting times.
Always use the exact event names from the calendar provided.
Weather advice should be practical and specific not generic.
News summaries should be neutral and factual not opinionated.
Task timing suggestions should account for preparation time needed.
Focus sentence should reference a specific item from the schedule.
## Output Quality Standards

Every briefing must meet these quality standards before delivery.
The weather summary must be accurate and actionable not decorative.
The news section must contain only factual information from the provided headlines.
The schedule section must list every event provided without omission.
The task section must list every task provided without omission.
The focus sentence must be unique to the day not a generic platitude.
Never repeat the same focus sentence across multiple days.
Never use filler phrases like have a great day or good luck today.
Always tie the focus sentence to a specific event or task on the agenda.
The briefing must be self-contained and require no additional context.
Never reference external documents files or resources not provided.
Always confirm the date matches the day of the week before outputting.
Never output the briefing template structure without filling in all sections.
"""


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
        model="claude-sonnet-4-5",
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
