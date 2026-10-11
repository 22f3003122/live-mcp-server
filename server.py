
import hashlib
import os

from mcp.server.fastmcp import FastMCP, Context

mcp = FastMCP(
    "exam-challenge-server",
    stateless_http=True,
    json_response=True,
)


@mcp.tool()
async def solve_challenge(ctx: Context) -> str:
    """Solve the current exam challenge using its request header."""

    request = ctx.request_context.request
    challenge = request.headers.get("x-exam-challenge")

    if not challenge:
        raise ValueError("Missing X-Exam-Challenge header")

    email = "22f3003122@ds.study.iitm.ac.in"
    message = f"{challenge}:{email}"

    return hashlib.sha256(message.encode("utf-8")).hexdigest()[:16]


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", "8000"))

    uvicorn.run(
        mcp.streamable_http_app(),
        host="0.0.0.0",
        port=port,
    )
