import anthropic

client = anthropic.Anthropic()
question = input("You: ")
message = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=1000,
    messages=[
        {
            "role": "user",
            "content": question,
        }
    ],
)
for block in message.content:
    if block.type == "text":
        print(f"Claude: {block.text}")