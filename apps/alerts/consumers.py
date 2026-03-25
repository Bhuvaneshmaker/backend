from channels.generic.websocket import AsyncJsonWebsocketConsumer


class AlertsConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("alerts", self.channel_name)
        await self.accept()

    async def disconnect(self, _close_code):
        await self.channel_layer.group_discard("alerts", self.channel_name)

    async def alert_created(self, event):
        await self.send_json(event["payload"])
