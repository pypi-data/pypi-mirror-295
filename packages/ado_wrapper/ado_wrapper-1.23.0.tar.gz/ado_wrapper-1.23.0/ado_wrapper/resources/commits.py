from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING, Any, Literal

from ado_wrapper.resources.users import Member
from ado_wrapper.state_managed_abc import StateManagedResource
from ado_wrapper.errors import InvalidPermissionsError
from ado_wrapper.utils import from_ado_date_string

# from ado_wrapper.resources.branches import Branch

if TYPE_CHECKING:
    from ado_wrapper.client import AdoClient

CommitChangeType = Literal["edit", "add", "delete"]
FIRST_COMMIT_ID = "0000000000000000000000000000000000000000"  # I don't know why this works, but it does, please leave it.


def get_commit_body_template(
    old_object_id: str | None, updates: dict[str, str], branch_name: str, change_type: CommitChangeType, commit_message: str
) -> dict[str, Any]:  # fmt: skip
    return {
        "refUpdates": [
            {
                "name": f"refs/heads/{branch_name}",
                "oldObjectId": old_object_id or FIRST_COMMIT_ID,
            },
        ],
        "commits": [
            {
                "comment": commit_message,
                "changes": [
                    {
                        "changeType": change_type,
                        "item": {
                            "path": path,
                        },
                        "newContent": {
                            "content": new_content_body,
                            "contentType": "rawtext",
                        },
                    }
                    for path, new_content_body in updates.items()
                ],
            }
        ],
    }


@dataclass
class Commit(StateManagedResource):
    """
    https://learn.microsoft.com/en-us/rest/api/azure/devops/git/commits?view=azure-devops-rest-7.1
    https://learn.microsoft.com/en-us/rest/api/azure/devops/git/pushes?view=azure-devops-rest-7.1
    """

    commit_id: str = field(metadata={"is_id_field": True})  # None are editable
    author: Member
    date: datetime
    message: str

    def __str__(self) -> str:
        return f"{self.commit_id} by {self.author!s} on {self.date}\n{self.message}"

    @classmethod
    def from_request_payload(cls, data: dict[str, Any]) -> "Commit":
        member = Member(data["author"]["name"], data["author"].get("email", "BOT USER"), "UNKNOWN")
        return cls(data["commitId"], member, from_ado_date_string(data["author"]["date"]), data["comment"])

    @classmethod
    def get_by_id(cls, ado_client: "AdoClient", repo_id: str, commit_id: str) -> "Commit":
        return super()._get_by_url(
            ado_client,
            f"/{ado_client.ado_project_name}/_apis/git/repositories/{repo_id}/commits/{commit_id}?api-version=7.1",
        )

    @classmethod
    def create(
        cls, ado_client: "AdoClient", repo_id: str, from_branch_name: str, to_branch_name: str, updates: dict[str, str], change_type: CommitChangeType, commit_message: str,  # fmt: skip
    ) -> "Commit":
        """Creates a commit in the given repository with the given updates and returns the commit object.
        Takes a branch to get the latest commit from (and to update), and a to_branch to fork to."""
        assert not (
            from_branch_name.startswith("refs/heads/") or to_branch_name.startswith("refs/heads/")
        ), "Branch names should not start with 'refs/heads/'"
        #
        # existing_branches = Branch.get_all_by_repo(ado_client, repo_id)
        # if to_branch_name not in [x.name for x in existing_branches]:
        #     ado_client.state_manager.add_resource_to_state("Branch", to_branch_name, {})
        #
        if not updates:
            raise ValueError("No updates provided! It's not possible to create a commit without updates.")
        latest_commit = cls.get_latest_by_repo(ado_client, repo_id, from_branch_name)
        latest_commit_id = None if latest_commit is None else latest_commit.commit_id
        data = get_commit_body_template(latest_commit_id, updates, to_branch_name, change_type, commit_message)
        request = ado_client.session.post(
            f"https://dev.azure.com/{ado_client.ado_org_name}/{ado_client.ado_project_name}/_apis/git/repositories/{repo_id}/pushes?api-version=7.1",
            json=data,
        )
        if request.status_code == 400:
            raise ValueError("The commit was not created successfully, the file(s) you're trying to add might already exist there.")
        if request.status_code == 403:
            raise InvalidPermissionsError("You do not have permission to create a commit in this repo (possibly due to main branch protections)")  # fmt: skip
        if not request.json().get("commits"):
            raise ValueError("The commit was not created successfully.\nError:", request.json())
        return cls.from_request_payload(request.json()["commits"][-1])

    @staticmethod
    def delete_by_id(ado_client: "AdoClient", commit_id: str) -> None:
        raise NotImplementedError

    # ============ End of requirement set by all state managed resources ================== #
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    # =============== Start of additional methods included with class ===================== #

    @classmethod
    def get_latest_by_repo(cls, ado_client: "AdoClient", repo_id: str, branch_name: str | None = None) -> "Commit":
        return max(cls.get_all_by_repo(ado_client, repo_id, branch_name), key=lambda commit: commit.date)

    @classmethod
    def get_all_by_repo(cls, ado_client: "AdoClient", repo_id: str, branch_name: str | None = None) -> "list[Commit]":
        """Returns a list of all commits in the given repository."""
        extra_query = (f"searchCriteria.itemVersion.version={branch_name}&searchCriteria.itemVersion.versionType={'branch'}&"
                       if branch_name is not None else "")  # fmt: skip
        return super()._get_all(
            ado_client,
            f"/{ado_client.ado_project_name}/_apis/git/repositories/{repo_id}/commits?{extra_query}api-version=7.1",
        )  # pyright: ignore[reportReturnType]

    @classmethod
    def add_initial_readme(cls, ado_client: "AdoClient", repo_id: str) -> "Commit":
        default_commit_body = get_commit_body_template(None, {}, "main", "add", "")
        default_commit_body["commits"] = [{
            "comment": "Add README.md",
            "changes": [{
                "changeType": 1, "item": {"path": "/README.md"},
                "newContentTemplate": {"name": "README.md", "type": "readme"}
            }],
        }]  # fmt: skip
        request = ado_client.session.post(
            f"https://dev.azure.com/{ado_client.ado_org_name}/{ado_client.ado_project_name}/_apis/git/repositories/{repo_id}/pushes?api-version=7.1",
            json=default_commit_body,
        )
        return cls.from_request_payload(request.json()["commits"][0])

    # @classmethod
    # def roll_back_to_commit(cls, ado_client: "AdoClient", repo_id: str, commit_id: str, branch_name: str) -> None:
    #     PAYLOAD = {
    #         "generatedRefName": f"refs/heads/{commit_id}[:8]-revert-from-main",
    #         "ontoRefName": f"refs/heads/{branch_name}",
    #         "source": {"commitList": [{"commitId": commit_id}]}}
    #         # "repository": {
    #         #     "id": repo_id,
    #         #     "name": "repo_name",
    #         #     "project": {"id": ado_client.ado_project_id, "name": ado_client.ado_project_name, "state": 1, "revision":399,
    #         #                 "visibility":0,"lastUpdateTime":"2024-02-06T14:14:30.360Z"
    #         #     },
    #         # },
    #     request = ado_client.session.post(
    #         f"https://dev.azure.com/{ado_client.ado_org_name}/{ado_client.ado_project_id}/_apis/git/repositories/{repo_id}/reverts",
    #         json=PAYLOAD
    #     )
    #     if request.status_code != 201:
    #         raise UnknownError("Could not rollback commit.")
    #     revert_get_request = ado_client.session.get(
    #         f"https://dev.azure.com/{ado_client.ado_org_name}/{ado_client.ado_project_id}/_apis/git/repositories/{repo_id}/reverts/{request.json()['revertId']}"
    #     ).json()
    #     if revert_get_request["status"] == 4 or revert_get_request["detailedStatus"]["conflict"]:
    #         raise UnknownError("Error, there was a detected conflict and therefore could not complete.")
