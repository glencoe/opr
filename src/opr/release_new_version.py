from .bump_version import VersionBumper
from abc import ABC, abstractmethod


class PackageReleaser(ABC):
    def __init__(self, bumper: VersionBumper) -> None:
        self._bumper = bumper

    @abstractmethod
    def _build(self) -> None: ...

    @abstractmethod
    def _publish(self) -> None: ...

    def __call__(self) -> None:
        self._build()
        self._publish()
