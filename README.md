# 🎤 语音识别自动输入助手

这是一个基于科大讯飞 WebSocket 实时语音识别接口的智能输入助手。程序运行后，用户只需长按鼠标左键即可进行语音输入，识别出的内容会自动粘贴到当前焦点输入框中，支持中英文自动分段处理，适用于微信、QQ、浏览器、IDE 等常见文本输入场景。

---

## 🚀 功能特点

- ✅ 鼠标左键长按开始录音，松开即停止
- ✅ 实时识别并自动粘贴到光标所在窗口
- ✅ 自动识别中英文并智能分段输入
- ✅ 支持“工作/休眠”模式切换（F2）
- ✅ 支持语音提示切换状态
- ✅ 支持 F4 快捷退出程序

---

## ⌨️ 快捷键说明

| 快捷键     | 功能                         |
|------------|------------------------------|
| 🖱 左键按住 | 开始录音                     |
| 🖱 左键松开 | 停止录音                     |
| F2         | 切换“工作 / 休眠”模式（语音提示） |
| F4         | 立即退出程序                 |

---

## 💻 环境依赖

- Windows 10+（需支持音频设备和剪贴板操作）
- Python 3.8 及以上

---

## 📦 安装与运行

### 1. 安装依赖包

`pip install -r requirements.txt`

### 2. 获取讯飞API许可
这里的许可是免费的，每日有500次，足够日常使用

#### 讯飞官网：https://www.xfyun.cn

#### 自行注册账号后点击 “控制台” -> “创建新应用”

#### 应用名称、分类、功能描述随便填写并提交

#### 点击左侧边栏：“语音识别” -> “语音听写（流式版）”

#### 复制APPID、APISecret、APIKey到test.py的相应位置

### 3. 运行程序

`python test.py`
（或将文件重命名为更有意义的名称后运行）

## 🧩 文件说明
test.py：主程序入口

requirements.txt：依赖项安装配置

README.md：项目说明文档

## 🛠 打包与开机自启动
生成可执行程序方便我们设置成开机自启动（.exe）：

`pyinstaller -F -w test.py`

-F: 打包为单一文件

-w: 隐藏控制台窗口（可选）

exe文件位于dist文件夹下

文件夹中选中exe文件，右键创建快捷方式

使用快捷键 win+r唤起窗口，在其中输入：`shell:startup`

将创建的快捷方式放入打开的文件夹中

## 🗒️ 注意事项
请确保麦克风权限已启用；

本程序依赖科大讯飞的实时语音识别服务，需保持网络连接；

识别效果依赖环境噪音与发音清晰度。

## 📞 联系方式
如有相关问题需要讨论，请联系QQ:1450417643