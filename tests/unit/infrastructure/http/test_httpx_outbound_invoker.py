from __future__ import annotations

import httpx
import pytest
import respx

from app.domain.errors import OutboundConnectionError, OutboundTimeoutError
from app.infrastructure.http.httpx_outbound_invoker import HttpxOutboundInvoker


@respx.mock
def test_httpx_outbound_invoker_returns_json_response() -> None:
    respx.post("https://example.invalid/chat").mock(
        return_value=httpx.Response(200, json={"id": "chatcmpl-123", "ok": True})
    )

    response = HttpxOutboundInvoker().post_json(
        endpoint="https://example.invalid/chat",
        body={"messages": []},
        headers={},
        timeout_ms=30000,
    )

    assert response.status_code == 200
    assert response.json_body == {"id": "chatcmpl-123", "ok": True}
    assert response.text_body is None


@respx.mock
def test_httpx_outbound_invoker_returns_text_response() -> None:
    respx.post("https://example.invalid/chat").mock(
        return_value=httpx.Response(
            502,
            text="bad gateway",
            headers={"content-type": "text/plain"},
        )
    )

    response = HttpxOutboundInvoker().post_json(
        endpoint="https://example.invalid/chat",
        body={"messages": []},
        headers={},
        timeout_ms=30000,
    )

    assert response.status_code == 502
    assert response.json_body is None
    assert response.text_body == "bad gateway"


@respx.mock
def test_httpx_outbound_invoker_maps_timeout() -> None:
    respx.post("https://example.invalid/chat").mock(side_effect=httpx.ReadTimeout("timeout"))

    with pytest.raises(OutboundTimeoutError):
        HttpxOutboundInvoker().post_json(
            endpoint="https://example.invalid/chat",
            body={"messages": []},
            headers={},
            timeout_ms=30000,
        )


@respx.mock
def test_httpx_outbound_invoker_maps_connection_error() -> None:
    request = httpx.Request("POST", "https://example.invalid/chat")
    respx.post("https://example.invalid/chat").mock(
        side_effect=httpx.ConnectError("connect failed", request=request)
    )

    with pytest.raises(OutboundConnectionError):
        HttpxOutboundInvoker().post_json(
            endpoint="https://example.invalid/chat",
            body={"messages": []},
            headers={},
            timeout_ms=30000,
        )


def test_httpx_outbound_invoker_builds_granular_timeout_policy() -> None:
    invoker = HttpxOutboundInvoker(
        connect_timeout_ms=2000,
        write_timeout_ms=4000,
        pool_timeout_ms=1000,
    )

    timeout = invoker._build_timeout(30000)

    assert timeout.connect == 2.0
    assert timeout.read == 30.0
    assert timeout.write == 4.0
    assert timeout.pool == 1.0


def test_httpx_outbound_invoker_closes_shared_client() -> None:
    client = httpx.Client()
    invoker = HttpxOutboundInvoker(client=client)

    invoker.close()

    assert client.is_closed is True
