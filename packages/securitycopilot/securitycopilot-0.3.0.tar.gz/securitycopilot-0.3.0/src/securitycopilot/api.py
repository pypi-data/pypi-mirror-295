# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# --------------------------------------------------------------------------


from azure.core.credentials import TokenCredential
from azure.core.pipeline import Pipeline
from azure.core.rest import HttpRequest, HttpResponse
from azure.core.pipeline.transport import RequestsTransport
from azure.core.pipeline.policies import (
    UserAgentPolicy,
    HeadersPolicy,
    RetryPolicy,
    RedirectPolicy,
    BearerTokenCredentialPolicy,
    ContentDecodePolicy,
    NetworkTraceLoggingPolicy,
    ProxyPolicy,
)



class TenantAwareBearerTokenCredentialPolicy(BearerTokenCredentialPolicy):
    """A BearerTokenCredentialPolicy that remembers a tenant ID and passes it during authentication requests."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._tenant_id = kwargs.get('tenant_id', None)

    def on_request(self, request) -> None:
        self._enforce_https(request)

        if self._token is None or self._need_new_token:
            if self._enable_cae:
                self._token = self._credential.get_token(*self._scopes, enable_cae=self._enable_cae, tenant_id=self._tenant_id)
            else:
                self._token = self._credential.get_token(*self._scopes, tenant_id=self._tenant_id)
        self._update_headers(request.http_request.headers, self._token.token)

    def authorize_request(self, request, *scopes: str, **kwargs) -> None:
        if self._tenant_id is not None:
            kwargs['tenant_id'] = self._tenant_id
        if self._enable_cae:
            kwargs.setdefault("enable_cae", self._enable_cae)
        self._token = self._credential.get_token(*scopes, **kwargs)
        self._update_headers(request.http_request.headers, self._token.token)


class SecurityCopilotAPIClient:
    """
    Client for the SecurityCopilot API.


    Ref: https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/core/azure-core/CLIENT_LIBRARY_DEVELOPER.md
    """

    def __init__(self, credential: TokenCredential, baseurl, geo_prefix: str = None, **kwargs):
        scopes = baseurl + "/.default"
        transport = kwargs.get("transport", RequestsTransport(**kwargs))
        policies = [
            kwargs.get(
                "user_agent_policy",
                UserAgentPolicy(
                    "securitycopilotpythonapi", user_agent_use_env=True, **kwargs
                ),
            ),
            kwargs.get("headers_policy", HeadersPolicy(**kwargs)),
            kwargs.get(
                "authentication_policy",
                TenantAwareBearerTokenCredentialPolicy(credential, scopes, **kwargs),
            ),
            ContentDecodePolicy(),
            kwargs.get("proxy_policy", ProxyPolicy(**kwargs)),
            kwargs.get("redirect_policy", RedirectPolicy(permit_redirects=False)),
            kwargs.get("retry_policy", RetryPolicy(**kwargs)),
            kwargs.get("logging_policy", NetworkTraceLoggingPolicy(**kwargs)),
        ]
        self._pipeline = Pipeline(transport, policies=policies)
        self._baseurl = baseurl
        self._geo_prefix = geo_prefix

    def _run_request(self, method, endpoint, params={}, **kwargs) -> HttpResponse:
        url_parts = [self._baseurl]
        if self._geo_prefix:
            url_parts.append(self._geo_prefix)
        url_parts.append(endpoint)
        self._http_request = HttpRequest(
            method, "/".join(url_parts), params=params, **kwargs
        )
        self._pipeline_response = self._pipeline.run(self._http_request, **kwargs)
        return self._pipeline_response.http_response

    def _GET(self, endpoint, params={}, **kwargs) -> HttpResponse:
        return self._run_request("GET", endpoint, params, **kwargs)

    def _POST(self, endpoint, params={}, json={}, **kwargs) -> HttpResponse:
        return self._run_request("POST", endpoint, params, json=json, **kwargs)
    
    def set_geo_prefix(self, geo_prefix: str):
        """Set the geo-specific prefix for subsequent API calls."""
        self._geo_prefix = geo_prefix
