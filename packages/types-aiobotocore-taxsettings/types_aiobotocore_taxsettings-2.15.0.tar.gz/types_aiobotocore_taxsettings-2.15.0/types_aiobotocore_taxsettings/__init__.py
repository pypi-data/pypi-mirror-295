"""
Main interface for taxsettings service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_taxsettings import (
        Client,
        ListTaxRegistrationsPaginator,
        TaxSettingsClient,
    )

    session = get_session()
    async with session.create_client("taxsettings") as client:
        client: TaxSettingsClient
        ...


    list_tax_registrations_paginator: ListTaxRegistrationsPaginator = client.get_paginator("list_tax_registrations")
    ```
"""

from .client import TaxSettingsClient
from .paginator import ListTaxRegistrationsPaginator

Client = TaxSettingsClient


__all__ = ("Client", "ListTaxRegistrationsPaginator", "TaxSettingsClient")
