# 快速测试指南

## 问题已修复

✅ **编码问题已修复**：`pytest.ini` 中的中文已改为英文  
✅ **测试脚本已优化**：`run_tests_fixed.py` 避免编码问题

## 快速开始（3步）

### 步骤1：安装 pytest

```powershell
pip install pytest pytest-cov
```

### 步骤2：设置编码（Windows）

```powershell
$env:PYTHONIOENCODING="utf-8"
```

### 步骤3：运行测试

```powershell
# 方法1：使用修复后的脚本（推荐）
python run_tests_fixed.py

# 方法2：直接使用 pytest
python -m pytest tests/test_base_agent.py -v
```

## 完整测试流程

```powershell
# 1. 进入项目目录
cd C:\Users\rchua\Desktop\AIFullStackDevelopment\manus-ai-system

# 2. 安装依赖
pip install pytest pytest-cov pytest-html pytest-mock

# 3. 设置编码
$env:PYTHONIOENCODING="utf-8"

# 4. 运行测试
python run_tests_fixed.py

# 或直接运行
python -m pytest tests/ -v
```

## 验证测试成功

### 成功输出示例

```
======================== test session starts ========================
tests/test_base_agent.py::test_base_agent_initialization PASSED
tests/test_base_agent.py::test_base_agent_process PASSED
...
======================== 5 passed in 0.12s ========================
```

### 判断标准

✅ **测试通过**：
- 看到 "PASSED" 或 "passed"
- 退出码为 0
- 没有错误信息

❌ **测试失败**：
- 看到 "FAILED" 或 "failed"
- 有错误堆栈信息
- 退出码不为 0

## 如果遇到问题

### 问题1：No module named pytest
```powershell
pip install pytest
```

### 问题2：编码错误
```powershell
$env:PYTHONIOENCODING="utf-8"
python -m pytest tests/ -v
```

### 问题3：导入错误
确保在项目根目录运行：
```powershell
cd manus-ai-system
python -m pytest tests/ -v
```

## 测试项目清单

运行以下测试验证系统：

1. ✅ **基础智能体测试** (`test_base_agent.py`)
   - 初始化、状态管理、记忆管理

2. ✅ **智能体管理器测试** (`test_agent_manager.py`)
   - 注册、消息总线、任务协调

3. ✅ **规划智能体测试** (`test_planning_agent.py`)
   - 任务分解、类型判断

4. ✅ **知识检索测试** (`test_knowledge_agent.py`)
   - 检索、结果融合

5. ✅ **GUI智能体测试** (`test_gui_agent.py`)
   - 动作解析、验证

6. ✅ **任务执行器测试** (`test_task_executor.py`)
   - 执行流程

7. ✅ **集成测试** (`test_integration.py`)
   - 完整流程

## 下一步

测试通过后：
1. 查看测试覆盖率：`python -m pytest tests/ --cov=src --cov-report=html`
2. 运行完整系统：`python main.py`
3. 查看文档：`docs/`

