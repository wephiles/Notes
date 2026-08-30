<h1 style="text-align: center;">系统命令执行器</h1>

**涉及库**: `subprocess`, `argparse`, `sys`, `os`

# 1. 功能需求

创建一个批量执行系统命令的工具：

- 支持执行单个或多个命令
- 捕获命令输出和错误
- 设置超时时间
- 支持环境变量设置
- 记录执行日志

# 2. 代码框架

```python
#!/usr/bin/env python3

"""
系统命令执行器
使用方法: python cmd_runner.py "ls -la" "pwd" --timeout 10 --env DEBUG=1
"""

import sys
import os
import argparse
import subprocess
from datetime import datetime


class CommandRunner:
    def __init__(self, timeout=30, capture_output=True, env_vars=None):
        self.timeout = timeout
        self.capture_output = capture_output
        self.env_vars = env_vars or {}
        self.results = []
        
    def _prepare_env(self):
        """准备环境变量"""
        env = os.environ.copy()
        for key, value in self.env_vars.items():
            env[key] = value
        return env
    
    def run_command(self, command):
        """执行单个命令"""
        try:
            # TODO: 使用 subprocess.run 执行命令
            # 提示: subprocess.run(command, shell=True, capture_output=True, timeout=...)
            pass
        except subprocess.TimeoutExpired:
            return {"status": "timeout", "command": command}
        except subprocess.CalledProcessError as e:
            return {"status": "error", "command": command, "error": str(e)}
        except Exception as e:
            return {"status": "exception", "command": command, "error": str(e)}
    
    def run_commands(self, commands):
        """批量执行命令"""
        for cmd in commands:
            result = self.run_command(cmd)
            self.results.append(result)
            self._print_result(result)
        return self.results
    
    def _print_result(self, result):
        """打印命令结果"""
        # TODO: 格式化输出结果
        pass
    
    def get_summary(self):
        """获取执行摘要"""
        # TODO: 统计成功/失败数量
        pass


def main():
    parser = argparse.ArgumentParser(description="系统命令执行器")
    parser.add_argument("commands", nargs="+", help="要执行的命令")
    parser.add_argument("--timeout", type=int, default=30, help="超时时间(秒)")
    parser.add_argument("--env", nargs="*", help="环境变量，格式: KEY=VALUE")
    parser.add_argument("--output", choices=["text", "json"], default="text", help="输出格式")
    
    args = parser.parse_args()
    
    # TODO: 解析环境变量
    # TODO: 创建执行器并运行命令
    # TODO: 根据结果决定 sys.exit() 的状态码


if __name__ == "__main__":
    main()

```

# 3. 练习任务

### 练习任务

1. 使用 `subprocess.run()` 实现命令执行
2. 处理 `TimeoutExpired` 和 `CalledProcessError` 异常
3. 使用 `os.environ` 和自定义环境变量
4. 根据执行结果使用 `sys.exit()` 返回不同状态码
5. 支持 `--output json` 格式输出

# 4. 实现

```python
"""
系统命令执行器
使用方法:
  python cmd_runner.py "ls -la"
  python cmd_runner.py "ls -la" "pwd" "date"
  python cmd_runner.py "ping google.com" --timeout 5
  python cmd_runner.py "echo $MY_VAR" --env MY_VAR=hello
  python cmd_runner.py "ls" "pwd" --output json
"""

import sys
import os
import json
import argparse
import subprocess
from datetime import datetime
from typing import List, Dict, Optional, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
import time


class CommandResult:
    """命令执行结果"""

    def __init__(self, command: str, status: str,
                 stdout: str = "", stderr: str = "",
                 return_code: int = 0, duration: float = 0.0,
                 error: str = ""):
        self.command = command
        self.status = status  # success, error, timeout, exception
        self.stdout = stdout
        self.stderr = stderr
        self.return_code = return_code
        self.duration = duration
        self.error = error
        self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "command": self.command,
            "status": self.status,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "return_code": self.return_code,
            "duration": self.duration,
            "error": self.error,
            "timestamp": self.timestamp
        }


class CommandRunner:
    """系统命令执行器"""

    def __init__(self, timeout: int = 30,
                 env_vars: Optional[Dict[str, str]] = None,
                 shell: bool = True,
                 working_dir: Optional[str] = None):
        self.timeout = timeout
        self.env_vars = env_vars or {}
        self.shell = shell
        self.working_dir = working_dir
        self.results: List[CommandResult] = []

    def _prepare_env(self) -> Dict[str, str]:
        """使用 os.environ 准备环境变量"""
        env = os.environ.copy()
        env.update(self.env_vars)
        return env

    def run_command(self, command: str) -> CommandResult:
        """使用 subprocess.run 执行单个命令"""
        start_time = time.time()

        try:
            result = subprocess.run(
                command,
                shell=self.shell,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                env=self._prepare_env(),
                cwd=self.working_dir
            )

            duration = time.time() - start_time
            status = "success" if result.returncode == 0 else "error"

            return CommandResult(
                command=command,
                status=status,
                stdout=result.stdout,
                stderr=result.stderr,
                return_code=result.returncode,
                duration=duration,
                error="" if result.returncode == 0 else f"返回码: {result.returncode}"
            )

        except subprocess.TimeoutExpired:
            return CommandResult(
                command=command,
                status="timeout",
                error=f"命令执行超时 (>{self.timeout}秒)",
                duration=self.timeout
            )

        except FileNotFoundError:
            return CommandResult(
                command=command,
                status="exception",
                error="命令未找到"
            )

        except Exception as e:
            return CommandResult(
                command=command,
                status="exception",
                error=str(e)
            )

    def run_commands(self, commands: List[str], parallel: bool = False) -> List[CommandResult]:
        """批量执行命令"""
        self.results = []

        if parallel:
            with ThreadPoolExecutor(max_workers=min(len(commands), 5)) as executor:
                futures = {executor.submit(self.run_command, cmd): cmd for cmd in commands}
                for future in as_completed(futures):
                    self.results.append(future.result())
        else:
            for i, cmd in enumerate(commands, 1):
                print(f"\n[{i}/{len(commands)}] 执行: {cmd}")
                result = self.run_command(cmd)
                self.results.append(result)
                self._print_result(result)

        return self.results

    def _print_result(self, result: CommandResult):
        """打印结果"""
        icon = "✓" if result.status == "success" else "✗"
        print(f"{icon} {result.status} | {result.duration:.2f}s")
        if result.stdout:
            print(f"输出: {result.stdout.strip()[:200]}")
        if result.stderr:
            print(f"错误: {result.stderr.strip()}")

    def get_summary(self) -> Dict[str, int]:
        """获取统计摘要"""
        summary = {"total": len(self.results), "success": 0, "error": 0, "timeout": 0, "exception": 0}
        for r in self.results:
            summary[r.status] += 1
        return summary

    def print_summary(self):
        """打印摘要"""
        s = self.get_summary()
        print(f"\n{'=' * 50}")
        print(f"成功: {s['success']} | 失败: {s['error']} | 超时: {s['timeout']}")
        print(f"{'=' * 50}")


def parse_env_vars(env_args: Optional[List[str]]) -> Dict[str, str]:
    """解析环境变量参数"""
    env_dict = {}
    if env_args:
        for arg in env_args:
            if '=' in arg:
                key, value = arg.split('=', 1)
                env_dict[key.strip()] = value.strip()
    return env_dict


def main():
    """主函数 - 使用 argparse 解析参数，使用 sys 返回状态码"""

    parser = argparse.ArgumentParser(
        description="系统命令执行器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python cmd_runner.py "ls -la"
  python cmd_runner.py "ls" "pwd" --timeout 5
  python cmd_runner.py "echo $VAR" --env VAR=hello
  python cmd_runner.py "ls" --output json
  python cmd_runner.py "sleep 1" "sleep 1" --parallel
        """
    )

    parser.add_argument("commands", nargs="+", help="要执行的命令")
    parser.add_argument("--timeout", "-t", type=int, default=30, help="超时时间(秒)")
    parser.add_argument("--env", "-e", nargs="*", metavar="KEY=VALUE", help="环境变量")
    parser.add_argument("--output", "-o", choices=["text", "json"], default="text")
    parser.add_argument("--export", metavar="FILE", help="导出到JSON文件")
    parser.add_argument("--parallel", "-p", action="store_true", help="并行执行")
    parser.add_argument("--cwd", metavar="DIR", help="工作目录")
    parser.add_argument("--quiet", "-q", action="store_true", help="安静模式")

    args = parser.parse_args()

    # 验证工作目录
    if args.cwd and not os.path.isdir(args.cwd):
        print(f"错误: 目录不存在: {args.cwd}", file=sys.stderr)
        sys.exit(1)

    # 创建执行器
    runner = CommandRunner(
        timeout=args.timeout,
        env_vars=parse_env_vars(args.env),
        working_dir=args.cwd
    )

    # 执行命令
    if not args.quiet:
        print(f"\n执行 {len(args.commands)} 个命令 (超时: {args.timeout}s)")

    results = runner.run_commands(args.commands, parallel=args.parallel)

    # 输出结果
    if args.output == "json":
        data = {"summary": runner.get_summary(), "results": [r.to_dict() for r in results]}
        print(json.dumps(data, indent=2, ensure_ascii=False))
    elif not args.quiet:
        runner.print_summary()

    # 导出
    if args.export:
        with open(args.export, 'w') as f:
            json.dump({"results": [r.to_dict() for r in results]}, f, indent=2)
        print(f"已导出到: {args.export}")

    # 根据结果返回状态码
    summary = runner.get_summary()
    if summary['success'] == summary['total']:
        sys.exit(0)  # 全部成功
    elif summary['success'] == 0:
        sys.exit(1)  # 全部失败
    else:
        sys.exit(2)  # 部分成功


if __name__ == "__main__":
    main()
```

