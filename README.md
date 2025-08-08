# figma-mcp-client-groq
A Groq client for the Figma MCP that allows Groq models to interact (read and write) with Figma projects.

## Setting it up
First install the [Figma write MCP server](https://github.com/oO/figma-mcp-write-server/) on your machine before running this project. Please refer to the installation instruction in their readme.

Once you are ready:
1. `git clone https://github.com/brayevalerien/figma-mcp-client-groq`
2. `cd figma-mcp-client-groq`
3. `pip install -r requirements.txt` (using a virtual environement is recommended)
4. create a `.env` file and set `GROQ_API_KEY` (get a free key on [groq.com](https://groq.com/)) and `SERVER_ROOT` (path to the root of the Figma write MCP server).
5. optionally set `MODEL` in the `.env` file ([available models](https://console.groq.com/docs/models)). Please ensures the model supports tool calling.
6. `python src/main.py`

This will start an interactive chat session in your terminal where you can talk to the model.

> [!WARNING]
> This is still WIP, expect bugs (please [report them](https://github.com/brayevalerien/figma-mcp-client-groq/issues) or [fix them](https://github.com/brayevalerien/figma-mcp-client-groq/pulls) :D).
> Please note that tool calling is not implemented yet!