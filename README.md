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

```bash
pip install -r requirements.txt
