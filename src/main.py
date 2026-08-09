import asyncio
import os
import logging
import sys

from dotenv import load_dotenv
from mcp.server import Server
from mcp.types import Tool, TextContent
from starlette.applications import Starlette
from starlette.routing import Route
import uvicorn
from mcp.server.sse import SseServerTransport

load_dotenv()

log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, log_level, logging.INFO))
logger = logging.getLogger(__name__)

from auth import authenticate
from services.docs import create_document
from services.gmail import draft_email

server_name = os.environ.get("MCP_SERVER_NAME", "google-workspace-mcp")
app = Server(server_name)
sse = SseServerTransport("/messages")

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available Google Workspace tools."""
    return [
        Tool(
            name="create_doc",
            description="Create a new Google Document with markdown/text content.",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Title of the document"},
                    "content": {"type": "string", "description": "Text content to insert into the document"}
                },
                "required": ["title", "content"]
            }
        ),
        Tool(
            name="draft_email",
            description="Draft an email in Gmail's outbox without sending it.",
            inputSchema={
                "type": "object",
                "properties": {
                    "to": {
                        "type": "array", 
                        "items": {"type": "string"},
                        "description": "List of recipient email addresses"
                    },
                    "subject": {"type": "string", "description": "Email subject line"},
                    "body": {"type": "string", "description": "Body of the email"}
                },
                "required": ["to", "subject", "body"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool execution requests."""
    try:
        # Authenticate on each request or keep a global creds object
        logger.info(f"Executing tool {name}")
        creds = authenticate()
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        return [TextContent(type="text", text=f"Authentication error: {e}")]

    if name == "create_doc":
        try:
            url = create_document(creds, arguments["title"], arguments.get("content", ""))
            return [TextContent(type="text", text=f"Document created successfully: {url}")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error creating document: {e}")]

    elif name == "draft_email":
        try:
            draft_id = draft_email(creds, arguments["to"], arguments["subject"], arguments.get("body", ""))
            return [TextContent(type="text", text=f"Email drafted successfully. Draft ID: {draft_id}")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error drafting email: {e}")]

    else:
        raise ValueError(f"Unknown tool: {name}")

async def handle_sse(request):
    """Handle SSE connections."""
    async with sse.connect_sse(
        request.scope, request.receive, request._send
    ) as streams:
        await app.run(
            streams[0], streams[1], app.create_initialization_options()
        )

async def handle_messages(request):
    """Handle incoming messages (POST)."""
    await sse.handle_post_message(request.scope, request.receive, request._send)

starlette_app = Starlette(
    routes=[
        Route("/sse", endpoint=handle_sse),
        Route("/messages", endpoint=handle_messages, methods=["POST"]),
    ]
)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    uvicorn.run("main:starlette_app", host="0.0.0.0", port=port, log_level=log_level.lower())
