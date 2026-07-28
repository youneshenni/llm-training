from langchain.agents import create_agent
from langchain.tools import tool
from langchain.messages import AIMessage, HumanMessage
import requests

@tool
def get_coordinates(city: str) -> list[float]:
    """Get coordinates for specific city."""
    response = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json")
    data = response.json()
    if "results" in data and len(data["results"]) > 0:
        latitude = data["results"][0]["latitude"]
        longitude = data["results"][0]["longitude"]
        return [latitude, longitude]

@tool
def get_weather(latitude: float, longitude: float) -> str:
    """Get weather for specific city."""
    response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m")
    data = response.json()
    if "hourly" in data and "temperature_2m" in data["hourly"]:
        temperature = data["hourly"]["temperature_2m"][0]
        return f"The current temperature is {temperature}°C."

system_prompt = """
Act as a weather specialist.
You have access to two tools: "get_coordinates" and "get_weather". Use these tools to provide weather information for different cities.
The "get_coordinates" tool takes a city name as input and returns the latitude and longitude of that city.
The "get_weather" tool takes latitude and longitude as input and returns the current weather information for that location.
Give weather information like you would to a 5 year old

The user will ask you about the weather in different cities. When they do, use the "get_weather" tool to get the information and respond with a simple explanation of the weather.
If the user asks about anything other than weather, politely inform them that you can only provide weather information and suggest they ask about the weather in a specific city.

Answer in a sarcastic tone.
Respond in markdown format, and make sure to include the city name in your response.
"""



agent = create_agent(model="anthropic:claude-haiku-4-5", tools=[get_weather, get_coordinates], system_prompt=system_prompt)
question = input("Ask a question about the weather: ")
stream = agent.stream_events({
    "messages": [{"role": "user", "content": question}]}, version="v3")

for snapshot in stream.values:
    # Each snapshot contains the full state at that point
    latest_message = snapshot["messages"][-1]
    if latest_message.content:
        if isinstance(latest_message, HumanMessage):
            print(f"User: {latest_message.content}")
        elif isinstance(latest_message, AIMessage):
            print(f"Agent: {latest_message.content}")