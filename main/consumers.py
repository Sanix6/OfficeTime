import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from .functions import check_employee_in_office
import json

logger = logging.getLogger(__name__)

class CheckInConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        logger.info("WebSocket соединение установлено")
        await self.accept()

    async def disconnect(self, close_code):
        logger.info(f"WebSocket соединение закрыто: {close_code}")

    async def receive(self, text_data):
        data = json.loads(text_data)
        lat_employee = data.get('lat_a')
        lon_employee = data.get('lon_a')

        if check_employee_in_office(lat_employee, lon_employee):
            status_message = 'Вы в офисе!'
        else:
            status_message = 'Вы не находитесь рядом с офисом.'

        logger.info(f"Статус для работника: {status_message}")

        await self.send(text_data=json.dumps({
            'status': status_message
        }))