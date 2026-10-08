import os
import requests

def fetch_weather(city: str) -> dict:
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "imperial"}
    data = requests.get(url, params=params).json()
    return {
        "temp": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "description": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"]
    }

def fetch_news(topic: str = "technology") -> list[str]:
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
    return [a["title"] for a in articles if a["title"]]

def fetch_calendar() -> list[dict]:
    return [
        {"time": "9:00 AM", "title": "Morning sync", "duration": "30 min"},
        {"time": "1:00 PM", "title": "Team meeting", "duration": "1 hour"},
        {"time": "3:00 PM", "title": "Planning session", "duration": "45 min"},
    ]

def fetch_tasks() -> list[str]:
    return [
        "Review pull requests",
        "Update project documentation",
        "Run test suite",
        "Check open issues",
    ]
