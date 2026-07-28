import subprocess
from pathlib import Path

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_ollama import ChatOllama


@tool
def run_ssh_command(host: str, command: str, private_key_path: str = "~/.ssh/id_rsa") -> str:
    """Run a command on a remote host via SSH.

    Args:
        host (str): The hostname or IP address of the remote host.
        command (str): The command to run on the remote host.
        private_key_path (str): Path to the private key used for authentication.
    """
    resolved_key = Path(private_key_path).expanduser()
    if not resolved_key.is_file():
        raise RuntimeError(
            f"Private key not found at '{resolved_key}'. Provide a valid private_key_path."
        )

    completed_process = subprocess.run(
        [
            "ssh",
            "-i",
            str(resolved_key),
            "-o",
            "IdentitiesOnly=yes",
            host,
            command,
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    if completed_process.returncode != 0:
        error_output = completed_process.stderr.strip()
        raise RuntimeError(
            f"SSH command failed with exit code {completed_process.returncode}: {error_output}"
        )

    return completed_process.stdout.strip()


llm = ChatOllama(
    model="qwen3.5:4b",
    validate_model_on_init=True,
    temperature=0,
)

tools = [run_ssh_command]

system_prompt = """
You are a helpful assistant that can run remote commands via the available tools.

You have access to the tool `run_ssh_command` which allows you to run commands on remote hosts via SSH.

Use this format:
Question: the input question you must answer
Thought: think about what to do
Action: the action to take, should be one of your tools
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question
"""

agent = create_agent(model=llm, tools=tools, system_prompt=system_prompt)

stream = agent.stream_events(
    {
        "messages": [{"role": "user", "content": "Please run the command `uname -a` on host `llm@192.168.52.2`."}]
    },
    version="v3"
)

for snapshot in stream.values:
    # Each snapshot contains the full state at that point
    latest_message = snapshot["messages"][-1]
    if latest_message.content:
        print(f"{latest_message.content}")