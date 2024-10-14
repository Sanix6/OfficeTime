import websocket
import json

def on_message(ws, message):
    print(f"Сообщение от сервера: {message}")

def on_error(ws, error):
    print(f"Ошибка: {error}")

def on_close(ws, close_status_code, close_msg):
    print("Соединение закрыто")

def on_open(ws):
    lat = 42.8738439 
    lon = 74.5765609 
    message = json.dumps({'lat_a': lat, 'lon_a': lon})
    ws.send(message)

if __name__ == "__main__":
    ws = websocket.WebSocketApp("ws://127.0.0.1:8000/ws/check-in/",
                                  on_open=on_open,
                                  on_message=on_message,
                                  on_error=on_error,
                                  on_close=on_close)
    ws.run_forever()
