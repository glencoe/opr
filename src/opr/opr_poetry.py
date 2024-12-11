from .bump_version import VersionBumper
from ._cmd import run_cmd
from .release_new_version import PackageReleaser


class PoetryVersionBumper(VersionBumper):
    def __init__(self):
        def run_poetry(*args):
            return run_cmd("poetry", "run", *args)

        super().__init__(
            run_poetry,
            run_cmd,
        )

    def _find_old_version(self) -> None:
        version = self._run_sys("poetry", "version", "-s")
        version = version.strip()
        version = version.strip()
        self._old_version = version

    def _bump_version(self) -> None:
        self._run_sys("poetry", "version", self._new_version)


class PoetryPackageReleaser(PackageReleaser):
    def __init__(self):
        super().__init__(PoetryVersionBumper())

    def _build(self) -> None:
        run_cmd("poetry", "build")

    def _publish(self) -> None:
        run_cmd("poetry", "publish")


if __name__ == "__main__":
    r = PoetryPackageReleaser()
    r()
