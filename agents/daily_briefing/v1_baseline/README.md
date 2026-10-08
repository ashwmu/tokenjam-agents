# v1 — Baseline (no optimization)

Uses claude-opus-4-5 with no caching. Every run re-processes
the system prompt from scratch.

## Run

```bash
python3 agents/daily_briefing/v1_baseline/agent.py
```

## Expected TokenJam findings

```bash
tj optimize --agent daily-briefing-agent-v1
```

- Reuse: $0.71 recoverable
- Cache efficacy: 0%
- Script analyzer: $0.72 recoverable by scripting
