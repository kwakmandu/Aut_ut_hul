import sys
from typing import Optional

from ssd.buffer import Buffer
from ssd.virtual_ssd import VirtualSSD


def main() -> None:
    ssd = VirtualSSD(Buffer(strategy="Heap"))

    cmd: Optional[str]
    address: Optional[str]
    value: Optional[str]

    cmd, address, value = (sys.argv[1:4] + [None] * 3)[:3]
    ssd.execute_command(cmd, address, value)


if __name__ == "__main__":
    main()
