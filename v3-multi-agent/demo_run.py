"""
V3 演示：从项目根目录加载 AgentManager + MessageBus（多智能体管理）。
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.core.agent_manager import AgentManager, MessageBus  # noqa: E402


def main() -> None:
    bus = MessageBus()
    log: list[str] = []

    def on_event(msg: dict) -> None:
        log.append(f"topic={msg.get('topic')} keys={list(msg.keys())}")

    bus.subscribe("demo", on_event)
    bus.publish("demo", {"hello": "manus_v3"})

    config = {
        "agents": {
            "planning": {
                "openai_api_key": "",
                "model": "gpt-4",
                "temperature": 0.1,
            }
        }
    }
    manager = AgentManager(config)
    print("MessageBus received:", len(log), "message(s)")
    print("Registered agents:", list(manager.agents.keys()))
    print("Status:", manager.get_agent_status())
    task = {"instruction": "V3 multi-agent smoke test；检索并总结要点"}
    plan = manager.coordinate_task(task)
    print("coordinate_task keys:", list(plan.keys()))


if __name__ == "__main__":
    main()
