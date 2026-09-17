import os
from mcp.client.streamable_http import streamablehttp_client
from strands.tools.mcp import MCPClient
from logger import get_logger
from identity_helper import get_token

l = get_logger(__name__)

GATEWAY_URL = os.environ.get("GATEWAY_URL")

_mcp_client = None
_mcp_tools_list = None

async def get_mcp_tools_list():
    """Lazily connects to the Gateway and fetches tools on first call, caches after."""
    global _mcp_client, _mcp_tools_list

    if _mcp_tools_list is not None:
        return _mcp_tools_list

    if not GATEWAY_URL:
        l.info("⚠️ GATEWAY_URL not available, gateway tools disabled")
        _mcp_tools_list = []
        return _mcp_tools_list

    gateway_access_token = await get_token()
    if not gateway_access_token:
        l.info("⚠️ gateway_access_token not available, gateway tools disabled")
        _mcp_tools_list = []
        return _mcp_tools_list

    _mcp_client = MCPClient(lambda: streamablehttp_client(
        GATEWAY_URL,
        headers={"Authorization": f"Bearer {gateway_access_token}"}
    ))
    _mcp_client.start()
    _mcp_tools_list = _mcp_client.list_tools_sync()
    l.info(f"✅ Retrieved {len(_mcp_tools_list)} tools")
    return _mcp_tools_list
