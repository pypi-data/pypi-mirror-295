from typing import Optional, List
from pydantic import BaseModel, Field, computed_field
from datetime import datetime, timezone, timedelta
from enum import Enum


class v1RegisterMethod(str, Enum):

    REGISTER_METHOD_UNSPECIFIED = "REGISTER_METHOD_UNSPECIFIED"
    REGISTER_METHOD_AUTH_KEY = "REGISTER_METHOD_AUTH_KEY"
    REGISTER_METHOD_CLI = "REGISTER_METHOD_CLI"
    REGISTER_METHOD_OIDC = "REGISTER_METHOD_OIDC"


class v1ApiKey(BaseModel):

    id: int = Field(alias="id", default=None)
    prefix: str = Field(alias="prefix", default=None)
    expiration: datetime = Field(alias="expiration", default=None)
    createdAt: datetime = Field(alias="createdAt", default=None)
    lastSeen: Optional[datetime] = Field(alias="lastSeen", default=None)

    @computed_field
    @property
    def expired(self) -> bool:
        tzinfo = timezone(timedelta(hours=0))  # UTC
        now = datetime.now(tzinfo)
        return self.expiration < now


class v1PreAuthKey(BaseModel):

    id: int = Field(alias="id", default=None)
    user: str = Field(alias="user", default=None)
    key: str = Field(alias="key", default=None)
    reusable: bool = Field(alias="reusable", default=True)
    ephemeral: bool = Field(alias="ephemeral", default=False)
    used: bool = Field(alias="used", default=None)
    expiration: datetime = Field(alias="expiration", default=None)
    createdAt: datetime = Field(alias="createdAt", default=None)
    aclTags: Optional[List[str]] = Field(alias="aclTags", default=None)

    @computed_field
    @property
    def expired(self) -> bool:
        tzinfo = timezone(timedelta(hours=0))  # UTC
        now = datetime.now(tzinfo)
        exptime = self.expiration < now
        expused = not self.reusable and self.used
        expephemereal = self.ephemeral and self.used
        return exptime or expused or expephemereal


class v1User(BaseModel):

    id: int = Field(alias="id", default=None)
    name: str = Field(alias="name", default=None)
    createdAt: datetime = Field(alias="createdAt", default=None)


class v1Node(BaseModel):
    """
    None model

    """

    id: int = Field(alias="id", default=None)
    machineKey: str = Field(alias="machineKey", default=None)
    nodeKey: str = Field(alias="nodeKey", default=None)
    discoKey: str = Field(alias="discoKey", default=None)
    ipAddresses: List[str] = Field(alias="ipAddresses", default=None)
    name: str = Field(alias="name", default=None)
    user: v1User = Field(alias="user", default=None)
    lastSeen: datetime = Field(alias="lastSeen", default=None)
    expiry: datetime = Field(alias="expiry", default=None)
    preAuthKey: Optional[v1PreAuthKey] = Field(
        alias="preAuthKey", default=None)

    createdAt: datetime = Field(alias="createdAt", default=None)
    registerMethod: Optional[v1RegisterMethod] = Field(
        alias="registerMethod", default=None)

    forcedTags: Optional[List[str]] = Field(alias="forcedTags", default=None)
    invalidTags: Optional[List[str]] = Field(alias="invalidTags", default=None)
    validTags: Optional[List[str]] = Field(alias="validTags", default=None)
    givenName: str = Field(alias="givenName", default=None)
    online: bool = Field(alias="online", default=None)

    @computed_field
    @property
    def expired(self) -> bool:
        tzinfo = timezone(timedelta(hours=0))  # UTC
        now = datetime.now(tzinfo)
        return self.expiry.year != 1 and self.expiry < now

    @computed_field
    @property
    def expireDate(self) -> Optional[int | datetime]:
        if self.expiry.year == 1:
            return 0
        return self.expiry


class v1Route(BaseModel):
    """
    None model

    """

    id: Optional[int] = Field(alias="id", default=None)
    node: v1Node = Field(alias="node", default=None)
    prefix: str = Field(alias="prefix", default=None)
    advertised: bool = Field(alias="advertised", default=None)
    enabled: bool = Field(alias="enabled", default=None)
    isPrimary: bool = Field(alias="isPrimary", default=None)
    createdAt: datetime = Field(alias="createdAt", default=None)
    updatedAt: datetime = Field(alias="updatedAt", default=None)
    deletedAt: Optional[datetime] = Field(alias="deletedAt", default=None)
