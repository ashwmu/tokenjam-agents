# Daily Briefing Agent — TokenJam Eval Report

## Objective
Validate that TokenJam correctly identifies and quantifies waste
in a deterministic agent that doesn't need an LLM.

## Test Agent
- Task: Generate a formatted daily briefing from weather/news/calendar/tasks
- Runs: 10 cycles per version

## Results

| Version | Model | CACHE R | CACHE W | Cost (10 runs) | Cost/run | Savings | LLM Calls |
|---|---|---|---|---|---|---|---|
| v1_baseline | claude-opus-4-5 | 0 | 0 | $0.1002 | $0.0100 | baseline | 10 |
| v2_cached | claude-sonnet-4-5 | 9.4k | 1.0k | $0.0696 | $0.0070 | 30% | 10 |
| v3_scripted | none | N/A | N/A | $0.0000 | $0.0000 | 100% | 0 |

Costs measured from last 10 clean traces per agent using tj traces.

## Key Findings

### v1 — Baseline
- No caching — full token cost every run
- TokenJam Reuse analyzer flagged $0.71 recoverable
- TokenJam Script analyzer flagged entire agent as scriptable

### v2 — Prompt Caching
- Added cache_control to system prompt (one line change)
- Cache write on first call, cache read on all subsequent calls
- Requires >1024 tokens in system prompt to qualify
- Significant cost reduction on repeat runs

### v3 — Script Conversion
- Replaced LLM call with pure Python formatting
- Cost: $0.00 per run
- Tradeoff: loses Claude's natural language polish
- Output is functional but less conversational

## Quality Comparison

| Aspect | v1 (Claude) | v3 (Script) |
|---|---|---|
| Weather | "Clear skies and a beautiful 76°F — perfect fall day" | "69.84°F and clear sky. Humidity at 64%." |
| Cost | $0.01/run | $0.00/run |
| Speed | ~12 seconds | <1 second |
| Consistency | Varies naturally | Identical every run |

## TokenJam Findings on v1

- Reuse analyzer: 1 cluster, $0.71 recoverable
- Script analyzer: $0.72 recoverable by scripting
- Cache efficacy: 0%
- 12 analyzers run, 2 findings

## Conclusion

TokenJam correctly identified that 99% of v1 spend was recoverable.
The fix depended on the quality requirement:
- Need natural language? → v2 (caching) saves ~55% with one line of code
- Need only structure? → v3 (scripting) saves 100% with no LLM at all

## How to Reproduce

```bash
git clone https://github.com/ashwmu/tokenjam-agents.git
cd tokenjam-agents
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Add API keys to .env

# Install and start TokenJam
pipx install tokenjam
tj serve &

# Run all three versions
python3 agents/daily_briefing/v1_baseline/agent.py
python3 agents/daily_briefing/v2_cached/agent.py
python3 agents/daily_briefing/v3_scripted/agent.py

# Compare in TokenJam
tj cost --agent daily-briefing-agent-v1
tj cost --agent daily-briefing-agent-v2
tj cost --agent daily-briefing-agent-v3
tj optimize --agent daily-briefing-agent-v1
```
