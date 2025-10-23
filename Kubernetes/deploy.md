helm install freshdesk-mcp-sandbox freshdesk-mcp -n freshdesk-mcp-sandbox --create-namespace -f freshdesk-mcp/sandbox.yaml
helm install freshdesk-mcp-production freshdesk-mcp -n freshdesk-mcp-production --create-namespace -f freshdesk-mcp/production.yaml

helm upgrade freshdesk-mcp freshdesk-mcp-sandbox -n freshdesk-mcp-sandbox -f freshdesk-mcp/sandbox.yaml
helm upgrade freshdesk-mcp freshdesk-mcp-production -n freshdesk-mcp-production -f freshdesk-mcp/production.yaml

helm uninstall freshdesk-mcp -n freshdesk-mcp-sandbox
helm uninstall freshdesk-mcp -n freshdesk-mcp-production