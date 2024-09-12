import websocket
import threading
import time

user_name = ""


def on_message(ws, message):
    print(f"收到消息: {message}")


def on_error(ws, error):
    print(f"错误: {error}")


def on_close(ws, close_status_code, close_msg):
    print("### 连接已关闭 ###")


def on_open(ws):
    print("连接已建立")
    global user_name
    user_name = input("请输入你的名字: ")

    def run(*args):
        while True:
            message = input("请输入消息 (输入 'quit' 退出): ")
            if message.lower() == 'quit':
                ws.close()
                break
            formatted_message = f"{user_name}:{message}"
            ws.send(formatted_message)
            time.sleep(1)

    threading.Thread(target=run).start()


def main():
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp("ws://47.96.151.94:8081/chat",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.run_forever()


if __name__ == "__main__":
    main()
