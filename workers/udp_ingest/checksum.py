def calc_checksum(frame: list[int]) -> int:
    return sum(frame[:53]) & 0xFF
