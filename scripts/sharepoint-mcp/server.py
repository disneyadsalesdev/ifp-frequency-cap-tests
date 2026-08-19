"""SharePoint search MCP server — developer-only read-only Graph API access."""

from __future__ import annotations

import json
import os
import sys
from typing import Any

import httpx
import msal
from mcp.server.fastmcp import FastMCP

# SECURITY-REVIEW: External HTTP to Microsoft Graph; credentials from env only.
DEFAULT_SITE = os.getenv(
    "SHAREPOINT_SITE_URL",
    "https://twdc.sharepoint.com/sites/ETAnthropic",
)
GRAPH_ROOT = "https://graph.microsoft.com/v1.0"
SCOPES = ["Sites.Read.All", "User.Read"]

mcp = FastMCP("sharepoint-search")


def _get_token() -> str:
    client_id = os.environ.get("AZURE_CLIENT_ID")
    tenant_id = os.environ.get("AZURE_TENANT_ID", "common")
    if not client_id:
        raise RuntimeError("Set AZURE_CLIENT_ID environment variable")

    app = msal.PublicClientApplication(
        client_id,
        authority=f"https://login.microsoftonline.com/{tenant_id}",
    )
    accounts = app.get_accounts()
    if accounts:
        result = app.acquire_token_silent(SCOPES, account=accounts[0])
        if result and "access_token" in result:
            return result["access_token"]

    flow = app.initiate_device_flow(scopes=SCOPES)
    if "user_code" not in flow:
        raise RuntimeError(f"Device flow failed: {flow}")
    print(flow["message"], file=sys.stderr)
    result = app.acquire_token_by_device_flow(flow)
    if "access_token" not in result:
        raise RuntimeError(result.get("error_description", "Authentication failed"))
    return result["access_token"]


def _headers() -> dict[str, str]:
    return {"Authorization": f"Bearer {_get_token()}"}


def _get_json(url: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
    with httpx.Client(timeout=30.0) as client:
        resp = client.get(url, headers=_headers(), params=params)
        resp.raise_for_status()
        return resp.json()


@mcp.tool()
def search_sharepoint(query: str, max_results: int = 10) -> str:
    """Search SharePoint content the signed-in user can read (Microsoft Graph)."""
    max_results = max(1, min(max_results, 25))
    body = {
        "requests": [
            {
                "entityTypes": ["driveItem", "listItem", "site"],
                "query": {"queryString": query},
                "from": 0,
                "size": max_results,
            }
        ]
    }
    with httpx.Client(timeout=30.0) as client:
        resp = client.post(
            f"{GRAPH_ROOT}/search/query",
            headers={**_headers(), "Content-Type": "application/json"},
            json=body,
        )
        resp.raise_for_status()
        data = resp.json()

    hits: list[dict[str, str]] = []
    for block in data.get("value", []):
        for container in block.get("hitsContainers", []):
            for hit in container.get("hits", []):
                resource = hit.get("resource", {})
                hits.append(
                    {
                        "name": resource.get("name") or hit.get("name", ""),
                        "webUrl": resource.get("webUrl", ""),
                        "summary": (hit.get("summary") or "")[:300],
                    }
                )
    return json.dumps({"query": query, "results": hits[:max_results]}, indent=2)


@mcp.tool()
def get_site_info(site_url: str | None = None) -> str:
    """Return metadata for a SharePoint site by URL."""
    url = site_url or DEFAULT_SITE
    # Graph expects hostname:path format, e.g. twdc.sharepoint.com:/sites/ETAnthropic
    from urllib.parse import urlparse

    parsed = urlparse(url)
    path = parsed.path.rstrip("/")
    graph_path = f"{parsed.hostname}:{path}"
    data = _get_json(f"{GRAPH_ROOT}/sites/{graph_path}")
    return json.dumps(
        {
            "displayName": data.get("displayName"),
            "webUrl": data.get("webUrl"),
            "id": data.get("id"),
        },
        indent=2,
    )


@mcp.tool()
def list_site_drives(site_url: str | None = None) -> str:
    """List document libraries (drives) on a SharePoint site."""
    url = site_url or DEFAULT_SITE
    from urllib.parse import urlparse

    parsed = urlparse(url)
    path = parsed.path.rstrip("/")
    graph_path = f"{parsed.hostname}:{path}"
    site = _get_json(f"{GRAPH_ROOT}/sites/{graph_path}")
    site_id = site["id"]
    drives = _get_json(f"{GRAPH_ROOT}/sites/{site_id}/drives")
    items = [
        {"name": d.get("name"), "webUrl": d.get("webUrl"), "id": d.get("id")}
        for d in drives.get("value", [])
    ]
    return json.dumps({"site": site.get("displayName"), "drives": items}, indent=2)


if __name__ == "__main__":
    mcp.run()
