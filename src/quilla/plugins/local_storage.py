'''
A plugin to add LocalStorage functionality for the VisualParity plugin.
'''


from argparse import (
    ArgumentParser,
    Namespace,
)
from pathlib import Path
from typing import (
    Optional,
    cast
)

from .base_storage import BaseStorage


class LocalStorage(BaseStorage):
    baseline_directory: Optional[Path]
    runs_directory: Optional[Path]

    def __init__(
        self,
        storage_directory: Optional[str] = None
    ):
        if storage_directory is None:
            self.baseline_directory = None
            self.runs_directory = None
            return

        self.configure(storage_directory)

    def configure(self, storage_directory: str):
        '''
        Initialize all the required data
        '''
        baseline_path = Path(storage_directory)
        self.baseline_directory = baseline_path / 'baselines'
        self.runs_directory = baseline_path / 'runs'
        self.runs_directory.mkdir(exist_ok=True)
        self.baseline_directory.mkdir(exist_ok=True)

    @property
    def is_enabled(self) -> bool:
        return self.baseline_directory is not None

    def run_path(self, run_id: str) -> Path:
        path = cast(Path, self.runs_directory) / run_id

        path.mkdir(exist_ok=True)

        return path

    def store_baseline_image(self, run_id: str, baseline_id: str, baseline: bytes) -> str:
        baseline_path = cast(Path, self.baseline_directory) / f'{baseline_id}.png'

        snapshot_path = baseline_path.parent / 'snapshots' / f'{baseline_id}_{run_id}.png'

        snapshot_path.parent.mkdir(exist_ok=True)

        baseline_path.touch()

        baseline_path.write_bytes(baseline)

        snapshot_path.touch()
        snapshot_path.write_bytes(baseline)

        return baseline_path.absolute().as_uri()

    def store_treatment_image(
        self,
        run_id: str,
        baseline_id: str,
        treatment: bytes
    ) -> str:

        run_path = self.run_path(run_id)

        image_path = run_path / f'{baseline_id}_treatment.png'

        image_path.write_bytes(treatment)

        return image_path.absolute().as_uri()

    def find_image_by_baseline(self, baseline_id: str) -> bytes:
        image_path = cast(Path, self.baseline_directory) / f'{baseline_id}.png'

        if not image_path.exists():
            return b''

        return image_path.read_bytes()

    def make_baseline_uri(self, run_id: str, baseline_id: str) -> str:
        image_data = self.find_image_by_baseline(baseline_id)

        run_path = self.run_path(run_id)

        image_path = run_path / f'{baseline_id}.png'

        image_path.touch()

        image_path.write_bytes(image_data)

        return image_path.absolute().as_uri()

    def cleanup_reports(self):
        '''
        Method left blank, as no cleanup is provided for LocalStorage since
        users are expected to have granular control over their own filesystems
        '''

    def quilla_addopts(self, parser: ArgumentParser):
        '''
        Using the Quilla hook to add a new group of CLI args to the parser
        '''

        ls_group = parser.add_argument_group(title='Local Storage Options')

        ls_group.add_argument(
            '--image-directory',
            dest='image_dir',
            action='store',
            default=None,
            help='The directory that should be used for the LocalStorage '
            'plugin to store VisualParity images'
        )

    def quilla_configure(self, args: Namespace):
        if args.image_dir is not None:
            self.configure(args.image_dir)
