import os
import requests
import json
from typing import Dict, Any, Optional, List
from langchain.tools import BaseTool
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END
from typing_extensions import TypedDict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class RestCountriesTool(BaseTool):
    name: str = "rest_countries_tool"
    description: str = """
    Get specific factual information about countries including:
    - Capital city, population, currency, area
    - Languages, region, timezones, flags
    - Borders and calling codes
    
    This tool should be used for specific factual queries about country data.
    """

    def _run(self, query: str) -> str:
        try:
            country_name = self._extract_country_name(query.lower())
            if not country_name:
                return "Could not identify a country in the request."
            
            country_data = self._get_country_data(country_name)
            if not country_data:
                return f"No data found for country: {country_name}"
            
            return self._process_query(query.lower(), country_data)
            
        except Exception as e:
            return f"Error accessing country data: {str(e)}"

    def _extract_country_name(self, query: str) -> Optional[str]:
        """Extract country name from the query"""
        patterns_to_remove = [
            "what is the capital of", "tell me the population of", "what currency does",
            "give me the area of", "what languages are spoken in", "what timezone is",
            "show me the flag of", "what countries border", "what is the calling code",
            "use?", "in?", "?", "the", "tell me about", "information about"
        ]
        
        country_name = query.strip()
        for pattern in patterns_to_remove:
            country_name = country_name.replace(pattern, "").strip()
        
        # Additional cleanup - remove common words that might remain
        words_to_remove = ["of", "for", "about", "in", "on", "at", "with"]
        country_words = [word for word in country_name.split() if word not in words_to_remove]
        
        return " ".join(country_words) if country_words else None

    def _get_country_data(self, country_name: str) -> Optional[Dict[str, Any]]:
        """Get country data from REST Countries API"""
        try:
            endpoints = [
                f"https://restcountries.com/v3.1/name/{country_name}?fullText=true",
                f"https://restcountries.com/v3.1/name/{country_name}"
            ]
            
            for endpoint in endpoints:
                response = requests.get(endpoint, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if data and len(data) > 0:
                        return data[0]
            return None
        except Exception:
            return None

    def _process_query(self, query: str, country_data: Dict[str, Any]) -> str:
        """Process the query and return appropriate information"""
        country_name = country_data.get('name', {}).get('common', 'Unknown')
        
        # Check for specific data requests
        if any(word in query for word in ['capital']):
            capitals = country_data.get('capital', [])
            return f"Capital of {country_name}: {capitals[0] if capitals else 'Not available'}"
        
        elif any(word in query for word in ['population']):
            population = country_data.get('population')
            return f"Population of {country_name}: {population:,}" if population else f"Population data not available for {country_name}"
        
        elif any(word in query for word in ['currency', 'currencies']):
            currencies = country_data.get('currencies', {})
            if currencies:
                currency_names = [info.get('name', code) for code, info in currencies.items()]
                return f"Currency of {country_name}: {', '.join(currency_names)}"
            return f"Currency data not available for {country_name}"
        
        elif any(word in query for word in ['area', 'size']):
            area = country_data.get('area')
            return f"Area of {country_name}: {area:,} sq km" if area else f"Area data not available for {country_name}"
        
        elif any(word in query for word in ['language', 'languages']):
            languages = country_data.get('languages', {})
            if languages:
                language_names = list(languages.values())
                return f"Languages of {country_name}: {', '.join(language_names)}"
            return f"Language data not available for {country_name}"
        
        elif any(word in query for word in ['timezone', 'time zone']):
            timezones = country_data.get('timezones', [])
            return f"Timezones of {country_name}: {', '.join(timezones)}" if timezones else f"Timezone data not available for {country_name}"
        
        elif any(word in query for word in ['flag']):
            flag_emoji = country_data.get('flag', '')
            flag_url = country_data.get('flags', {}).get('png', '')
            result = f"Flag of {country_name}:"
            if flag_emoji:
                result += f" {flag_emoji}"
            if flag_url:
                result += f" (Image: {flag_url})"
            return result if (flag_emoji or flag_url) else f"Flag data not available for {country_name}"
        
        elif any(word in query for word in ['border', 'borders']):
            borders = country_data.get('borders', [])
            return f"Countries bordering {country_name}: {', '.join(borders)}" if borders else f"{country_name} has no land borders"
        
        # Return comprehensive info if no specific request
        else:
            info = []
            
            capitals = country_data.get('capital', [])
            if capitals:
                info.append(f"Capital: {capitals[0]}")
            
            population = country_data.get('population')
            if population:
                info.append(f"Population: {population:,}")
            
            region = country_data.get('region')
            if region:
                info.append(f"Region: {region}")
                
            currencies = country_data.get('currencies', {})
            if currencies:
                currency_names = [info_item.get('name', code) for code, info_item in currencies.items()]
                info.append(f"Currency: {', '.join(currency_names)}")
            
            area = country_data.get('area')
            if area:
                info.append(f"Area: {area:,} sq km")
            
            return f"Basic facts about {country_name}:\n" + "\n".join(info) if info else f"Limited data available for {country_name}"

class LLMCountryAgent:
    """Enhanced agent that combines REST Countries tool with LLM capabilities"""
    
    def __init__(self, openai_api_key: str):
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            api_key=openai_api_key,
            temperature=0.1
        )
        self.countries_tool = RestCountriesTool()
    
    def should_use_tool(self, query: str) -> bool:
        """Determine if the query should use the REST Countries tool"""
        # Keywords that indicate factual country data requests
        factual_keywords = [
            'capital', 'population', 'currency', 'area', 'size', 'language', 'languages',
            'timezone', 'time zone', 'flag', 'border', 'borders', 'calling code'
        ]
        
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in factual_keywords)
    
    def extract_country_from_query(self, query: str) -> Optional[str]:
        """Extract country name for context"""
        return self.countries_tool._extract_country_name(query.lower())
    
    def get_country_context(self, country_name: str) -> str:
        """Get basic country data for LLM context"""
        country_data = self.countries_tool._get_country_data(country_name)
        if not country_data:
            return f"No basic data available for {country_name}"
        
        # Get comprehensive country info for context
        return self.countries_tool._process_query("general info", country_data)
    
    def process_query(self, query: str) -> str:
        """Main method to process any country-related query"""
        
        # First, try to identify if there's a country in the query
        country_name = self.extract_country_from_query(query)
        
        # If it's a factual query that our tool can handle, use the tool
        if self.should_use_tool(query) and country_name:
            tool_result = self.countries_tool.run(query)
            
            # If tool found data, return it
            if "not available" not in tool_result.lower() and "error" not in tool_result.lower():
                return tool_result
        
        # For everything else, use LLM with context
        if country_name:
            # Get country context for the LLM
            country_context = self.get_country_context(country_name)
            
            system_message = SystemMessage(content=f"""
You are a knowledgeable assistant specializing in country information. 

Here's what I know about {country_name} from reliable sources:
{country_context}

When answering questions:
1. Use the factual data provided above when relevant
2. For questions beyond the basic facts (history, culture, politics, geography, economy, etc.), provide informative answers based on your knowledge
3. Be honest if you're not certain about specific details
4. Keep responses informative but concise
5. If the question is about current events, mention that your information might not be completely up to date
""")
        else:
            system_message = SystemMessage(content="""
You are a knowledgeable assistant specializing in country and geography information. 
Provide helpful, accurate information about countries, regions, and related topics.
Be honest about limitations in your knowledge, especially for current events.
""")
        
        # Get LLM response
        messages = [system_message, HumanMessage(content=query)]
        response = self.llm.invoke(messages)
        
        return response.content

# LangGraph Integration
class AgentState(TypedDict):
    messages: List[BaseMessage]

def enhanced_country_agent_node(state: AgentState):
    """Enhanced agent node that uses both tool and LLM"""
    messages = state["messages"]
    last_message = messages[-1]
    
    if isinstance(last_message, HumanMessage):
        # Initialize the enhanced agent
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            return {"messages": [AIMessage(content="OpenAI API key not configured. Please set OPENAI_API_KEY environment variable.")]}
        
        agent = LLMCountryAgent(openai_api_key)
        result = agent.process_query(last_message.content)
        
        response = AIMessage(content=result)
        return {"messages": [response]}
    
    return {"messages": []}

def create_enhanced_country_agent():
    """Create the enhanced country agent using LangGraph"""
    workflow = StateGraph(AgentState)
    workflow.add_node("agent", enhanced_country_agent_node)
    workflow.set_entry_point("agent")
    workflow.add_edge("agent", END)
    return workflow.compile()

def main():
    print("🌍 Enhanced Country Agent with LLM Integration")
    print("=" * 60)
    
    # Test queries that demonstrate the improvement
    test_queries = [
        # These should use the tool
        "What is the capital of Ghana?",
        "Tell me the population of Brazil",
        "What currency does Japan use?",
        
        # These should use LLM with country context
        "Tell me about the history of France",
        "What is the political system of Germany?",
        "What are the main industries in Nigeria?",
        "What is the culture like in Peru?",
        "What are some tourist attractions in Italy?",
        
        # General questions
        "What's the difference between a country and a nation?",
        "Which continent has the most countries?",
    ]
    
    # Test the enhanced agent
    try:
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            print("⚠️  OpenAI API key not found. Please set OPENAI_API_KEY environment variable.")
            print("Testing with REST Countries tool only...")
            
            tool = RestCountriesTool()
            for query in test_queries[:3]:  # Only test tool-compatible queries
                print(f"\n🟡 Query: {query}")
                result = tool.run(query)
                print(f"🟢 Answer: {result}")
        else:
            agent = LLMCountryAgent(openai_api_key)
            
            for query in test_queries:
                print(f"\n🟡 Query: {query}")
                result = agent.process_query(query)
                print(f"🟢 Answer: {result}")
                print("-" * 50)
    
    except Exception as e:
        print(f"🔴 Error: {str(e)}")

if __name__ == "__main__":
    main()