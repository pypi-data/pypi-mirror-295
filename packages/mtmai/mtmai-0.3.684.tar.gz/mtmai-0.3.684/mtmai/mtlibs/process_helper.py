import logging
import shlex
import subprocess
import threading

logger = logging.getLogger()


def process_output(process):
    while True:
        output = process.stdout.readline().decode()
        if process.poll() is not None:
            break
        if output:
            print(output, flush=True)


# def process_output_threadhandler(process):
#     """用线程的方式将进程的输出显示到终端上"""

#     def _handler(process):
#         while True:
#             result = process.poll()
#             if result is not None:
#                 print(f"进程结束:{result}")
#                 break
#             else:
#                 output = process.stdout.readline().decode()
#                 if output:
#                     print(output.rstrip(), flush=True)
#                 if process.stderr:
#                     err = process.stderr.readline().decode()
#                     if err:
#                         print(f"stderr, {err}", flush=True)

#     threading.Thread(target=_handler, args=(process,)).start()


# def exec_cmd(cmd):
#     """
#     助手函数, 启动系统进程,并直接从sys.stdout 回显
#     """

#     def handle_output(process):
#         while True:
#             output = process.stdout.readline().decode()
#             if process.poll() is not None:
#                 break
#             if output:
#                 logger.info(output)
#                 # sys.stdout.flush()

#     process = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)
#     threading.Thread(target=handle_output, args=(process,)).start()


def exec_cmd2(cmd, output_file="/var/log/clilog.log"):
    """
    助手函数, 启动系统进程,并将进程的输出写入到文件中
    TODO: 应该升级为流模式, 这样就不用关日志是不是文件,可以使用StringIO
    """

    def handle_output(process):
        try:
            with open(output_file, "ab+") as logfile:
                while True:
                    if process.stdout:
                        bytes = process.stdout.read()
                        logfile.write(bytes)
                        logfile.flush()
                    if process.stderr:
                        bytes = process.stderr.read()
                        logfile.write(bytes)
                        logfile.flush()

                    if process.poll() is not None:
                        break
        except Exception as e:
            print(e)

    process = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)  # noqa: S603
    threading.Thread(target=handle_output, args=(process,)).start()


# def bash(bash_script: str):
#     process = subprocess.Popen(
#         bash_script,
#         shell=True,
#         stdout=sys.stdout,
#         stderr=sys.stderr,
#         text=True,
#     )

#     process.wait()  # 等待进程结束
#     return_code = process.returncode

#     if return_code != 0:
#         raise subprocess.CalledProcessError(return_code, bash_script)

#     return return_code


# async def subprocess_shell(script):
#     """以异步的方式运行shell"""
#     # logger.info("[subprocess_shell 开始]")
#     proc = await asyncio.create_subprocess_shell(
#         script, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT
#     )
#     # 循环读取，能达到效果，更高级的写法是使用protocol
#     # 参考：http://songcser.github.io/2017/10/26/working-with-subprocesses/
#     line = await proc.stdout.readline()
#     while line:
#         logger.info(line.decode().strip())
#         line = await proc.stdout.readline()
