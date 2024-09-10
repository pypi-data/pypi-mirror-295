from typing import Optional, List
from pydantic import BaseModel, Field
from .schemas import v1PreAuthKey
from .model import HSAPICall, formatTags


class v1ListPreAuthKeysResponse(BaseModel):
    preAuthKeys: Optional[List[Optional[v1PreAuthKey]]
                          ] = Field(alias="preAuthKeys", default=None)


class v1PreAuthKeyResponse(BaseModel):
    preAuthKey: Optional[v1PreAuthKey] = Field(
        alias="preAuthKey", default=None)


class v1ExpirePreAuthKeyRequest(BaseModel):
    user: str = Field(alias="user", default=None)
    key: str = Field(alias="key", default=None)


class v1CreatePreAuthKeyRequest(BaseModel):
    user: str = Field(alias="user", default=None)
    reusable: Optional[bool] = Field(alias="reusable", default=None)
    ephemeral: Optional[bool] = Field(alias="ephemeral", default=None)
    expiration: Optional[str] = Field(alias="expiration", default=None)
    aclTags: Optional[List[str]] = Field(alias="aclTags", default=None)


class v1ListPreAuthKeyRequest(BaseModel):
    user: Optional[str] = Field(
        alias="user", default=None)


class PreAuthKey(HSAPICall):

    objectPath = "preauthkey"

    def list(self, data: v1ListPreAuthKeyRequest) -> v1ListPreAuthKeysResponse:
        response = self.call('get', query=data.model_dump())
        return v1ListPreAuthKeysResponse(**response.json())

    def create(self, data: v1CreatePreAuthKeyRequest) -> v1PreAuthKeyResponse:
        data.aclTags = formatTags(data.aclTags)
        response = self.call('post', data=data)
        return v1PreAuthKeyResponse(**response.json())

    def expire(self, data: v1ExpirePreAuthKeyRequest) -> None:
        self.call('post',  data=data)
