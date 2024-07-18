from abc import ABC, abstractmethod
from collections import deque
from typing import Any, List, Tuple
import heapq


class InterfaceStrategy(ABC):
    @abstractmethod
    def update(self, cmdlist: List[Any], new_cmd: Tuple[str, int, Any]) -> List[Any]:
        pass

    @abstractmethod
    def read(self, cmdlist: List[Any], address: int) -> Any:
        pass


class DequeStrategy(InterfaceStrategy):
    def update(self, cmdlist: List[Any], new_cmd: Tuple[str, int, Any]) -> List[Any]:
        deque_cmdlist = deque(cmdlist)
        updated_cmdlist = deque()

        cmd_type, address, value = new_cmd
        if cmd_type == "W":
            heap_writeaddress = []

            while deque_cmdlist:
                old_cmd = deque_cmdlist.popleft()
                old_cmd_type, old_address, old_value = old_cmd
                if old_cmd_type == "W" and old_address == address:
                    continue
                self._update_heap_writeaddress(heap_writeaddress, old_cmd)
                self._delete_overlap_and_add_cmd(updated_cmdlist, old_cmd)
            self._update_heap_writeaddress(heap_writeaddress, new_cmd)
            self._delete_overlap_and_add_cmd(updated_cmdlist, new_cmd)
            self._optimise_eraserange(updated_cmdlist, heap_writeaddress)

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
            (new_cmd_address <= pop_cmd_address + int(pop_cmd_value) - 1)
            and (new_cmd_address + int(new_cmd_value) - 1 >= pop_cmd_address)
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

    def _update_heap_writeaddress(self, heap_writeaddress, cmd):
        cmd_type, cmd_address, cmd_value = cmd
        if cmd_type == "W":
            heapq.heappush(heap_writeaddress, cmd_address)

    def _optimise_eraserange(self, updated_cmdlist, heap_writeaddress):
        cmdlist_index = []
        for idx, cmd in enumerate(updated_cmdlist):
            cmd_type, cmd_address, cmd_value = cmd
            if cmd_type == "E" and (
                cmd_address in heap_writeaddress
                or (cmd_address + int(cmd_value) - 1) in heap_writeaddress
            ):
                cmdlist_index.append(idx)
        if not cmdlist_index:
            return

        cum_idx = 0
        stack_list = []
        for idx in cmdlist_index:
            for pop_count in range(idx - cum_idx):
                cmd = updated_cmdlist.popleft()
                cum_idx += 1
                stack_list.append(cmd)

            cmd = updated_cmdlist.popleft()
            cum_idx += 1

            edit_cmd = self._recursive_edit_eraserange(cmd, heap_writeaddress)
            if not edit_cmd:
                continue

            stack_list.append(edit_cmd)

        while stack_list:
            cmd_in_stack = stack_list.pop()
            updated_cmdlist.appendleft(cmd_in_stack)

    def _recursive_edit_eraserange(self, cmd, heap_writeaddress):
        cmd_type, cmd_address, cmd_value = cmd
        from_address = cmd_address
        to_address = cmd_address + int(cmd_value) - 1
        if int(cmd_value) == 0:
            return None

        if from_address in heap_writeaddress:
            from_address += 1
            cmd = [cmd_type, from_address, str(to_address - from_address + 1)]
            cmd = self._recursive_edit_eraserange(cmd, heap_writeaddress)
        elif to_address in heap_writeaddress:
            to_address -= 1
            cmd = [cmd_type, from_address, str(to_address - from_address + 1)]
            cmd = self._recursive_edit_eraserange(cmd, heap_writeaddress)

        return cmd
