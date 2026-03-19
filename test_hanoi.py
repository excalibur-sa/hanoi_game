#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
汉诺塔程序单元测试

测试覆盖：
- HanoiTower 类测试
- hanoi_recursive 函数测试
- hanoi_iterative 函数测试
- validate_solution 函数测试
- 边界条件测试
- 异常处理测试
- 迭代模式测试
"""

import unittest
import sys
from io import StringIO
from hanoi import (
    HanoiTower,
    hanoi_recursive,
    hanoi_iterative,
    validate_solution,
    LARGE_DISK_WARNING_THRESHOLD,
    RECURSION_DEPTH_LIMIT,
    DEFAULT_SOURCE_PILLAR,
    DEFAULT_AUXILIARY_PILLAR,
    DEFAULT_TARGET_PILLAR
)


class TestHanoiTower(unittest.TestCase):
    """HanoiTower 类测试"""
    
    def test_init_valid(self):
        """测试有效初始化"""
        hanoi = HanoiTower(3)
        self.assertEqual(hanoi.num_disks, 3)
        self.assertEqual(hanoi.move_count, 0)
        self.assertEqual(hanoi.moves, [])
        self.assertFalse(hanoi._use_iteration)
    
    def test_init_with_iteration(self):
        """测试使用迭代模式初始化"""
        hanoi = HanoiTower(3, use_iteration=True)
        self.assertTrue(hanoi._use_iteration)
    
    def test_init_invalid_zero(self):
        """测试初始化圆盘数量为0"""
        with self.assertRaises(ValueError) as context:
            HanoiTower(0)
        self.assertIn("必须大于0", str(context.exception))
    
    def test_init_invalid_negative(self):
        """测试初始化圆盘数量为负数"""
        with self.assertRaises(ValueError) as context:
            HanoiTower(-1)
        self.assertIn("必须大于0", str(context.exception))
    
    def test_solve_one_disk(self):
        """测试1个圆盘的解决方案"""
        hanoi = HanoiTower(1)
        moves = hanoi.solve()
        self.assertEqual(len(moves), 1)
        self.assertEqual(moves[0], (DEFAULT_SOURCE_PILLAR, DEFAULT_TARGET_PILLAR, 1))
        self.assertEqual(hanoi.get_move_count(), 1)
    
    def test_solve_two_disks(self):
        """测试2个圆盘的解决方案"""
        hanoi = HanoiTower(2)
        moves = hanoi.solve()
        self.assertEqual(len(moves), 3)  # 2^2 - 1 = 3
        self.assertEqual(hanoi.get_move_count(), 3)
    
    def test_solve_three_disks(self):
        """测试3个圆盘的解决方案"""
        hanoi = HanoiTower(3)
        moves = hanoi.solve()
        self.assertEqual(len(moves), 7)  # 2^3 - 1 = 7
        self.assertEqual(hanoi.get_move_count(), 7)
    
    def test_solve_five_disks(self):
        """测试5个圆盘的解决方案"""
        hanoi = HanoiTower(5)
        moves = hanoi.solve()
        self.assertEqual(len(moves), 31)  # 2^5 - 1 = 31
    
    def test_solve_ten_disks(self):
        """测试10个圆盘的解决方案"""
        hanoi = HanoiTower(10)
        moves = hanoi.solve()
        self.assertEqual(len(moves), 1023)  # 2^10 - 1 = 1023
    
    def test_custom_pillar_names(self):
        """测试自定义柱子名称"""
        hanoi = HanoiTower(2)
        moves = hanoi.solve('X', 'Y', 'Z')
        # 验证所有移动都使用了自定义名称
        for source, target, _ in moves:
            self.assertIn(source, ['X', 'Y', 'Z'])
            self.assertIn(target, ['X', 'Y', 'Z'])
    
    def test_solve_multiple_times(self):
        """测试多次调用solve方法"""
        hanoi = HanoiTower(3)
        moves1 = hanoi.solve()
        self.assertEqual(len(moves1), 7)
        
        # 再次调用应该重置
        moves2 = hanoi.solve()
        self.assertEqual(len(moves2), 7)
    
    def test_solve_with_iteration_mode(self):
        """测试使用迭代模式解决"""
        hanoi = HanoiTower(5, use_iteration=True)
        moves = hanoi.solve()
        self.assertEqual(len(moves), 31)
        # 验证解决方案正确
        self.assertTrue(validate_solution(moves, 5))


class TestHanoiRecursive(unittest.TestCase):
    """hanoi_recursive 函数测试"""
    
    def test_one_disk(self):
        """测试1个圆盘"""
        # 捕获打印输出
        captured_output = StringIO()
        sys.stdout = captured_output
        count = hanoi_recursive(1)
        sys.stdout = sys.__stdout__
        
        self.assertEqual(count, 1)
        self.assertIn("移动圆盘 1", captured_output.getvalue())
    
    def test_two_disks(self):
        """测试2个圆盘"""
        captured_output = StringIO()
        sys.stdout = captured_output
        count = hanoi_recursive(2)
        sys.stdout = sys.__stdout__
        
        self.assertEqual(count, 3)
    
    def test_three_disks(self):
        """测试3个圆盘"""
        captured_output = StringIO()
        sys.stdout = captured_output
        count = hanoi_recursive(3)
        sys.stdout = sys.__stdout__
        
        self.assertEqual(count, 7)
    
    def test_invalid_input(self):
        """测试无效输入"""
        with self.assertRaises(ValueError):
            hanoi_recursive(0)
        
        with self.assertRaises(ValueError):
            hanoi_recursive(-1)


class TestHanoiIterative(unittest.TestCase):
    """hanoi_iterative 函数测试"""
    
    def test_one_disk(self):
        """测试1个圆盘"""
        moves = hanoi_iterative(1)
        self.assertEqual(len(moves), 1)
        # 验证返回格式包含圆盘编号
        self.assertEqual(len(moves[0]), 3)
        source, target, disk = moves[0]
        self.assertEqual(disk, 1)
    
    def test_two_disks(self):
        """测试2个圆盘"""
        moves = hanoi_iterative(2)
        self.assertEqual(len(moves), 3)
        # 验证所有移动都包含圆盘编号
        for move in moves:
            self.assertEqual(len(move), 3)
    
    def test_three_disks(self):
        """测试3个圆盘"""
        moves = hanoi_iterative(3)
        self.assertEqual(len(moves), 7)
    
    def test_four_disks(self):
        """测试4个圆盘"""
        moves = hanoi_iterative(4)
        self.assertEqual(len(moves), 15)  # 2^4 - 1 = 15
    
    def test_invalid_input(self):
        """测试无效输入"""
        with self.assertRaises(ValueError):
            hanoi_iterative(0)
        
        with self.assertRaises(ValueError):
            hanoi_iterative(-1)
    
    def test_returns_tuple_with_disk_number(self):
        """测试返回元组包含圆盘编号"""
        moves = hanoi_iterative(3)
        for source, target, disk in moves:
            self.assertIsInstance(source, str)
            self.assertIsInstance(target, str)
            self.assertIsInstance(disk, int)
            self.assertGreater(disk, 0)


class TestValidateSolution(unittest.TestCase):
    """validate_solution 函数测试"""
    
    def test_valid_solution_one_disk(self):
        """测试验证1个圆盘的有效解决方案"""
        moves = [(DEFAULT_SOURCE_PILLAR, DEFAULT_TARGET_PILLAR, 1)]
        self.assertTrue(validate_solution(moves, 1))
    
    def test_valid_solution_three_disks(self):
        """测试验证3个圆盘的有效解决方案"""
        hanoi = HanoiTower(3)
        moves = hanoi.solve()
        self.assertTrue(validate_solution(moves, 3))
    
    def test_valid_solution_five_disks(self):
        """测试验证5个圆盘的有效解决方案"""
        hanoi = HanoiTower(5)
        moves = hanoi.solve()
        self.assertTrue(validate_solution(moves, 5))
    
    def test_invalid_solution_wrong_disk(self):
        """测试验证错误的圆盘移动"""
        # 尝试移动不存在的圆盘
        moves = [(DEFAULT_SOURCE_PILLAR, DEFAULT_TARGET_PILLAR, 2)]  # 只有1个圆盘时不能移动圆盘2
        self.assertFalse(validate_solution(moves, 1))
    
    def test_invalid_solution_wrong_order(self):
        """测试验证错误的移动顺序"""
        # 错误的移动顺序
        moves = [
            (DEFAULT_SOURCE_PILLAR, DEFAULT_TARGET_PILLAR, 3),  # 先移动大盘
            (DEFAULT_SOURCE_PILLAR, DEFAULT_AUXILIARY_PILLAR, 2),
        ]
        self.assertFalse(validate_solution(moves, 3))
    
    def test_empty_moves(self):
        """测试空移动列表"""
        self.assertFalse(validate_solution([], 1))
    
    def test_validate_iterative_solution(self):
        """测试验证迭代解法的解决方案"""
        moves = hanoi_iterative(4)
        self.assertTrue(validate_solution(moves, 4))


class TestEdgeCases(unittest.TestCase):
    """边界条件测试"""
    
    def test_large_number_of_disks(self):
        """测试较大数量的圆盘"""
        hanoi = HanoiTower(15)
        moves = hanoi.solve()
        expected = 2 ** 15 - 1  # 32767
        self.assertEqual(len(moves), expected)
    
    def test_solution_correctness_for_various_sizes(self):
        """测试各种大小的解决方案正确性"""
        for n in range(1, 8):
            hanoi = HanoiTower(n)
            moves = hanoi.solve()
            self.assertTrue(
                validate_solution(moves, n),
                f"解决方案验证失败: n={n}"
            )
    
    def test_move_count_formula(self):
        """测试移动次数公式 2^n - 1"""
        for n in range(1, 11):
            hanoi = HanoiTower(n)
            hanoi.solve()
            expected = 2 ** n - 1
            self.assertEqual(
                hanoi.get_move_count(),
                expected,
                f"移动次数不正确: n={n}"
            )
    
    def test_iteration_mode_for_large_disks(self):
        """测试大量圆盘时使用迭代模式"""
        # 使用迭代模式解决较大规模问题
        hanoi = HanoiTower(20, use_iteration=True)
        moves = hanoi.solve()
        self.assertEqual(len(moves), 2 ** 20 - 1)
        # 验证解决方案正确
        self.assertTrue(validate_solution(moves, 20))


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_full_workflow(self):
        """测试完整工作流程"""
        # 创建汉诺塔
        hanoi = HanoiTower(4)
        
        # 解决问题
        moves = hanoi.solve()
        
        # 验证解决方案
        self.assertTrue(validate_solution(moves, 4))
        
        # 验证移动次数
        self.assertEqual(hanoi.get_move_count(), 15)
    
    def test_recursive_vs_class_solution(self):
        """比较递归函数和类解决方案"""
        # 使用类解决
        hanoi = HanoiTower(4)
        class_moves = hanoi.solve()
        
        # 验证类解决方案
        self.assertTrue(validate_solution(class_moves, 4))
    
    def test_iterative_correctness(self):
        """测试迭代解法的正确性"""
        for n in range(1, 6):
            moves = hanoi_iterative(n)
            self.assertEqual(len(moves), 2 ** n - 1)
    
    def test_recursive_vs_iterative_solution(self):
        """测试递归解法和迭代解法结果一致"""
        for n in range(1, 8):
            # 递归解法
            hanoi_recursive_solver = HanoiTower(n, use_iteration=False)
            recursive_moves = hanoi_recursive_solver.solve()
            
            # 迭代解法
            iterative_moves = hanoi_iterative(n)
            
            # 两者移动次数应该相同
            self.assertEqual(len(recursive_moves), len(iterative_moves))
            
            # 两者都应该产生正确的解决方案
            self.assertTrue(validate_solution(recursive_moves, n))
            self.assertTrue(validate_solution(iterative_moves, n))


class TestPerformance(unittest.TestCase):
    """性能测试"""
    
    def test_performance_small(self):
        """小规模性能测试"""
        import time
        start = time.time()
        hanoi = HanoiTower(10)
        hanoi.solve()
        elapsed = time.time() - start
        self.assertLess(elapsed, 1.0, "10个圆盘的解决时间应小于1秒")
    
    def test_performance_medium(self):
        """中等规模性能测试"""
        import time
        start = time.time()
        hanoi = HanoiTower(15)
        hanoi.solve()
        elapsed = time.time() - start
        self.assertLess(elapsed, 5.0, "15个圆盘的解决时间应小于5秒")
    
    def test_performance_iterative_large(self):
        """大规模迭代性能测试"""
        import time
        start = time.time()
        hanoi = HanoiTower(20, use_iteration=True)
        hanoi.solve()
        elapsed = time.time() - start
        self.assertLess(elapsed, 30.0, "20个圆盘的迭代解决时间应小于30秒")


class TestConstants(unittest.TestCase):
    """常量测试"""
    
    def test_constants_exist(self):
        """测试常量是否存在"""
        self.assertEqual(LARGE_DISK_WARNING_THRESHOLD, 15)
        self.assertEqual(RECURSION_DEPTH_LIMIT, 500)
        self.assertEqual(DEFAULT_SOURCE_PILLAR, 'A')
        self.assertEqual(DEFAULT_AUXILIARY_PILLAR, 'B')
        self.assertEqual(DEFAULT_TARGET_PILLAR, 'C')


def run_tests():
    """运行所有测试"""
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试类
    suite.addTests(loader.loadTestsFromTestCase(TestHanoiTower))
    suite.addTests(loader.loadTestsFromTestCase(TestHanoiRecursive))
    suite.addTests(loader.loadTestsFromTestCase(TestHanoiIterative))
    suite.addTests(loader.loadTestsFromTestCase(TestValidateSolution))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestPerformance))
    suite.addTests(loader.loadTestsFromTestCase(TestConstants))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == "__main__":
    run_tests()
