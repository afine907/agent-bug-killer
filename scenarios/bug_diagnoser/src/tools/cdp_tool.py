"""CDP (Chrome DevTools Protocol) tools for browser debugging."""

from __future__ import annotations

import asyncio
import json
from pathlib import Path

from langchain_core.tools import tool

from core.settings import settings


async def _run_async(coro):
    """Run an async coroutine, handling existing event loops."""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        import concurrent.futures

        with concurrent.futures.ThreadPoolExecutor() as pool:
            return await asyncio.wrap_future(pool.submit(asyncio.run, coro))
    return await coro


@tool
async def cdp_connect(ws_url: str, timeout: int = 0) -> str:
    """Connect to a browser via Chrome DevTools Protocol WebSocket.

    Args:
        ws_url: WebSocket URL of the browser (e.g., ws://localhost:9222/devtools/browser/...).
        timeout: Connection timeout in seconds. 0 uses settings default.

    Returns:
        Session ID or error message.
    """
    if timeout <= 0:
        timeout = settings.cdp_timeout

    try:
        import websockets

        async def _connect() -> str:
            ws = await asyncio.wait_for(websockets.connect(ws_url), timeout=timeout)
            await ws.close()
            return f"Connected to browser at {ws_url}"

        return await _connect()
    except ImportError:
        return "Error: websockets library not installed. Run: pip install websockets"
    except Exception as e:
        return f"Error connecting to browser: {e}"


@tool
async def cdp_screenshot(
    ws_url: str,
    output_path: str = "",
    width: int = 1920,
    height: int = 1080,
) -> str:
    """Take a screenshot of the current browser page via CDP.

    Args:
        ws_url: WebSocket URL of the browser.
        output_path: Path to save the screenshot. Empty uses settings default.
        width: Viewport width in pixels.
        height: Viewport height in pixels.

    Returns:
        Path to the saved screenshot or error message.
    """
    if not output_path:
        output_path = str(Path(settings.cdp_screenshot_dir) / "screenshot.png")

    try:
        import websockets
        import base64

        async def _screenshot() -> str:
            ws = await asyncio.wait_for(websockets.connect(ws_url), timeout=settings.cdp_timeout)

            # Set viewport
            await ws.send(json.dumps({
                "id": 1,
                "method": "Emulation.setDeviceMetricsOverride",
                "params": {"width": width, "height": height, "deviceScaleFactor": 1, "mobile": False},
            }))
            await ws.recv()

            # Take screenshot
            await ws.send(json.dumps({"id": 2, "method": "Page.captureScreenshot", "params": {"format": "png"}}))
            response = json.loads(await ws.recv())

            if "result" in response and "data" in response["result"]:
                img_data = base64.b64decode(response["result"]["data"])
                Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                Path(output_path).write_bytes(img_data)
                await ws.close()
                return f"Screenshot saved to: {output_path}"

            await ws.close()
            return f"Error: {response.get('error', 'Unknown error')}"

        return await _screenshot()
    except ImportError:
        return "Error: websockets library not installed. Run: pip install websockets"
    except Exception as e:
        return f"Error taking screenshot: {e}"


@tool
async def cdp_console(ws_url: str, levels: str = "error,warning") -> str:
    """Get browser console logs via CDP.

    Args:
        ws_url: WebSocket URL of the browser.
        levels: Comma-separated log levels to filter (e.g., error,warning,info).

    Returns:
        JSON string of console log entries or error message.
    """
    try:
        import websockets

        async def _get_console() -> str:
            ws = await asyncio.wait_for(websockets.connect(ws_url), timeout=settings.cdp_timeout)

            # Enable Console domain
            await ws.send(json.dumps({"id": 1, "method": "Console.enable"}))
            await ws.recv()

            # Enable Runtime for console API
            await ws.send(json.dumps({"id": 2, "method": "Runtime.enable"}))
            await ws.recv()

            # Collect console messages
            logs = []
            try:
                while True:
                    msg = await asyncio.wait_for(ws.recv(), timeout=2)
                    data = json.loads(msg)
                    if data.get("method") == "Console.messageAdded":
                        entry = data.get("params", {}).get("message", {})
                        logs.append({
                            "level": entry.get("level", "info"),
                            "text": entry.get("text", ""),
                            "source": entry.get("source", ""),
                            "timestamp": entry.get("timestamp", 0),
                        })
            except asyncio.TimeoutError:
                pass
            except json.JSONDecodeError:
                pass

            await ws.close()

            # Filter by level
            filter_levels = [l.strip().lower() for l in levels.split(",")]
            if filter_levels:
                logs = [l for l in logs if l["level"].lower() in filter_levels]

            return json.dumps(logs, indent=2)

        return await _get_console()
    except ImportError:
        return "Error: websockets library not installed. Run: pip install websockets"
    except Exception as e:
        return f"Error getting console logs: {e}"


@tool
async def cdp_network(ws_url: str) -> str:
    """Get network requests via CDP.

    Args:
        ws_url: WebSocket URL of the browser.

    Returns:
        JSON string of network requests or error message.
    """
    try:
        import websockets

        async def _get_network() -> str:
            ws = await asyncio.wait_for(websockets.connect(ws_url), timeout=settings.cdp_timeout)

            # Enable Network domain
            await ws.send(json.dumps({"id": 1, "method": "Network.enable"}))
            await ws.recv()

            # Collect network events
            requests = []
            try:
                while True:
                    msg = await asyncio.wait_for(ws.recv(), timeout=2)
                    data = json.loads(msg)
                    if data.get("method") == "Network.requestWillBeSent":
                        req = data.get("params", {})
                        requests.append({
                            "url": req.get("request", {}).get("url", ""),
                            "method": req.get("request", {}).get("method", ""),
                            "status": None,
                        })
                    elif data.get("method") == "Network.responseReceived":
                        resp = data.get("params", {})
                        url = resp.get("response", {}).get("url", "")
                        status = resp.get("response", {}).get("status", 0)
                        for r in requests:
                            if r["url"] == url:
                                r["status"] = status
                                break
            except asyncio.TimeoutError:
                pass
            except json.JSONDecodeError:
                pass

            await ws.close()
            return json.dumps(requests, indent=2)

        return await _get_network()
    except ImportError:
        return "Error: websockets library not installed. Run: pip install websockets"
    except Exception as e:
        return f"Error getting network requests: {e}"
