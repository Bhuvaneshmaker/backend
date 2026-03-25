import logging
import os
import socket

import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
django.setup()

from django.conf import settings

from apps.telemetry.services import save_elevator_states, save_packet
from workers.udp_ingest.parser import FrameValidationError, parse_frame, parse_udp_payload


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)



def run_listener():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((settings.UDP_LISTENER_HOST, settings.UDP_LISTENER_PORT))
    logger.info("UDP listener bound on %s:%s", settings.UDP_LISTENER_HOST, settings.UDP_LISTENER_PORT)

    while True:
        payload, address = sock.recvfrom(4096)
        source_ip = address[0]
        try:
            frame = parse_udp_payload(payload)
            parsed = parse_frame(frame)
            packet = save_packet(parsed, source_ip)
            states = save_elevator_states(parsed, source_ip)
            logger.info("Processed packet %s with %s states from %s", packet["id"], len(states), source_ip)
        except (ValueError, FrameValidationError) as exc:
            logger.warning("Invalid packet from %s: %s", source_ip, exc)


if __name__ == "__main__":
    run_listener()
