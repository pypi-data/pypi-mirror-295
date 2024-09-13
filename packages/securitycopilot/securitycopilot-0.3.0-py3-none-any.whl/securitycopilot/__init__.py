# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# --------------------------------------------------------------------------


from time import sleep
from azure.identity import DefaultAzureCredential
from azure.core.credentials import TokenCredential
from .api import SecurityCopilotAPIClient


_ENVPROD = "prod"
_ENVDEV = "dev"

_ENDPOINTS = {
    _ENVDEV: "https://api.medeina-dev.defender.microsoft.com",
    _ENVPROD: "https://api.securitycopilot.microsoft.com",
}
_SCOPES = {
    _ENVDEV: "https://api.medeina-dev.defender.microsoft.com/.default",
    _ENVPROD: "https://api.securitycopilot.microsoft.com/.default",
}
_SOURCE = "api.python"
_CONTEXT = {
    "apiclient": None,
    "cred": None,
    "env": _ENVPROD,
    "session": None,
    "tenant_id": None,
    "initialized": False,
    "session": None,
}


def init(
    interactive_auth: bool = True, tenant_id: str = None, dev: bool = False, 
    geo_prefix: str = None, credential: TokenCredential = None,  **apikwargs
):
    """Initializes the Security Copilot client, optionally setting params that apply to subsequent interactions.

    :keyword bool interactive_auth: Whether to enable browser-based interactive login. Defaults to True.
    :keyword str tenant_id: Optional tenant ID for token requests. Recommended if your user account has
        access to more than one tenant.
    :keyword bool dev: Whether to point to the development environment (defaults to False).
    :keyword str geo_prefix: The geo-specific region prefix to add to API calls (defaults to None).
    :raises SecurityCopilotClientError: if the package is already initiated
    """
    if _CONTEXT["initialized"]:
        raise SecurityCopilotClientError("Package is already initialized")
    _CONTEXT["cred"] = credential if credential else DefaultAzureCredential(
        exclude_interactive_browser_credential=not interactive_auth,
        additionally_allowed_tenants = [tenant_id] if tenant_id else []
    )
    _CONTEXT["tenant_id"] = tenant_id
    if dev:
        _CONTEXT["env"] = _ENVDEV
    if tenant_id:
        apikwargs["tenant_id"] = tenant_id
    _CONTEXT["geo_prefix"] = geo_prefix
    _CONTEXT["apiclient"] = SecurityCopilotAPIClient(
        _CONTEXT["cred"], _ENDPOINTS[_CONTEXT["env"]], geo_prefix=geo_prefix, **apikwargs
    )
    _CONTEXT["initialized"] = True

def determine_geo_prefix():
    """Determine the geo prefix to use for subsequent API requests. 
    
    Prefix is stored in module context and configured in the API client for subsequent use."""
    _ensure_init()
    r = _CONTEXT["apiclient"]._GET("auth")
    if r.status_code != 307:
        raise SecurityCopilotClientError(
            "Could not determine geo prefix, got status code {r.status_code} from API, expected 307."
        )
    redirect_target = r.headers["Location"]
    _CONTEXT["geo_prefix"] = "/".join(redirect_target.split("/")[1:3])
    _CONTEXT["apiclient"].set_geo_prefix(_CONTEXT["geo_prefix"])



def submit_prompt(prompt: str) -> "Session":
    """Submit a prompt to the SecurityCopilot API."""
    _ensure_init()
    _ensure_geo()
    _ensure_session()
    prompt = _CONTEXT["session"].submit_prompt(prompt, source=_SOURCE).evaluate()
    return _CONTEXT["session"]


def run_skill(skillname: str, params={}) -> "Session":
    """Submit a skill type prompt to the SecurityCopilot API."""
    _ensure_init()
    _ensure_geo()
    _ensure_session()
    prompt = _CONTEXT["session"].run_skill(skillname, params, source=_SOURCE).evaluate()
    return _CONTEXT["session"]


def get_session() -> "Session":
    return _CONTEXT["session"]


def get_api() -> SecurityCopilotAPIClient:
    """Get the currently configured SecurityCopilot API client."""
    _ensure_init()
    return _CONTEXT["apiclient"]


def get_geo() -> str:
    return _CONTEXT["geo_prefix"]


def _ensure_init():
    if not _CONTEXT["initialized"]:
        raise SecurityCopilotClientError(
            "Package is not yet initilized; run securitycopilot.init() first to begin"
        )


def _ensure_session():
    from ._model import Session

    if _CONTEXT["session"] is None:
        _CONTEXT["session"] = Session()

def _ensure_geo():
    if _CONTEXT["geo_prefix"] is None:
        raise SecurityCopilotClientError(
            "Geo region is not set; run securitycopilot.determine_geo() to set it or pass it to init()."
        )

def wait_for_response(sleeptime=3, markdown=False):
    while _CONTEXT["session"].is_prompt_pending:
        sleep(sleeptime)
        updates = _CONTEXT["session"].refresh()
        if updates is None:
            print("Working...")
        else:
            if markdown:
                from IPython.display import display_markdown
                display_markdown(_CONTEXT["session"].most_recent_prompt.last_completed_eval.content)
            else:
                print(
                    _CONTEXT["session"].most_recent_prompt.last_completed_eval.content
                )


class SecurityCopilotClientError(Exception):
    pass


from ._model import Session, Prompt, Evaluation
