# block-l4d2-rpg-server-for-ufw

### 基于 `ufw` 与 `gufw` 屏蔽 `L4D2 RPG` 服务器
### 使用[yxnan/block-l4d2-rpg-servers](https://github.com/yxnan/block-l4d2-rpg-servers)的L4D2 RPG服务器列表

---

## 使用说明

### 获取项目
```shell
git clone https://github.com/strluck/block-l4d2-rpg-server-for-ufw.git
cd block-l4d2-rpg-server-for-ufw
```

### 启用ufw防火墙规则
```shell
python3 block-l4d2-rpg.py start
```

### 移除ufw防火墙规则
```shell
python3 block-l4d2-rpg.py stop
```

### gufw配置文件使用方式
1. 执行 `python3 block-l4d2-rpg.py` 生成gufw配置文件
2. 执行 `cd gen` 进入生成文件的目录
3. 执行 `sudo chown root:root l4d2-rpg-server.profile` 和 `sudo chmod a+rwx,u-x,g-rwx,o-rwx l4d2-rpg-server.profile` 修改权限
4. 打开 `gufw` 导入配置文件

注意: 需要 `sudo rm l4d2-rpg-server.profile` 才能重新生成新的配置文件
