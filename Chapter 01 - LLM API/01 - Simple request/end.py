import anthropic

client = anthropic.Anthropic()
message = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=1000,
    messages=[
        {
            "role": "user",
            "content": "How many wilayas are there in Algeria?",
        }
    ],
)
print(f"User: How many wilayas are there in Algeria?")
for block in message.content:
    if block.type == "text":
        print(f"Claude: {block.text}")