import os
import requests
import json
from typing import Dict, Any, Optional
from langchain.tools import BaseTool

from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

# Enhanced RestCountriesTool with more features
class RestCountriesTool(BaseTool):
    name: str = "rest_countries_tool"
    description: str = """
    Get information about countries including:
    - Capital city
    - Population
    - Currency
    - Area (in square kilometers)
    - Languages
    - Region and subregion
    - Timezones
    - Flag emoji and image URL
    - Borders (neighboring countries)
    - Calling codes
    
    Usage examples:
    - "What is the capital of Ghana?"
    - "Tell me the population of Brazil"
    - "What currency does Egypt use?"
    - "Give me the area of Nigeria"
    - "What languages are spoken in Peru?"
    - "What timezone is Australia in?"
    - "Show me the flag of Nigeria"
    - "What countries border Germany?"
    """

    def _run(self, query: str) -> str:
        try:
            # Extract country name and query type
            country_name = self._extract_country_name(query.lower())
            if not country_name:
                return "I couldn't identify a country in your request. Please specify a country (e.g., 'What is the capital of Ghana?')."
            
            # Get country data
            country_data = self._get_country_data(country_name)
            if not country_data:
                return f"Sorry, I couldn't find information for '{country_name}'. Please check the spelling."
            
            # Determine what information to return based on query
            return self._process_query(query.lower(), country_data)
            
        except Exception as e:
            return f"An error occurred: {str(e)}"

    def _extract_country_name(self, query: str) -> Optional[str]:
        """Extract country name from the query"""
        # Common patterns to remove
        patterns_to_remove = [
            "what is the capital of", "tell me the population of", "what currency does",
            "give me the area of", "what languages are spoken in", "who are the languages spoken in",
            "what timezone is", "what time zone is", "show me the flag of", "what is the flag of",
            "what countries border", "which countries border", "what are the borders of",
            "what is the calling code", "what is the phone code", "use?", "in?", "?", "the"
        ]
        
        country_name = query.strip()
        for pattern in patterns_to_remove:
            country_name = country_name.replace(pattern, "").strip()
        
        return country_name if country_name else None

    def _get_country_data(self, country_name: str) -> Optional[Dict[str, Any]]:
        """Get country data from REST Countries API"""
        try:
            # Try different endpoints for better matching
            endpoints = [
                f"https://restcountries.com/v3.1/name/{country_name}?fullText=true",
                f"https://restcountries.com/v3.1/name/{country_name}"
            ]
            
            for endpoint in endpoints:
                response = requests.get(endpoint, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if data and len(data) > 0:
                        return data[0]  # Return first match
            
            return None
        except Exception:
            return None

    def _process_query(self, query: str, country_data: Dict[str, Any]) -> str:
        """Process the query and return appropriate information"""
        country_name = country_data.get('name', {}).get('common', 'Unknown')
        
        # Capital
        if any(word in query for word in ['capital']):
            capitals = country_data.get('capital', [])
            if capitals:
                return f"The capital of {country_name} is: {capitals[0]}"
            return f"I could not find the capital for {country_name}."
        
        # Population
        elif any(word in query for word in ['population']):
            population = country_data.get('population')
            if population:
                return f"The population of {country_name} is: {population:,}"
            return f"I could not find the population for {country_name}."
        
        # Currency
        elif any(word in query for word in ['currency', 'currencies']):
            currencies = country_data.get('currencies', {})
            if currencies:
                currency_names = [info.get('name', code) for code, info in currencies.items()]
                return f"The currency of {country_name} is: {', '.join(currency_names)}"
            return f"I could not find the currency for {country_name}."
        
        # Area
        elif any(word in query for word in ['area', 'size']):
            area = country_data.get('area')
            if area:
                return f"The area of {country_name} is: {area:,} square kilometers"
            return f"I could not find the area for {country_name}."
        
        # Languages
        elif any(word in query for word in ['language', 'languages']):
            languages = country_data.get('languages', {})
            if languages:
                language_names = list(languages.values())
                return f"The languages of {country_name} are: {', '.join(language_names)}"
            return f"I could not find the languages for {country_name}."
        
        # Timezone
        elif any(word in query for word in ['timezone', 'time zone', 'timezones']):
            timezones = country_data.get('timezones', [])
            if timezones:
                return f"The timezones of {country_name} are: {', '.join(timezones)}"
            return f"I could not find the timezone for {country_name}."
        
        # Flag
        elif any(word in query for word in ['flag']):
            flag_emoji = country_data.get('flag', '')
            flag_url = country_data.get('flags', {}).get('png', '')
            if flag_emoji or flag_url:
                result = f"The flag of {country_name}:"
                if flag_emoji:
                    result += f" {flag_emoji}"
                if flag_url:
                    result += f" (Image: {flag_url})"
                return result
            return f"I could not find the flag for {country_name}."
        
        # Borders
        elif any(word in query for word in ['border', 'borders', 'neighboring', 'neighbor']):
            borders = country_data.get('borders', [])
            if borders:
                return f"The countries that border {country_name} are: {', '.join(borders)}"
            return f"{country_name} has no land borders or I could not find border information."
        
        # Calling codes
        elif any(word in query for word in ['calling code', 'phone code', 'dial code']):
            calling_codes = country_data.get('idd', {})
            root = calling_codes.get('root', '')
            suffixes = calling_codes.get('suffixes', [])
            if root and suffixes:
                codes = [f"{root}{suffix}" for suffix in suffixes]
                return f"The calling codes for {country_name} are: {', '.join(codes)}"
            return f"I could not find the calling codes for {country_name}."
        
        # Default: return general info
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
            
            if info:
                return f"Information about {country_name}:\n" + "\n".join(info)
            return f"I found {country_name} but couldn't retrieve specific information."

# LangGraph State
class AgentState(TypedDict):
    messages: list[BaseMessage]

# Agent Node Functions
def country_agent_node(state: AgentState):
    """Main agent node that processes country queries"""
    messages = state["messages"]
    last_message = messages[-1]
    
    if isinstance(last_message, HumanMessage):
        tool = RestCountriesTool()
        result = tool.run(last_message.content)
        
        response = AIMessage(content=result)
        return {"messages": [response]}
    
    return {"messages": []}

def create_country_agent():
    """Create the country facts agent using LangGraph"""
    # Create the graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("agent", country_agent_node)
    
    # Set entry point
    workflow.set_entry_point("agent")
    
    # Add ending
    workflow.add_edge("agent", END)
    
    # Compile the graph
    return workflow.compile()

def main():
    print("🌍 Enhanced Country Facts AI Agent")
    print("=" * 50)
    
    # Test the enhanced tool directly
    print("--- Testing Enhanced RestCountriesTool ---")
    tool = RestCountriesTool()
    
    test_queries = [
        "What is the capital of Kenya?",
        "Tell me the population of Brazil",
        "What currency does Egypt use?",
        "Give me the area of Nigeria",
        "What languages are spoken in Peru?",
        "What timezone is Australia in?",
        "What is the flag of Nigeria?",
        "What countries border Germany?",
        "What is the calling code for Ghana?",
        "Population of Wakanda"  # Invalid country test
    ]
    
    for query in test_queries:
        print(f"🟡 Query: {query}")
        result = tool.run(query)
        print(f"🟢 Answer: {result}")
        print()
    
    print("--- Testing LangGraph Agent ---")
    
    # Create and test the LangGraph agent
    agent = create_country_agent()
    
    # Test queries for the agent
    agent_queries = [
        "What is the capital of Ghana?",
        "Tell me about the population and currency of Japan",
        "What timezone is India in?",
        "Show me the flag of Canada"
    ]
    
    for query in agent_queries:
        print(f"🟡 Agent Query: {query}")
        try:
            # Create initial state
            initial_state = {"messages": [HumanMessage(content=query)]}
            
            # Run the agent
            result = agent.invoke(initial_state)
            
            # Get the last message (AI response)
            if result["messages"]:
                last_message = result["messages"][-1]
                if isinstance(last_message, AIMessage):
                    print(f"🟢 Agent Answer: {last_message.content}")
                else:
                    print(f"🟢 Agent Answer: {last_message}")
            else:
                print("🔴 No response from agent")
        except Exception as e:
            print(f"🔴 Error: {str(e)}")
        print()
    
    print("--- Interactive Mode ---")
    print("Ask me about any country! (Type 'quit' to exit)")
    
    while True:
        try:
            user_input = input("\n🌍 Your question: ").strip()
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if user_input:
                # Use the direct tool for interactive mode (faster)
                result = tool.run(user_input)
                print(f"🤖 Answer: {result}")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"🔴 Error: {str(e)}")

if __name__ == "__main__":
    main()