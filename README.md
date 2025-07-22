# Country Fact Agent

The Country Fact Agent is an AI-powered agent designed using the ReAct (Reasoning + Acting) paradigm. It accepts natural language questions about any country and returns concise, accurate answers by using external knowledge sources.

## 🎯 Objectives

- **Natural Language Understanding**: The agent should parse and understand user questions related to countries.
- **Tool-Enabled Reasoning**: Use ReAct reasoning to identify what information is needed, then use tools to retrieve it.
- **External Knowledge Integration**: Integrate with APIs like RESTCountries or Wikipedia to fetch reliable country data.
- **Clean Response Generation**: Present well-formatted, human-friendly answers.
- **Modular Architecture**: The codebase should be modular, testable, and easy to extend (tools, prompts, agents).
- **Automated Testing**: Ensure correctness through unit tests and coverage.

## 🛠️ Tools & Technologies

- **Language**: Python 3.10+
- **Agent Framework**: LangChain (ReAct AgentExecutor)
- **API**: RESTCountries
- **LLM**: OpenAI (gpt-4, gpt-3.5)
- **Environment**: venv, .env for secrets
- **Testing**: pytest

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- An OpenAI API key

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/country-fact-ai-agent.git
    cd country-fact-ai-agent
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your environment variables:**
    Create a `.env` file in the root directory and add your OpenAI API key:
    ```
    OPENAI_API_KEY='your_openai_api_key'
    ```

### Usage

To run the agent, execute the `main.py` script with your question as an argument:

```bash
python main.py "What is the capital of Nigeria?"
```

The agent will process the question, use its tools to find the information, and print the answer to the console.

## 🧪 Testing

To run the automated tests, use `pytest`:

```bash
pytest
```

This will execute all the unit tests in the `tests/` directory to ensure the agent and its tools are functioning correctly.
