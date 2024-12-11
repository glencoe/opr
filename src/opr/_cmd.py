from subprocess import PIPE, Popen


def run_cmd(*cmd) -> str:
    """run a command, capture its output as string and print it to stdout"""
    buff = []
    print("running:", " ".join(cmd))
    with Popen(cmd, stdout=PIPE, universal_newlines=True, bufsize=1) as p:
        for line in p.stdout:  # type: ignore
            buff.append(line)
    return "".join(buff)
