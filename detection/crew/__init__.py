"""
detection.crew — CrewAI multi-agent orchestration for the detection pipeline.

Three agents, run sequentially:
  1. Crop Classification Agent  -> classify_crop tool
  2. Disease Detection Agent    -> detect_disease tool
  3. Recommendation Agent       -> generate_recommendation tool

Every tool wraps the SAME underlying code as the direct (non-agentic) pipeline
in detection/services.py and recommendation/rag.py — the agents add reasoning/
orchestration on top, they do not reimplement the ML or RAG logic. This keeps
one source of truth for correctness while giving you the CrewAI structure.

Enable with USE_CREWAI_PIPELINE=True in .env. Adds LLM latency/cost per scan
purely for orchestration — see detection/crew_service.py for the tradeoff notes.
"""
