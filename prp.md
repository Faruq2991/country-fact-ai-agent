# country-fact-ai-agent
Project Name: Country Fact Agent
Team Lead: [Umar Adam]
Mentor: AI Agent Development Lead (ChatGPT)
Start Date: [2025-07-22]
Expected Completion: [TBD — based on sprint progress]

1. 🎯 Project Summary
The Country Fact Agent is an AI-powered agent designed using the ReAct (Reasoning + Acting) paradigm. It will accept natural language questions about any country and return concise, accurate answers by using external knowledge sources (APIs or databases). This project will serve as a foundational agent pattern for more advanced use cases and will adhere to modern software and AI agent engineering standards.

2. 🧭 Objectives
Objective	Description
🌍 Natural Language Understanding	The agent should parse and understand user questions related to countries.
🛠 Tool-Enabled Reasoning	Use ReAct reasoning to identify what information is needed, then use tools to retrieve it.
📡 External Knowledge Integration	Integrate with APIs like RESTCountries or Wikipedia to fetch reliable country data.
💬 Clean Response Generation	Present well-formatted, human-friendly answers.
🧱 Modular Architecture	The codebase should be modular, testable, and easy to extend (tools, prompts, agents).
🧪 Automated Testing	Ensure correctness through unit tests and coverage.
📊 Logging and Tracing	Log reasoning steps, tool invocations, and agent output for observability.
🚀 Deployability (Optional)	Allow CLI or Web UI interface with potential for Docker-based deployment.

3. 🧩 Scope
In-Scope
Building a ReAct Agent using LangChain

Creating at least one external Tool (RESTCountries API)

Building a reasoning + action loop

Writing prompt templates and integrating with OpenAI or local LLM

Creating unit tests and sample queries

Optional: CLI or basic Streamlit interface

Out-of-Scope (MVP)
Full UI/UX design or mobile support

Multi-lingual queries

Multi-hop questions (e.g., “Which African country with the largest GDP uses French?”)

4. 🛠 Tools & Technologies
Category	Tech Stack
Language	Python 3.10+
Agent Framework	LangChain (ReAct AgentExecutor)
API	RESTCountries
LLM	OpenAI (gpt-4, gpt-3.5), Ollama (optional local)
Environment	venv / poetry, .env for secrets
Testing	pytest
Logging	logging or rich
Deployment (optional)	CLI / Streamlit / Docker

5. 👥 Target Users
Learners and developers exploring LangChain agents

People seeking fast, factual country data

Internal testing base for building more complex multi-agent workflows

6. 📈 Success Metrics
Metric	Target
🧠 Accuracy	90%+ correct factual responses on a curated 50-query test set
⚙️ Tool Usage Rate	>95% of questions should invoke the correct tool
🔁 Average Latency	< 1.5s (from input to answer)
🧪 Test Coverage	>80% for tool logic and agent core
📝 Trace Logging	All ReAct steps logged per query

7. 🔁 Project Roadmap
Phase 1 – Discovery & Planning ✅
Define use case, scope, and tools

Write this objectives document

Phase 2 – Environment & Tools (Sprint 1)
Setup environment

Implement RESTCountries Tool

Phase 3 – Agent Integration
Create prompt template

Integrate LangChain ReAct agent

Execute sample queries

Phase 4 – Testing & Evaluation
Write unit tests

Create sample query test set

Evaluate reasoning logs

Phase 5 – Hardening & (Optional) Deployment
Add CLI or Streamlit UI

Containerize (Docker)

Logging and monitoring

8. 🛡️ Risks & Mitigations
Risk	Mitigation
API instability	Add fallback APIs or local cache
Query ambiguity	Improve prompt and tool interface
LLM hallucinations	Use structured outputs and fact-check
Tool error handling	Implement timeouts, retries, and logging

9. 🤝 Dependencies
OpenAI API key (or local model like Ollama)

Network access to RESTCountries API

Python and LangChain installation
