import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List
from urllib.parse import urljoin

import requests
import yaml
from jsonpath import jsonpath
from loguru import logger
from requests import RequestException


class Clash:
    def __init__(
            self,
            config_file: str = "",
            delay_timeout: int = 5,
            verify_url: str = "https://www.google.com",
    ):
        self._init_clash(config_file)
        self.delay_timeout = delay_timeout
        self.verify_url = verify_url

    def _init_clash(self, config_file):
        """初始化clash"""
        if not config_file:
            if sys.platform == "win32":
                config_file = os.path.expanduser("~") + r"\.config\clash\config.yaml"
            else:
                raise RuntimeError("This script only supports Windows platform")
        host, secret = self._read_config(config_file)
        self.base_api = f"http://{host}"
        self.headers = {"Authorization": f"Bearer {secret}"}
        self.rule_groups = self.get_rule_groups()
        self.group_name = self.rule_groups[0]

    @staticmethod
    def _read_config(config_file):
        """获取clash config"""
        with open(config_file, encoding="utf-8") as f:
            data = yaml.safe_load(f)
            host = data["external-controller"]
            secret = data["secret"]
            return host, secret

    def _request(
            self, endpoint: str, method: str = "GET", data=None, timeout=10
    ) -> requests.Response:
        url = urljoin(self.base_api, endpoint)
        try:
            response = requests.request(
                method,
                url,
                headers=self.headers,
                json=data,
                timeout=timeout,
                verify=False,
            )
            response.raise_for_status()
            return response
        except RequestException as rex:
            logger.error(f"Request error: {rex}")
            raise

    def get_rule_groups(self):
        """获取代理组名称"""
        response = self._request(endpoint="proxies")
        rule_groups = jsonpath(response.json(), '$.proxies[?(@.type=="Selector")].name')
        rule_groups.remove("GLOBAL")
        return rule_groups[0], "GLOBAL"

    def get_proxies(self):
        """获取策略组中的所有节点"""
        response = self._request(endpoint="proxies")
        proxies = jsonpath(response.json(), f"$.proxies.{self.group_name}.all[*]")
        selected_list = []
        for group_name in self.rule_groups:
            selected = jsonpath(response.json(), f"$.proxies.{group_name}.now")[0]
            selected_list.append(selected)
        return proxies, selected_list

    def verify_proxy(self, name: str = "", retry_num: int = 1):
        """验证节点,默认验证global选中节点"""
        if not name:
            name = self.get_proxies()[1][1]
        retry_count = 0
        endpoint = f"/proxies/{name}/delay?timeout={self.delay_timeout * 1000}&url={self.verify_url}"
        while retry_count <= retry_num:
            try:
                response = self._request(endpoint, timeout=self.delay_timeout)
                err_info = response.json().get("message", "")
                if err_info:
                    logger.error(f"<{name}> {err_info}")
                    break
                delay = response.json().get("delay", 0)
                logger.success(f"[{self.group_name}] <{name}> Delay: {delay}ms")
                return name, delay
            except RequestException as ex:
                retry_count += 1
                logger.error(f"Verify proxy failed for {name}: {ex}")
        return None, None

    def change_node(self, name: str, is_global=True):
        """更换节点"""
        group_name = self.rule_groups[1] if is_global else self.rule_groups[0]
        endpoint = f"proxies/{group_name}"
        data = {"name": name}
        self._request(endpoint, method="PUT", data=data)
        return True

    def auto_switch(self, is_global=True):
        """自动切换可用节点"""
        proxies, selected_list = self.get_proxies()
        if is_global:
            selected = selected_list[1]
            proxy_name, delay = self.verify_proxy(name=selected)
            if delay is not None:
                logger.success(
                    f"[{self.group_name}] <{selected}> Delay: {delay}ms -> Node is OK"
                )
                return

            proxies.remove(selected)

        available_nodes = self._verify_proxies_concurrently(proxies)

        if available_nodes:
            min_delay_node = min(available_nodes, key=lambda x: x[1])
            if self.change_node(min_delay_node[0], is_global):
                logger.success(
                    f"[{self.group_name}] <{min_delay_node[0]}> Delay: {min_delay_node[1]}ms -> Switched to node"
                )
            else:
                logger.error(
                    f"[{self.group_name}] <{min_delay_node[0]}> Delay: {min_delay_node[1]}ms -> Failed to switch node"
                )
        else:
            logger.error(f"[{self.group_name}] -> No available nodes found")

    def _verify_proxies_concurrently(self, proxies: List[str], max_workers: int = 20):
        available_nodes = []
        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            futures = [
                pool.submit(self.verify_proxy, proxy_name) for proxy_name in proxies
            ]
            for future in as_completed(futures):
                try:
                    proxy_name, delay = future.result()
                    if delay is not None and delay > 0:
                        available_nodes.append((proxy_name, delay))
                except Exception as ex:
                    logger.exception(f"Error in verifying proxy: {ex}")
        return available_nodes
