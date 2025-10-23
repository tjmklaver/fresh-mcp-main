FROM ghcr.io/astral-sh/uv:bookworm-slim

RUN adduser --disabled-password --uid 1000 mcpserver
RUN mkdir /.cache
RUN chown -R mcpserver /.cache
USER mcpserver
COPY --chown=mcpserver:mcpserver Kubernetes/freshdesk_mcp /home/mcpserver/freshdesk_mcp
WORKDIR /home/mcpserver/freshdesk_mcp
RUN uv sync --frozen

EXPOSE 8080
ENTRYPOINT ["uv", "run", "/home/mcpserver/freshdesk_mcp/server.py", "--http", "8080"]