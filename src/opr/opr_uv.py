from .bump_version import VersionBumper
from .release_new_version import PackageReleaser
import tomlkit as t
from ._cmd import run_cmd


class UVVersionBumper(VersionBumper):
    def __init__(self):
        def run(*args):
            return run_cmd("uv", "run", *args)

        super().__init__(run, run_cmd)

    def _find_old_version(self):
        with open("pyproject.tml", "rb") as f:
            self._config = t.load(f)
        self._old_version = self._config.get("version")

    def _bump_version(self):
        self._config.add("version", self._new_version)
        with open("pyproject.toml", "w") as f:
            t.dump(self._config, f)


class UVPackageReleaser(PackageReleaser):
    def __init__(self):
        super().__init__(UVVersionBumper())

    def _build(self):
        run_cmd("uv", "build")

    def _publish(self):
        run_cmd("uv", "publish")
