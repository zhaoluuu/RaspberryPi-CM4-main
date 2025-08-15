#RaspberryPi-CM4
RaspberryPi-CM4 AI模块代码

## 关于此仓库

此仓库包含以下组件：

- [app/](https://github.com/Xgorobot/RaspberryPi-CM4/tree/main/app) -- 用于通过移动应用程序控制xgo2的树莓派服务器。
- [demos/](https://github.com/Xgorobot/RaspberryPi-CM4/tree/main/demos) -- 官方创建的可以直接运行的演示程序。
- [extra_demos/](https://github.com/Xgorobot/RaspberryPi-CM4/tree/main/extra_demos) -- 一些不成熟的演示程序，仅供学习和参考使用。不保证它们能正常运行。
- [firmware/](https://github.com/Xgorobot/RaspberryPi-CM4/tree/main/firmware) -- xgo-mini和xgo-lite的出厂固件。
- [pics/](https://github.com/Xgorobot/RaspberryPi-CM4/tree/main/pics) -- 内置程序中使用的图像资源。
- [tools/](https://github.com/Xgorobot/RaspberryPi-CM4/tree/main/tools) -- 一些测试和编译工具。

如果您想升级xgo-pythonlib，请运行以下两个命令：

```
pip install --upgrade xgo-pythonlib
sudo pip install --upgrade xgo-pythonlib
```

[Xgorobot/XGO-PythonLib(github.com)](https://github.com/Xgorobot/XGO-PythonLib)

## 更新日志
### [xgo0627] - 2023-6-27

#### 修复
- 英文语言关键词已修订。
- 统一5G SSID和音量的交互逻辑。
- 升级了mini和lite的bin固件。

### [1.0.1] - 2023-6-25

#### 修复

- 修复了在未连接网络时应用程序和语音会卡住且无法退出的错误。
- 修复了声音演示会卡住且无法退出的错误。
- 修复了语音演示无法正确运行的错误。

### [1.0.0] - 2023-6-20 

### 镜像文件的稳定版本已发布。

#### 新增

- 添加了中文、英文和日文语言切换功能。
- 在主页面显示当前版本号。 