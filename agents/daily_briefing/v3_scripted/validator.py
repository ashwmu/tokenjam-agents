def validate_briefing(briefing: str) -> bool:
    """
    Validate briefing contains all required sections.
    Uses simple string matching — no LLM call needed.
    """
    required_sections = [
        "weather",
        "news",
        "schedule",
        "tasks",
        "focus"
    ]
    briefing_lower = briefing.lower()
    results = {s: s in briefing_lower for s in required_sections}
    passed = all(results.values())

    if not passed:
        missing = [s for s, found in results.items() if not found]
        print(f"⚠️  Missing sections: {missing}")

    return passed
