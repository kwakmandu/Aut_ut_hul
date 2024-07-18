import sys
from typing import Optional

from ssd.virtual_ssd import VirtualSSD

if __name__ == "__main__":
    ssd = VirtualSSD()
    cmd: Optional[str]
    address: Optional[str]
    value: Optional[str]

    cmd, address, value = (sys.argv[1:4] + [None] * 3)[:3]

    if cmd == "W":
        if address is not None and value is not None:
            ssd.write(int(address), value)
    elif cmd == "R":
        if address is not None:
            ssd.read(int(address))
    elif cmd == "E":
        if address is not None and value is not None:
            ssd.erase(int(address), int(value))
