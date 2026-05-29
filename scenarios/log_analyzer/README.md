# 场景1: 日志分析器 (Log Analyzer)

## 概述

从日志文件中提取错误信息，分析错误模式，生成结构化诊断报告。

## 功能

- 读取本地日志文件（支持多种编码）
- 解析标准日志格式（时间戳、级别、模块、消息）
- 提取 Python Traceback 和堆栈信息
- 生成 JSON 格式的诊断报告

## 工具

| 工具 | 功能 |
|------|------|
| `file_reader` | 读取文件内容，支持编码回退和大小限制 |
| `log_parser` | 解析日志提取结构化错误信息 |

## 使用方法

### CLI

```bash
# 分析日志文件
uv run python scenarios/log_analyzer/cli.py --file /path/to/error.log

# 直接传入日志文本
uv run python scenarios/log_analyzer/cli.py --text "2024-01-15 ERROR Something failed"

# 指定输出格式
uv run python scenarios/log_analyzer/cli.py --file app.log --output json

# 调试模式
uv run python scenarios/log_analyzer/cli.py --file app.log --debug
```

### Python API

```python
from scenarios.log_analyzer.src.agent import analyze_log

result = analyze_log("/path/to/error.log")
print(result)
```

## 测试

```bash
# 运行单元测试
uv run pytest scenarios/log_analyzer/tests/ -v

# 运行集成测试
uv run pytest scenarios/log_analyzer/tests/ -v -m integration
```
