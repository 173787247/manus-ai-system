# 如何查看测试输出

## 🎯 快速查看

### 最简单的方法

```bash
cd manus-ai-system
python run_tests_fixed.py
```

**输出位置**: PowerShell/CMD 控制台  
**输出内容**: 测试进度、通过/失败状态、总结

---

## 📍 输出位置说明

### 1. 控制台输出（默认）

**位置**: 运行命令的终端窗口

**查看方式**:
```bash
# 直接运行，输出显示在控制台
python run_tests_fixed.py
```

**输出示例**:
```
============================================================
Manus AI System - Test Suite (Fixed Version)
============================================================

[1/7] 运行: python -m pytest tests/test_base_agent.py -v --no-cov
------------------------------------------------------------
============================ test session starts =============================
tests/test_base_agent.py::test_base_agent_initialization PASSED [ 20%]
...
======================== 5 passed in 0.03s =========================

============================================================
Test Summary
============================================================
[PASS]: tests/test_base_agent.py
...
Total: 7/7 passed

[SUCCESS] All tests passed!
```

---

### 2. 保存到文件

**位置**: 项目根目录下的文本文件

**方法**:
```bash
# 保存所有输出到文件
python run_tests_fixed.py > test_results.txt 2>&1

# 或使用 pytest 直接保存
python -m pytest tests/ -v > test_results.txt 2>&1
```

**查看文件**:
```bash
# Windows
type test_results.txt

# 或使用编辑器打开
notepad test_results.txt
```

---

### 3. HTML 报告（可视化）

**位置**: `test_report.html` 文件

**生成方法**:
```bash
# 安装插件（如果还没安装）
pip install pytest-html

# 生成HTML报告
python -m pytest tests/ --html=test_report.html --self-contained-html
```

**查看方式**: 用浏览器打开 `test_report.html`

**报告内容**:
- 测试列表
- 通过/失败状态
- 执行时间
- 错误详情（如果有）

---

### 4. 覆盖率报告

**位置**: `htmlcov/index.html` 文件

**生成方法**:
```bash
# 安装插件（如果还没安装）
pip install pytest-cov

# 生成覆盖率报告
python -m pytest tests/ --cov=src --cov-report=html
```

**查看方式**: 用浏览器打开 `htmlcov/index.html`

**报告内容**:
- 代码覆盖率百分比
- 每个文件的覆盖率详情
- 未覆盖的代码行

---

### 5. JUnit XML 报告（CI/CD）

**位置**: `junit.xml` 文件

**生成方法**:
```bash
python -m pytest tests/ --junitxml=junit.xml
```

**用途**: 用于CI/CD系统（如Jenkins、GitHub Actions）

---

## 🔍 查看特定测试的输出

### 查看单个测试文件

```bash
# 查看基础智能体测试
python -m pytest tests/test_base_agent.py -v

# 查看规划智能体测试
python -m pytest tests/test_planning_agent.py -v
```

### 查看单个测试函数

```bash
# 查看特定测试函数
python -m pytest tests/test_base_agent.py::test_base_agent_initialization -v
```

### 查看失败的测试详情

```bash
# 显示详细错误信息
python -m pytest tests/ -v --tb=long

# 显示简短错误信息
python -m pytest tests/ -v --tb=short

# 显示所有输出（包括print）
python -m pytest tests/ -v -s
```

---

## 📊 输出内容解读

### 测试通过示例

```
tests/test_base_agent.py::test_base_agent_initialization PASSED [ 20%]
```

**含义**:
- `tests/test_base_agent.py`: 测试文件路径
- `test_base_agent_initialization`: 测试函数名
- `PASSED`: 测试通过 ✅
- `[ 20%]`: 当前测试进度

### 测试失败示例

```
tests/test_xxx.py::test_xxx FAILED [100%]
================================= FAILURES ==================================
___________________ test_xxx ____________________
tests/test_xxx.py:10: in test_xxx
    assert result["status"] == "success"
E   AssertionError: assert 'error' == 'success'
```

**含义**:
- `FAILED`: 测试失败 ❌
- `AssertionError`: 断言错误类型
- 显示具体的错误位置和原因

### 测试总结

```
======================== 26 passed, 1 warning in 0.17s =======================
```

**含义**:
- `26 passed`: 26个测试通过
- `1 warning`: 1个警告（通常可忽略）
- `0.17s`: 总执行时间

---

## 🛠️ 实用命令

### 查看所有测试列表

```bash
# 列出所有测试（不执行）
python -m pytest tests/ --collect-only
```

### 只运行失败的测试

```bash
# 运行上次失败的测试
python -m pytest tests/ --lf

# 运行失败的测试，然后运行其他测试
python -m pytest tests/ --ff
```

### 按标记运行测试

```bash
# 只运行集成测试
python -m pytest tests/ -m integration

# 排除慢速测试
python -m pytest tests/ -m "not slow"
```

### 显示详细输出

```bash
# 显示所有print输出
python -m pytest tests/ -v -s

# 显示最详细的输出
python -m pytest tests/ -vv -s
```

---

## 📂 输出文件位置总结

| 文件类型 | 位置 | 生成命令 |
|---------|------|---------|
| 控制台输出 | 终端窗口 | `python run_tests_fixed.py` |
| 文本报告 | `test_results.txt` | `python -m pytest tests/ -v > test_results.txt` |
| HTML报告 | `test_report.html` | `python -m pytest tests/ --html=test_report.html` |
| 覆盖率报告 | `htmlcov/index.html` | `python -m pytest tests/ --cov=src --cov-report=html` |
| JUnit XML | `junit.xml` | `python -m pytest tests/ --junitxml=junit.xml` |

---

## 🎯 推荐查看方式

### 日常开发
```bash
# 快速查看测试结果
python run_tests_fixed.py
```

### 详细分析
```bash
# 生成HTML报告
python -m pytest tests/ --html=test_report.html --self-contained-html
# 然后用浏览器打开 test_report.html
```

### 代码覆盖率
```bash
# 生成覆盖率报告
python -m pytest tests/ --cov=src --cov-report=html
# 然后用浏览器打开 htmlcov/index.html
```

---

## 💡 提示

1. **实时查看**: 直接运行 `python run_tests_fixed.py` 在控制台查看
2. **保存结果**: 使用 `> test_results.txt` 保存到文件
3. **可视化**: 使用 `--html` 生成HTML报告，更易阅读
4. **覆盖率**: 使用 `--cov` 查看代码覆盖率，找出未测试的代码

