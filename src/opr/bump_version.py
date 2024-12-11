from abc import ABC, abstractmethod
from typing import Protocol
from ._cmd import run_cmd


class RunCmd(Protocol):
    def __call__(self, *args: str) -> str: ...


class VersionBumper(ABC):
    def __init__(self, run_cmd: RunCmd, run_sys_cmd: RunCmd):
        self._run = run_cmd
        self._run_sys = run_sys_cmd
        self._old_version = "0"
        self._new_version = "0"
        self.dry_run = False
        self._git_user = ""
        self._git_mail = ""

    def set_git_user(self, user_name: str, mail: str) -> None:
        self._git_user = user_name
        self._git_mail = mail

    def _configure_git(self) -> None:
        if self._git_user != "":
            self._run_sys("git", "config", "set", "user.name", self._git_user)
            self._run_sys("git", "config", "set", "user.email", self._git_mail)

    def __call__(self) -> None:
        self.bump_version_and_tag()

    def bump_version_and_tag(self) -> None:
        if self.dry_run:
            print("dry run")
        print("checking for uncommitted changes")
        self._check_for_uncommitted_changes()
        self._find_old_version()
        self._find_new_version()
        print(f"updating from {self._old_version} to {self._new_version}")
        print("creating changelog")
        self._write_changelog()
        print("updating version")
        if not self.dry_run:
            self._bump_version()
            print("creating bump commit")
            self._commit_changelog_and_pyproject()
            print("tagging new version")
            self._tag_version()
        else:
            print("commit and tagging skipped for dry run")

    def _write_changelog(self) -> None:
        cl = self._run("git-cliff", "--bump")
        if self.dry_run:
            print(cl)
        else:
            with open("CHANGELOG.md", "w") as f:
                f.write(cl)

    def _get_changed_files(self) -> list[str]:
        """
        output from git status is

        ```
             M file.txt
            ?? other.txt
             A more.txt
        ```
        """
        filelist = self._run_sys("git", "status", "-s").strip()
        files = filelist.splitlines()
        changed = []

        def has_changed(line):
            return any(line.startswith(p) for p in ("M", "A"))

        for line in files:
            line = line.strip()
            if has_changed(line):
                changed.extend(line.split(" ", maxsplit=1))
        return changed

    @abstractmethod
    def _bump_version(self) -> None: ...

    @abstractmethod
    def _find_old_version(self) -> None: ...

    def _find_new_version(self) -> None:
        self._new_version = self._run("git-cliff", "--bumped-version").strip()

    def _commit_changelog_and_pyproject(self) -> None:
        run_cmd = self._run_sys
        run_cmd("git", "add", "CHANGELOG.md", "pyproject.toml")
        run_cmd(
            "git",
            "commit",
            "--no-verify",
            "-m",
            f"bump: {self._old_version} to {self._new_version}",
        )

    def _check_for_uncommitted_changes(self):
        changed_files = self._get_changed_files()
        if len(changed_files) > 0:
            raise Exception(
                "you have uncommitted changes, please stash or commit them before continuing."
            )

    def _tag_version(self) -> None:
        run_cmd("git", "tag", self._new_version)
