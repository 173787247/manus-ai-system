# 测试指南

## 1. 如何启动测试

### 1.1 安装测试依赖

```bash
# 确保已安装pytest
pip install pytest pytest-asyncio pytest-cov

# 或安装所有依赖（包括测试依赖）
pip install -r requirements.txt
```

### 1.2 运行测试

#### 运行所有测试

```bash
# 在项目根目录
pytest

# 或使用详细输出
pytest -v

# 或显示打印输出
pytest -s
```

#### 运行特定测试文件

```bash
# 运行基础智能体测试
pytest tests/test_base_agent.py

# 运行规划智能体测试
pytest tests/test_planning_agent.py

# 运行集成测试
pytest tests/test_integration.py
```

#### 运行特定测试函数

```bash
# 运行特定测试函数
pytest tests/test_base_agent.py::test_base_agent_initialization

# 运行多个测试
pytest tests/test_base_agent.py::test_base_agent_initialization tests/test_base_agent.py::test_base_agent_process
```

#### 按标记运行测试

```bash
# 只运行单元测试
pytest -m unit

# 只运行集成测试
pytest -m integration

# 排除慢速测试
pytest -m "not slow"
```

#### 生成覆盖率报告

```bash
# 生成覆盖率报告
pytest --cov=src --cov-report=html

# 查看覆盖率报告
# 打开 htmlcov/index.html
```

### 1.3 使用Docker运行测试

```bash
# 构建测试镜像
docker build -t manus-ai-test -f Dockerfile.test .

# 运行测试
docker run --rm manus-ai-test pytest
```

## 2. 建议测试的项目

### 2.1 单元测试（Unit Tests）

#### ✅ 基础智能体测试 (`test_base_agent.py`)
- [x] 智能体初始化
- [x] 状态管理
- [x] 记忆管理
- [x] 统计信息更新

**成功标准**:
- 所有测试通过
- 覆盖率 > 90%

#### ✅ 规划智能体测试 (`test_planning_agent.py`)
- [x] 任务分解功能
- [x] 任务类型判断
- [x] 关键词提取
- [x] 依赖关系分析

**成功标准**:
- 任务能正确分解为子任务
- 子任务类型判断准确
- 依赖关系正确识别

#### ✅ 知识检索智能体测试 (`test_knowledge_agent.py`)
- [x] 知识检索功能
- [x] 结果融合
- [x] 结果重排序

**成功标准**:
- 能返回检索结果
- 结果去重正确
- 排序按相关性

#### ✅ GUI智能体测试 (`test_gui_agent.py`)
- [x] 动作解析
- [x] 动作验证
- [x] 控制符识别

**成功标准**:
- 能正确解析模型输出
- 只保留安全动作
- 控制符正确识别

#### ✅ 智能体管理器测试 (`test_agent_manager.py`)
- [x] 智能体注册
- [x] 消息总线
- [x] 任务协调

**成功标准**:
- 智能体能正确注册
- 消息能正确传递
- 任务能正确协调

### 2.2 集成测试（Integration Tests）

#### ✅ 任务执行流程测试 (`test_integration.py`)
- [x] 完整任务流程
- [x] 智能体协作
- [x] 错误处理

**成功标准**:
- 任务能完整执行
- 各智能体正确协作
- 错误能正确处理

### 2.3 功能测试（Functional Tests）

#### GUI操作测试
```python
# 测试屏幕截图
def test_screenshot_capture():
    agent = GUIAgent(config)
    obs = agent.observe()
    assert obs["status"] == "success"
    assert "screenshot" in obs

# 测试动作执行
def test_action_execution():
    agent = GUIAgent(config)
    actions = ["moveTo(100, 200)", "click()"]
    result = agent.act(actions)
    assert result["status"] in ["success", "DONE"]
```

#### 知识检索测试
```python
# 测试向量检索
def test_vector_search():
    agent = KnowledgeAgent(config)
    result = agent.retrieve("测试查询", top_k=5)
    assert result["status"] == "success"
    assert len(result["results"]) <= 5
```

#### 任务规划测试
```python
# 测试任务分解
def test_task_decomposition():
    agent = PlanningAgent(config)
    task = {"instruction": "打开浏览器，搜索AI"}
    plan = agent.decompose_task(task)
    assert "subtasks" in plan
    assert len(plan["subtasks"]) > 0
```

### 2.4 性能测试

#### 响应时间测试
```python
import time

def test_response_time():
    start = time.time()
    result = executor.execute(task)
    elapsed = time.time() - start
    
    # 单步执行时间应 < 3秒
    assert elapsed < 3.0
```

#### 并发测试
```python
import concurrent.futures

def test_concurrent_execution():
    tasks = [task1, task2, task3]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(execute_task, tasks))
    
    # 所有任务应成功
    assert all(r["status"] == "completed" for r in results)
```

### 2.5 端到端测试（E2E Tests）

#### 完整任务流程
```python
def test_complete_task_flow():
    # 1. 创建任务
    task = {
        "instruction": "打开记事本，输入Hello World，保存",
        "max_steps": 10
    }
    
    # 2. 执行任务
    result = executor.execute(task)
    
    # 3. 验证结果
    assert result["status"] == "completed"
    assert result["steps"] > 0
    assert result["evaluation"]["completion_score"] > 0.8
```

## 3. 如何准确判断测试成功与否

### 3.1 测试成功标准

#### 单元测试成功标准

1. **所有测试通过**
   ```bash
   pytest tests/ -v
   # 期望输出: PASSED
   ```

2. **无错误和警告**
   ```bash
   pytest tests/ -W error
   # 不应有任何警告
   ```

3. **覆盖率达标**
   ```bash
   pytest --cov=src --cov-report=term-missing
   # 覆盖率应 > 80%
   ```

#### 集成测试成功标准

1. **任务能完整执行**
   - 状态为 "completed" 或 "partial"
   - 执行步骤数 > 0
   - 执行时间在合理范围内

2. **智能体正确协作**
   - 规划智能体成功分解任务
   - 各智能体正确响应
   - 消息正确传递

3. **错误正确处理**
   - 错误被正确捕获
   - 错误信息清晰
   - 系统能恢复

#### 功能测试成功标准

1. **GUI操作**
   - 截图能成功捕获
   - 动作能正确执行
   - 控制符正确识别

2. **知识检索**
   - 能返回相关结果
   - 结果数量符合要求
   - 结果相关性高

3. **任务规划**
   - 任务能正确分解
   - 子任务类型正确
   - 依赖关系正确

### 3.2 测试结果验证

#### 检查测试输出

```bash
# 运行测试并查看详细输出
pytest -v -s tests/

# 期望看到:
# =============== test session starts ===============
# tests/test_base_agent.py::test_base_agent_initialization PASSED
# tests/test_base_agent.py::test_base_agent_process PASSED
# ...
# =============== X passed in Y.YYs ===============
```

#### 检查覆盖率

```bash
# 生成覆盖率报告
pytest --cov=src --cov-report=html

# 查看覆盖率
# 打开 htmlcov/index.html
# 覆盖率应 > 80%
```

#### 检查日志

```bash
# 运行测试并查看日志
pytest -v --log-cli-level=INFO tests/

# 检查是否有错误日志
```

### 3.3 测试失败处理

#### 常见失败原因

1. **依赖缺失**
   ```bash
   # 解决: 安装依赖
   pip install -r requirements.txt
   ```

2. **配置错误**
   ```bash
   # 解决: 检查配置文件
   # 确保 .env 文件正确配置
   ```

3. **API密钥缺失**
   ```bash
   # 解决: 设置环境变量
   export OPENAI_API_KEY=your_key
   # 或使用测试模式（不使用真实API）
   ```

4. **环境问题**
   ```bash
   # 解决: 检查Python版本
   python --version  # 应 >= 3.9
   
   # 检查虚拟环境
   which python  # 应在虚拟环境中
   ```

### 3.4 测试报告

#### 生成HTML报告

```bash
# 安装pytest-html
pip install pytest-html

# 生成HTML报告
pytest --html=report.html --self-contained-html
```

#### 生成JUnit XML报告

```bash
# 生成JUnit XML（用于CI/CD）
pytest --junitxml=report.xml
```

## 4. 测试最佳实践

### 4.1 测试编写原则

1. **独立性**: 每个测试应独立，不依赖其他测试
2. **可重复**: 测试结果应可重复
3. **快速**: 单元测试应快速执行
4. **清晰**: 测试名称应清晰描述测试内容

### 4.2 测试数据

```python
# 使用fixture提供测试数据
@pytest.fixture
def sample_task():
    return {
        "instruction": "测试任务",
        "max_steps": 5
    }

def test_with_fixture(sample_task):
    result = executor.execute(sample_task)
    assert result["status"] in ["completed", "error"]
```

### 4.3 Mock外部依赖

```python
from unittest.mock import Mock, patch

@patch('src.agents.planning_agent.ChatOpenAI')
def test_with_mock(mock_llm):
    mock_llm.return_value.invoke.return_value.content = '{"goal": "test"}'
    
    agent = PlanningAgent(config)
    result = agent.decompose_task(task)
    
    assert result["status"] == "success"
```

## 5. 持续集成测试

### 5.1 GitHub Actions示例

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - run: pip install -r requirements.txt
      - run: pytest --cov=src --cov-report=xml
      - uses: codecov/codecov-action@v2
```

## 6. 测试检查清单

### 运行测试前检查

- [ ] 所有依赖已安装
- [ ] 配置文件正确
- [ ] 环境变量已设置（如需要）
- [ ] 测试数据已准备

### 测试后检查

- [ ] 所有测试通过
- [ ] 覆盖率达标（>80%）
- [ ] 无警告和错误
- [ ] 性能指标正常
- [ ] 日志无异常

## 7. 快速测试命令

```bash
# 快速运行所有测试
pytest

# 运行并显示覆盖率
pytest --cov=src --cov-report=term

# 运行特定模块
pytest tests/test_agents/

# 运行并生成报告
pytest --html=report.html --self-contained-html

# 只运行失败的测试
pytest --lf

# 运行最后失败的测试
pytest --ff
```

