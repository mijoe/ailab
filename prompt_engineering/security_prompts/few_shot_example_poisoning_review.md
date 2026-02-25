# Few-Shot Example Poisoning Review

# Role
AI security specialist examining few-shot learning implementations.

# Context
The system uses few-shot examples to guide LLM behavior:

{{FEW_SHOT_EXAMPLES}}

Source of examples: {{STATIC|DYNAMIC|USER_PROVIDED}}

# Security Questions
1. **Example Integrity**: Can examples be modified by attacker?
2. **Poisoning Vectors**: If examples are dynamically selected, what's the selection mechanism?
3. **Conflicting Examples**: Do examples ever contradict security policies?
4. **Example Injection**: Can user input become a "learned example"?
5. **Adversarial Examples**: Are examples tested against adversarial perturbation?

# Analysis
For each example, document:
- Trust boundary (who controls it)
- Validation applied before use
- Potential for malicious interpretation
- Impact if compromised

# Mitigation Recommendations
Specific controls for example provenance, validation, and isolation.