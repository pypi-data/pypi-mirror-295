from typing import Optional, List
from pydantic import BaseModel, Field
from .schemas import v1User
from .model import HSAPICall


class v1CreateUserRequest(BaseModel):
    name: str = Field(alias="name", default=None)


class v1ListUsersResponse(BaseModel):
    users: Optional[List[Optional[v1User]]] = Field(
        alias="users", default=None)


class v1UserResponse(BaseModel):
    user: Optional[v1User] = Field(alias="user", default=None)


class User(HSAPICall):

    objectPath = "user"

    def list(self) -> v1ListUsersResponse:
        response = self.call('get')
        return v1ListUsersResponse(**response.json())

    def get(self, name: str) -> v1UserResponse:
        response = self.call('get', call_path=name)
        return v1UserResponse(**response.json())

    def create(self, data: v1CreateUserRequest) -> v1UserResponse:
        response = self.call('post', data=data)
        return v1UserResponse(**response.json())

    def delete(self, name: str) -> None:
        self.call('delete',  name)

    def rename(self, oldName: str, newName: str) -> v1UserResponse:
        response = self.call('post',  call_path=f"{oldName}/rename/{newName}")
        return v1UserResponse(**response.json())
