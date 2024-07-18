from dataclasses import dataclass


@dataclass
class BufferCmd:
    type: str
    address: int
    value: str
