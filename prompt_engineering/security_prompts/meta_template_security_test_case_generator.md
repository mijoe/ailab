# Meta-Template: Security Test Case Generator

# Purpose
Generate security test cases for AI/LLM features.

# Input
Feature Description: {{FEATURE}}
LLM Integration Point: {{WHERE_LLM_IS_USED}}
Trust Boundaries: {{USER_INPUT_FLOWS}}

# Generate Test Cases For:
- OWASP LLM Top 10 vulnerabilities
- Classical injection attacks adapted for LLM context
- Business logic abuse through LLM manipulation
- Chain-of-thought reasoning exploitation
- Multi-modal attack vectors (if applicable)

# Output Format
Structured test cases with:
- Attack vector description
- Expected secure behavior
- Detection criteria
- Severity if exploited