"""命令行用户界面"""
import sys
import os
from pathlib import Path
from typing import Dict, Any

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.core.task_executor import TaskExecutor


class ManusAICLI:
    """Manus AI 命令行界面"""
    
    def __init__(self):
        """初始化CLI"""
        self.config = self._load_config()
        self.executor = TaskExecutor(self.config)
    
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
    
    def run_interactive(self):
        """运行交互式界面"""
        print("=" * 60)
        print("🤖 Manus AI 代理系统 - 命令行界面")
        print("=" * 60)
        print()
        print("输入任务指令，系统将自动执行")
        print("输入 'quit' 或 'exit' 退出")
        print("输入 'help' 查看帮助")
        print("=" * 60)
        print()
        
        while True:
            try:
                # 获取用户输入
                instruction = input("请输入任务指令: ").strip()
                
                if not instruction:
                    continue
                
                # 处理特殊命令
                if instruction.lower() in ['quit', 'exit', 'q']:
                    print("\n感谢使用 Manus AI 代理系统！")
                    break
                
                if instruction.lower() == 'help':
                    self._show_help()
                    continue
                
                # 执行任务
                print(f"\n[执行中] {instruction}")
                print("-" * 60)
                
                task = {
                    "instruction": instruction,
                    "max_steps": 10,
                    "evaluator": {
                        "type": "screenshot_check",
                        "expected": "任务完成"
                    }
                }
                
                result = self.executor.execute(task)
                
                # 显示结果
                self._display_result(result)
                print()
                
            except KeyboardInterrupt:
                print("\n\n用户中断，退出系统")
                break
            except Exception as e:
                print(f"\n[错误] {str(e)}")
                print()
    
    def _show_help(self):
        """显示帮助信息"""
        print("\n" + "=" * 60)
        print("帮助信息")
        print("=" * 60)
        print("""
任务示例:
  1. 打开记事本
  2. 打开浏览器，访问百度
  3. 打开记事本，输入"Hello World"，保存为test.txt
  4. 打开浏览器，搜索"AI Agent"

命令:
  help  - 显示帮助信息
  quit  - 退出系统
  exit  - 退出系统

提示:
  - 使用清晰、具体的任务描述
  - 包含具体的操作步骤
  - 指定文件路径和名称
        """)
        print("=" * 60)
        print()
    
    def _display_result(self, result: Dict[str, Any]):
        """显示执行结果"""
        status = result.get("status", "unknown")
        steps = result.get("steps", 0)
        execution_time = result.get("execution_time", 0)
        
        print(f"\n[结果]")
        print(f"  状态: {status}")
        print(f"  步骤数: {steps}")
        print(f"  执行时间: {execution_time:.2f}秒")
        
        if status == "completed":
            print("  ✅ 任务成功完成！")
            if "plan" in result:
                plan = result["plan"]
                if "subtasks" in plan:
                    print(f"\n  执行了 {len(plan['subtasks'])} 个子任务:")
                    for i, subtask in enumerate(plan["subtasks"], 1):
                        print(f"    {i}. {subtask.get('description', 'N/A')}")
        elif status == "error":
            message = result.get("message", "未知错误")
            print(f"  ❌ 任务执行失败: {message}")
        else:
            print("  ⚠️  任务状态未知")


def main():
    """主函数"""
    cli = ManusAICLI()
    cli.run_interactive()


if __name__ == "__main__":
    main()

