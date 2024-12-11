from subprocess import PIPE, Popen, STDOUT


def run_cmd(*cmd) -> str:
    """run a command, capture its output as string and print it to stdout"""
    buff = []
    print("running:", " ".join(cmd))
    with Popen(
        cmd, stdout=PIPE, stderr=STDOUT, universal_newlines=True, bufsize=1
    ) as p:
        for line in p.stdout:  # type: ignore
            print(line, end="")
            buff.append(line)
    return "\n".join(buff)