import base64
import json
import os
from multiprocessing import Event
from multiprocessing.pool import ThreadPool
from pathlib import Path
from typing import Dict, List

import typer
from google.cloud import storage
from tqdm import tqdm
from typing_extensions import Annotated

from .md5_cache import cached_md5_hash

app = typer.Typer()

available_datasets: List[Dict[str, str]] = json.load(
    (Path(__file__).parent / "dataset_info.json").open("r")
)["datasets"]


def does_blob_match_uri(blob, destination_uri):
    local_md5_match = False
    if destination_uri.exists():
        with destination_uri.open("rb") as f:
            local_md5 = cached_md5_hash(destination_uri)
        blob_md5 = base64.b64decode(blob.md5_hash)
        local_md5_match = local_md5 == blob_md5
    return local_md5_match


class SingleDatasetDownloader:
    def __init__(self, root_dir: Path, dataset_name: str, interrupt_event):
        self.data_dir = root_dir / dataset_name
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.interrupt_event = interrupt_event
        self.dataset_version = next(
            ds["version"] for ds in available_datasets if ds["name"] == dataset_name
        )

        (self.data_dir / self.dataset_version).mkdir(parents=True, exist_ok=True)

        storage_client = storage.Client()
        bucket = storage_client.bucket("gresearch")

        self.remote_prefix = f"robotics/{dataset_name}/{self.dataset_version}"

        blobs = list(
            bucket.list_blobs(
                prefix=self.remote_prefix,
            )
        )
        self.blobs = [
            blob for blob in blobs if Path(blob.name).is_relative_to(self.remote_prefix)
        ]

        self.progress_bar = tqdm(
            total=sum(blob.size for blob in self.blobs),
            unit="B",
            unit_scale=True,
            desc=f"{dataset_name}",
        )

    def download_blobs(self):
        for blob in self.blobs:
            if self.interrupt_event.is_set():
                return

            destination_uri = self.data_dir / Path(blob.name).relative_to(
                self.remote_prefix
            )
            destination_uri.parent.mkdir(parents=True, exist_ok=True)

            if not does_blob_match_uri(blob, destination_uri):
                blob.download_to_filename(destination_uri)
                cached_md5_hash(destination_uri)

            # Make a symlink to the blob in the version directory
            version_symlink = (
                self.data_dir
                / self.dataset_version
                / Path(blob.name).relative_to(self.remote_prefix)
            )
            # Ensure the symlink is pointing to the correct destination
            # If the symlink already exists, it will be overwritten
            if version_symlink.exists():
                version_symlink.unlink()
            version_symlink.symlink_to(
                destination_uri.relative_to(version_symlink.parent, walk_up=True)
            )

            self.progress_bar.update(blob.size)


class MultiDatasetDownloader:
    def __init__(self, root_dir: Path, dataset_names: List[str]):
        self.root_dir = root_dir
        self.interrupt_event = Event()
        self.dataset_names = dataset_names
        self.downloaders = [
            SingleDatasetDownloader(root_dir, dataset_name, self.interrupt_event)
            for dataset_name in dataset_names
        ]

    def __len__(self):
        return len(self.downloaders)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Clean up downloaders
        self.close()

    def download_dataset(self, index: int):
        downloader = self.downloaders[index]
        downloader.download_blobs()
        return downloader

    def is_done(self):
        return self.downloader_iter

    def close(self):
        self.interrupt_event.set()
        self.downloaders = []


def autocomplete_dataset_names(incomplete: str):
    for ds in available_datasets:
        if ds["name"].startswith(incomplete):
            yield ds["name"]


@app.command()
def main(
    datasets: Annotated[
        List[str],
        typer.Option(
            "--dataset",
            "-d",
            help="List of dataset names to sync. If not provided, will sync all datasets.",
            autocompletion=autocomplete_dataset_names,
        ),
    ] = {ds["name"] for ds in available_datasets},
    local_base_path: Annotated[
        Path, typer.Option("--path", "-p", help="Base local path for syncing datasets")
    ] = "./oxe",
    max_workers: Annotated[
        int,
        typer.Option("--workers", "-w", help="Maximum number of concurrent downloads"),
    ] = os.cpu_count(),
):
    """
    Main function to handle dataset synchronization.
    """
    dataset_name_set = {ds["name"] for ds in available_datasets}
    dataset_names_to_sync = set(datasets)

    if not set(dataset_names_to_sync).issubset(dataset_name_set):
        invalid_datasets = set(dataset_names_to_sync) - dataset_name_set
        typer.echo(
            f"Error: The following datasets are not recognized: {', '.join(invalid_datasets)}"
        )
        raise typer.Exit(code=1)

    with MultiDatasetDownloader(
        Path(local_base_path), dataset_names_to_sync
    ) as multi_downloader, ThreadPool(max_workers) as threadpool:

        try:
            threadpool.map(
                multi_downloader.download_dataset,
                range(len(multi_downloader)),
            )
        except Exception as e:
            multi_downloader.close()
            threadpool.close()
            threadpool.join()
            # re-raise the exception to exit the program
            raise e

    typer.echo("All downloads completed.")


if __name__ == "__main__":
    app()
