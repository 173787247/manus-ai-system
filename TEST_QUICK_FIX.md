# 测试快速修复指南

## 问题

Windows 系统上 pytest 出现编码错误：
```
UnicodeDecodeError: 'gbk' codec can't decode byte 0x80
```

## 快速修复方法

### 方法1：使用修复后的测试脚本（推荐）

```bash
# 在项目根目录
python run_tests_fixed.py
```

这个脚本会：
- 自动设置 UTF-8 编码
- 跳过可能有问题的配置文件
- 直接运行测试

### 方法2：手动运行测试（不使用配置文件）

```bash
# 设置编码环境变量
$env:PYTHONIOENCODING="utf-8"

# 运行单个测试文件
python -m pytest tests/test_base_agent.py -v --no-cov

# 运行所有测试
python -m pytest tests/ -v --no-cov
```

### 方法3：删除 pytest.ini，使用 pyproject.toml

```bash
# 如果 pytest.ini 仍有问题，可以删除它
# pytest 会自动使用 pyproject.toml（已创建）
del pytest.ini

# 然后运行测试
python -m pytest tests/ -v
```

## 验证修复

运行以下命令验证：

```bash
# 最简单的测试
python -m pytest tests/test_base_agent.py::test_base_agent_initialization -v --no-cov
```

如果看到：
```
======================== test session starts ========================
tests/test_base_agent.py::test_base_agent_initialization PASSED
======================== 1 passed in X.XXs ========================
```

说明修复成功！

## 如果还有问题

1. **检查 pytest 是否安装**
   ```bash
   pip install pytest pytest-cov
   ```

2. **检查 Python 版本**
   ```bash
   python --version  # 应该是 3.9+
   ```

3. **直接运行 Python 测试（不通过 pytest）**
   ```bash
   python -c "import sys; sys.path.insert(0, 'tests'); from test_base_agent import *; test_base_agent_initialization()"
   ```

## 推荐工作流程

1. 先运行修复脚本验证：
   ```bash
   python run_tests_fixed.py
   ```

2. 如果通过，再运行完整测试：
   ```bash
   $env:PYTHONIOENCODING="utf-8"
   python -m pytest tests/ -v --cov=src
   ```

