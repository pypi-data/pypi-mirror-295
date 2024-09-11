from pydantic import BaseModel
from typing import Union, List
from pathlib import Path
from typing import Optional
from collections import defaultdict

from .StorageConfig import LocalStorageConfig, S3StorageConfig


class ScriptConfig(BaseModel):
    name: str
    run_on_start: bool = True
    command: Optional[str] = None
    run_every: Optional[int] = None  # seconds (in cloud minutes)
    storage: Optional[str] = None  # folder to bind in cloud
    type: str = "script"

    # make sure that at least run_on_start or run_every is set
    def __init__(self, **data):
        super().__init__(**data)
        if not self.run_on_start and not self.run_every:
            raise ValueError(
                f"Script {self.name} must have either run_on_start or run_every set."
            )


class NotebookConfig(BaseModel):
    name: str
    command: Union[str, None] = None
    storage: Union[str, None] = None  # folder to bind in cloud
    port: int = 8888
    host: str = "0.0.0.0"
    type: str = "notebook"


class APIConfig(BaseModel):
    name: str
    command: Union[str, None] = None
    port: int = 8000
    host: str = "0.0.0.0"
    storage: Union[str, None] = None  # folder to bind in cloud
    type: str = "api"


class UIConfig(BaseModel):
    name: str
    command: str  # steamlit, javascript, ...
    port: int = 3000
    host: str = "0.0.0.0"
    env: dict = {}  # can accept the name of another service as a url placeholder
    type: str = "ui"


class Config(BaseModel):
    dir: Path
    project: str
    scripts: List[ScriptConfig] = []
    notebooks: List[NotebookConfig] = []
    apis: List[APIConfig] = []
    uis: List[UIConfig] = []
    storage: List[Union[LocalStorageConfig, S3StorageConfig]] = []

    def __init__(self, **data):
        super().__init__(**data)

    # iterator for all the services
    def __iter__(self):
        # if self.storage:
        #     for storage in self.storage:
        #         yield storage
        if self.scripts:
            for script in self.scripts:
                yield script
        if self.notebooks:
            for notebook in self.notebooks:
                yield notebook
        if self.apis:
            for api in self.apis:
                yield api
        if self.uis:
            for ui in self.uis:
                yield ui
        if self.storage:
            for storage in self.storage:
                yield storage

    def type2folder(self, type):
        return type + "s"
