"""
Main interface for ivschat service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_ivschat import (
        Client,
        IvschatClient,
    )

    session = get_session()
    async with session.create_client("ivschat") as client:
        client: IvschatClient
        ...

    ```
"""

from .client import IvschatClient

Client = IvschatClient

__all__ = ("Client", "IvschatClient")
