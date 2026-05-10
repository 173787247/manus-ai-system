"""
V1 骨架演示：BaseAgent + 最小具体智能体（无外部依赖，可单独运行）。
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List


class BaseAgent(ABC):
    """与主仓库设计理念一致的极简基类（教学用快照）。"""

    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.config = config
        self.state = "idle"
        self.memory: List[Dict[str, Any]] = []
        self.statistics = {"tasks_completed": 0, "tasks_failed": 0}

    @abstractmethod
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError

    def get_status(self) -> Dict[str, Any]:
        return {"name": self.name, "state": self.state, "statistics": self.statistics}


class EchoAgent(BaseAgent):
    """回显输入，模拟最小 process 闭环。"""

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        self.state = "working"
        text = input_data.get("text", "")
        self.memory.append({"text": text, "ts": datetime.now().isoformat()})
        self.state = "idle"
        self.statistics["tasks_completed"] += 1
        return {"status": "ok", "echo": text}


def main() -> None:
    agent = EchoAgent("Echo", {})
    out = agent.process({"text": "Manus V1 skeleton"})
    print("状态:", agent.get_status())
    print("输出:", out)


if __name__ == "__main__":
    main()
