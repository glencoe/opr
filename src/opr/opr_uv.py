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
        self._run_sys("pwd")
        with open("pyproject.toml", "rb") as f:
            self._config = t.load(f)
        self._old_version = self._config["project"]["version"]

    def _match_old_version_style(self) -> None:
        if self._old_version.startswith("v") and not self._new_version.startswith("v"):
            self._new_version = f"v{self._new_version}"
        elif not self._old_version.startswith("v") and self._new_version.startswith(
            "v"
        ):
            self._new_version = self._new_version[1:]

    def _bump_version(self):
        self._match_old_version_style()
        self._config["project"]["version"] = self._new_version
        with open("pyproject.toml", "w") as f:
            t.dump(self._config, f)


class UVPackageReleaser(PackageReleaser):
    def __init__(self):
        super().__init__(UVVersionBumper())

    def _build(self):
        run_cmd("uv", "build")

    def _publish(self):
        run_cmd("uv", "publish")
