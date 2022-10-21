from typing import (
    Optional,
    cast,
)
from argparse import (
    ArgumentParser,
    Namespace
)
from datetime import datetime

from azure.storage.blob import ContainerClient

from .base_storage import BaseStorage


class BlobStorage(BaseStorage):
    _container_client: Optional[ContainerClient]
    max_retention_days: int

    def __init__(self):
        self._container_client = None

    def quilla_addopts(self, parser: ArgumentParser):
        '''
        Adds the appropriate CLI arguments

        Args:
            parser: The Quilla argument parser
        '''
        az_group = parser.add_argument_group(
            title='Azure Blob Storage Options'
        )

        az_group.add_argument(
            '--connection-string',
            dest='connection_string',
            action='store',
            default=None,
            help='A connection string for the azure storage account to be used'
        )

        az_group.add_argument(
            '--container-name',
            dest='container_name',
            action='store',
            default='quilla',
            help='The name of the container that will be used for storing Quilla images'
        )

        az_group.add_argument(
            '--retention-days',
            dest='retention_days',
            type=int,
            default=30,
            help='The maximum number of days that reports should be allowed to exist. '
            'Reports older than this amount of days will be deleted. Set to -1 to let '
            'reports be kept indefinitely.'
        )

    def configure(
        self,
        connection_string: str,
        container_name: str,
        retention_days: int,
    ):
        '''
        Configure the container client and other necessary data, such as the max cleanup time.

        If a container with that name does not exist, it will be created.

        Args:
            connection_string: The full connection string to the storage account
            container_name: The name of the container that should be used to store all images
            retention_days: The maximum number of days a report should be allowed to have before
                being cleaned up
        '''
        client: ContainerClient = ContainerClient.from_connection_string(
            connection_string,
            container_name=container_name
        )

        self._container_client = client

        self.max_retention_days = retention_days
        try:
            if not client.exists():
                client.create_container()
        except Exception:
            self._container_client = None

    @property
    def container_client(self) -> ContainerClient:
        '''
        An instance of the container client, casting it to ContainerClient.

        This should be used exclusively from the abstract methods from BaseStorage

        Returns:
            The container client
        '''

        return cast(ContainerClient, self._container_client)

    def quilla_configure(self, args: Namespace):
        '''
        Configures the plugin to run

        Args:
            args: A namespace generated by parsing the args from the CLI
        '''
        if args.connection_string is None or args.connection_string == '':
            return

        self.configure(
            args.connection_string,
            args.container_name,
            args.retention_days,
        )

    @property
    def is_enabled(self) -> bool:
        return self._container_client is not None

    def find_image_by_baseline(self, baseline_id: str) -> bytes:
        blob = self.container_client.get_blob_client(f'baselines/{baseline_id}.png')

        if not blob.exists():
            return b''

        downloader = blob.download_blob()

        blob_data = downloader.readall()

        return blob_data

    def store_baseline_image(self, run_id: str, baseline_id: str, baseline: bytes) -> str:
        blob = self.container_client.get_blob_client(f'baselines/{baseline_id}.png')
        snapshot = self.container_client.get_blob_client(
            f'baselines/snapshots/{run_id}/{baseline_id}.png'
        )

        blob.upload_blob(baseline, overwrite=True)
        snapshot.upload_blob(baseline)

        return blob.url

    def store_treatment_image(self, run_id: str, baseline_id: str, treatment: bytes) -> str:
        blob = self.container_client.get_blob_client(f'runs/{run_id}/{baseline_id}_treatment.png')
        blob.upload_blob(treatment)

        return blob.url

    def make_baseline_uri(self, run_id: str, baseline_id: str) -> str:
        baseline_data = self.find_image_by_baseline(baseline_id)
        blob = self.container_client.get_blob_client(f'runs/{run_id}/{baseline_id}.png')

        blob.upload_blob(baseline_data)

        return blob.url

    def cleanup_reports(self):
        blobs = self.container_client.list_blobs()
        current_time = datetime.now()

        for blob in filter(lambda x: 'runs' in x.name, blobs):
            time_created: datetime = datetime.fromtimestamp(blob.creation_time.timestamp())

            delta = current_time - time_created
            if self.max_retention_days > -1 and delta.days > self.max_retention_days:
                blob_client = self.container_client.get_blob_client(blob)
                blob_client.delete_blob()
