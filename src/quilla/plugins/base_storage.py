'''
This module contains a base class that can be useful when defining new
storage plugins, as there are some behaviours that will be shared among
the configuration objects
'''

from abc import (
    ABC,
    abstractproperty,
    abstractmethod
)
from typing import (
    Optional
)

from quilla.common.enums import VisualParityImageType


class BaseStorage(ABC):
    @abstractproperty
    def is_enabled(self) -> bool:
        '''
        A property to be used to determine if the plugin is configured and
        therefore able to run

        Returns:
            True if the plugin is configured, False otherwise
        '''

    @abstractmethod
    def find_image_by_baseline(self, baseline_id: str) -> bytes:
        '''
        Searches the defined storage method for the image matching some
        baseline ID

        Args:
            baseline_id: The unique ID to search for. It is assumed every
                baseline ID is unique regardless of what test is requesting it.

        Returns:
            The bytes representation of the stored image if found, or an empty
            bytes object if the image is not found.
        '''

    @abstractmethod
    def cleanup_reports(self):
        '''
        Searches for reports that match some cleanup criteria
        '''

    @abstractmethod
    def store_treatment_image(
        self,
        run_id: str,
        baseline_id: str,
        treatment: bytes,
    ) -> str:
        '''
        Stores a treatment image within the storage mechanism enabled by the plugin

        Args:
            run_id: The run ID of the current Quilla run, to version the treatment images
            baseline_id: The ID of the baseline that this treatment image is associated
                with
            treatment: The image data in bytes

        Returns:
            An identifier that can locate the newly stored treatment image
        '''

    @abstractmethod
    def store_baseline_image(
        self,
        baseline_id: str,
        baseline: bytes,
    ) -> str:
        '''
        Stores a baseline image under the given baseline_id.

        This function should be used to update the current baseline
        image, or create a new one if the baseline did not previously exist

        Args:
            baseline_id: A unique identifier for the image
            baseline: The image data in bytes

        Returns:
            A URI for the new baseline image
        '''

    @abstractmethod
    def make_baseline_uri(
        self,
        run_id: str,
        baseline_id: str
    ) -> str:
        '''
        Generates a baseline URI for the current run given the baseline_id of the image.

        It is recommended that plugins create a clone of the baseline image
        when generating the URI so that the returned URI will uniquely identify
        the baseline that was used for the associated run ID. This ensures that
        even if the baseline image is updated, the report is still meaningful.

        Args:
            run_id: The unique ID identifying the current run
            baseline_id: The unique identifier for the image

        Returns:
            A URI that can locate the baseline image used for the given run
        '''

    def get_image(self, baseline_id: str) -> Optional[bytes]:
        '''
        Determines if the plugin should run, and if so searches for the image
        with the specified baseline ID and returns the byte data for it

        Args:
            baseline_id: The unique ID to search for

        Returns:
            None if the plugin is not enabled, a ``bytes`` representation
            of the image if it is. If no baseline image is found, returns an
            empty byte string
        '''
        if not self.is_enabled:
            return None

        return self.find_image_by_baseline(baseline_id)

    def get_baseline_uri(self, run_id: str, baseline_id: str) -> Optional[str]:
        '''
        Retrieves the URI for the baseline image

        Args:
            run_id: The unique ID for the current run of Quilla
            baseline_id: The unique ID for the baseline image

        Returns:
            None if the plugin is not enabled, a string URI if it is
        '''
        if not self.is_enabled:
            return None

        return self.make_baseline_uri(run_id, baseline_id)

    def store_image(
        self,
        run_id: str,
        baseline_id: str,
        image_data: bytes,
        image_type: VisualParityImageType
    ) -> Optional[str]:
        '''
        Stores a given image based on its type and possibly the run ID

        Args:
            run_id: The unique ID for the current Quilla run
            baseline_id: The unique identifier for the image
            image_data: The byte data for the image
            image_type: The kind of image that is being stored

        Returns:
            A URI for the image that was stored, or None if the plugin
            is not enabled. The URI might be the empty string if the
            image type is not supported
        '''

        if not self.is_enabled:
            return None

        image_uri = ''

        if image_type == VisualParityImageType.TREATMENT:
            image_uri = self.store_treatment_image(
                run_id,
                baseline_id,
                treatment=image_data
            )
        elif image_type == VisualParityImageType.BASELINE:
            image_uri = self.store_baseline_image(
                baseline_id,
                baseline=image_data,
            )

        self.cleanup_reports()

        return image_uri
