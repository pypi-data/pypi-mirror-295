import logging

logger = logging.getLogger()


def register_easyspider_commands(cli):
    @cli.command()
    def easyspider():
        # print("args", args)

        # if len(args) < 2:
        #     print("Usage: easyspider <server|ui|worker> [options]")
        #     return

        # command_type = args[1]

        # if command_type == "server":
        #     run_easy_spider_server()
        # elif command_type == "ui":
        #     run_easy_spider_ui()
        # elif command_type == "worker":
        #     config = {
        #         "ids": [0],
        #         "saved_file_name": "",
        #         "user_data": False,
        #         "config_folder": "",
        #         "config_file_name": "config.json",
        #         "read_type": "local",
        #         "headless": False,
        #         "keyboard": False,
        #         "pause_key": "p",
        #         "version": "0.6.2",
        #         "docker_driver": "http://localhost:4444/wd/hub",
        #     }
        #     # 可以根据需要从args中解析更多参数来更新config
        #     main(config)
        # else:
        #     print("Invalid command. Use 'server', 'ui', or 'worker'.")
        #     return
        print("easyspider")
