from .checksum import calc_checksum


class FrameValidationError(ValueError):
    pass



def parse_frame(frame: list[int]) -> dict:
    if len(frame) != 55:
        raise FrameValidationError("invalid length")
    if frame[0] != 0x80:
        raise FrameValidationError("invalid header")
    if frame[54] != 0xFF:
        raise FrameValidationError("invalid footer")

    checksum_valid = calc_checksum(frame) == frame[53]

    device_id = frame[2]
    elevators = []
    idx = 3
    while idx + 4 < 53:
        slave_id = frame[idx]
        response = frame[idx + 1]
        data_byte_1 = frame[idx + 2]
        data_byte_2 = frame[idx + 3]
        floor_count = frame[idx + 4]

        if slave_id != 0:
            connected = response == 0
            elevators.append(
                {
                    "slave_id": slave_id,
                    "response_code": response,
                    "connection_status": "Disconnected" if response == 1 else "Connected",
                    "overload": bool(data_byte_1 & 0x01) if connected else None,
                    "mimo": bool(data_byte_1 & 0x02) if connected else None,
                    "independent_mode": bool(data_byte_1 & 0x04) if connected else None,
                    "fireman_switch_status": bool(data_byte_1 & 0x08) if connected else None,
                    "fire_emergency_status": bool(data_byte_1 & 0x10) if connected else None,
                    "fire_emergency_return_status": bool(data_byte_1 & 0x20) if connected else None,
                    "malfunction": bool(data_byte_1 & 0x40) if connected else None,
                    "run_stop": "Running" if (data_byte_1 & 0x80) else "Stopped",
                    "door_status": "Open" if (data_byte_2 & 0x01) else "Closed",
                    "lift_direction_up": bool(data_byte_2 & 0x02) if connected else None,
                    "lift_direction_down": bool(data_byte_2 & 0x04) if connected else None,
                    "lift_position": floor_count if connected else None,
                    "raw_data_byte_1": data_byte_1,
                    "raw_data_byte_2": data_byte_2,
                }
            )
        idx += 5

    return {
        "device_id": device_id,
        "frame_type": frame[1],
        "checksum": frame[53],
        "checksum_valid": checksum_valid,
        "footer": frame[54],
        "elevators": elevators,
    }



def parse_udp_payload(payload: bytes) -> list[int]:
    text = payload.decode("utf-8").strip()
    return [int(part.strip()) for part in text.split(",") if part.strip()]
