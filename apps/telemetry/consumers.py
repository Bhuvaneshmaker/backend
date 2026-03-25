from channels.generic.websocket import AsyncJsonWebsocketConsumer


class BaseTelemetryConsumer(AsyncJsonWebsocketConsumer):
    group_name = ""

    async def connect(self):
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, _close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def telemetry_update(self, event):
        await self.send_json(event["payload"])


class BlockConsumer(BaseTelemetryConsumer):
    async def connect(self):
        self.group_name = f"block_{self.scope['url_route']['kwargs']['block_id']}"
        await super().connect()


class DeviceConsumer(BaseTelemetryConsumer):
    async def connect(self):
        self.group_name = f"device_{self.scope['url_route']['kwargs']['device_id']}"
        await super().connect()


class ElevatorConsumer(BaseTelemetryConsumer):
    async def connect(self):
        self.group_name = f"elevator_{self.scope['url_route']['kwargs']['elevator_id']}"
        await super().connect()
