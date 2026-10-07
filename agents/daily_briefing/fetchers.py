import os
import requests
from opentelemetry import trace

tracer = trace.get_tracer("daily-briefing-agent")

def fetch_weather(city: str) -> dict:
    with tracer.start_as_current_span("fetch_weather") as span:
        span.set_attribute("city", city)
        api_key = os.getenv("OPENWEATHER_API_KEY")
        url = "http://api.openweathermap.org/data/2.5/weather"
        params = {"q": city, "appid": api_key, "units": "imperial"}
        data = requests.get(url, params=params).json()
        weather = {
            "temp": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"]
        }
        span.set_attribute("temp_f", weather["temp"])
        return weather

def fetch_news(topic: str = "technology") -> list[str]:
    with tracer.start_as_current_span("fetch_news") as span:
        span.set_attribute("topic", topic)
        api_key = os.getenv("NEWS_API_KEY")
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            "category": topic,
            "language": "en",
            "country": "us",
            "pageSize": 5,
            "apiKey": api_key
        }
        articles = requests.get(url, params=params).json().get("articles", [])
        headlines = [a["title"] for a in articles if a["title"]]
        span.set_attribute("headline_count", len(headlines))
        return headlines

def fetch_calendar() -> list[dict]:
    with tracer.start_as_current_span("fetch_calendar") as span:
        events = [
            {"time": "9:00 AM", "title": "Morning sync", "duration": "30 min"},
            {"time": "1:00 PM", "title": "Team meeting", "duration": "1 hour"},
            {"time": "3:00 PM", "title": "Planning session", "duration": "45 min"},
        ]
        span.set_attribute("event_count", len(events))
        return events

def fetch_tasks() -> list[str]:
    with tracer.start_as_current_span("fetch_tasks") as span:
        tasks = [
            "Review pull requests",
            "Update project documentation",
            "Run test suite",
            "Check open issues",
        ]
        span.set_attribute("task_count", len(tasks))
        return tasks
