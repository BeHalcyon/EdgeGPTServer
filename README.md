# EdgeGPTServer

### 简介
EdgeGPTServer是一个基于EdgeGPT (new bing) 的用于生成文本、问答、对话等多种应用场景的服务框架。
EdgeGPTServer提供了API接口，可以方便地与其他应用程序进行集成，便于不具有外网访问的环境访问。

### 使用方法
1. 安装EdgeGPT
```bash
python3 -m pip install EdgeGPT --upgrade 
```
2. 在具备外网的机器上部署本应用 (python3.8+)
```bash
git clone https://github.com/BeHalcyon/EdgeGPTServer.git
cd /path/to/EdgeGPTServer
python server.py #启动EdgeGPTServer服务
```
3. 访问：
```bash
浏览器输入：IP:5000
```

### 示例

![image](example.png)