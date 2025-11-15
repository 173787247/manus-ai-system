"""Web用户界面"""
import gradio as gr
import logging
import os
from typing import Dict, Any
from pathlib import Path

# 添加项目根目录到路径
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.core.agent_manager import AgentManager
from src.core.task_planner import TaskPlanner
from src.core.task_executor import TaskExecutor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ManusAIWebUI:
    """Manus AI Web界面"""
    
    def __init__(self):
        """初始化Web界面"""
        self.config = self._load_config()
        self.agent_manager = AgentManager(self.config.get("agents", {}))
        self.task_planner = TaskPlanner(self.config)
        self.task_executor = TaskExecutor(self.config)
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置"""
        return {
            "agents": {
                "planning": {
                    "openai_api_key": os.getenv("OPENAI_API_KEY"),
                    "model": os.getenv("DEFAULT_LLM_MODEL", "gpt-4"),
                    "temperature": float(os.getenv("TEMPERATURE", "0.1"))
                },
                "knowledge": {
                    "vector_collection": "knowledge"
                },
                "code": {
                    "openai_api_key": os.getenv("OPENAI_API_KEY"),
                    "model": os.getenv("DEFAULT_LLM_MODEL", "gpt-4")
                },
                "gui": {
                    "openai_api_key": os.getenv("OPENAI_API_KEY"),
                    "vl_model": os.getenv("DEFAULT_VL_MODEL", "gpt-4-vision-preview")
                },
                "evaluation": {
                    "openai_api_key": os.getenv("OPENAI_API_KEY"),
                    "model": os.getenv("DEFAULT_LLM_MODEL", "gpt-4")
                }
            },
            "max_steps": int(os.getenv("MAX_STEPS", "10"))
        }
    
    def execute_task(self, instruction: str, max_steps: int = 10) -> str:
        """
        执行任务
        
        Args:
            instruction: 任务指令
            max_steps: 最大步骤数
            
        Returns:
            执行结果
        """
        try:
            # 创建任务
            task = {
                "instruction": instruction,
                "max_steps": max_steps,
                "evaluator": {
                    "type": "screenshot_check",
                    "expected": "任务完成"
                }
            }
            
            # 执行任务
            result = self.task_executor.execute(task)
            
            # 格式化结果
            output = f"""
任务执行结果
============

状态: {result.get('status', 'unknown')}
步骤数: {result.get('steps', 0)}

执行详情:
{self._format_result(result)}
"""
            return output
            
        except Exception as e:
            logger.error(f"任务执行失败: {e}")
            return f"错误: {str(e)}"
    
    def _format_result(self, result: Dict[str, Any]) -> str:
        """格式化结果"""
        if result.get("status") == "completed":
            return "任务成功完成！"
        elif result.get("status") == "error":
            return f"任务执行失败: {result.get('message', '未知错误')}"
        else:
            return "任务执行中..."
    
    def create_interface(self):
        """创建Gradio界面"""
        with gr.Blocks(title="Manus AI 代理系统") as interface:
            gr.Markdown("""
            # 🤖 Manus AI 代理系统
            
            工业级多智能体代理系统，支持GUI自动化、任务规划、知识检索等功能。
            """)
            
            with gr.Row():
                with gr.Column(scale=2):
                    instruction_input = gr.Textbox(
                        label="任务指令",
                        placeholder="例如：打开浏览器，搜索'AI Agent'，并截图保存",
                        lines=3
                    )
                    max_steps_input = gr.Slider(
                        label="最大步骤数",
                        minimum=1,
                        maximum=50,
                        value=10,
                        step=1
                    )
                    execute_btn = gr.Button("执行任务", variant="primary")
                
                with gr.Column(scale=1):
                    gr.Markdown("### 系统状态")
                    status_output = gr.Textbox(
                        label="智能体状态",
                        value=self._get_agent_status(),
                        lines=5,
                        interactive=False
                    )
            
            output = gr.Textbox(
                label="执行结果",
                lines=10,
                interactive=False
            )
            
            # 绑定事件
            execute_btn.click(
                fn=self.execute_task,
                inputs=[instruction_input, max_steps_input],
                outputs=output
            )
            
            # 示例
            gr.Markdown("""
            ### 示例任务
            
            - 打开记事本，输入"Hello World"，保存为test.txt
            - 打开浏览器，访问百度，搜索"AI Agent"
            - 打开Excel，创建一个包含姓名和年龄的表格
            """)
        
        return interface
    
    def _get_agent_status(self) -> str:
        """获取智能体状态"""
        status = self.agent_manager.get_agent_status()
        lines = []
        for name, agent_status in status.items():
            lines.append(f"{name}: {agent_status['state']}")
        return "\n".join(lines) if lines else "无智能体"


def main():
    """主函数"""
    import socket
    
    def find_free_port(start_port=7860, max_attempts=10):
        """查找可用端口"""
        for i in range(max_attempts):
            port = start_port + i
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('', port))
                    return port
            except OSError:
                continue
        return None
    
    ui = ManusAIWebUI()
    interface = ui.create_interface()
    
    # 尝试使用7860，如果被占用则自动查找其他端口
    port = 7860
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', port))
    except OSError:
        # 端口被占用，查找可用端口
        port = find_free_port(7860)
        if port is None:
            logger.error("无法找到可用端口")
            return
        logger.info(f"端口7860被占用，使用端口 {port}")
    
    print(f"\n{'='*60}")
    print(f"系统已启动！")
    print(f"{'='*60}")
    print(f"访问地址: http://localhost:{port}")
    print(f"{'='*60}\n")
    
    interface.launch(
        server_name="127.0.0.1",
        server_port=port,
        share=False,
        show_error=True
    )


if __name__ == "__main__":
    main()

