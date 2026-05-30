# Best Practices for Agent Bug Killer

## For Users

### 1. Provide Clear Bug Descriptions

**Good:**
```
The checkout page returns 500 error when user has more than 10 items in cart.
Started happening after the latest deployment.
```

**Bad:**
```
Site is broken
```

### 2. Include Relevant Context

```bash
# Include server info
uv run python scenarios/bug_diagnoser/cli.py \
  --bug "Checkout fails with 500" \
  --host prod-server \
  --user deploy \
  --key ~/.ssh/id_rsa \
  --code /path/to/source
```

### 3. Use Multiple Data Sources

The more data you provide, the better the diagnosis:

- **SSH**: Server logs, process status
- **CDP**: Browser console, network requests
- **Code**: Source code search

### 4. Review and Validate

Always review the diagnosis results:

```python
result = diagnose_bug(...)

# Check confidence
if result.get("confidence", 0) > 0.7:
    print("High confidence diagnosis")
else:
    print("Low confidence - manual review recommended")
```

### 5. Build Knowledge Base

Save successful diagnoses for future reference:

```python
from core.history import DiagnosticHistory

history = DiagnosticHistory()
history.save(result, metadata={
    "bug": "Checkout 500 error",
    "resolution": "Increased connection pool size",
})
```

## For Developers

### 1. Write Good Error Messages

```python
# Bad
return "Error occurred"

# Good
return f"Failed to connect to {host}:{port}: {error}"
```

### 2. Use Type Annotations

```python
# Bad
def process(data):
    pass

# Good
def process(data: dict[str, Any]) -> Result:
    pass
```

### 3. Handle Errors Gracefully

```python
try:
    result = risky_operation()
except SpecificError as e:
    return f"Operation failed: {e}"
except Exception as e:
    logger.error("Unexpected error: %s", e)
    return "Internal error occurred"
```

### 4. Write Tests

```python
def test_success_case():
    result = my_function("input")
    assert result == "expected"

def test_error_case():
    with pytest.raises(ValueError):
        my_function("bad_input")
```

### 5. Document Your Code

```python
def complex_function(param1: str, param2: int) -> dict[str, Any]:
    """Do something complex.

    Args:
        param1: First parameter description.
        param2: Second parameter description.

    Returns:
        Dictionary with results.

    Raises:
        ValueError: If param1 is empty.
    """
    pass
```

## For Operators

### 1. Monitor Performance

```python
from core.metrics import metrics, MetricNames

# Track request duration
start = time.time()
result = process_request()
duration = time.time() - start

metrics.observe(MetricNames.REQUEST_DURATION, duration)
metrics.increment(MetricNames.REQUEST_COUNT)
```

### 2. Set Up Alerts

Monitor key metrics:

- Error rate > 5%
- Response time > 5s
- Knowledge base miss rate > 50%

### 3. Regular Backups

```bash
# Backup diagnostics
cp -r .diagnostics/ .diagnostics.backup/

# Backup knowledge base
cp knowledge_base.json knowledge_base.backup.json
```

### 4. Update Knowledge Base

Regularly review and update the knowledge base:

```python
from core.knowledge_base import KnowledgeBase

kb = KnowledgeBase()
kb.add_entry(KnowledgeEntry(
    id="kb-new",
    title="New Error Pattern",
    error_pattern="...",
    category="...",
    root_cause="...",
    solution="...",
))
```

### 5. Review Logs

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG

# Run with debug
uv run python scenarios/log_analyzer/cli.py --file error.log --debug
```

## Performance Tips

### 1. Use Caching

```python
from core.cache import cached

@cached(ttl=3600)
def expensive_operation(param: str) -> dict:
    # Expensive computation
    return result
```

### 2. Batch Operations

```python
# Bad
for error in errors:
    analyze_error(error)

# Good
results = analyze_errors(errors)
```

### 3. Limit History Queries

```python
# Bad
all_reports = history.list_reports(limit=10000)

# Good
recent_reports = history.list_reports(limit=20)
```

### 4. Use Connection Pooling

For production, configure connection pooling:

```python
# In settings
SSH_POOL_SIZE = 10
DB_POOL_SIZE = 20
```

## Security Best Practices

### 1. Protect API Keys

```bash
# Never commit API keys
echo ".env" >> .gitignore

# Use environment variables
export ANTHROPIC_API_KEY=sk-ant-...
```

### 2. Validate Inputs

```python
from core.validators import validate_host, validate_port

is_valid, error = validate_host(host)
if not is_valid:
    return f"Invalid host: {error}"
```

### 3. Use Least Privilege

```bash
# Use read-only SSH keys
# Limit API key permissions
# Use non-root containers
```

### 4. Enable Rate Limiting

```python
# In API configuration
RATE_LIMIT = 60  # requests per minute
```

## Integration Patterns

### 1. CI/CD Integration

```yaml
# GitHub Actions
- name: Analyze Logs
  run: |
    uv run python scenarios/log_analyzer/cli.py \
      --file logs/error.log \
      --output report.md \
      --format markdown
```

### 2. Slack Integration

```python
import requests

def send_to_slack(diagnosis: dict) -> None:
    webhook_url = os.getenv("SLACK_WEBHOOK")
    message = f"Bug Diagnosis: {diagnosis['summary']}"
    requests.post(webhook_url, json={"text": message})
```

### 3. Jira Integration

```python
def create_jira_issue(diagnosis: dict) -> str:
    # Create Jira issue from diagnosis
    return issue_key
```

## Common Pitfalls

### 1. Don't Ignore Low Confidence

```python
# Bad
if result:
    apply_fix(result)

# Good
if result and result.get("confidence", 0) > 0.7:
    apply_fix(result)
else:
    request_human_review(result)
```

### 2. Don't Over-rely on AI

AI diagnosis is a starting point, not the final answer.
Always verify with human expertise.

### 3. Don't Forget Error Handling

```python
# Bad
result = diagnose_bug(...)

# Good
try:
    result = diagnose_bug(...)
except Exception as e:
    logger.error("Diagnosis failed: %s", e)
    result = {"error": str(e)}
```

### 4. Don't Skip Tests

Always test your integrations:

```python
def test_my_integration():
    result = my_integration_function()
    assert result["status"] == "success"
```
