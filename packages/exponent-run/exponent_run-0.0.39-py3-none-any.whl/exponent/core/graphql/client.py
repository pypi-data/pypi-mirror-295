from collections.abc import AsyncGenerator
from typing import Any

from gql import Client, gql
from gql.transport.httpx import HTTPXAsyncTransport
from gql.transport.websockets import WebsocketsTransport


class GraphQLClient:
    def __init__(self, api_key: str, base_api_url: str):
        graphql_url = f"{base_api_url}/graphql"
        websocket_url = f"{base_api_url}/graphql_ws".replace("https", "wss").replace(
            "http", "ws"
        )

        self.transport = HTTPXAsyncTransport(
            url=graphql_url,
            headers={"API-KEY": api_key},
        )

        self.ws_transport = WebsocketsTransport(
            url=websocket_url,
            init_payload={"apiKey": api_key},
        )

    async def query(
        self,
        query_str: str,
        vars: dict[str, Any] | None = None,
        op_name: str | None = None,
    ) -> Any:
        async with Client(
            transport=self.transport,
            fetch_schema_from_transport=True,
        ) as session:
            # Execute single query
            query = gql(query_str)
            result = await session.execute(query, vars, op_name)
            return result

    async def subscribe(
        self,
        subscription_str: str,
        vars: dict[str, Any] | None = None,
    ) -> AsyncGenerator[dict[str, Any], None]:
        async with Client(
            transport=self.ws_transport,
        ) as session:
            # Execute subscription
            subscription = gql(subscription_str)
            async for result in session.subscribe(subscription, vars):
                yield result
