from subprocess import run as _srun


def run_cmd(cmd: list[str]) -> str:
    """run a command, capture its output as string and raise exception on non-zero exit"""
    result = _srun(cmd, capture_output=True, check=True, text=True)
    return result.stdout


def build():
    run_cmd(["poetry", "build"])


def publish():
    run_cmd(["poetry", "publish"])


if __name__ == "__main__":
    build()
    publish()
