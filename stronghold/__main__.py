from .cli import cli

# Lets `python -m stronghold` run the same command as `stronghold`.
cli(prog_name="stronghold")
