import sys
from .opr_poetry import PoetryVersionBumper
from .opr_uv import UVVersionBumper


def bump():
    arg = sys.argv[1]
    match arg:
        case "poetry":
            b = PoetryVersionBumper()
        case "uv":
            b = UVVersionBumper()
        case _:
            print("pick either uv or poetry")
            sys.exit(1)
    b()
