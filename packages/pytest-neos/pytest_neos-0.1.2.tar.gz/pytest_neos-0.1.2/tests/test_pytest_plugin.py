from unittest import mock

import pytest

import pytest_neos
from neos_common import base, error
from neos_common.authorization.token import TokenData
from neos_common.authorization.util import ActionResource, DepAuthorizationFactory
from neos_common.authorization.validator import AccessValidator, SignatureValidator
from neos_common.base import ResourceBase
from neos_common.client.keycloak_client import KeycloakClient
from pytest_neos import _auth_patch_factory  # noqa: F401


class AsyncMock(mock.MagicMock):
    def __init__(self, *args, name=None, **kwargs) -> None:
        super().__init__(name, *args, **kwargs)
        self.__str__ = mock.MagicMock(return_value=name)

    async def __call__(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)


class Resource(ResourceBase):
    @classmethod
    def generate_from_config(cls, config, resource_type, **kwargs):  # noqa: ARG003
        return cls()

    @classmethod
    def get_resource_id_template(cls) -> str:
        return ""

    @classmethod
    def format_resource_id(cls, *args) -> str:  # noqa: ARG003
        return ""


async def test_auth_patch_factory(_auth_patch_factory):  # noqa: F811, PT019
    _auth_patch_factory("user", access_validator=AccessValidator, resources=["1", "2"])

    DepAuthorization = DepAuthorizationFactory.build(  # noqa: N806
        mock.Mock(),
        mock.Mock(),
        mock.Mock(),
        mock.Mock(),  # type: ignore[reportGeneralTypeIssues]
    )
    request = mock.Mock(headers={"Authorization": "Bearer token"})
    token = await DepAuthorization([ActionResource(base.Action.core_announce, "resource", Resource)])(
        request,
        KeycloakClient("host", "realm", "client_id", "client_secret"),
        "config",  # type: ignore[reportGeneralTypeIssues]
        "signature_validator",  # type: ignore[reportGeneralTypeIssues]
        AccessValidator("hub_client"),  # type: ignore[reportGeneralTypeIssues]
    )
    assert isinstance(token, TokenData)
    assert token.user_id == "user"
    assert token.resources == ["1", "2"]


async def test_auth_patch_factory_handles_edge_case_support(_auth_patch_factory):  # noqa: F811, PT019
    _auth_patch_factory("user", access_validator=AccessValidator, resources=None)
    DepAuthorization = DepAuthorizationFactory.build(  # noqa: N806
        mock.Mock(),
        mock.Mock(),
        mock.Mock(),
        mock.Mock(),  # type: ignore[reportGeneralTypeIssues]
    )

    request = mock.Mock(headers={"Authorization": "Bearer token"})
    token = await DepAuthorization([])(
        request,
        KeycloakClient("host", "realm", "client_id", "client_secret"),
        "config",  # type: ignore[reportGeneralTypeIssues]
        "signature_validator",  # type: ignore[reportGeneralTypeIssues]
        AccessValidator("hub_client"),  # type: ignore[reportGeneralTypeIssues]
    )
    assert isinstance(token, TokenData)
    assert token.user_id == "user"
    assert token.resources == []


async def test_auth_patch_factory_raises_for_none_resources(_auth_patch_factory):  # noqa: F811, PT019
    _auth_patch_factory("user", access_validator=AccessValidator, resources=None)
    DepAuthorization = DepAuthorizationFactory.build(  # noqa: N806
        mock.Mock(),
        mock.Mock(),
        mock.Mock(),
        mock.Mock(),  # type: ignore[reportGeneralTypeIssues]
    )

    request = mock.Mock(headers={"Authorization": "Bearer token"})
    with pytest.raises(error.InsufficientPermissionsError):
        await DepAuthorization([ActionResource(base.Action.core_announce, "resource", Resource)])(
            request,
            KeycloakClient("host", "realm", "client_id", "client_secret"),
            "config",  # type: ignore[reportGeneralTypeIssues]
            "signature_validator",  # type: ignore[reportGeneralTypeIssues]
            AccessValidator("hub_client"),  # type: ignore[reportGeneralTypeIssues]
        )


async def test_signed_auth_patch_factory(_auth_patch_factory):  # noqa: F811, PT019
    _auth_patch_factory("user", signature_validator=SignatureValidator, resources=["1", "2"])

    DepAuthorization = DepAuthorizationFactory.build(  # noqa: N806
        mock.Mock(),
        mock.Mock(),
        mock.Mock(),
        mock.Mock(),  # type: ignore[reportGeneralTypeIssues]
    )
    request = mock.Mock(headers={"Authorization": "NEOS4-HMAC-SHA256 token"})
    token = await DepAuthorization([ActionResource(base.Action.core_announce, "resource", Resource)])(
        request,
        KeycloakClient("host", "realm", "client_id", "client_secret"),
        "config",  # type: ignore[reportGeneralTypeIssues]
        SignatureValidator("hub_client"),  # type: ignore[reportGeneralTypeIssues]
        "access_validator",  # type: ignore[reportGeneralTypeIssues]
    )
    assert isinstance(token, TokenData)
    assert token.user_id == "user"
    assert token.resources == ["1", "2"]


async def test_signed_auth_patch_factory_raises_for_none_resources(_auth_patch_factory):  # noqa: F811, PT019
    _auth_patch_factory("user", signature_validator=SignatureValidator, resources=None)
    DepAuthorization = DepAuthorizationFactory.build(  # noqa: N806
        mock.Mock(),
        mock.Mock(),
        mock.Mock(),
        mock.Mock(),  # type: ignore[reportGeneralTypeIssues]
    )

    request = mock.Mock(headers={"Authorization": "NEOS4-HMAC-SHA256 token"})
    with pytest.raises(error.InsufficientPermissionsError):
        await DepAuthorization([ActionResource(base.Action.core_announce, "resource", Resource)])(
            request,
            KeycloakClient("host", "realm", "client_id", "client_secret"),
            "config",  # type: ignore[reportGeneralTypeIssues]
            SignatureValidator("hub_client"),  # type: ignore[reportGeneralTypeIssues]
            "access_validator",  # type: ignore[reportGeneralTypeIssues]
        )


@pytest.mark.parametrize("method", ["get", "put", "post", "delete", "request"])
async def test_bearer_web_client(method):
    web_client = AsyncMock(return_value="")

    c = pytest_neos.BearerWebClient(web_client)

    await getattr(c, method)()

    assert getattr(web_client, method).call_args == mock.call(headers={"authorization": "bearer token"})


@pytest.mark.parametrize("method", ["get", "put", "post", "delete", "request"])
async def test_global_web_client(method):
    web_client = AsyncMock(return_value="")

    c = pytest_neos.GlobalWebClient(web_client)

    await getattr(c, method)()

    assert getattr(web_client, method).call_args == mock.call(
        headers={"authorization": "bearer token", "x-account": "root", "x-partition": "ksa"},
    )
