from .commands import (
    help,
    rebuild,
    run
)


def command_help():
    help.main()


def command_run():
    run.main()


def command_rebuild():
    rebuild.main()

