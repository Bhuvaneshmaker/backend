from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer



def publish_telemetry_update(state: dict):
    layer = get_channel_layer()
    if layer is None:
        return

    groups = [
        f"device_{state.get('device_pk') or state['device_id']}",
        f"elevator_{state.get('elevator_id') or state['slave_id']}",
    ]
    if state.get("block_id"):
        groups.append(f"block_{state['block_id']}")

    for group in groups:
        async_to_sync(layer.group_send)(
            group,
            {"type": "telemetry_update", "payload": {"type": "telemetry.update", **state}},
        )



def publish_alert_event(alert: dict):
    layer = get_channel_layer()
    if layer is None:
        return

    async_to_sync(layer.group_send)(
        "alerts",
        {"type": "alert_created", "payload": {"type": "alert.created", **alert}},
    )
