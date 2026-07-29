from enum import Enum
from pydantic import BaseModel
from os import remove

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_ollama import ChatOllama

class Extension(Enum):
    CSV: str = "csv"
    MARKDOWN: str = "md"
    PYTHON: str = "py"

class Answer(BaseModel):
    extension: Extension
    description: str



@tool
def read_file(filename: str) -> str:
    """Read the contents of a file.

    Args:
        filename (str): The name of the file to read.
    """
    try:
        with open(filename, "r") as f:
            return f.read()
    except FileNotFoundError:
        return f"File '{filename}' not found."
    except Exception as e:
        return f"Error reading file '{filename}': {str(e)}"
    
@tool
def set_extension(filename: str, extension: Extension) -> str:
    """Set the extension of a file.

    Args:
        filename (str): The name of the file to set the extension for.
        extension (Extension): The new extension to set for the file.
    """
    new_filename = f"{filename}.{extension.value}"
    try:
        with open(filename, "r") as f:
            content = f.read()
        with open(new_filename, "w") as f:
            f.write(content)
        # Delete file with old extension if it exists
        remove(filename)
        return f"File '{filename}' renamed to '{new_filename}'."
    except FileNotFoundError:
        return f"File '{filename}' not found."
    except Exception as e:
        return f"Error renaming file '{filename}': {str(e)}"

llm = ChatOllama(
    model="qwen3.5:4b",
    validate_model_on_init=True,
    temperature=0,
)

tools = [read_file, set_extension]

system_prompt = """
You have a list of files under the folder `files`
The user will give you a filename, you will read the contents of the file using the `read_file` tool. When using this tool, you should indicate the relative path to the file, for example: `files/file_0.txt`
Then you will decide what extension the file should have, and you will set the extension using the `set_extension` tool
Then, you will reply to the user with the new file extension and a description of the file contents.
"""

agent = create_agent(model=llm, tools=tools, system_prompt=system_prompt, response_format=Answer)

for i in range(4):
    answer = agent.invoke({
        "messages": [{"role": "user", "content": f"Please read the file 'redacted_{i}.txt' and set the appropriate extension."}]                       
    })
    print(answer)