"""Definitions for ansible-creator init action."""

from __future__ import annotations

import shutil
import uuid

from pathlib import Path
from typing import TYPE_CHECKING

from ansible_creator.exceptions import CreatorError
from ansible_creator.templar import Templar
from ansible_creator.types import TemplateData
from ansible_creator.utils import Copier


if TYPE_CHECKING:

    from ansible_creator.config import Config
    from ansible_creator.output import Output


class Init:
    """Class representing ansible-creator init subcommand.

    Attributes:
        common_resources: List of common resources to copy.
    """

    common_resources = (
        "common.devcontainer",
        "common.devfile",
        "common.gitignore",
        "common.vscode",
    )

    def __init__(
        self: Init,
        config: Config,
    ) -> None:
        """Initialize the init action.

        Args:
            config: App configuration object.
        """
        self._namespace: str = config.namespace
        self._collection_name = config.collection_name or ""
        self._init_path: Path = Path(config.init_path)
        self._force = config.force
        self._creator_version = config.creator_version
        self._project = config.project
        self._scm_org = config.scm_org or ""
        self._scm_project = config.scm_project or ""
        self._templar = Templar()
        self.output: Output = config.output

    def run(self: Init) -> None:
        """Start scaffolding skeleton."""
        self._construct_init_path()
        self.output.debug(msg=f"final collection path set to {self._init_path}")

        if self._init_path.exists():
            self.init_exists()
        self._init_path.mkdir(parents=True, exist_ok=True)

        if self._project == "collection":
            self._scaffold_collection()
        elif self._project == "ansible-project":
            self._scaffold_playbook()

    def _construct_init_path(self: Init) -> None:
        """Construct the init path based on project type."""
        if self._project == "ansible-project":
            return

        if (
            self._init_path.parts[-2:] == ("collections", "ansible_collections")
            and self._project == "collection"
            and isinstance(self._collection_name, str)
        ):
            self._init_path = self._init_path / self._namespace / self._collection_name

    def init_exists(self) -> None:
        """Handle existing init path.

        Raises:
            CreatorError: When init path is a file or not empty and --force is not provided.
        """
        # check if init_path already exists
        # init-path exists and is a file
        if self._init_path.is_file():
            msg = f"the path {self._init_path} already exists, but is a file - aborting"
            raise CreatorError(msg)
        if next(self._init_path.iterdir(), None):
            # init-path exists and is not empty, but user did not request --force
            if not self._force:
                msg = (
                    f"The directory {self._init_path} is not empty.\n"
                    f"You can use --force to re-initialize this directory."
                    f"\nHowever it will delete ALL existing contents in it."
                )
                raise CreatorError(msg)

            # user requested --force, re-initializing existing directory
            self.output.warning(
                f"re-initializing existing directory {self._init_path}",
            )
            try:
                shutil.rmtree(self._init_path)
            except OSError as e:
                err = f"failed to remove existing directory {self._init_path}: {e}"
                raise CreatorError(err) from e

    def unique_name_in_devfile(self) -> str:
        """Use project specific name in devfile.

        Returns:
            Unique name entry.
        """
        final_name: str
        if self._project == "collection":
            final_name = f"{self._namespace}.{self._collection_name}"
        if self._project == "ansible-project":
            final_name = f"{self._scm_org}.{self._scm_project}"
        final_uuid = str(uuid.uuid4())[:8]
        return f"{final_name}-{final_uuid}"

    def _scaffold_collection(self) -> None:
        """Scaffold a collection project."""
        self.output.debug(msg="started copying collection skeleton to destination")
        template_data = TemplateData(
            namespace=self._namespace,
            collection_name=self._collection_name,
            creator_version=self._creator_version,
            dev_file_name=self.unique_name_in_devfile(),
        )
        copier = Copier(
            resources=["collection_project", *self.common_resources],
            resource_id="collection_project",
            dest=self._init_path,
            output=self.output,
            templar=self._templar,
            template_data=template_data,
        )
        copier.copy_containers()

        self.output.note(
            f"collection {self._namespace}.{self._collection_name} "
            f"created at {self._init_path}",
        )

    def _scaffold_playbook(self: Init) -> None:
        """Scaffold a playbook project."""
        self.output.debug(msg="started copying ansible-project skeleton to destination")

        template_data = TemplateData(
            creator_version=self._creator_version,
            scm_org=self._scm_org,
            scm_project=self._scm_project,
            dev_file_name=self.unique_name_in_devfile(),
        )

        copier = Copier(
            resources=["playbook_project", *self.common_resources],
            resource_id="playbook_project",
            dest=self._init_path,
            output=self.output,
            templar=self._templar,
            template_data=template_data,
        )
        copier.copy_containers()

        self.output.note(
            f"ansible project created at {self._init_path}",
        )
