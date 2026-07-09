# SentinelIQ

SentinelIQ is an enterprise-grade AI Support Copilot designed to process customer support tickets, parse unstructured technical manuals, and orchestrate intelligent resolutions. Leveraging a Retrieval-Augmented Generation (RAG) architecture powered by Gemini, LangGraph, and ChromaDB, the system automates data validation, sanitization, and knowledge enrichment, providing context-aware, highly accurate support agents backed by a secure Oracle Database infrastructure.

## Prerequisites

Before setting up the project, ensure you have the following installed on your local machine:
* **Python 3.11+** (The project utilizes specific features requiring `py -3.11`)
* **Oracle Instant Client** (Required if connecting to an external Oracle instance using Thick Client mode; optional if using `oracledb` Thin Client mode)
* **Git**

## Installation

Follow these steps to set up your local development environment:

```bash
# Clone the repository
git clone <https://github.com/the-shiva-123/SentinelIQ.git>
cd sentineliq

# Set up environment configuration
cp .env.example .env

# Install dependencies in development and editable mode
make install