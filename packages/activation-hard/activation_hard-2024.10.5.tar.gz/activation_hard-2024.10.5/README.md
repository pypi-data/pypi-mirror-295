# 介绍

基于 linux机器序列码来进行激活认证的工具

# 安装

`pip install activation-hard`

# 获取许可机器序列码

`cat /sys/class/dmi/id/product_serial`

# 生成激活码
```python
serial=['217252987']   # 这里为你上面获取的序列号，如果有多台机器，可以写多个
from activation.activate import encrypt
token=encrypt(serial)
print('token')
```

# 认证激活码
```bash
from activation.activate import decrypt
active = decrypt(token)
```


