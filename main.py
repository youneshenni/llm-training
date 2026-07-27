import anthropic

client = anthropic.Anthropic()
messages = []
while True:
    user_input = input("You: ")
    messages.append({"role": "user", "content": user_input})
    if user_input.lower() in ["exit", "quit"]:
        break

    message = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1000,
        messages=messages,
    )
    messages.append({"role": "assistant", "content": message.content[0].text })

    for block in message.content:
        if block.type == "text":
            print(f"Claude: {block.text}")
            
for block in messages:
    print(messages)