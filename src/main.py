import asyncio
import json
import os
import shutil

from dotenv import load_dotenv
from prompt_toolkit import PromptSession

import pretty_print
from mcp_groq_client import MCPClient

load_dotenv()
SERVER_ROOT = os.getenv("SERVER_ROOT", "~/figma-mcp-write-server/")
MODEL = os.getenv("MODEL", "llama-3.1-8b-instant")
SYSTEM_TERMINAL_PROMPT = "[SYSTEM]"
USER_TERMINAL_PROMPT = "[USER]"
AGENT_TERMINAL_PROMPT = f"[{MODEL.upper()}]"


def get_server_config():
    node_path = shutil.which("node")
    if not node_path:
        raise EnvironmentError("Node.js executable not found. Please ensure Node.js is installed and in your PATH.")
    server_script = os.path.join(SERVER_ROOT, "dist/index.js")
    return {"command": node_path, "args": [server_script], "cwd": SERVER_ROOT}


def format_tools_list(tools):
    """
    Converts a list of Tool objects into OpenAI's function tool format.

    Args:
        tools (List[object]): List of Tool objects, each expected to have
            `name`, `description`, and `inputSchema` attributes.

    Returns:
        List[dict]: OpenAI-compliant tool definitions.
    """
    return [
        {
            "type": "function",
            "function": {
                "name": getattr(tool, "name"),
                "description": getattr(tool, "description", "No description provided."),
                "parameters": getattr(tool, "inputSchema"),
            },
        }
        for tool in tools
    ]


async def main():
    server_config = get_server_config()
    print(
        SYSTEM_TERMINAL_PROMPT, f"Starting server with command: {server_config['command']} {server_config['args'][0]}"
    )
    try:
        async with MCPClient(**server_config, init_delay=5) as client:
            print(SYSTEM_TERMINAL_PROMPT, "MCP Client connected to Figma server successfully.")
            tool_names = await client.list_tool_names()
            print(SYSTEM_TERMINAL_PROMPT, f"Found {len(tool_names)} tools.")

            tools = await client.get_tools()
            tools = format_tools_list(tools)
            with open("figma_tools.json", "w") as f:
                f.write(json.dumps(tools, indent=2))

            chat_session = PromptSession()
            print(
                SYSTEM_TERMINAL_PROMPT,
                f"Session started, you can now interact with {MODEL}. Type 'exit' to close the session.",
            )
            while True:
                try:
                    user_prompt = await chat_session.prompt_async(USER_TERMINAL_PROMPT + " ")
                    if not user_prompt:
                        continue
                    if user_prompt.lower() == "exit":
                        print(SYSTEM_TERMINAL_PROMPT, "Exiting...")
                        break

                    agent_response = await client.chat(user_prompt, model=MODEL, tools=tools)
                    agent_called_tools = bool(agent_response.tool_calls)
                    print(AGENT_TERMINAL_PROMPT, "(called tool)" if agent_called_tools else agent_response.content)
                    if agent_called_tools:
                        # TODO: implement tool calls
                        print(
                            SYSTEM_TERMINAL_PROMPT,
                            f"{MODEL} tried calling {', '.join([f'"{tool_call.function.name}"' for tool_call in agent_response.tool_calls])} but tool calls not implemented yet, skipping.",
                        )
                        continue

                # TODO: proper error handling
                except Exception as e:
                    print(f"Error during chat session: {str(e)}")

    # TODO: proper error handling
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
