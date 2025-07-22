from langchain.tools import BaseTool
import requests


class RestCountriesTool(BaseTool):
    name = "rest_countries_api"
    description = (
        "Useful for answering questions about countries. "
        "Input should be a string in the format: 'country:fact_type', "
        "e.g., 'Ghana:capital'"
    )

    def _parse_input(self, input_str: str):
        input_str = input_str.lower()
        country = None
        fact_type = None

        countries = ["ghana", "france", "japan", "united states", "canada", "nigeria", "germany", "brazil", "india", "united kingdom", "australia", "china", "mexico", "egypt"]
        countries.sort(key=len(), reverse=True)
        for place in countries:
            if place in input_str:
                country = place 
                break
        if "capital" in input_str:
            fact_type = "capital"
        elif "population" in input_str:
            fact_type = "population"
        elif "language" in input_str or "languages" in input_str:
            fact_type = "language"
        elif "currency" in input_str or "currencies" in input_str:
            fact_type = "currency"
        elif "area" in input_str or "size" in input_str:
            fact_type = "area"
        elif "continent" in input_str:
            fact_type = "continent"
        elif "region" in input_str:
            fact_type = "region"
        elif "timezone" in input_str:
            fact_type = "timezone"
        elif "subregion" in input_str:
            fact_type = "subregion"
            fact_type = "timezone"
        elif "flag" in input_str:
            fact_type = "flag"
        
        

        return country, fact_type

    def _call_api(self, country: str):
        if not country:
            return None

        api_url = f"https://restcountries.com/v3.1/name/{country}?fullText=true"
        
        try:
            response = requests.get(api_url, timeout=5) # Add a timeout
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
            data = response.json()
            return data
        except requests.exceptions.Timeout:
            print(f"API call timed out for {country}.")
            return None
        except requests.exceptions.ConnectionError:
            print(f"Network error: Could not connect to API for {country}.")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error calling API for {country}: {e}")
            return None
        except ValueError: # Catches JSON decoding errors
            print(f"Error parsing JSON response for {country}")
            return None

    def _extract_fact(self, api_data: list, fact_type: str):
        if not api_data or not fact_type:
            return None

        country_data = api_data[0] 

        if fact_type == "capital":
            return country_data.get("capital", ["N/A"])[0] if country_data.get("capital") else "N/A"
        elif fact_type == "population":
            return f"{country_data.get('population', 'N/A'):,}"
        elif fact_type == "language":
            languages = country_data.get("languages")
            if languages:
                return ", ".join(languages.values())
            return "N/A"
        elif fact_type == "currency":
            currencies = country_data.get("currencies")
            if currencies:
                currency_names = [c_info.get("name") for c_code, c_info in currencies.items()]
                return ", ".join(filter(None, currency_names)) 
            return "N/A"
        elif fact_type == "area":
            area = country_data.get("area")
            if area is not None:
                return f"{area:,} square kilometers"
            return "N/A"
        
        return "Fact type not supported or not found for this country."

    def _run(self, input_str: str) -> str:
        country, fact_type = self._parse_input(input_str)

        if not country:
            return "I couldn't identify a country in your request. Please specify a country (e.g., 'What is the capital of Ghana?')."
        if not fact_type:
            return f"I couldn't identify the type of fact you're looking for about {country.title()}. Try asking about 'capital', 'population', 'language', 'currency', or 'area'."

        api_data = self._call_api(country)

        if not api_data:
            return f"I could not retrieve information for {country.title()}. This might be due to a network error or an invalid country name."
        
        fact = self._extract_fact(api_data, fact_type)

        if fact and fact != "N/A" and "Fact type not supported" not in fact:
            return f"The {fact_type} of {country.title()} is: {fact}"
        else:
            return f"I could not find the {fact_type} for {country.title()}."
