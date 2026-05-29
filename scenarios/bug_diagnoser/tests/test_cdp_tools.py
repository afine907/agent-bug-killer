"""Tests for CDP tools."""

from unittest.mock import patch

from scenarios.bug_diagnoser.src.tools.cdp_tool import (
    cdp_connect,
    cdp_console,
    cdp_network,
    cdp_screenshot,
)


class TestCdpConnect:
    """Tests for the cdp_connect tool."""

    async def test_connect_without_websockets(self) -> None:
        """Should return error if websockets not installed."""
        with patch.dict("sys.modules", {"websockets": None}):
            result = await cdp_connect.ainvoke({"ws_url": "ws://localhost:9222"})
            assert "Error" in result or "websockets" in result.lower()

    async def test_connect_exception(self) -> None:
        """Should handle connection exceptions gracefully."""
        result = await cdp_connect.ainvoke({"ws_url": "ws://invalid:9222"})
        assert isinstance(result, str)


class TestCdpScreenshot:
    """Tests for the cdp_screenshot tool."""

    async def test_screenshot_without_websockets(self) -> None:
        """Should return error if websockets not installed."""
        with patch.dict("sys.modules", {"websockets": None}):
            result = await cdp_screenshot.ainvoke({"ws_url": "ws://localhost:9222"})
            assert "Error" in result or "websockets" in result.lower()

    async def test_screenshot_exception(self) -> None:
        """Should handle exceptions gracefully."""
        result = await cdp_screenshot.ainvoke({"ws_url": "ws://invalid:9222"})
        assert isinstance(result, str)


class TestCdpConsole:
    """Tests for the cdp_console tool."""

    async def test_console_without_websockets(self) -> None:
        """Should return error if websockets not installed."""
        with patch.dict("sys.modules", {"websockets": None}):
            result = await cdp_console.ainvoke({"ws_url": "ws://localhost:9222"})
            assert "Error" in result or "websockets" in result.lower()

    async def test_console_exception(self) -> None:
        """Should handle exceptions gracefully."""
        result = await cdp_console.ainvoke({"ws_url": "ws://invalid:9222"})
        assert isinstance(result, str)


class TestCdpNetwork:
    """Tests for the cdp_network tool."""

    async def test_network_without_websockets(self) -> None:
        """Should return error if websockets not installed."""
        with patch.dict("sys.modules", {"websockets": None}):
            result = await cdp_network.ainvoke({"ws_url": "ws://localhost:9222"})
            assert "Error" in result or "websockets" in result.lower()

    async def test_network_exception(self) -> None:
        """Should handle exceptions gracefully."""
        result = await cdp_network.ainvoke({"ws_url": "ws://invalid:9222"})
        assert isinstance(result, str)
