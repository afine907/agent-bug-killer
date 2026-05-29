# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly.

### How to Report

1. **Do NOT** open a public GitHub issue
2. Email security concerns to: [your-email@example.com]
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### Response Timeline

- **Acknowledgment**: Within 48 hours
- **Initial assessment**: Within 1 week
- **Fix timeline**: Depends on severity
  - Critical: Within 24 hours
  - High: Within 1 week
  - Medium: Within 2 weeks
  - Low: Within 1 month

## Security Best Practices

### API Keys

- Never commit API keys to version control
- Use environment variables or secret managers
- Rotate keys regularly

### SSH Keys

- Use key-based authentication (not passwords)
- Limit key permissions (principle of least privilege)
- Rotate keys periodically

### Dependencies

- Regularly update dependencies
- Run security audits (`uv audit`)
- Monitor for CVEs

### Network

- Use HTTPS in production
- Implement rate limiting
- Validate all inputs

## Security Features

- Rate limiting on API endpoints
- Input validation via Pydantic
- Non-root Docker user
- Request logging for audit trails
