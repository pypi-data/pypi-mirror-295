import argparse
import logging

from mtmai.cli.gen import CliGen
from mtmai.cli.release import CliRelease
from mtmai.cli.serve import CliServe
from mtmai.cli.tunnel import CliTunnel
from mtmai.core.bootstraps import bootstrap_core

bootstrap_core()
logger = logging.getLogger()

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="mtmai")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Serve command
    serve_parser = subparsers.add_parser("serve", help="Start the server")
    cli_serve = CliServe()
    serve_parser.set_defaults(func=cli_serve.run)

    # Init command
    init_parser = subparsers.add_parser("init", help="Run initialization")

    # Clean command
    clean_parser = subparsers.add_parser("clean", help="Run clean-up")

    # Test command
    test_parser = subparsers.add_parser("test", help="Run tests")

    # Release command
    release_parser = subparsers.add_parser("release", help="Release Python package")

    cli_release = CliRelease()
    release_parser.set_defaults(func=cli_release.run)
    # targetFn = CliRelease()
    # Deploy command
    dp_parser = subparsers.add_parser("dp", help="Run deployment")

    # Docker build base command
    docker_build_base_parser = subparsers.add_parser(
        "docker_build_base", help="Build Docker base image"
    )

    # Release npm command
    release_npm_parser = subparsers.add_parser(
        "release_npm", help="Release npm package"
    )

    # Deploy Cloudflare Pages command
    dp_cfpage_parser = subparsers.add_parser(
        "dp_cfpage", help="Deploy to Cloudflare Pages"
    )

    # Generate command
    gen_parser = subparsers.add_parser("gen", help="Generate code")
    cli_gen = CliGen()
    gen_parser.set_defaults(func=cli_gen.run)

    # Tunnel command
    tunnel_parser = subparsers.add_parser("tunnel", help="Start Cloudflared tunnel")
    cli_tunnel = CliTunnel()
    tunnel_parser.set_defaults(func=cli_tunnel.run)

    # # Run command
    # run_parser = subparsers.add_parser("run", help="Run a task")

    args = parser.parse_args()

    if args.command == "init":
        from mtmai.mtlibs import dev_helper

        dev_helper.init_project()
    elif args.command == "clean":
        from mtmai.mtlibs import dev_helper

        dev_helper.run_clean()
    elif args.command == "test":
        from mtmai.mtlibs import dev_helper

        dev_helper.run_testing()
    # elif args.command == "release":
    #     from mtmai.mtlibs import dev_helper

    #     dev_helper.release_py()
    elif args.command == "dp":
        from mtmai.cli.dp import CliDeploy

        CliDeploy().run()
    elif args.command == "docker_build_base":
        from mtmai.mtlibs import dev_helper

        dev_helper.docker_build_base()
    elif args.command == "release_npm":
        from mtmai.mtlibs import dev_helper

        dev_helper.release_npm()
    elif args.command == "dp_cfpage":
        from mtmai.mtlibs import dev_helper

        dev_helper.dp_cfpage()
    if hasattr(args, "func"):
        args.func()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
