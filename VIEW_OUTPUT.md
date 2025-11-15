# 如何查看输出

## 📍 输出位置总览

### 1. 测试输出（控制台）

**位置**: 运行测试时的控制台窗口

**查看方法**:
```bash
# 运行测试
python run_tests_fixed.py
```

**输出内容**:
- ✅ 每个测试的执行状态
- ✅ 测试通过/失败信息
- ✅ 测试执行时间
- ✅ 错误信息（如果有）

**示例输出**:
```
[1/7] 运行: python -m pytest tests/test_base_agent.py -v --no-cov
======================== test session starts ============================
tests/test_base_agent.py::test_base_agent_initialization PASSED
tests/test_base_agent.py::test_base_agent_process PASSED
...
======================== 5 passed in 0.07s =============================
```

---

### 2. 测试报告文件

#### HTML报告

**先安装插件**:
```bash
pip install pytest-html
```

**生成命令**:
```bash
python -m pytest tests/ --html=report.html --self-contained-html
```

**输出位置**: `report.html`（项目根目录）

**查看方法**:
```bash
# Windows
start report.html

# 或直接双击文件
```

**报告内容**:
- 所有测试用例列表
- 通过/失败状态
- 执行时间
- 错误详情（如果有）

---

#### 覆盖率报告

**生成命令**:
```bash
python -m pytest tests/ --cov=src --cov-report=html
```

**输出位置**: `htmlcov/index.html`

**查看方法**:
```bash
# Windows
start htmlcov\index.html
```

**报告内容**:
- 代码覆盖率百分比
- 每个文件的覆盖详情
- 未覆盖的代码行
- 覆盖率趋势

---

### 3. 日志文件

**位置**: `logs/` 目录

**查看方法**:
```bash
# Windows PowerShell
Get-Content logs\manus.log -Tail 50

# 或使用文本编辑器打开
notepad logs\manus.log
```

**日志内容**:
- 系统运行日志
- 错误信息
- 调试信息
- 执行时间戳

---

### 4. 数据输出

#### 知识数据
**位置**: `data/knowledge/`

**查看方法**:
```bash
dir data\knowledge
```

#### 经验数据
**位置**: `data/experiences/`

**查看方法**:
```bash
dir data\experiences
```

#### 记录数据
**位置**: `data/recordings/`

**查看方法**:
```bash
dir data\recordings
```

---

## 🔍 详细查看方法

### 方法1: 实时查看（推荐用于调试）

```bash
# 运行测试，显示详细输出
python -m pytest tests/ -v -s

# -v: 详细模式
# -s: 显示print输出
```

**优点**: 实时查看，立即反馈  
**适用**: 调试和开发

---

### 方法2: 保存到文件

```bash
# 保存所有输出到文件
python run_tests_fixed.py > test_output.txt 2>&1

# 查看文件
type test_output.txt

# 或使用编辑器
notepad test_output.txt
```

**输出位置**: `test_output.txt`  
**优点**: 可以保存历史记录  
**适用**: 记录测试结果

---

### 方法3: HTML报告（推荐用于查看结果）

```bash
# 生成HTML报告
python -m pytest tests/ --html=test_report.html --self-contained-html

# 打开报告
start test_report.html
```

**输出位置**: `test_report.html`  
**优点**: 可视化，易于阅读  
**适用**: 查看测试结果

---

### 方法4: JSON输出

```bash
# 生成JSON格式报告
python -m pytest tests/ --json-report --json-report-file=report.json
```

**输出位置**: `report.json`  
**优点**: 结构化数据，易于程序处理  
**适用**: 自动化分析

---

## 📊 查看特定功能的输出

### 查看基础智能体功能输出

```bash
python -m pytest tests/test_base_agent.py -v -s
```

**输出内容**:
- 智能体初始化过程
- 状态变化
- 统计信息更新

---

### 查看任务分解输出

```bash
python -m pytest tests/test_planning_agent.py::test_planning_agent_decompose_task -v -s
```

**输出内容**:
- 任务理解过程
- 子任务分解结果
- 执行计划

---

### 查看知识检索输出

```bash
python -m pytest tests/test_knowledge_agent.py::test_knowledge_agent_retrieve -v -s
```

**输出内容**:
- 检索查询
- 检索结果
- 结果排序

---

### 查看完整任务执行输出

```bash
python -m pytest tests/test_integration.py::test_simple_task_flow -v -s
```

**输出内容**:
- 任务执行流程
- 各步骤结果
- 最终执行结果

---

## 🎯 实际执行的功能和输出

### 功能1: 智能体初始化

**执行代码**:
```python
agent = TestAgent("TestAgent", {"max_memory": 10})
```

**输出位置**: 控制台  
**输出内容**: 
```
test_base_agent_initialization PASSED
```

**验证**: 智能体成功创建，状态为 "idle"

---

### 功能2: 任务分解

**执行代码**:
```python
task = {"instruction": "打开浏览器，搜索AI Agent"}
plan = planning_agent.decompose_task(task)
```

**输出位置**: 控制台  
**输出内容**: 
```
test_planning_agent_decompose_task PASSED
```

**实际结果** (在代码中):
```python
{
    "subtasks": [
        {"id": "task_1", "description": "打开浏览器", "type": "gui_action"},
        {"id": "task_2", "description": "搜索AI Agent", "type": "gui_action"}
    ],
    "execution_order": ["task_1", "task_2"]
}
```

---

### 功能3: 知识检索

**执行代码**:
```python
result = knowledge_agent.retrieve("AI Agent", top_k=5)
```

**输出位置**: 控制台  
**输出内容**: 
```
test_knowledge_agent_retrieve PASSED
```

**实际结果** (在代码中):
```python
{
    "status": "success",
    "results": [
        {"content": "...", "source": "vector_store", "score": 0.9}
    ]
}
```

---

### 功能4: 动作解析

**执行代码**:
```python
actions = action_parser.parse("pyautogui.moveTo(100, 200)\npyautogui.click()")
```

**输出位置**: 控制台  
**输出内容**: 
```
test_action_parser PASSED
```

**实际结果** (在代码中):
```python
["moveTo(100, 200)", "click()"]
```

---

## 📋 快速查看命令

### 查看所有测试输出

```bash
# 方法1: 运行测试脚本
python run_tests_fixed.py

# 方法2: 直接运行pytest
python -m pytest tests/ -v

# 方法3: 生成HTML报告
python -m pytest tests/ --html=report.html --self-contained-html
start report.html
```

### 查看特定测试输出

```bash
# 查看基础智能体测试
python -m pytest tests/test_base_agent.py -v

# 查看规划智能体测试
python -m pytest tests/test_planning_agent.py -v

# 查看集成测试
python -m pytest tests/test_integration.py -v -m integration
```

### 查看详细调试信息

```bash
# 显示print输出和详细日志
python -m pytest tests/ -v -s --log-cli-level=DEBUG
```

---

## 🔧 输出配置

### 修改输出详细程度

```bash
# 最详细
python -m pytest tests/ -vv -s

# 详细
python -m pytest tests/ -v

# 简洁
python -m pytest tests/ -q
```

### 输出到文件

```bash
# 保存到文件
python -m pytest tests/ -v > output.txt 2>&1

# 同时显示和保存
python -m pytest tests/ -v | Tee-Object -FilePath output.txt
```

---

## 📝 总结

### 输出位置速查表

| 输出类型 | 位置 | 命令 |
|---------|------|------|
| 控制台输出 | 终端窗口 | `python run_tests_fixed.py` |
| HTML报告 | `report.html` | `pytest --html=report.html` |
| 覆盖率报告 | `htmlcov/index.html` | `pytest --cov=src --cov-report=html` |
| 日志文件 | `logs/manus.log` | 查看日志文件 |
| 测试输出文件 | `test_output.txt` | `pytest > test_output.txt` |

### 推荐查看方式

1. **开发调试**: 使用控制台实时输出 (`-v -s`)
2. **查看结果**: 使用HTML报告 (`--html=report.html`)
3. **代码覆盖**: 使用覆盖率报告 (`--cov-report=html`)
4. **保存记录**: 保存到文件 (`> output.txt`)

