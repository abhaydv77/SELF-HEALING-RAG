# Self-Healing RAG System

A RAG pipeline that not only retrieves answers but also detects factual issues and automatically generates patches to improve the knowledge base over time.

## Features
- Detects incorrect or vague information
- Generates structured patches (before/after)
- Maintains patch history logs
- Improves data quality iteratively

## Tech Stack
- Python
- FastAPI
- LLM (for patch generation)
- JSON logging system

## How it works
1. Input document
2. Analyse issues
3. Generate patches
4. Save patch logs
5. Improve future responses

## Run
```bash
uvicorn api:app --reload
