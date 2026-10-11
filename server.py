
import hashlib
import os

from mcp.server.mcpserver import MCPServer, Context

mcp = MCPServer("exam-challenge-server")


@mcp.tool()
async def solve_challenge(ctx: Context) -> str:
    """Solve the exam challenge using the request header."""

    request = ctx.request_context.request
    challenge = request.headers.get("x-exam-challenge")

    if not challenge:
        raise ValueError("Missing X-Exam-Challenge header")

    email = "22f3003122@ds.study.iitm.ac.in"
    message = f"{challenge}:{email}"

    return hashlib.sha256(
        message.encode("utf-8")
    ).hexdigest()[:16]


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))

    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=port,
        stateless_http=True,
        json_response=True,
    )
