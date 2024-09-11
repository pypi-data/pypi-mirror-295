import argparse

from mtmai.core.bootstraps import bootstrap_core

bootstrap_core()


def main():
    from mtmai.cli.clean import CliClean
    from mtmai.cli.db import CliDb
    from mtmai.cli.dp import CliDeploy
    from mtmai.cli.easyspider import CliEasySpider
    from mtmai.cli.gen import CliGen
    from mtmai.cli.init import CliInit
    from mtmai.cli.mtmflow import CliMtmflow
    from mtmai.cli.release import CliRelease
    from mtmai.cli.selenium import CliSelenium
    from mtmai.cli.serve import CliServe
    from mtmai.cli.tunnel import CliTunnel

    # logger = get_logger()
    parser = argparse.ArgumentParser(description="mtmai")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    parser_db = subparsers.add_parser("db", help="db commands")
    parser_db.add_argument("action", type=str, help="action(init, migrate, upgrade)")
    parser_db.set_defaults(func=CliDb().run)

    # Init command
    init_parser = subparsers.add_parser("init", help="Run initialization")
    cli_init = CliInit()
    init_parser.set_defaults(func=cli_init.run)

    # serve
    serve_parser = subparsers.add_parser("serve", help="Run serve")
    serve_parser.set_defaults(func=CliServe().run)

    # Clean command
    clean_parser = subparsers.add_parser("clean", help="Run clean-up")
    cli_clean = CliClean()
    clean_parser.set_defaults(func=cli_clean.run)

    # Selenium
    selenium_parser = subparsers.add_parser("selenium", help="Run selenium")
    cli_selenium = CliSelenium()
    selenium_parser.set_defaults(func=cli_selenium.run)

    # Mtmflow
    mtmflow_parser = subparsers.add_parser("mtmflow", help="Run mtmflow")
    cli_mtmflow = CliMtmflow()
    mtmflow_parser.set_defaults(func=cli_mtmflow.run)

    # Easyspider
    easyspider_parser = subparsers.add_parser("easyspider", help="Run easyspider")
    cli_easyspider = CliEasySpider()
    easyspider_parser.set_defaults(func=cli_easyspider.run)

    # Release
    release_parser = subparsers.add_parser("release", help="Run release")
    cli_release = CliRelease()
    release_parser.set_defaults(func=cli_release.run)

    # Deploy
    deploy_parser = subparsers.add_parser("dp", help="Run deploy")
    cli_deploy = CliDeploy()
    deploy_parser.set_defaults(func=cli_deploy.run)

    # Generate
    gen_parser = subparsers.add_parser("gen", help="Generate code")
    cli_gen = CliGen()
    gen_parser.set_defaults(func=cli_gen.run)

    # Tunnel
    tunnel_parser = subparsers.add_parser("tunnel", help="Run tunnel")
    tunnel_parser.set_defaults(func=CliTunnel().run)

    # Release npm
    release_npm_parser = subparsers.add_parser("release_npm", help="Run release_npm")
    cli_release_npm = CliRelease()
    release_npm_parser.set_defaults(func=cli_release_npm.run)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
