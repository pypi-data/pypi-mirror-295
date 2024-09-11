# import argparse

# from mtmflow.cli.serve import CliServe
# from mtmflow.cli.install import CliInstall


# def main():
#     parser = argparse.ArgumentParser(description="mtmflow")
#     subparsers = parser.add_subparsers(dest="command", help="Available commands")

#     # Serve
#     serve_parser = subparsers.add_parser("serve", help="Start the server")
#     cli_serve = CliServe()
#     serve_parser.set_defaults(func=cli_serve.run)

#     # Install
#     install_parser = subparsers.add_parser("install", help="Install the server")
#     cli_install = CliInstall()
#     install_parser.set_defaults(func=cli_install.run)

#     args = parser.parse_args()

#     if hasattr(args, "func"):
#         positional_args = [getattr(args, arg) for arg in vars(args) if arg != 'func']
#         keyword_args = {arg: getattr(args, arg) for arg in vars(args) if arg != 'func'}
#         args.func(*positional_args, **keyword_args)
#     else:
#         parser.print_help()


# if __name__ == "__main__":
#     main()


import click
from mtmai.core.bootstraps import bootstrap_core

from mtmflow.cli.install import register_install_commands

bootstrap_core()


def main():
    @click.group()
    def cli():
        pass

    register_install_commands(cli)
    cli()


if __name__ == "__main__":
    main()
