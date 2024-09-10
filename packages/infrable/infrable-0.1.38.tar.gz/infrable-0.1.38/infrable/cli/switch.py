import typer
from click import Choice

from infrable import infra

app = typer.Typer(no_args_is_help=True)


for name, sw in infra.switches.items():
    help = f"Get or set the value of the {name} switch."

    def main(
        value: str = typer.Argument(None, click_type=Choice(list(sw.options))),
        options: bool = False,
    ):
        if options:
            for opt in sorted(sw.options):
                print(opt)
            return

        if value is None:
            print(sw())
        else:
            sw.set(value)

    app.command(name=name, help=help)(main)
