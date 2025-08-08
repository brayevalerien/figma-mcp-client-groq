import asyncio
import json
import os
import signal

from dotenv import load_dotenv
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from groq import Groq

load_dotenv()


def find_server_pid(command_name: str, server_path: str | None) -> int | None:
    """
    Given the command that launched a server, returns its PID
    """
    try:
        import psutil

        current_pid = os.getpid()
        for proc in psutil.process_iter(["pid", "ppid", "name", "cmdline"]):
            try:
                if (
                    proc.info["ppid"] == current_pid
                    and proc.info["cmdline"]
                    and len(proc.info["cmdline"]) >= 2
                    and command_name in proc.info["cmdline"][0]
                    and server_path in proc.info["cmdline"][1]
                ):
                    return proc.info["pid"]
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    except ImportError:
        pass
    return None


class MCPClient:
    def __init__(
        self,
        command: str,
        args: str | list[str] | None = None,
        cwd: str = None,
        init_delay: float = 2,
        system_prompt: str
        | None = "You are an AI assistant with access to various tools to read and write to Figma files.",
    ):
        assert command, "A command must be provided to run the MCP server."
        assert 0 <= init_delay, f"Initialization delay must be positive, got {init_delay}."
        self.transport = StdioTransport(command=command, args=args or [], cwd=cwd or os.getcwd())
        self.command = command
        self.fastmcp_client = None
        self.groq_client = Groq()
        self.messages = [{"role": "system", "content": system_prompt}]
        self.init_delay = init_delay
        self.server_path = args[0] if args else None
        self.server_pid = None

    async def __aenter__(self):
        self.fastmcp_client = Client(transport=self.transport)
        await self.fastmcp_client.__aenter__()
        self.server_pid = find_server_pid(self.command, self.server_path)
        if self.init_delay != 0:
            await asyncio.sleep(self.init_delay)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.fastmcp_client:
            await self.fastmcp_client.__aexit__(exc_type, exc_val, exc_tb)
        if self.server_pid:
            print(f"[SYSTEM] Killing the MCP server (PID {self.server_pid}).")
            import psutil

            proc = psutil.Process(self.server_pid)
            proc.send_signal(signal.SIGTERM)

    async def list_tool_names(self) -> list[str]:
        """
        Lists all the tools provided by the MCP server.
        """
        tools = await self.fastmcp_client.list_tools()
        return list(map(lambda tool: tool.name, tools))

    async def get_tools(self) -> list:
        return await self.fastmcp_client.list_tools()

    async def call_tool(self, tool_name: str, tool_args: dict | None):
        return await self.fastmcp_client.call_tool(tool_name, arguments=tool_args)

    async def chat(self, user_prompt: str, model: str = "llama-3.3-70b-versatile", tools: list | None = None):
        self.messages.append({"role": "user", "content": user_prompt})
        completion = self.groq_client.chat.completions.create(messages=self.messages, model=model, tools=tools)
        return completion.choices[0].message
