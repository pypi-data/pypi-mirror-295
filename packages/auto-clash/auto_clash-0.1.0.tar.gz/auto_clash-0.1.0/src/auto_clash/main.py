import argparse
import time

from .clash import Clash


def read_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", "-c", default="", help="clash配置文件config.yaml")
    parser.add_argument(
        "--delay", "-T", default=20, type=int, help="自动切换节点间隔时间秒"
    )
    parser.add_argument(
        "--node-timeout", "-t", default=5, type=int, help="节点超时时间秒"
    )
    parser.add_argument(
        "--verify-url", "-v", default="https://www.google.com", help="用于测试延时的url"
    )
    parser.add_argument(
        "--global", "-g", default=1, type=int, help="自动切换节点是否为GLOBAL"
    )
    parser.add_argument(
        "--show-proxies", "-p", action="store_true", default=False, help="查看所有代理"
    )
    parser.add_argument(
        "--show-selected",
        "-s",
        action="store_true",
        default=False,
        help="查看已选择代理",
    )
    return parser.parse_args()


def main():
    args = read_cli_args()
    clash = Clash(
        config_file=args.config,
        delay_timeout=args.node_timeout,
        verify_url=args.verify_url,
    )
    if args.show_proxies:
        proxies, selected = clash.get_proxies()
        print(proxies)

    if args.show_selected:
        proxies, selected = clash.get_proxies()
        print(selected)

    if not any([args.show_proxies, args.show_selected]):
        while True:
            clash.auto_switch(getattr(args, "global"))
            time.sleep(args.delay)
