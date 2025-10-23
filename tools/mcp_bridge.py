#!/usr/bin/env python3
"""
Simple working bridge script - based on what we know works
"""
import sys
import json
import httpx
import asyncio
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/tmp/mcp_bridge.log', mode='w'),
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger('MCPBridge')

logger.info("=== MCP Bridge Starting ===")

async def handle_message(client, line):
    """Handle a single message - we know this works from manual test"""
    try:
        if not line.strip():
            return
            
        logger.info(f"Processing: {line[:100]}...")
        
        # Parse JSON
        message = json.loads(line)
        method = message.get('method')
        msg_id = message.get('id')
        
        logger.info(f"Method: {method}, ID: {msg_id}")
        
        # Send to HTTP server
        response = await client.post(
            "http://localhost:8080/mcp",
            json=message,
            headers={"Content-Type": "application/json"},
            timeout=10.0
        )
        
        logger.info(f"HTTP response: {response.status_code}")
        
        if response.status_code == 204:
            logger.info(f"No response needed for {method}")
            return
        elif response.status_code == 200:
            response_data = response.json()
            response_line = json.dumps(response_data)
            print(response_line, flush=True)
            logger.info(f"Sent response for {method}")
        else:
            logger.error(f"HTTP error {response.status_code}")
            error_response = {
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {
                    "code": -32603,
                    "message": f"HTTP error {response.status_code}"
                }
            }
            print(json.dumps(error_response), flush=True)
            
    except Exception as e:
        logger.error(f"Error: {e}")
        if 'message' in locals():
            error_response = {
                "jsonrpc": "2.0",
                "id": message.get('id'),
                "error": {
                    "code": -32603,
                    "message": str(e)
                }
            }
            print(json.dumps(error_response), flush=True)

async def main():
    logger.info("Starting main loop")
    
    # Test connection first
    try:
        async with httpx.AsyncClient(timeout=5.0) as test_client:
            response = await test_client.get("http://localhost:8080/health")
            logger.info(f"Health check: {response.status_code}")
    except Exception as e:
        logger.error(f"Cannot connect to HTTP server: {e}")
        sys.exit(1)
    
    # Main processing loop
    async with httpx.AsyncClient(timeout=30.0) as client:
        logger.info("Ready to process messages")
        
        # Use simple line-by-line reading that we know works
        try:
            for line in sys.stdin:
                await handle_message(client, line.strip())
                
        except KeyboardInterrupt:
            logger.info("Interrupted")
        except Exception as e:
            logger.error(f"Fatal error: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"Startup error: {e}")
        sys.exit(1)