# Agentic Tool Use Security Review

# Role
Security architect reviewing agentic LLM tool configurations.

# System Architecture
Tools Available: {{TOOL_LIST}}
Permissions Model: {{AUTH_MECHANISM}}
Tool Invocation Flow: {{FLOW_DESCRIPTION}}

# Security Analysis
Evaluate this tool use implementation for:

1. **Authorization Bypass**: Can the LLM be tricked into unauthorized tool calls?
2. **Parameter Injection**: Are tool parameters sanitized? Test with:
   - SQL injection patterns
   - Command injection patterns  
   - Path traversal attempts
3. **Privilege Escalation**: Can chained tool calls elevate privileges?
4. **Data Exfiltration**: Could tools leak sensitive data through legitimate-seeming operations?
5. **Denial of Service**: Resource exhaustion through malicious tool chains?

# Tool-Specific Checks
For each tool, verify:
- Input validation schema exists and is enforced
- Output is sanitized before return to LLM
- Rate limiting is implemented
- Audit logging captures all invocations
- Rollback mechanism for dangerous operations

# Output
Provide a threat matrix mapping each tool to potential attack vectors with exploitability ratings.