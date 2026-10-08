# Daily Briefing Agent — TokenJam Eval Report

## Objective
Validate that TokenJam correctly identifies and quantifies waste
in a deterministic agent that doesn't need an LLM.

## Test Agent
- Agent: `daily-briefing-agent`
- Model: `claude-opus-4-5`
- Task: Generate a formatted daily briefing from weather/news/calendar/tasks

## Phase 1 — Baseline (no optimization)
- Sessions: 75
- Tokens: 50.9k
- Spend: $0.72
- TokenJam findings:
  - Reuse analyzer: 1 cluster, $0.71 recoverable
  - Script analyzer: $0.72 recoverable by scripting
  - Cache efficacy: 0%
  - Downsize: no candidates

## Phase 2 — Prompt Caching (pending)
- Apply cache_control to SYSTEM_PROMPT
- Expected: cache efficacy ~90%, cost ~$0.07

## Phase 3 — Script Conversion (pending)
- Replace LLM call with Python formatting
- Expected: $0.00 LLM spend, no reuse/script findings

## Conclusion
TokenJam correctly identified that 99% of spend ($0.71/$0.72) was
recoverable — the agent was using an expensive LLM for a task that
a simple Python function handles equally well.
