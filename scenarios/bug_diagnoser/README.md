# 场景2: 线上 Bug 诊断器 (Bug Diagnoser)

## 概述

通过多数据源（SSH 服务器日志、浏览器 CDP、代码搜索）诊断线上 Bug，生成综合诊断报告。

## 功能

- SSH 执行远程命令和读取日志
- CDP 浏览器截图、Console 日志、Network 请求
- 代码搜索定位错误处理逻辑
- 多源关联分析，生成诊断报告

## 工具

| 工具 | 功能 |
|------|------|
| `ssh_exec` | SSH 执行远程命令 |
| `ssh_read_log` | 读取远程日志文件 |
| `cdp_connect` | 连接浏览器 CDP |
| `cdp_screenshot` | 浏览器截图 |
| `cdp_console` | 获取 Console 日志 |
| `cdp_network` | 获取 Network 请求 |
| `code_search` | 代码搜索 |
| `log_parser` | 日志解析（复用自 log_analyzer） |

## 使用方法

### CLI

```bash
# 基本诊断
uv run python scenarios/bug_diagnoser/cli.py \
  --bug "页面白屏" \
  --host prod-server \
  --user deploy \
  --key ~/.ssh/id_rsa

# 带浏览器诊断
uv run python scenarios/bug_diagnoser/cli.py \
  --bug "接口超时" \
  --host api-server \
  --browser ws://localhost:9222/devtools/browser/...

# 带代码搜索
uv run python scenarios/bug_diagnoser/cli.py \
  --bug "NPE in checkout" \
  --code /path/to/source
```

### Python API

```python
from scenarios.bug_diagnoser.src.agent import diagnose_bug

result = diagnose_bug(
    bug_description="页面白屏",
    server_info={"host": "prod-server", "user": "deploy"},
    browser_ws="ws://localhost:9222/devtools/browser/...",
    code_path="/path/to/source",
)
print(result)
```

## 前置条件

- SSH: 需要可访问的服务器和密钥
- CDP: 需要运行中的 Chrome（`chrome --remote-debugging-port=9222`）
- Code: 需要本地源代码目录

## 测试

```bash
# 运行单元测试
uv run pytest scenarios/bug_diagnoser/tests/ -v

# 运行集成测试
uv run pytest scenarios/bug_diagnoser/tests/ -v -m integration
```
