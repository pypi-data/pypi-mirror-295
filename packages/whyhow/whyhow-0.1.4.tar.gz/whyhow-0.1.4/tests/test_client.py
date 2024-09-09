"""Tests for the client module."""

from unittest.mock import MagicMock, Mock

import pytest
from httpx import AsyncClient, Client, Request

from whyhow.client import AsyncWhyHow, WhyHow, _APIKeyAuth


class TestAPIKeyAuth:
    def test_independent(self):
        auth = _APIKeyAuth(api_key="key")

        request = Request("GET", "https://example.com")
        request = next(auth.auth_flow(request))
        assert request.headers["x-api-key"] == "key"


class TestWhyHow:
    """Tests for the WhyHow class."""

    def test_resources(self):
        client = WhyHow(api_key="key")

        assert hasattr(client, "chunks")
        assert hasattr(client, "documents")
        assert hasattr(client, "graphs")
        assert hasattr(client, "schemas")
        assert hasattr(client, "workspaces")

    def test_constructor_missing_api_key_no_envvar(self):
        """Test that an error raised when the API key is missing."""
        # conftest.py guarantees that WHYHOW_API_KEY is not set
        with pytest.raises(ValueError, match="WHYHOW_API_KEY must be set"):
            WhyHow()

    def test_constructor_missing_api_key_envvar_present(self, monkeypatch):
        monkeypatch.setenv("WHYHOW_API_KEY", "key")
        client = WhyHow()

        assert client.httpx_client.auth.api_key == "key"

    def test_constructor_custom_base_url(self):
        client = WhyHow(api_key="key", base_url="https://example.com")

        assert client.httpx_client.base_url == "https://example.com"

    def test_httpx_kwargs(self, monkeypatch):
        """Test that httpx_kwargs passed to the httpx client."""
        fake_httpx_client_inst = Mock(spec=Client)
        fake_httpx_client_class = Mock(return_value=fake_httpx_client_inst)

        monkeypatch.setattr("whyhow.client.Client", fake_httpx_client_class)
        httpx_kwargs = {"verify": False}
        client = WhyHow(
            api_key="key",
            httpx_kwargs=httpx_kwargs,
        )

        assert fake_httpx_client_class.call_count == 1
        args, kwargs = fake_httpx_client_class.call_args

        assert not args
        assert kwargs["base_url"] == "https://api.whyhow.ai"
        assert not kwargs["verify"]

        assert client.httpx_client is fake_httpx_client_class.return_value

    def test_base_url_twice(self):
        """Test that an error raised when base_url is set twice."""
        with pytest.raises(
            ValueError, match="base_url cannot be set in httpx_kwargs."
        ):
            WhyHow(
                api_key="key",
                httpx_kwargs={"base_url": "https://example.com"},
            )

    def test_context_manager(self, monkeypatch):
        fake_httpx_client = MagicMock(spec=Client)
        client = WhyHow(api_key="key")

        monkeypatch.setattr(client, "httpx_client", fake_httpx_client)

        with client as c:
            assert c is client
            assert fake_httpx_client.__enter__.call_count == 1

        assert fake_httpx_client.__exit__.call_count == 1

    def test_close(self, monkeypatch):
        fake_httpx_client = MagicMock(spec=Client)
        client = WhyHow(api_key="key")

        monkeypatch.setattr(client, "httpx_client", fake_httpx_client)

        client.close()

        assert fake_httpx_client.close.call_count == 1


class TestAsyncWhyHow:
    """Tests for the AsyncWhyHow class."""

    def test_resources(self):
        client = AsyncWhyHow(api_key="key")

        assert hasattr(client, "chunks")
        assert hasattr(client, "documents")
        assert hasattr(client, "graphs")
        assert hasattr(client, "schemas")
        assert hasattr(client, "workspaces")

    def test_constructor_missing_api_key_no_envvar(self):
        """Test that an error raised when the API key is missing."""
        # conftest.py guarantees that WHYHOW_API_KEY is not set
        with pytest.raises(ValueError, match="WHYHOW_API_KEY must be set"):
            AsyncWhyHow()

    def test_constructor_missing_api_key_envvar_present(self, monkeypatch):
        monkeypatch.setenv("WHYHOW_API_KEY", "key")
        client = AsyncWhyHow()

        assert client.httpx_client.auth.api_key == "key"

    def test_constructor_custom_base_url(self):
        client = AsyncWhyHow(api_key="key", base_url="https://example.com")

        assert client.httpx_client.base_url == "https://example.com"

    def test_httpx_kwargs(self, monkeypatch):
        """Test that httpx_kwargs passed to the httpx client."""
        fake_httpx_client_inst = Mock(spec=AsyncClient)
        fake_httpx_client_class = Mock(return_value=fake_httpx_client_inst)

        monkeypatch.setattr(
            "whyhow.client.AsyncClient", fake_httpx_client_class
        )
        httpx_kwargs = {"verify": False}
        client = AsyncWhyHow(
            api_key="key",
            httpx_kwargs=httpx_kwargs,
        )

        assert fake_httpx_client_class.call_count == 1
        args, kwargs = fake_httpx_client_class.call_args

        assert not args
        assert kwargs["base_url"] == "https://api.whyhow.ai"
        assert not kwargs["verify"]

        assert client.httpx_client is fake_httpx_client_class.return_value

    def test_base_url_twice(self):
        """Test that an error raised when base_url is set twice."""
        with pytest.raises(
            ValueError, match="base_url cannot be set in httpx_kwargs."
        ):
            AsyncWhyHow(
                api_key="key",
                httpx_kwargs={"base_url": "https://example.com"},
            )

    @pytest.mark.asyncio
    async def test_context_manager(self, monkeypatch):
        fake_httpx_client = MagicMock(spec=AsyncClient)
        client = AsyncWhyHow(api_key="key")

        monkeypatch.setattr(client, "httpx_client", fake_httpx_client)

        async with client as c:
            assert c is client
            assert fake_httpx_client.__aenter__.call_count == 1

        assert fake_httpx_client.__aexit__.call_count == 1

    @pytest.mark.asyncio
    async def test_close(self, monkeypatch):
        fake_httpx_client = MagicMock(spec=AsyncClient)
        client = AsyncWhyHow(api_key="key")

        monkeypatch.setattr(client, "httpx_client", fake_httpx_client)

        await client.close()

        assert fake_httpx_client.aclose.call_count == 1
