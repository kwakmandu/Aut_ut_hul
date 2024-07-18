from abc import ABC, abstractmethod
from collections import deque
from typing import Any
import heapq

from ssd.buffer_cmd import BufferCmd


class InterfaceStrategy(ABC):
    @abstractmethod
    def update(self, cmd_list: list[BufferCmd], new_cmd: BufferCmd) -> list[BufferCmd]:
        pass

    @abstractmethod
    def read(self, cmd_list: list[BufferCmd], address: int) -> str | None:
        pass


class DequeStrategy(InterfaceStrategy):
    def update(self, cmd_list: list[BufferCmd], new_cmd: BufferCmd) -> deque[BufferCmd]:
        deque_cmd_list = deque(cmd_list)
        updated_cmd_list = deque()

        if new_cmd.type == "W":
            heap_w_addr = []

            while deque_cmd_list:
                old_cmd = deque_cmd_list.popleft()
                if old_cmd.type == "W" and old_cmd.address == new_cmd.address:
                    continue
                self._update_heap_write_address(heap_w_addr, old_cmd)
                self._delete_overlap_and_add_cmd(updated_cmd_list, old_cmd)
            self._update_heap_write_address(heap_w_addr, new_cmd)
            self._delete_overlap_and_add_cmd(updated_cmd_list, new_cmd)
            self._optimise_erase_range(updated_cmd_list, heap_w_addr)

        if new_cmd.type == "E":
            while deque_cmd_list:
                old_cmd = deque_cmd_list.popleft()
                if old_cmd.type == "W" and (
                    new_cmd.address
                    <= old_cmd.address
                    < new_cmd.address + int(new_cmd.value)
                ):
                    continue
                updated_cmd_list = self._delete_overlap_and_add_cmd(
                    updated_cmd_list, old_cmd
                )
            updated_cmd_list = self._delete_overlap_and_add_cmd(
                updated_cmd_list, new_cmd
            )
        return updated_cmd_list

    def _delete_overlap_and_add_cmd(
        self, cmd_list: deque[BufferCmd], new_cmd: BufferCmd
    ) -> deque[BufferCmd]:
        if not cmd_list:
            cmd_list.append(new_cmd)
            return cmd_list

        right_top_cmd = cmd_list[-1]

        if (right_top_cmd.type == new_cmd.type == "E") and (
            (new_cmd.address <= right_top_cmd.address + int(right_top_cmd.value) - 1)
            and (new_cmd.address + int(new_cmd.value) - 1 >= right_top_cmd.address)
        ):
            cmd_list.pop()
            from_index = right_top_cmd.address
            to_index = new_cmd.address + int(new_cmd.value)
            cmd_list.append(BufferCmd("E", from_index, str(to_index - from_index)))
            return cmd_list

        cmd_list.append(new_cmd)
        return cmd_list

    def read(self, cmd_list: list[BufferCmd], address: int) -> str | None:
        if not cmd_list:
            return None

        for cmd in reversed(cmd_list):
            # cmd_type, cmd_address, cmd_value = cmd
            if cmd.type == "E" and cmd.address <= address <= int(cmd.value):
                return "Erase"
            if cmd.type == "W" and cmd.address == address:
                return cmd.value
        return None

    def _update_heap_write_address(
        self, heap_w_addr: list[int], cmd: BufferCmd
    ) -> None:
        # cmd_type, cmd_address, cmd_value = cmd
        if cmd.type == "W":
            heapq.heappush(heap_w_addr, cmd.address)

    def _optimise_erase_range(
        self, updated_cmd_list: deque[BufferCmd], heap_w_addr: list[int]
    ) -> None:
        cmd_list_index = []
        for idx, cmd in enumerate(updated_cmd_list):
            if cmd.type == "E" and (
                cmd.address in heap_w_addr
                or (cmd.address + int(cmd.value) - 1) in heap_w_addr
            ):
                cmd_list_index.append(idx)
        if not cmd_list_index:
            return

        cum_idx = 0
        stack_list = []
        for idx in cmd_list_index:
            for pop_count in range(idx - cum_idx):
                cmd = updated_cmd_list.popleft()
                cum_idx += 1
                stack_list.append(cmd)

            cmd = updated_cmd_list.popleft()
            cum_idx += 1

            edit_cmd = self._recursive_edit_erase_range(cmd, heap_w_addr)
            if not edit_cmd:
                continue

            stack_list.append(edit_cmd)

        while stack_list:
            cmd_in_stack = stack_list.pop()
            updated_cmd_list.appendleft(cmd_in_stack)

    def _recursive_edit_erase_range(
        self, cmd: BufferCmd, heap_w_addr: list[int]
    ) -> BufferCmd | None:
        # cmd_type, cmd_address, cmd_value = cmd
        from_address = cmd.address
        to_address = cmd.address + int(cmd.value) - 1
        if int(cmd.value) == 0:
            return None

        if from_address in heap_w_addr:
            from_address += 1
            cmd = BufferCmd(cmd.type, from_address, str(to_address - from_address + 1))
            cmd = self._recursive_edit_erase_range(cmd, heap_w_addr)
        elif to_address in heap_w_addr:
            to_address -= 1
            cmd = BufferCmd(cmd.type, from_address, str(to_address - from_address + 1))
            cmd = self._recursive_edit_erase_range(cmd, heap_w_addr)

        return cmd
