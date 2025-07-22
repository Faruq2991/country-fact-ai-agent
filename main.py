from tools.rest_countries_tool import RestCountriesTool

tool = RestCountriesTool()

queries = [
    "What is the capital of Kenya?",
    "Tell me the population of Brazil",
    "What currency does Egypt use?",
    "Give me the area of Nigeria",
    "Who are the languages spoken in Peru?",
    "What timezone is Australia in?",
    "What is the flag of France?",
    "Population of Wakanda"
]

for q in queries:
    print(f"\n🟡 Query: {q}")
    print("🟢 Answer:", tool._run(q))
