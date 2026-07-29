from langchain.agents import create_agent
from langchain.tools import tool
from langchain.messages import AIMessage, HumanMessage


@tool
def get_weather(city: str) -> str:
    """Get weather for specific city."""
    return f"The weather in {city} is sunny with a high of 25°C."

system_prompt = """
Act as a weather specialist. You have access to a tool called "get_weather" that can provide weather information for specific cities.
Give weather information like you would to a 5 year old

The user will ask you about the weather in different cities. When they do, use the "get_weather" tool to get the information and respond with a simple explanation of the weather.
If the user asks about anything other than weather, politely inform them that you can only provide weather information and suggest they ask about the weather in a specific city.

Answer in a sarcastic tone.
Respond in markdown format, and make sure to include the city name in your response.
"""



agent = create_agent(model="anthropic:claude-sonnet-4-6", tools=[get_weather], system_prompt=system_prompt)
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