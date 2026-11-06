# Module 6 — Talking to a Local Model — Ollama

This project integrates a local LLM (`granite4.1:3b` via Ollama) with deterministic tool guardrails to build a reliable conversational assistant.

## Mini-Project Reflection

The model performed well when answering factual questions directly grounded in the system instructions, such as providing the office address and required documentation. However, it struggled when asked about services outside of the prompt context, occasionally making assumptions rather than strictly offering a human handoff. To maintain reliability, deterministic logic—such as schedule changes, booking requests, and tool lookup triggers—was kept strictly in code rules. Using code-first guardrails prevents user prompt injections and ensures critical operational tasks execute accurately while reserving the model exclusively for natural language responses.
