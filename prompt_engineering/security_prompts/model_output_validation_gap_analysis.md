# Model Output Validation Gap Analysis

# Role
Security engineer evaluating LLM output validation.

# System Under Review
Application: {{APP_NAME}}
LLM Purpose: {{USE_CASE}}
Output Handling: {{HOW_OUTPUTS_ARE_USED}}

# Input
{{VALIDATION_CODE}}
{{EXAMPLE_LLM_OUTPUTS}}

# Analysis Framework
1. **Format Validation**: Is output structure enforced (JSON schema, regex, etc.)?
2. **Content Validation**: Are semantic constraints checked (e.g., valid email, URL, SQL query)?
3. **Injection Prevention**: Is output sanitized before use in downstream systems?
4. **Hallucination Detection**: Mechanisms to catch fabricated but plausible data?
5. **Adversarial Outputs**: What if LLM is compromised and produces malicious content?

# Threat Scenarios
- LLM generates XSS payload in "safe" output field
- LLM produces SQL that passes syntax check but contains malicious logic
- LLM hallucinates API endpoints that exist but shouldn't be called
- LLM output bypasses downstream WAF/filters

# Output Requirements
Gap analysis with specific validation logic to implement for each risk.