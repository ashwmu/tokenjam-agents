# v2 — Prompt Caching

Same agent as v1 but with cache_control on the system prompt.
Claude processes the prompt once then reads from cache.

## Run

```bash
python3 agents/daily_briefing/v2_cached/agent.py
```

## Expected TokenJam findings

```bash
tj optimize --agent daily-briefing-agent-v2
```

- Cache efficacy: ~90%
- Cost: ~$0.07 (vs $0.72 in v1)
- Reuse still flagged (structure still repeated)
