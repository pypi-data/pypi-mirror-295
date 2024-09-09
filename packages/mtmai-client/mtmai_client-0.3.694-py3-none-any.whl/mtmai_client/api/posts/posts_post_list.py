from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.blog_post_list_response import BlogPostListResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    query: Union[Unset, str] = "",
    offset: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["query"] = query

    params["offset"] = offset

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/posts/items",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[BlogPostListResponse, HTTPValidationError]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = BlogPostListResponse.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[BlogPostListResponse, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    query: Union[Unset, str] = "",
    offset: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Response[Union[BlogPostListResponse, HTTPValidationError]]:
    """Post List

    Args:
        query (Union[Unset, str]):  Default: ''.
        offset (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[BlogPostListResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        query=query,
        offset=offset,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    query: Union[Unset, str] = "",
    offset: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Optional[Union[BlogPostListResponse, HTTPValidationError]]:
    """Post List

    Args:
        query (Union[Unset, str]):  Default: ''.
        offset (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BlogPostListResponse, HTTPValidationError]
    """

    return sync_detailed(
        client=client,
        query=query,
        offset=offset,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    query: Union[Unset, str] = "",
    offset: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Response[Union[BlogPostListResponse, HTTPValidationError]]:
    """Post List

    Args:
        query (Union[Unset, str]):  Default: ''.
        offset (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[BlogPostListResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        query=query,
        offset=offset,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    query: Union[Unset, str] = "",
    offset: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Optional[Union[BlogPostListResponse, HTTPValidationError]]:
    """Post List

    Args:
        query (Union[Unset, str]):  Default: ''.
        offset (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BlogPostListResponse, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            client=client,
            query=query,
            offset=offset,
            limit=limit,
        )
    ).parsed
