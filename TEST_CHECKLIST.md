# 测试检查清单

## 快速测试指南

### 1. 安装测试依赖

```bash
pip install pytest pytest-cov pytest-html pytest-mock
```

### 2. 运行测试

#### Windows
```bash
# 方法1: 使用Python脚本
python run_tests.py

# 方法2: 使用批处理文件
scripts\run_tests.bat

# 方法3: 直接使用pytest
pytest tests/ -v
```

#### Linux/Mac
```bash
# 方法1: 使用Python脚本
python run_tests.py

# 方法2: 使用Shell脚本
chmod +x scripts/run_tests.sh
./scripts/run_tests.sh

# 方法3: 直接使用pytest
pytest tests/ -v
```

## 测试项目清单

### ✅ 必须测试的项目

#### 1. 基础功能测试
- [ ] **基础智能体** (`test_base_agent.py`)
  - 初始化测试
  - 状态管理测试
  - 记忆管理测试
  - 统计信息测试
  
  **成功标准**: 所有测试通过，覆盖率 > 90%

- [ ] **智能体管理器** (`test_agent_manager.py`)
  - 初始化测试
  - 智能体注册测试
  - 消息总线测试
  - 状态查询测试
  
  **成功标准**: 所有测试通过，智能体正确注册

#### 2. 智能体功能测试
- [ ] **规划智能体** (`test_planning_agent.py`)
  - 任务分解测试
  - 任务类型判断测试
  - 关键词提取测试
  
  **成功标准**: 
  - 任务能正确分解为子任务
  - 子任务类型判断准确率 > 80%
  - 关键词提取准确率 > 70%

- [ ] **知识检索智能体** (`test_knowledge_agent.py`)
  - 知识检索测试
  - 结果融合测试
  - 结果重排序测试
  
  **成功标准**:
  - 能返回检索结果
  - 结果去重正确
  - 排序按相关性（分数降序）

- [ ] **GUI智能体** (`test_gui_agent.py`)
  - 动作解析测试
  - 动作验证测试
  - 控制符识别测试
  
  **成功标准**:
  - 能正确解析模型输出
  - 只保留安全动作（白名单）
  - 控制符（DONE/FAIL/WAIT）正确识别

#### 3. 核心模块测试
- [ ] **任务执行器** (`test_task_executor.py`)
  - 任务执行流程测试
  - 错误处理测试
  
  **成功标准**:
  - 任务能执行完成
  - 错误能正确处理
  - 返回结构正确

#### 4. 集成测试
- [ ] **完整任务流程** (`test_integration.py`)
  - 简单任务流程测试
  - 智能体协作测试
  
  **成功标准**:
  - 任务能完整执行
  - 各智能体正确协作
  - 执行时间 < 10秒（无真实API调用）

### 🔍 建议测试的项目

#### 1. 性能测试
- [ ] 响应时间测试
  - 单步执行时间 < 3秒
  - 完整任务执行时间 < 30秒

- [ ] 并发测试
  - 多任务并发执行
  - 资源竞争处理

#### 2. 边界测试
- [ ] 空输入测试
- [ ] 超长输入测试
- [ ] 特殊字符测试
- [ ] 异常情况测试

#### 3. 安全测试
- [ ] 动作白名单测试
- [ ] 坐标验证测试
- [ ] 代码沙箱测试

## 测试成功判断标准

### 1. 单元测试成功标准

#### 检查点
- ✅ 所有测试用例通过（exit code = 0）
- ✅ 无错误和警告
- ✅ 代码覆盖率 > 80%
- ✅ 测试执行时间合理

#### 验证命令
```bash
# 运行测试
pytest tests/ -v

# 期望输出:
# =============== test session starts ===============
# tests/test_base_agent.py::test_base_agent_initialization PASSED
# tests/test_base_agent.py::test_base_agent_process PASSED
# ...
# =============== X passed in Y.YYs ===============

# 检查覆盖率
pytest --cov=src --cov-report=term-missing

# 期望输出:
# ----------- coverage: platform win32, python 3.9.x -----------
# Name                                    Stmts   Miss  Cover
# ------------------------------------------------------------
# src/agents/base_agent.py                  XX     X    XX%
# ...
# ------------------------------------------------------------
# TOTAL                                      XXX    XX    XX%
```

### 2. 集成测试成功标准

#### 检查点
- ✅ 任务能完整执行
- ✅ 返回状态为 "completed" 或 "partial"
- ✅ 执行步骤数 > 0
- ✅ 执行时间在合理范围内（< 30秒）
- ✅ 各智能体正确协作

#### 验证方法
```python
result = executor.execute(task)

# 验证
assert result["status"] in ["completed", "partial", "error"]
assert result.get("steps", 0) > 0
assert result.get("execution_time", 0) < 30
assert "plan" in result or result.get("status") == "error"
```

### 3. 功能测试成功标准

#### GUI操作测试
```python
# 测试截图
obs = gui_agent.observe()
assert obs["status"] == "success"
assert "screenshot" in obs

# 测试动作解析
actions = action_parser.parse(model_output)
assert len(actions) > 0
assert all(a in whitelist or a in ["DONE", "FAIL", "WAIT"] for a in actions)
```

#### 知识检索测试
```python
# 测试检索
result = knowledge_agent.retrieve("查询", top_k=5)
assert result["status"] == "success"
assert len(result["results"]) <= 5
assert all("content" in r for r in result["results"])
```

#### 任务规划测试
```python
# 测试分解
plan = planning_agent.decompose_task(task)
assert "subtasks" in plan
assert len(plan["subtasks"]) > 0
assert all("type" in st for st in plan["subtasks"])
```

### 4. 性能测试成功标准

#### 响应时间
- 单步执行: < 3秒
- 完整任务: < 30秒（无真实API）
- 知识检索: < 1秒

#### 资源使用
- 内存使用: < 2GB
- CPU使用: < 80%

### 5. 覆盖率标准

#### 目标覆盖率
- 总体覆盖率: > 80%
- 核心模块覆盖率: > 90%
- 智能体模块覆盖率: > 85%

#### 检查命令
```bash
pytest --cov=src --cov-report=html
# 查看 htmlcov/index.html
```

## 测试失败处理

### 常见问题及解决方案

#### 1. 依赖缺失
```bash
# 问题: ModuleNotFoundError
# 解决:
pip install -r requirements.txt
```

#### 2. 配置错误
```bash
# 问题: 配置加载失败
# 解决: 检查配置文件是否存在
ls configs/
```

#### 3. API密钥缺失
```bash
# 问题: API调用失败
# 解决: 
# 1. 设置环境变量
export OPENAI_API_KEY=your_key
# 2. 或使用测试模式（不使用真实API）
# 在测试中使用 mock
```

#### 4. 路径问题
```bash
# 问题: 导入错误
# 解决: 确保在项目根目录运行
cd manus-ai-system
pytest tests/
```

## 测试报告示例

### 成功报告
```
======================== test session starts ========================
platform win32 -- Python 3.9.0, pytest-7.4.0
collected 25 items

tests/test_base_agent.py::test_base_agent_initialization PASSED
tests/test_base_agent.py::test_base_agent_process PASSED
...
tests/test_integration.py::test_simple_task_flow PASSED

======================== 25 passed in 2.34s ========================

---------- coverage: platform win32, python 3.9.x -----------
Name                                    Stmts   Miss  Cover
------------------------------------------------------------
src/agents/base_agent.py                  45      2    96%
src/agents/planning_agent.py             120     15    88%
...
------------------------------------------------------------
TOTAL                                     850    120    86%
```

### 失败报告
```
======================== test session starts ========================
...
tests/test_base_agent.py::test_base_agent_initialization FAILED
...

FAILED tests/test_base_agent.py::test_base_agent_initialization
AssertionError: assert agent.name == "TestAgent"
```

## 快速验证命令

```bash
# 1. 快速运行所有测试
pytest tests/ -v

# 2. 运行并查看覆盖率
pytest --cov=src --cov-report=term

# 3. 只运行失败的测试
pytest --lf

# 4. 运行特定测试文件
pytest tests/test_base_agent.py -v

# 5. 运行并生成HTML报告
pytest --html=report.html --self-contained-html
```

## 测试检查清单

### 运行测试前
- [ ] 已安装所有依赖 (`pip install -r requirements.txt`)
- [ ] 配置文件存在 (`configs/`)
- [ ] 环境变量已设置（如需要）
- [ ] 在项目根目录

### 运行测试后
- [ ] 所有测试通过
- [ ] 覆盖率 > 80%
- [ ] 无警告和错误
- [ ] 执行时间合理
- [ ] 日志无异常

## 下一步

测试通过后，可以：
1. 运行完整系统: `python main.py`
2. 查看文档: `docs/`
3. 部署系统: `docker-compose up`

