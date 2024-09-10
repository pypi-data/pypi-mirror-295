import json
from pathlib import Path
from typing import Dict, List

import argilla as rg
import typer
from typing_extensions import Annotated

app = typer.Typer()


def load_prompt_file(prompt_file: Path) -> List[Dict[str, str]]:
    with open(prompt_file, "r") as f:
        prompts_and_answers: List[Dict[str, str]] = json.load(f)

        return prompts_and_answers


def workspace_exists(workspace_name: str, client: rg.Argilla) -> bool:
    workspace = client.workspaces(name=workspace_name)

    if workspace:
        return True

    return False


def dataset_exists(
    dataset_name: str, workspace_name: str, client: rg.Argilla
) -> bool:
    dataset = client.datasets(name=dataset_name, workspace=workspace_name)

    if dataset:
        return True

    return False


def get_dataset(
    workspace_name: str, dataset_name: str, client: rg.Argilla
) -> rg.Dataset:
    dataset = client.datasets(name=dataset_name, workspace=workspace_name)

    return dataset


def create_records(
    prompts_and_answers: List[Dict[str, str]]
) -> List[rg.Record]:
    records = []
    for prompt in prompts_and_answers:
        record = rg.Record(
            id=int(prompt["instance_id"]),
            fields={
                "prompt": prompt["prompt"],
                "answer_a": prompt["answer_A"],
                "answer_b": prompt["answer_B"],
            },
            metadata={
                "lang": prompt["lang"],
                "model_A": prompt["model_A"],
                "model_B": prompt["model_B"],
            },
        )
        records.append(record)

    return records


@app.command()
def main(
    api_url: Annotated[str, typer.Option(help="A/B testing platform URL")],
    api_key: Annotated[str, typer.Option(help="API key for testing platform")],
    prompt_file: Annotated[
        str,
        typer.Option(
            help="Name of prompts file to send to the A/B testing platform"
        ),
    ],
    workspace_name: Annotated[
        str,
        typer.Option(
            help="Name of the workspace in the Argilla A/B testing platform"
        ),
    ],
    dataset_name: Annotated[
        str, typer.Option(help="Dataset to add prompts to")
    ],
) -> None:
    """
    Send prompts that need annotations to the A/B testing platform.
    Make sure WORKSPACE_NAME and DATASET_NAME already exist on the
    platform!
    """
    prompt_file_path = Path(prompt_file)

    client = rg.Argilla(api_url=api_url, api_key=api_key)

    if not workspace_exists(workspace_name, client):
        raise ValueError(f"Workspace does not exist: {workspace_name}")

    if not dataset_exists(dataset_name, workspace_name, client):
        raise ValueError(f"Dataset does not exist: {dataset_name}")

    prompts_and_answers = load_prompt_file(prompt_file_path)
    records = create_records(prompts_and_answers)
    dataset = get_dataset(workspace_name, dataset_name, client)
    dataset.records.log(records)
