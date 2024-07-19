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


class HeapStrategy(InterfaceStrategy):
    def __init__(self) -> None:
        self.heap_cmd_list = []
        self.write_address_hashset = set()

    def update(self, cmd_list: list[BufferCmd], new_cmd: BufferCmd) -> list[BufferCmd]:
        if new_cmd.type == "W":
            self._add_write_cmd_to_heap_list_and_update_hash(cmd_list, new_cmd)
        elif new_cmd.type == "E":
            self._add_erase_cmd_to_heap_list_and_update_hash(cmd_list, new_cmd)

        self._optimise_erase_in_cmd_list()
        cmd_list = self._convert_to_list()
        return cmd_list

    def read(self, cmd_list: list[BufferCmd], address: int) -> str | None:
        if not cmd_list:
            return None

        for cmd in reversed(cmd_list):
            # cmd_type, cmd_address, cmd_value = cmd
            if (
                cmd.type == "E"
                and cmd.address <= address <= cmd.address + int(cmd.value) - 1
            ):
                return "Erase"
            if cmd.type == "W" and cmd.address == address:
                return cmd.value
        return None

    def _convert_to_list(self) -> list[BufferCmd]:
        list_converted_from_heap = []
        while self.heap_cmd_list:
            heap_cmd = heapq.heappop(self.heap_cmd_list)
            cmd_type, cmd_address, cmd_value = heap_cmd
            list_converted_from_heap.append(
                BufferCmd(cmd_type, cmd_address, str(cmd_value))
            )
        return list_converted_from_heap

    def _optimise_erase_in_cmd_list(self) -> None:
        temp_erase_cmd_list = []
        while self.heap_cmd_list:
            if self.heap_cmd_list[0][0] == "W":
                break

            erase_cmd = heapq.heappop(self.heap_cmd_list)
            adjusted_cmd = self._adjust_erase_range_begin_end_index(erase_cmd)
            if not adjusted_cmd:
                continue

            heapq.heappush(temp_erase_cmd_list, adjusted_cmd)

        if len(temp_erase_cmd_list) < 2:
            while temp_erase_cmd_list:
                heapq.heappush(self.heap_cmd_list, temp_erase_cmd_list.pop())
            return

        merged_erase_cmd_list = self._merge_erase_range(temp_erase_cmd_list)
        while merged_erase_cmd_list:
            heapq.heappush(self.heap_cmd_list, merged_erase_cmd_list.pop())

    def _add_write_cmd_to_heap_list_and_update_hash(
        self, cmd_list: list[BufferCmd], new_cmd: BufferCmd
    ) -> None:
        for cmd in cmd_list:
            if cmd.type == "W":
                if cmd.address == new_cmd.address:
                    continue
                self.write_address_hashset.add(cmd.address)
            heapq.heappush(self.heap_cmd_list, (cmd.type, cmd.address, cmd.value))

        self.write_address_hashset.add(new_cmd.address)
        heapq.heappush(
            self.heap_cmd_list, (new_cmd.type, new_cmd.address, new_cmd.value)
        )

    def _add_erase_cmd_to_heap_list_and_update_hash(
        self, cmd_list: list[BufferCmd], new_cmd: BufferCmd
    ) -> None:
        for cmd in cmd_list:
            if cmd.type == "W":
                if (
                    new_cmd.address
                    <= cmd.address
                    <= new_cmd.address + int(new_cmd.value) - 1
                ):
                    continue
                self.write_address_hashset.add(cmd.address)
            heapq.heappush(self.heap_cmd_list, (cmd.type, cmd.address, cmd.value))
        heapq.heappush(
            self.heap_cmd_list, (new_cmd.type, new_cmd.address, new_cmd.value)
        )

    def _adjust_erase_range_begin_end_index(self, erase_cmd: tuple) -> tuple | None:
        cmd_type, cmd_address, cmd_value = erase_cmd
        from_address = cmd_address
        to_address = cmd_address + int(cmd_value) - 1

        if int(cmd_value) < 1:
            return None

        found_hash = 0
        if from_address in self.write_address_hashset:
            from_address += 1
            found_hash += 1
        if to_address in self.write_address_hashset:
            to_address -= 1
            found_hash += 1

        if found_hash < 1:
            return erase_cmd

        erase_cmd = (cmd_type, from_address, str(to_address - from_address + 1))
        erase_cmd = self._adjust_erase_range_begin_end_index(erase_cmd)
        return erase_cmd

    def _merge_erase_range(self, erase_cmd_list: list[tuple]) -> list[tuple]:
        merged_cmd_list = [erase_cmd_list[0]]

        for erase_cmd in erase_cmd_list[1:]:
            erase_type, erase_address, erase_value = erase_cmd
            erase_from = erase_address
            erase_to = erase_address + int(erase_value) - 1

            last_merged_cmd = merged_cmd_list[-1]
            base_type, base_address, base_value = last_merged_cmd
            base_from = base_address
            base_to = base_address + int(base_value) - 1

            if erase_from <= base_to:
                merged_cmd_list[-1][2] = str(max(base_to, erase_to))
            else:
                # 겹치지 않으면 새로운 범위를 추가
                merged_cmd_list.append(erase_cmd)

        return merged_cmd_list
