import time

from auto_clash.clash import Clash

clash = Clash()
print(clash.rule_groups)
print(clash.get_proxies())
clash.change_node("vip1 香港-01 测试")
clash.verify_proxy()
while True:
    clash.auto_switch()
    time.sleep(10)
