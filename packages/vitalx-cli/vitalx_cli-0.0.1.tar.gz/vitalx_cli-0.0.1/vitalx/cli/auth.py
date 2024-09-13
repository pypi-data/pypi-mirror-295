import typer
from vitalx.cli_auth import (
    current_tokens,
    initiate_device_code_flow,
    poll_for_device_code_flow_completion,
)

auth_commands = typer.Typer(no_args_is_help=True)


@auth_commands.command()
def login() -> None:
    if current_tokens():
        typer.confirm(
            "There is an existing Vital Dashboard login. Do you want to re-authenticate?",
            abort=True,
        )

    flow = initiate_device_code_flow()

    import webbrowser

    webbrowser.open(flow["verification_uri_complete"])

    poll_for_device_code_flow_completion(flow)
