# 修复编码问题

## 问题描述

在 Windows 系统上运行 pytest 时出现错误：
```
UnicodeDecodeError: 'gbk' codec can't decode byte 0x80 in position 268: illegal multibyte sequence
```

## 原因

`pytest.ini` 文件中包含 UTF-8 编码的中文字符，但 Windows 系统默认使用 GBK 编码读取配置文件，导致解码失败。

## 解决方案

已修复：将 `pytest.ini` 中的中文注释改为英文。

## 验证修复

运行以下命令验证：

```bash
# 在项目根目录（manus-ai-system）
python -m pytest tests/test_base_agent.py::test_base_agent_initialization -v
```

如果仍然有问题，可以：

1. **删除 pytest.ini，使用 pyproject.toml**
   ```bash
   # pytest.ini 已修复，但如果还有问题，可以删除它
   # pytest 会自动使用 pyproject.toml
   ```

2. **设置环境变量强制使用 UTF-8**
   ```powershell
   $env:PYTHONIOENCODING="utf-8"
   python -m pytest tests/ -v
   ```

3. **直接运行测试文件（不依赖配置文件）**
   ```bash
   python -m pytest tests/test_base_agent.py -v --no-cov
   ```

## 测试命令（修复后）

```bash
# 1. 安装依赖（如果还没安装）
pip install pytest pytest-cov

# 2. 运行单个测试
python -m pytest tests/test_base_agent.py -v

# 3. 运行所有测试
python -m pytest tests/ -v

# 4. 运行并查看覆盖率
python -m pytest tests/ --cov=src --cov-report=term
```

