from ollama import ChatResponse
from ollama import Client

client = Client(
    host='127.0.0.1:11434',
)


system_prompt = """
  You are a redactor who will redact multiple types of documents
    including but not limited to: text, code, CSV, and lists.
  
  The user will give you a document type, and you will creatively write that document for him
  
  You shouldn't expect any other input from the user, and you should not ask for any other input from the user.
  Generate the document creatively based only on the document type given by the user.
  """
  
for index, type in enumerate(["text", "code", "CSV", "list"]):
    prompt = f"Please redact a {type} "
    redacted_document = client.chat(
        model='qwen3.5:9b',
        messages=[
          {
                'role': 'user',
                'content': prompt,
            },
          {
            'role': 'system',
            'content': system_prompt,
          }
        ],
        think=True,
    )
    print(f"Redacted {type} document:\n{redacted_document}\n")
    with open(f"redacted_{index}.txt", "w") as f:
        f.write(redacted_document.message.content)