import click
import typing

from ..registry import get_global_registry
from ..handlers.base import Param
from ..interactive import start_session
from ..constants import DEFAULT_HISTORY_FILE_PATH


history_file: str


@click.group()
@click.option("--history-file", "history_file_value", default=DEFAULT_HISTORY_FILE_PATH)
def cli(
    history_file_value: str
):
    global history_file
    history_file = history_file_value


registry = get_global_registry()
for handler in registry.handlers:
    @click.argument("file-paths", nargs=-1, type=click.Path(exists=True))
    def func(
        file_paths: typing.Tuple[str],
        __handler=handler,
        **kwargs
    ):
        start_session(
            registry,
            file_paths,
            __handler,
            kwargs,
            history_file
        )

    for key, value in handler.read_params().items():
        if isinstance(value, Param):
            multiple = value.multiple
            type = value.type
        else:
            multiple = False
            type = value

        func = click.option(
            f"--{key}",
            type=type,
            multiple=multiple,
        )(func)

    cli.command(name=handler.name)(func)
