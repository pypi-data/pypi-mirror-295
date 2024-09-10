import logging

from mtmai.cli.cli import Cli

logger = logging.getLogger()


class CliEasySpider(Cli):
    """
    easyspider 服务

    """

    def run(self) -> None:
        import sys

        from mtmai.mtlibs.easyspider.easyspider_executestage import main

        if len(sys.argv) < 3:
            print("Usage: easyspider <command> <server|ui>")
            return

        command_type = sys.argv[2]

        if command_type == "server":
            print("1")
        elif command_type == "ui":
            print("2")
        else:
            print("Invalid command. Use 'server' or 'ui'.")
            return

        example_config = {
            "ids": [0],
            "saved_file_name": "",
            "user_data": False,
            "config_folder": "",
            "config_file_name": "config.json",
            "read_type": "local",
            "headless": False,
            "keyboard": False,  # 是否监听键盘输入
            "pause_key": "p",  # 暂停键
            "version": "0.6.2",
            "docker_driver": "http://localhost:4444/wd/hub",
        }
        main(example_config)
