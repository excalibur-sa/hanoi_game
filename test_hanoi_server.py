"""
Flask 后端服务器测试文件
测试汉诺塔 API 端点
"""
import unittest
import json
from hanoi_server import app


class TestHanoiAPI(unittest.TestCase):
    """汉诺塔 API 测试类"""
    
    def setUp(self):
        """每个测试前的设置"""
        app.config['TESTING'] = True
        self.client = app.test_client()
    
    def test_solve_hanoi_3_disks(self):
        """测试解决 3 个圆盘的汉诺塔问题"""
        response = self.client.post('/api/solve', 
            json={'disks': 3},
            content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # 验证返回结构
        self.assertIn('steps', data)
        self.assertIn('count', data)
        self.assertEqual(data['count'], 7)  # 3个圆盘需要 2^3 - 1 = 7 步
        
        # 验证步骤格式
        for step in data['steps']:
            self.assertIn('from', step)
            self.assertIn('to', step)
            self.assertIn('disk', step)
            self.assertIn(step['from'], ['A', 'B', 'C'])
            self.assertIn(step['to'], ['A', 'B', 'C'])
    
    def test_solve_hanoi_1_disk(self):
        """测试解决 1 个圆盘的汉诺塔问题"""
        response = self.client.post('/api/solve',
            json={'disks': 1},
            content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertEqual(data['count'], 1)
        self.assertEqual(len(data['steps']), 1)
        self.assertEqual(data['steps'][0]['from'], 'A')
        self.assertEqual(data['steps'][0]['to'], 'C')
    
    def test_solve_hanoi_5_disks(self):
        """测试解决 5 个圆盘的汉诺塔问题"""
        response = self.client.post('/api/solve',
            json={'disks': 5},
            content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # 5个圆盘需要 2^5 - 1 = 31 步
        self.assertEqual(data['count'], 31)
    
    def test_solve_hanoi_invalid_disks(self):
        """测试无效圆盘数量"""
        response = self.client.post('/api/solve',
            json={'disks': 0},
            content_type='application/json')
        
        # 应该返回错误或默认处理
        self.assertIn(response.status_code, [400, 200])
    
    def test_solve_hanoi_missing_disks(self):
        """测试缺少圆盘参数"""
        response = self.client.post('/api/solve',
            json={},
            content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
    
    def test_health_check(self):
        """测试健康检查端点"""
        response = self.client.get('/api/health')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'ok')


class TestHanoiAlgorithm(unittest.TestCase):
    """汉诺塔算法测试类"""
    
    def setUp(self):
        """每个测试前的设置"""
        app.config['TESTING'] = True
        self.client = app.test_client()
    
    def test_algorithm_correctness(self):
        """验证算法正确性 - 模拟移动过程"""
        response = self.client.post('/api/solve',
            json={'disks': 3},
            content_type='application/json')
        
        data = json.loads(response.data)
        steps = data['steps']
        
        # 模拟三根柱子
        towers = {
            'A': [3, 2, 1],  # 初始：大盘在下
            'B': [],
            'C': []
        }
        
        # 执行每一步
        for step in steps:
            disk = step['disk']
            from_tower = step['from']
            to_tower = step['to']
            
            # 验证移动合法性
            self.assertGreater(len(towers[from_tower]), 0, f"柱子 {from_tower} 为空")
            self.assertEqual(towers[from_tower][-1], disk, f"顶部圆盘不匹配")
            
            if len(towers[to_tower]) > 0:
                self.assertGreater(towers[to_tower][-1], disk, f"不能将大盘放在小盘上")
            
            # 执行移动
            towers[from_tower].pop()
            towers[to_tower].append(disk)
        
        # 验证最终状态：所有圆盘在 C 柱
        self.assertEqual(towers['A'], [])
        self.assertEqual(towers['B'], [])
        self.assertEqual(towers['C'], [3, 2, 1])


if __name__ == '__main__':
    unittest.main()