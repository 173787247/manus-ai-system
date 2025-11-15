# 安装和测试指南

## 步骤1：安装依赖

### 安装 pytest 和相关工具

```bash
# 方法1：安装所有依赖
pip install -r requirements.txt

# 方法2：只安装测试依赖
pip install pytest pytest-cov pytest-html pytest-mock

# 方法3：使用 conda（如果使用 Anaconda）
conda install pytest pytest-cov -c conda-forge
```

### 验证安装

```bash
python -m pytest --version
# 应该显示：pytest X.X.X
```

## 步骤2：修复编码问题

### 问题
Windows 系统上可能出现编码错误：
```
UnicodeDecodeError: 'gbk' codec can't decode byte 0x80
```

### 解决方案

**已修复**：`pytest.ini` 文件中的中文已改为英文。

如果仍有问题，可以：

1. **设置环境变量**
   ```powershell
   $env:PYTHONIOENCODING="utf-8"
   ```

2. **删除 pytest.ini**（pytest 会使用 pyproject.toml）
   ```bash
   del pytest.ini
   ```

## 步骤3：运行测试

### 方法1：使用修复后的脚本（推荐）

```bash
# 在项目根目录
python run_tests_fixed.py
```

### 方法2：直接使用 pytest

```powershell
# 设置编码
$env:PYTHONIOENCODING="utf-8"

# 运行所有测试
python -m pytest tests/ -v

# 运行单个测试文件
python -m pytest tests/test_base_agent.py -v

# 运行并查看覆盖率
python -m pytest tests/ --cov=src --cov-report=term
```

### 方法3：运行特定测试

```bash
# 运行基础智能体测试
python -m pytest tests/test_base_agent.py -v

# 运行规划智能体测试
python -m pytest tests/test_planning_agent.py -v

# 运行集成测试
python -m pytest tests/test_integration.py -v -m integration
```

## 步骤4：验证测试成功

### 成功标志

看到以下输出表示成功：
```
======================== test session starts ========================
tests/test_base_agent.py::test_base_agent_initialization PASSED
tests/test_base_agent.py::test_base_agent_process PASSED
...
======================== X passed in Y.YYs ========================
```

### 失败处理

如果测试失败：

1. **检查错误信息**
   - 查看具体的错误堆栈
   - 检查是否是依赖问题

2. **检查导入路径**
   ```bash
   # 确保在项目根目录运行
   cd manus-ai-system
   python -m pytest tests/ -v
   ```

3. **检查 Python 版本**
   ```bash
   python --version  # 应该是 3.9+
   ```

## 快速测试命令

```bash
# 1. 安装依赖
pip install pytest pytest-cov

# 2. 设置编码（Windows）
$env:PYTHONIOENCODING="utf-8"

# 3. 运行测试
python -m pytest tests/test_base_agent.py::test_base_agent_initialization -v

# 4. 如果通过，运行所有测试
python -m pytest tests/ -v
```

## 常见问题

### Q1: No module named pytest
**解决**：
```bash
pip install pytest
```

### Q2: 编码错误
**解决**：
```powershell
$env:PYTHONIOENCODING="utf-8"
python -m pytest tests/ -v
```

### Q3: 导入错误
**解决**：
- 确保在项目根目录运行
- 检查 `src/` 目录是否存在
- 检查 `__init__.py` 文件是否存在

### Q4: 测试文件找不到
**解决**：
```bash
# 检查测试文件是否存在
dir tests\test_*.py

# 如果不存在，确保在正确的目录
cd manus-ai-system
```

## 测试检查清单

- [ ] pytest 已安装
- [ ] 在项目根目录（manus-ai-system）
- [ ] 设置了编码环境变量（Windows）
- [ ] 测试文件存在
- [ ] 源代码文件存在

## 下一步

测试通过后，可以：
1. 运行完整系统：`python main.py`
2. 查看文档：`docs/`
3. 部署系统：`docker-compose up`

