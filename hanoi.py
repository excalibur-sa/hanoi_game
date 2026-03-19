#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
汉诺塔（Tower of Hanoi）程序

汉诺塔是一个经典的递归问题：
- 有三根柱子 A、B、C
- A 柱上有 n 个大小不一的圆盘，小的在上，大的在下
- 目标是将所有圆盘从 A 移动到 C
- 规则：每次只能移动一个圆盘，大盘不能放在小盘上面

时间复杂度：O(2^n)
空间复杂度：O(n) - 递归栈深度
"""

from typing import List, Tuple
import sys

# ==================== 常量定义 ====================
LARGE_DISK_WARNING_THRESHOLD = 15
RECURSION_DEPTH_LIMIT = 500
DEFAULT_SOURCE_PILLAR = 'A'
DEFAULT_AUXILIARY_PILLAR = 'B'
DEFAULT_TARGET_PILLAR = 'C'


class HanoiTower:
    """汉诺塔类，封装汉诺塔问题的解决方案"""
    
    def __init__(self, num_disks: int, use_iteration: bool = False):
        if num_disks < 1:
            raise ValueError("圆盘数量必须大于0")
        self.num_disks = num_disks
        self.moves: List[Tuple[str, str, int]] = []
        self.move_count = 0
        self._use_iteration = use_iteration
    
    def solve(self, source: str = DEFAULT_SOURCE_PILLAR, auxiliary: str = DEFAULT_AUXILIARY_PILLAR, target: str = DEFAULT_TARGET_PILLAR) -> List[Tuple[str, str, int]]:
        self.moves = []
        self.move_count = 0
        
        if self.num_disks > RECURSION_DEPTH_LIMIT and not self._use_iteration:
            print(f"警告：圆盘数量 {self.num_disks} 超过递归深度限制 {RECURSION_DEPTH_LIMIT}")
            print("建议使用迭代解法以避免栈溢出。正在自动切换到迭代模式...")
            self._use_iteration = True
        
        if self._use_iteration:
            iterative_moves = hanoi_iterative(self.num_disks)
            self.moves = iterative_moves
            self.move_count = len(self.moves)
        else:
            self._move_disks(self.num_disks, source, auxiliary, target)
        
        return self.moves
    
    def _move_disks(self, n: int, source: str, auxiliary: str, target: str) -> None:
        if n == 1:
            self._record_move(source, target, n)
        else:
            self._move_disks(n - 1, source, target, auxiliary)
            self._record_move(source, target, n)
            self._move_disks(n - 1, auxiliary, source, target)
    
    def _record_move(self, source: str, target: str, disk: int) -> None:
        self.move_count += 1
        self.moves.append((source, target, disk))
    
    def get_move_count(self) -> int:
        return self.move_count
    
    def print_moves(self) -> None:
        print(f"\n汉诺塔解决方案（{self.num_disks} 个圆盘）：")
        print("=" * 50)
        for i, (source, target, disk) in enumerate(self.moves, 1):
            print(f"第 {i:3d} 步: 将圆盘 {disk} 从 {source} 柱移动到 {target} 柱")
        print("=" * 50)
        print(f"总移动次数: {self.move_count}")
        print(f"理论最少次数: {2 ** self.num_disks - 1}")


def hanoi_recursive(n: int, source: str = 'A', auxiliary: str = 'B', target: str = 'C') -> int:
    if n < 1:
        raise ValueError("圆盘数量必须大于0")
    
    if n == 1:
        print(f"移动圆盘 1 从 {source} 到 {target}")
        return 1
    else:
        count = 0
        count += hanoi_recursive(n - 1, source, target, auxiliary)
        print(f"移动圆盘 {n} 从 {source} 到 {target}")
        count += 1
        count += hanoi_recursive(n - 1, auxiliary, source, target)
        return count


def hanoi_iterative(n: int) -> List[Tuple[str, str, int]]:
    if n < 1:
        raise ValueError("圆盘数量必须大于0")
    
    towers = {
        DEFAULT_SOURCE_PILLAR: list(range(n, 0, -1)),
        DEFAULT_AUXILIARY_PILLAR: [],
        DEFAULT_TARGET_PILLAR: []
    }
    
    moves: List[Tuple[str, str, int]] = []
    total_moves = 2 ** n - 1
    
    if n % 2 == 1:
        clockwise = [DEFAULT_SOURCE_PILLAR, DEFAULT_TARGET_PILLAR, DEFAULT_AUXILIARY_PILLAR]
    else:
        clockwise = [DEFAULT_SOURCE_PILLAR, DEFAULT_AUXILIARY_PILLAR, DEFAULT_TARGET_PILLAR]
    
    def get_top_disk(pillar: str) -> int:
        return towers[pillar][-1] if towers[pillar] else float('inf')
    
    def move_disk(source: str, target: str) -> Tuple[str, str, int]:
        disk = towers[source].pop()
        towers[target].append(disk)
        return (source, target, disk)
    
    def find_smallest_disk_pillar() -> str:
        for pillar in [DEFAULT_SOURCE_PILLAR, DEFAULT_AUXILIARY_PILLAR, DEFAULT_TARGET_PILLAR]:
            if towers[pillar] and towers[pillar][-1] == 1:
                return pillar
        return DEFAULT_SOURCE_PILLAR
    
    def get_next_pillar(pillar: str, direction: List[str]) -> str:
        idx = direction.index(pillar)
        return direction[(idx + 1) % 3]
    
    def make_legal_non_smallest_move() -> Tuple[str, str, int]:
        pillars = [DEFAULT_SOURCE_PILLAR, DEFAULT_AUXILIARY_PILLAR, DEFAULT_TARGET_PILLAR]
        non_smallest_pillars = []
        for pillar in pillars:
            if not towers[pillar] or towers[pillar][-1] != 1:
                non_smallest_pillars.append(pillar)
        
        if len(non_smallest_pillars) != 2:
            return None
        
        p1, p2 = non_smallest_pillars
        top1 = get_top_disk(p1)
        top2 = get_top_disk(p2)
        
        if top1 < top2:
            return move_disk(p1, p2)
        else:
            return move_disk(p2, p1)
    
    for step in range(1, total_moves + 1):
        if step % 2 == 1:
            source = find_smallest_disk_pillar()
            target = get_next_pillar(source, clockwise)
            move = move_disk(source, target)
        else:
            move = make_legal_non_smallest_move()
        
        if move:
            moves.append(move)
    
    return moves


def validate_solution(moves: List[Tuple[str, str, int]], num_disks: int) -> bool:
    towers = {
        'A': list(range(num_disks, 0, -1)),
        'B': [],
        'C': []
    }
    
    for i, (source, target, disk) in enumerate(moves):
        if not towers[source]:
            print(f"错误：第 {i+1} 步，源柱 {source} 为空")
            return False
        
        top_disk = towers[source][-1]
        if top_disk != disk:
            print(f"错误：第 {i+1} 步，尝试移动圆盘 {disk}，但源柱顶部是圆盘 {top_disk}")
            return False
        
        if towers[target] and towers[target][-1] < disk:
            print(f"错误：第 {i+1} 步，不能将圆盘 {disk} 放在较小的圆盘 {towers[target][-1]} 上")
            return False
        
        towers[source].pop()
        towers[target].append(disk)
    
    if towers['C'] != list(range(num_disks, 0, -1)):
        print("错误：最终状态不正确，所有圆盘应该在C柱")
        return False
    
    return True


def main():
    print("=" * 60)
    print("           汉诺塔（Tower of Hanoi）程序")
    print("=" * 60)
    
    try:
        num_disks = int(input("\n请输入圆盘数量（建议 1-10）: "))
        if num_disks < 1:
            print("错误：圆盘数量必须大于0")
            return
        if num_disks > LARGE_DISK_WARNING_THRESHOLD:
            confirm = input(f"警告：{num_disks} 个圆盘需要 {2**num_disks - 1} 次移动，是否继续？(y/n): ")
            if confirm.lower() != 'y':
                return
    except ValueError:
        print("错误：请输入有效的整数")
        return
    
    hanoi = HanoiTower(num_disks, use_iteration=(num_disks > RECURSION_DEPTH_LIMIT))
    moves = hanoi.solve()
    hanoi.print_moves()
    
    print("\n验证解决方案...")
    if validate_solution(moves, num_disks):
        print("✓ 解决方案验证通过！")
    else:
        print("✗ 解决方案验证失败！")
    
    print("\n程序执行完毕。")


if __name__ == "__main__":
    main()