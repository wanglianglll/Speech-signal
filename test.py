import websocket
import hashlib
import base64
import hmac
import json
from urllib.parse import urlencode
import time
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import _thread as thread
import pyaudio
from pynput import mouse, keyboard
import win32gui
from pynput.keyboard import Controller as KeyboardController, Key
import re
import pyperclip
import os
import winsound

# ========== 配置项（公共变量） ==========
MOUSE_TRIGGER_BUTTON = mouse.Button.left
SLEEP_TOGGLE_KEY = Key.f2
EXIT_HOLD_KEY = Key.f4
APPID = ''
APIKEY = ''
API_SECRET = ''

# 状态变量
is_recording = False
is_ws_connected = False
is_sleeping = False
press_start_time = None

# WebSocket/音频状态
audio_stream = None
p = None
ws = None
recording_results = ""
ws_param = None
STATUS_CONTINUE_FRAME = 1
STATUS_LAST_FRAME = 2


# ========== 播放提示音 ==========
def beep(freq=800, dur=800):
    winsound.Beep(freq, dur)


def speak_mode(mode="开始工作"):
    import pyttsx3
    engine = pyttsx3.init()
    time.sleep(0.5)
    engine.say(mode)
    engine.runAndWait()
    time.sleep(0.5)


# ========== 中英文语言分段 ==========
def split_by_language(text):
    segments = []
    current_lang = None
    buffer = ""
    for char in text:
        if re.match(r'[\u4e00-\u9fff]', char):
            if current_lang != 'zh':
                if buffer:
                    segments.append((current_lang, buffer))
                buffer = char
                current_lang = 'zh'
            else:
                buffer += char
        else:
            if current_lang != 'en':
                if buffer:
                    segments.append((current_lang, buffer))
                buffer = char
                current_lang = 'en'
            else:
                buffer += char
    if buffer:
        segments.append((current_lang, buffer))
    return segments


# ========== 文本粘贴 ==========
def paste_text(text):
    pyperclip.copy(text)
    key_board = KeyboardController()
    with key_board.pressed(Key.ctrl):
        key_board.press('v')
        key_board.release('v')


# ========== WebSocket 参数类 ==========
class WsParam:
    def __init__(self, appid, apikey, apisecret):
        self.APPID = appid
        self.APIKey = apikey
        self.APISecret = apisecret
        self.CommonArgs = {"app_id": self.APPID}
        self.BusinessArgs = {
            "domain": "iat",
            "language": "zh_cn",
            "accent": "mandarin",
            "vinfo": 1,
            "vad_eos": 1000
        }

    def create_url(self):
        url = 'wss://ws-api.xfyun.cn/v2/iat'
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))
        signature_origin = f"host: ws-api.xfyun.cn\ndate: {date}\nGET /v2/iat HTTP/1.1"
        signature_sha = (hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'), hashlib.sha256).
                         digest())
        signature_sha = base64.b64encode(signature_sha).decode('utf-8')
        authorization_origin = (f'api_key="{self.APIKey}", algorithm="hmac-sha256", headers="host date request-line", '
                                f'signature="{signature_sha}"')
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode('utf-8')
        v = {"authorization": authorization, "date": date, "host": "ws-api.xfyun.cn"}
        return url + '?' + urlencode(v)


# ========== WebSocket 回调 ==========
def on_message(wss, message):
    global recording_results
    try:
        data = json.loads(message)
        if data["code"] != 0:
            print("Error:", data["message"])
            return
        result = ""
        for item in data["data"]["result"]["ws"]:
            for w in item["cw"]:
                result += w["w"]
        if result.strip():
            recording_results += result
            if result.strip()[-1] in "。！？!?":
                print("识别结果:", recording_results)
                try:
                    hwnd = win32gui.GetForegroundWindow()
                    win32gui.SetForegroundWindow(hwnd)
                    time.sleep(0.2)
                    for lang, seg in split_by_language(recording_results):
                        paste_text(seg)
                        time.sleep(0.1)
                except Exception as e:
                    print("写入失败:", e)
                recording_results = ""
    except Exception as e:
        print("解析异常:", e)


def on_error(wss, error):
    print("### 错误 ###:", error)


def on_close(wss, *args):
    global is_ws_connected
    is_ws_connected = False
    print("### 连接关闭 ###")


def on_open(wss):
    global is_ws_connected
    is_ws_connected = True

    def run(*args):
        global is_recording, audio_stream, p, is_ws_connected
        p = pyaudio.PyAudio()
        audio_stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
        print("开始录音...")
        try:
            while is_recording and is_ws_connected:
                data = audio_stream.read(1024)
                d = {
                    "common": ws_param.CommonArgs,
                    "business": ws_param.BusinessArgs,
                    "data": {
                        "status": STATUS_CONTINUE_FRAME,
                        "format": "audio/L16;rate=16000",
                        "audio": base64.b64encode(data).decode('utf-8'),
                        "encoding": "raw"
                    }
                }
                try:
                    wss.send(json.dumps(d))
                except websocket._exceptions.WebSocketConnectionClosedException:
                    break
                time.sleep(0.1)
        finally:
            d["data"]["status"] = STATUS_LAST_FRAME
            try:
                wss.send(json.dumps(d))
            except:
                pass
            audio_stream.stop_stream()
            audio_stream.close()
            p.terminate()
            print("停止录音")

    thread.start_new_thread(run, ())


# ========== 控制函数 ==========
def start_recognition():
    global is_recording, ws, ws_param, is_ws_connected
    if not is_recording:
        beep(600)
        is_recording = True
        ws_param = WsParam(
            appid=APPID,
            apikey=APIKEY,
            apisecret=API_SECRET
        )
        ws = websocket.WebSocketApp(ws_param.create_url(), on_message=on_message, on_error=on_error, on_close=on_close)
        ws.on_open = on_open
        thread.start_new_thread(ws.run_forever, ())


def stop_recognition():
    global is_recording, ws, is_ws_connected
    if is_recording:
        beep(400)
        is_recording = False
        time.sleep(1.2)
        if ws and is_ws_connected:
            ws.close()


# ========== 输入监听 ==========
def on_click(x, y, button, pressed):
    global press_start_time
    if is_sleeping or button != MOUSE_TRIGGER_BUTTON:
        return
    if pressed:
        press_start_time = time.time()
        start_recognition()
    else:
        stop_recognition()


def on_key_event(key, pressed):
    global is_sleeping
    if not pressed:
        if key == SLEEP_TOGGLE_KEY:
            is_sleeping = not is_sleeping
            print(f"🟡 模式切换：{'休眠' if is_sleeping else '工作'}")
            speak_mode("开始休眠" if is_sleeping else "开始工作")
        elif key == EXIT_HOLD_KEY:
            print("🔴 程序已退出")
            speak_mode("程序已退出")
            os._exit(0)


if __name__ == '__main__':
    mouse.Listener(on_click=on_click).start()
    keyboard.Listener(on_press=lambda k: on_key_event(k, True), on_release=lambda k: on_key_event(k, False)).start()
    print("按住鼠标左键开始/停止录音（F2 切换工作/休眠，F4 退出）...")
    while True:
        time.sleep(1)