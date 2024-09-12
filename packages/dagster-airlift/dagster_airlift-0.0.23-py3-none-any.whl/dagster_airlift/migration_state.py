from pathlib import Path
from typing import Any, Dict, NamedTuple, Optional, Sequence

import yaml


class TaskMigrationState(NamedTuple):
    task_id: str
    migrated: bool

    @staticmethod
    def from_dict(task_dict: Dict[str, Any]) -> "TaskMigrationState":
        if set(task_dict.keys()) != {"id", "migrated"}:
            raise Exception(
                f"Expected 'migrated' and 'id' keys in the task dictionary. Found keys: {task_dict.keys()}"
            )
        if task_dict["migrated"] not in [True, False]:
            raise Exception("Expected 'migrated' key to be a boolean")
        return TaskMigrationState(task_id=task_dict["id"], migrated=task_dict["migrated"])

    def to_dict(self) -> Dict[str, Any]:
        return {"id": self.task_id, "migrated": self.migrated}


class DagMigrationState(NamedTuple):
    tasks: Dict[str, TaskMigrationState]

    @staticmethod
    def from_dict(dag_dict: Dict[str, Sequence[Dict[str, Any]]]) -> "DagMigrationState":
        if "tasks" not in dag_dict:
            raise Exception(
                f"Expected a 'tasks' key in the dag dictionary. Instead; got: {dag_dict}"
            )
        task_list = dag_dict["tasks"]
        task_migration_states = {}
        for task_dict in task_list:
            task_state = TaskMigrationState.from_dict(task_dict)
            task_migration_states[task_state.task_id] = task_state
        return DagMigrationState(tasks=task_migration_states)

    def to_dict(self) -> Dict[str, Sequence[Dict[str, Any]]]:
        return {"tasks": [task_state.to_dict() for task_state in self.tasks.values()]}

    def is_task_migrated(self, task_id: str) -> bool:
        if task_id not in self.tasks:
            return False
        return self.tasks[task_id].migrated


class AirflowMigrationState(NamedTuple):
    dags: Dict[str, DagMigrationState]

    def get_migration_state_for_task(self, *, dag_id: str, task_id: str) -> Optional[bool]:
        if dag_id not in self.dags:
            return None
        if task_id not in self.dags[dag_id].tasks:
            return None
        return self.dags[dag_id].tasks[task_id].migrated

    def dag_has_migration_state(self, dag_id: str) -> bool:
        return self.get_migration_dict_for_dag(dag_id) is not None

    def get_migration_dict_for_dag(
        self, dag_id: str
    ) -> Optional[Dict[str, Sequence[Dict[str, Any]]]]:
        if dag_id not in self.dags:
            return None
        return {
            "tasks": [
                {"migrated": task_state.migrated, "id": task_id}
                for task_id, task_state in self.dags[dag_id].tasks.items()
            ]
        }

    @staticmethod
    def from_dict(migration_dict: Dict[str, Any]) -> "AirflowMigrationState":
        dags = {}
        for dag_id, dag_dict in migration_dict.items():
            dags[dag_id] = DagMigrationState.from_dict(dag_dict)
        return AirflowMigrationState(dags=dags)


class MigrationStateParsingError(Exception):
    pass


def load_migration_state_from_yaml(migration_yaml_path: Path) -> AirflowMigrationState:
    # Expect migration_yaml_path to be a directory, where each file represents a dag, and each
    # file in the subdir represents a task. The dictionary for each task should contain two keys;
    # id: the task id, and migrated: a boolean indicating whether the task has been migrated.
    dag_migration_states = {}
    try:
        for dag_file in migration_yaml_path.iterdir():
            # Check that the file is a yaml file or yml file
            if dag_file.suffix not in [".yaml", ".yml"]:
                continue
            dag_id = dag_file.stem
            yaml_dict = yaml.safe_load(dag_file.read_text())
            if not isinstance(yaml_dict, dict):
                raise Exception("Expected a dictionary")
            dag_migration_states[dag_id] = DagMigrationState.from_dict(yaml_dict)
    except Exception as e:
        raise MigrationStateParsingError("Error parsing migration yaml") from e
    return AirflowMigrationState(dags=dag_migration_states)
