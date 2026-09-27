# Week 1 — Foundations of Agentic AI

Module 1. Three sessions (Mon 2h · Wed 2h · Sat 4h lab). This week is about
**building the mental model** — it is deliberately light on coding. You'll run a
few short demos, design an agent on paper, and finish by building one small,
real **agent loop**.

## Learning objectives
By the end of the week you can:
- Explain what an AI **agent** is and how it differs from an assistant.
- Name the **four parts** of every agent: goal, tools, memory, actions.
- Describe three LLM limits (hallucination, no-action, reasoning drift) and how agents address them.
- Trace the **agent loop**: observe → reason → act → evaluate.
- Run a working agent loop and design a blueprint of your own.

## Files (work in `skeleton/`)

| File | What it is | Coding? |
|------|-----------|---------|
| `00_setup_check.py` | Verify your environment + first LLM call | run only |
| `01_assistant_vs_agent.py` | Assistant (words) vs agent (tool) | 2 small TODOs |
| `02_llm_reasoning_limits.py` | See hallucination & reasoning drift | 1 small TODO |
| `03_agent_anatomy.py` | Blueprint of an agent (goal, tools, memory, actions) | **Deliverable** |
| `04_agent_loop.py` | Minimal agent loop: observe → reason → act → eval | **Core Coding** |
| `05_reflection_loop.py` | Extension: Self-critique & reflection loop | 2 TODOs |
| `06_multi_tool_agent.py` | Extension: Multi-tool agent + AST-safe calculator | 3 TODOs |
| `07_advanced_agent.py` | Advanced: Native function calling via Groq / OpenAI | 2 TODOs + challenges |
