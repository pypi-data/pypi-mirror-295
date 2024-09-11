from __future__ import annotations

import shutil
import uuid
from abc import ABC, abstractmethod
from copy import deepcopy
from pathlib import Path
from typing import Any, Generic, Sequence, TypeVar

from rdagent.core.conf import RD_AGENT_SETTINGS

"""
This file contains the all the class about organizing the task in RD-Agent.
"""


class Task(ABC):
    @abstractmethod
    def get_task_information(self) -> str:
        """
        Get the task information string to build the unique key
        """


ASpecificTask = TypeVar("ASpecificTask", bound=Task)


class Workspace(ABC, Generic[ASpecificTask]):
    """
    A workspace is a place to store the task implementation. It evolves as the developer implements the task.
    To get a snapshot of the workspace, make sure call `copy` to get a copy of the workspace.
    """

    def __init__(self, target_task: ASpecificTask | None = None) -> None:
        self.target_task: ASpecificTask | None = target_task

    @abstractmethod
    def execute(self, *args: Any, **kwargs: Any) -> object | None:
        error_message = "execute method is not implemented."
        raise NotImplementedError(error_message)

    @abstractmethod
    def copy(self) -> Workspace:
        error_message = "copy method is not implemented."
        raise NotImplementedError(error_message)


ASpecificWS = TypeVar("ASpecificWS", bound=Workspace)


class WsLoader(ABC, Generic[ASpecificTask, ASpecificWS]):
    @abstractmethod
    def load(self, task: ASpecificTask) -> ASpecificWS:
        error_message = "load method is not implemented."
        raise NotImplementedError(error_message)


class FBWorkspace(Workspace):
    """
    File-based task workspace

    The implemented task will be a folder which contains related elements.
    - Data
    - Code Workspace
    - Output
        - After execution, it will generate the final output as file.

    A typical way to run the pipeline of FBWorkspace will be:
    (We didn't add it as a method due to that we may pass arguments into
    `prepare` or `execute` based on our requirements.)

    .. code-block:: python

        def run_pipeline(self, **files: str):
            self.prepare()
            self.inject_code(**files)
            self.execute()

    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.code_dict: dict[str, Any] = {}
        self.code_dict = (
            {}
        )  # The code injected into the folder, store them in the variable to reproduce the former result
        self.workspace_path: Path = RD_AGENT_SETTINGS.workspace_path / uuid.uuid4().hex

    @property
    def code(self) -> str:
        code_string = ""
        for file_name, code in self.code_dict.items():
            code_string += f"File: {file_name}\n{code}\n"
        return code_string

    def prepare(self) -> None:
        """
        Prepare the workspace except the injected code
        - Data
        - Documentation
            typical usage of `*args, **kwargs`:
                Different methods shares the same data. The data are passed by the arguments.
        """
        self.workspace_path.mkdir(parents=True, exist_ok=True)

    def inject_code(self, **files: str) -> None:
        """
        Inject the code into the folder.
        {
            <file name>: <code>
        }
        """
        self.prepare()
        for k, v in files.items():
            self.code_dict[k] = v
            with Path.open(self.workspace_path / k, "w") as f:
                f.write(v)

    def get_files(self) -> list[Path]:
        """
        Get the environment description.

        To be general, we only return a list of filenames.
        How to summarize the environment is the responsibility of the Developer.
        """
        return list(self.workspace_path.iterdir())

    def inject_code_from_folder(self, folder_path: Path) -> None:
        """
        Load the workspace from the folder
        """
        for file_path in folder_path.iterdir():
            if file_path.suffix in {".py", ".yaml"}:
                self.inject_code(**{file_path.name: file_path.read_text()})

    def copy(self) -> FBWorkspace:
        """
        copy the workspace from the original one
        """
        return deepcopy(self)

    def clear(self) -> None:
        """
        Clear the workspace
        """
        shutil.rmtree(self.workspace_path)
        self.code_dict = {}

    def execute(self) -> object | None:
        """
        Before each execution, make sure to prepare and inject code
        """
        self.prepare()
        self.inject_code(**self.code_dict)
        return None


ASpecificWSForExperiment = TypeVar("ASpecificWSForExperiment", bound=Workspace)
ASpecificWSForSubTasks = TypeVar("ASpecificWSForSubTasks", bound=Workspace)


class Experiment(ABC, Generic[ASpecificTask, ASpecificWSForExperiment, ASpecificWSForSubTasks]):
    """
    The experiment is a sequence of tasks and the implementations of the tasks after generated by the Developer.
    """

    def __init__(self, sub_tasks: Sequence[ASpecificTask]) -> None:
        self.sub_tasks = sub_tasks
        self.sub_workspace_list: list[ASpecificWSForSubTasks | None] = [None] * len(self.sub_tasks)
        self.based_experiments: Sequence[ASpecificWSForExperiment] = []
        self.result: object = None  # The result of the experiment, can be different types in different scenarios.
        self.experiment_workspace: ASpecificWSForExperiment | None = None


ASpecificExp = TypeVar("ASpecificExp", bound=Experiment)

TaskOrExperiment = TypeVar("TaskOrExperiment", Task, Experiment)


class Loader(ABC, Generic[TaskOrExperiment]):
    @abstractmethod
    def load(self, *args: Any, **kwargs: Any) -> TaskOrExperiment:
        err_msg = "load method is not implemented."
        raise NotImplementedError(err_msg)
