from typing import Optional

from anyscale._private.sdk.base_sdk import BaseSDK
from anyscale.client.openapi_client.models import Dataset


def upload(
    dataset_file: str,
    name: str,
    *,
    description: Optional[str] = None,
    cloud: Optional[str] = None,
    project: Optional[str] = None,
) -> Dataset:
    """Uploads a dataset, or a new version of a dataset, to your Anyscale cloud.

    :param dataset_file: Path to the dataset file to upload.
    :param name: Name of a new dataset, or an existing dataset, to upload a new version of.
    :param description: Description of the dataset version.
    :param cloud: Name of the Anyscale cloud to upload a new dataset to. If not provided, the default cloud will be used.
    :param project: Name of the Anyscale project to upload a new dataset to. If not provided, the default project of the cloud will be used.

    Example usage:
    ```python
    anyscale.llm.dataset.upload("path/to/my_first_dataset.jsonl", name="my_first_dataset")
    anyscale.llm.dataset.upload("my_dataset.jsonl", "second_dataset.jsonl")
    anyscale.llm.dataset.upload("my_dataset2.jsonl", "second_dataset.jsonl", description="added 3 lines")
    ```
    :return: The `Dataset` object representing the uploaded dataset.

    NOTE:
    If you are uploading a new version, have run this from within an Anyscale workspace,
    and neither `cloud` nor `project` are provided, the cloud and project of the workspace will be used.
    """
    _sdk = BaseSDK()
    dataset = _sdk.client.upload_dataset(
        dataset_file, name, description, cloud, project,
    )
    return dataset


def download(
    name: str, version: Optional[int] = None, project: Optional[str] = None
) -> bytes:
    """Downloads a dataset from your Anyscale cloud.

    :param name: Name of the dataset to download.
    :param version: Version of the dataset to download. If a negative integer is provided, the dataset returned is this many versions back of the latest version. Default: Latest version.
    :param project: Name of the Anyscale project to download the dataset from. If not provided, all projects will be searched.

    Example usage:
    ```python
    dataset_contents = anyscale.llm.dataset.download("my_first_dataset.jsonl")
    jsonl_obj = [json.loads(line) for line in dataset_contents.decode().splitlines()]

    prev_dataset_contents = anyscale.llm.dataset.download("my_first_dataset.jsonl", version=-1)
    ```
    :return: The contents of the dataset file.
    """
    _sdk = BaseSDK()
    dataset_bytes = _sdk.client.download_dataset(name, version, project)
    return dataset_bytes
