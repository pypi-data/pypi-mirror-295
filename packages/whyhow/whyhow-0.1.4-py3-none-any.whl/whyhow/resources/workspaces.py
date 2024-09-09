"""Workspaces resource."""

from typing import AsyncIterator, Iterator

from whyhow.raw import (
    acreate_workspace,
    adelete_workspace,
    aget_all_workspaces,
    aget_workspace,
    aupdate_workspace,
    create_workspace,
    delete_workspace,
    get_all_workspaces,
    get_workspace,
    update_workspace,
)
from whyhow.resources.base import AsyncResource, Resource, validate
from whyhow.schemas import Workspace


class WorkspacesResource(Resource):
    """Workspaces resource."""

    def get(self, workspace_id: str) -> Workspace:
        """Get a workspaces.

        Parameters
        ----------
        workspace_id : str
            The workspace ID.

        Returns
        -------
        Workspace
            The workspace.
        """
        result = get_workspace(self.client, workspace_id)
        body = validate(result)

        workspace = Workspace(
            workspace_id=body.workspaces[0].field_id,
            name=body.workspaces[0].name,
            created_at=body.workspaces[0].created_at,
            updated_at=body.workspaces[0].updated_at,
        )

        return workspace

    def get_all(
        self, limit: int = 10, name: str | None = None
    ) -> Iterator[Workspace]:
        """Iterate over all workspaces.

        Parameters
        ----------
        limit : int, optional
            The maximum number of workspaces to fetch in each request.

        name : str, optional
            The name of the workspace to filter by.

        Yields
        ------
        Workspace
            A workspace.

        """
        skip = 0
        while True:
            result = get_all_workspaces(
                self.client, limit=limit, skip=skip, name=name
            )
            body = validate(result)

            for workspace in body.workspaces:
                skip += 1
                yield Workspace(
                    workspace_id=workspace.field_id,
                    name=workspace.name,
                    created_at=workspace.created_at,
                    updated_at=workspace.updated_at,
                )

            if len(body.workspaces) < limit:
                break

    def create(self, name: str) -> Workspace:
        """Create a workspace.

        Parameters
        ----------
        name : str
            The name of the workspace.

        Returns
        -------
        Workspace
            The created workspace.
        """
        result = create_workspace(self.client, name)
        body = validate(result)

        workspace = Workspace(
            workspace_id=body.workspaces[0].field_id,
            name=body.workspaces[0].name,
            created_at=body.workspaces[0].created_at,
            updated_at=body.workspaces[0].updated_at,
        )

        return workspace

    def update(self, workspace_id: str, name: str) -> Workspace:
        """Update a workspace.

        Parameters
        ----------
        workspace_id : str
            The workspace ID.
        name : str
            The new name for the workspace.

        Returns
        -------
        Workspace
            The updated workspace.
        """
        result = update_workspace(self.client, workspace_id, name)
        body = validate(result)

        workspace = Workspace(
            workspace_id=body.workspaces[0].field_id,
            name=body.workspaces[0].name,
            created_at=body.workspaces[0].created_at,
            updated_at=body.workspaces[0].updated_at,
        )

        return workspace

    def delete(self, workspace_id: str) -> Workspace:
        """Delete a workspace.

        Parameters
        ----------
        workspace_id : str
            The workspace ID.
        """
        result = delete_workspace(self.client, workspace_id)
        body = validate(result)

        workspace = Workspace(
            workspace_id=body.workspaces[0].field_id,
            name=body.workspaces[0].name,
            created_at=body.workspaces[0].created_at,
            updated_at=body.workspaces[0].updated_at,
        )

        return workspace


class AsyncWorkspacesResource(AsyncResource):
    """Workspaces resource."""

    async def get(self, workspace_id: str) -> Workspace:
        """Get a workspaces.

        Parameters
        ----------
        workspace_id : str
            The workspace ID.

        Returns
        -------
        Workspace
            The workspace.
        """
        result = await aget_workspace(self.client, workspace_id)
        body = validate(result)

        workspace = Workspace(
            workspace_id=body.workspaces[0].field_id,
            name=body.workspaces[0].name,
            created_at=body.workspaces[0].created_at,
            updated_at=body.workspaces[0].updated_at,
        )

        return workspace

    async def get_all(
        self, limit: int = 10, name: str | None = None
    ) -> AsyncIterator[Workspace]:
        """Iterate over all workspaces.

        Parameters
        ----------
        limit : int, optional
            The maximum number of workspaces to fetch in each request.

        name : str, optional
            The name of the workspace to filter by.

        Yields
        ------
        Workspace
            A workspace.

        """
        skip = 0
        while True:
            result = await aget_all_workspaces(
                self.client, limit=limit, skip=skip, name=name
            )
            body = validate(result)

            for workspace in body.workspaces:
                skip += 1
                yield Workspace(
                    workspace_id=workspace.field_id,
                    name=workspace.name,
                    created_at=workspace.created_at,
                    updated_at=workspace.updated_at,
                )

            if len(body.workspaces) < limit:
                break

    async def create(self, name: str) -> Workspace:
        """Create a workspace.

        Parameters
        ----------
        name : str
            The name of the workspace.

        Returns
        -------
        Workspace
            The created workspace.
        """
        result = await acreate_workspace(self.client, name)
        body = validate(result)

        workspace = Workspace(
            workspace_id=body.workspaces[0].field_id,
            name=body.workspaces[0].name,
            created_at=body.workspaces[0].created_at,
            updated_at=body.workspaces[0].updated_at,
        )

        return workspace

    async def update(self, workspace_id: str, name: str) -> Workspace:
        """Update a workspace.

        Parameters
        ----------
        workspace_id : str
            The workspace ID.
        name : str
            The new name for the workspace.

        Returns
        -------
        Workspace
            The updated workspace.
        """
        result = await aupdate_workspace(self.client, workspace_id, name)
        body = validate(result)

        workspace = Workspace(
            workspace_id=body.workspaces[0].field_id,
            name=body.workspaces[0].name,
            created_at=body.workspaces[0].created_at,
            updated_at=body.workspaces[0].updated_at,
        )

        return workspace

    async def delete(self, workspace_id: str) -> Workspace:
        """Delete a workspace.

        Parameters
        ----------
        workspace_id : str
            The workspace ID.
        """
        result = await adelete_workspace(self.client, workspace_id)
        body = validate(result)

        workspace = Workspace(
            workspace_id=body.workspaces[0].field_id,
            name=body.workspaces[0].name,
            created_at=body.workspaces[0].created_at,
            updated_at=body.workspaces[0].updated_at,
        )

        return workspace
