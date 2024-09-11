import logging
import threading

logger = logging.getLogger()



def register_tunnel_commands(cli):
    @cli.command()
    def tunnel():
        import asyncio

        from mtmlib import tunnel

        threading.Thread(target=lambda: asyncio.run(tunnel.start_cloudflared())).start()
