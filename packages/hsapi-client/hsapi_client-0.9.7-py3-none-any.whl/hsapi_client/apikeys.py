from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from .model import HSAPICall
from .schemas import v1ApiKey


class v1CreateApiKeyRequest(BaseModel):
    expiration: str = Field(alias="expiration", default=None)


class v1ExpireApiKeyRequest(BaseModel):
    prefix: str = Field(alias="prefix", default=None)


class v1ListApiKeysResponse(BaseModel):
    apiKeys: Optional[List[Optional[v1ApiKey]]] = Field(
        alias="apiKeys", default=None)


class v1CreateApiKeyResponse(BaseModel):
    apiKey: str = Field(alias="apiKey", default=None)


class APIKey(HSAPICall):

    objectPath = "apikey"

    def list(self) -> v1ListApiKeysResponse:
        response = self.call('get')
        return v1ListApiKeysResponse(**response.json())

    def create(self, data: v1CreateApiKeyRequest) -> v1CreateApiKeyResponse:
        response = self.call('post', data=data)
        return v1CreateApiKeyResponse(**response.json())

    def expire(self, data: v1ExpireApiKeyRequest) -> None:
        self.call('post', call_path='expire', data=data)

    def delete(self, prefix: str) -> None:
        self.call('delete', call_path=prefix)
