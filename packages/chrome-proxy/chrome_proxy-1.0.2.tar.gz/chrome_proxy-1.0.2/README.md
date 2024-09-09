# chrome-proxy
安装
``` 
pip install chrome-proxy -U 
```
启动代理
```shell
# 正常模式
chrome-proxy
# 无头模式
chrome-proxy --headless
```
使用
```python
from selenium import webdriver

options = webdriver.ChromeOptions()
# 本地
# options.debugger_address = "127.0.0.1:9222"
# 远程
options.debugger_address = "192.168.100.156:9223"
driver = webdriver.Chrome(options=options)
driver.get("https://www.baidu.com")
print(driver.title)

```