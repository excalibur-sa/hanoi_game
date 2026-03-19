# -*- coding: utf-8 -*-
"""
Flask 后端服务器
提供汉诺塔解决方案 API
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='static')
CORS(app)


def solve_hanoi(n, source='A', auxiliary='B', target='C', steps=None):
    """
    递归解决汉诺塔问题
    
    Args:
        n: 圆盘数量
        source: 源柱子
        auxiliary: 辅助柱子
        target: 目标柱子
        steps: 步骤列表
    
    Returns:
        步骤列表
    """
    if steps is None:
        steps = []
    
    if n == 1:
        steps.append({
            'from': source,
            'to': target,
            'disk': n
        })
    else:
        # 将 n-1 个圆盘从源柱子移到辅助柱子
        solve_hanoi(n - 1, source, target, auxiliary, steps)
        # 将最大的圆盘从源柱子移到目标柱子
        steps.append({
            'from': source,
            'to': target,
            'disk': n
        })
        # 将 n-1 个圆盘从辅助柱子移到目标柱子
        solve_hanoi(n - 1, auxiliary, source, target, steps)
    
    return steps


@app.route('/')
def index():
    """提供主页"""
    return send_from_directory('static', 'index.html')


@app.route('/<path:filename>')
def serve_static(filename):
    """提供静态文件"""
    return send_from_directory('static', filename)


@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查端点"""
    return jsonify({'status': 'ok'})


@app.route('/api/solve', methods=['POST'])
def solve():
    """
    解决汉诺塔问题 API
    
    请求体:
        {
            "disks": 3
        }
    
    返回:
        {
            "steps": [...],
            "count": 7
        }
    """
    data = request.get_json()
    
    if not data or 'disks' not in data:
        return jsonify({'error': 'Missing disks parameter'}), 400
    
    try:
        disks = int(data['disks'])
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid disks parameter'}), 400
    
    if disks < 1:
        return jsonify({'error': 'Disks must be at least 1'}), 400
    
    if disks > 20:
        return jsonify({'error': 'Too many disks (max 20)'}), 400
    
    steps = solve_hanoi(disks)
    
    return jsonify({
        'steps': steps,
        'count': len(steps)
    })


if __name__ == '__main__':
    app.run(debug=True, port=5001, use_reloader=False)