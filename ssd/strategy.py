from abc import ABC, abstractmethod
from collections import deque


class InterfaceStrategy(ABC):
    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def read(self):
        pass


class DequeStrategy(InterfaceStrategy):
    def update(self, cmdlist, new_cmd):
        deque_cmdlist = deque(cmdlist)
        updated_cmdlist = list()

        cmd_type, address, value = new_cmd
        if cmd_type == "W":
            while deque_cmdlist:
                old_cmd = deque_cmdlist.popleft()
                old_cmd_type, old_address, old_value = old_cmd
                if old_cmd_type == "W" and old_address == address:
                    continue
                updated_cmdlist = self._delete_overlap_and_add_cmd(
                    updated_cmdlist, old_cmd
                )
            updated_cmdlist = self._delete_overlap_and_add_cmd(updated_cmdlist, new_cmd)

        if cmd_type == "E":
            while deque_cmdlist:
                old_cmd = deque_cmdlist.popleft()
                old_cmd_type, old_address, old_value = old_cmd
                if old_cmd_type == "W" and (address <= old_address < address + value):
                    continue
                updated_cmdlist = self._delete_overlap_and_add_cmd(
                    updated_cmdlist, old_cmd
                )
            updated_cmdlist = self._delete_overlap_and_add_cmd(updated_cmdlist, new_cmd)
        return updated_cmdlist

    def _delete_overlap_and_add_cmd(self, cmdlist, new_cmd):
        if not cmdlist:
            cmdlist.append(new_cmd)
            return cmdlist

        righttop_cmd = cmdlist[-1]
        pop_cmd_type, pop_cmd_address, pop_cmd_value = righttop_cmd
        new_cmd_type, new_cmd_address, new_cmd_value = new_cmd

        if (pop_cmd_type == new_cmd_type == "E") and (
            new_cmd_address <= pop_cmd_address + pop_cmd_value
        ):
            cmdlist.pop()
            from_index = pop_cmd_address
            to_index = new_cmd_address + new_cmd_value
            cmdlist.append(["E", from_index, to_index - from_index])
            return cmdlist

        cmdlist.append(new_cmd)
        return cmdlist

    def read(self, cmdlist, address):
        if not cmdlist:
            return None

        for cmd in reversed(cmdlist):
            cmd_type, cmd_address, cmd_value = cmd
            if address == cmd_address:
                if cmd_type == "W":
                    return cmd_value
                return "Erase"
        return None
