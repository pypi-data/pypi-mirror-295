from .model import HSAPICall, formatTags
from .schemas import v1Route, v1Node
from typing import Optional, List
from pydantic import BaseModel, Field


class v1SetTagsNodeRequest(BaseModel):
    tags: Optional[List[str]] = Field(alias="tags", default=None)

    def model_post_init(self, ctx):
        self.tags = formatTags(self.tags)


class v1MoveNodeRequest(BaseModel):
    user: Optional[str] = Field(alias="user", default=None)


class v1BackfillNodeIPsRequest(BaseModel):
    confirmed: Optional[bool] = Field(alias="confirmed", default=True)


class v1ListNodesResponse(BaseModel):
    nodes: Optional[List[Optional[v1Node]]] = Field(
        alias="nodes", default=None)


class v1NodeResponse(BaseModel):
    node: Optional[v1Node] = Field(alias="node", default=None)


class v1GetNodeRoutesResponse(BaseModel):
    routes: Optional[List[Optional[v1Route]]] = Field(
        alias="routes", default=None)


class v1BackfillNodeIPsResponse(BaseModel):
    changes: Optional[List[str]] = Field(alias="changes", default=None)


class Node(HSAPICall):

    objectPath = "node"

    def list(self) -> v1ListNodesResponse:
        response = self.call('get')
        return v1ListNodesResponse(**response.json())

    def get(self, nodeId: int) -> v1Node:
        # There is a bug in headscale API
        # retrieving a specific node does not return the tags
        # so we get the full list of nodes and extract the node with the
        # ID we want
        # response = self.call('get', call_path=nodeId)
        nodelist = self.list()
        node = next((n for n in nodelist.nodes if n.id == nodeId), v1Node())
        return node  # type: ignore

    def _get(self, nodeId: int) -> v1Node:
        # There is a bug in headscale API
        # retrieving a specific node does not return the tags
        # This does a real get
        node = self.call('get', call_path=nodeId)
        return v1Node(**node.json()['node'])

    def byUser(self, username: str) -> v1ListNodesResponse:
        nodelist = self.list()

        byUser = [n for n in nodelist.nodes if n.user.name == username]

        return v1ListNodesResponse(nodes=byUser)

    def delete(self, nodeId: int) -> None:
        self.call('delete', call_path=nodeId)

    def expire(self, nodeId: int) -> None:
        self.call('post', f'{nodeId}/expire')

    def rename(self, nodeId: int, newName: str) -> v1NodeResponse:
        response = self.call('post', f'{nodeId}/rename/{newName}')
        return v1NodeResponse(**response.json())

    def move(self, nodeId: int, data: v1MoveNodeRequest) -> v1NodeResponse:
        response = self.call('post', f'{nodeId}/user', data)
        return v1NodeResponse(**response.json())

    def routes(self, nodeId: int) -> v1GetNodeRoutesResponse:
        response = self.call('get', f'{nodeId}/routes')
        return v1GetNodeRoutesResponse(**response.json())

    def setTags(self, nodeId: int, data: v1SetTagsNodeRequest) -> v1NodeResponse:
        response = self.call('post', f'{nodeId}/tags', data)
        return v1NodeResponse(**response.json())

    # Broken on server
    def backfillips(self) -> v1BackfillNodeIPsResponse:
        response = self.call(
            'post', f'backfillips',
            query=dict(confirmed=True))
        return v1BackfillNodeIPsResponse(**response.json())
