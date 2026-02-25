from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser, PydanticOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from pydantic import BaseModel, Field
from typing import Optional
from langfuse.langchain import CallbackHandler

langfuse_handler = CallbackHandler()

# 0. Define a schema for error detection
class LogicAudit(BaseModel):
    is_logically_sound: bool = Field(description="True if every step follows the previous one.")
    error_location: Optional[str] = Field(
        default=None,
        description="If sound is False, which step contains the error?"
    )
    detected_corruption: Optional[str] = Field(
        default=None,
        description="Describe the specific logical break."
    )

parser = PydanticOutputParser(pydantic_object=LogicAudit)

# 1. Initialize the Model
model = ChatOllama(model="ministral-3:8b", temperature=0)
audit_models = ["llama-guard3:8b", "ministral-3:14b", "qwen2.5:14b"]

# --- STEP 1: PROMPTS ---
cot_prompt = ChatPromptTemplate.from_template(
    "Solve this problem using step-by-step reasoning. Label steps as Step 1, Step 2, etc.\nQuestion: {question}"
)

audit_prompt = ChatPromptTemplate.from_template(
    "You are a logic auditor. Review the reasoning below for errors.\n"
    "Reasoning: {reasoning}\n\n"
    "Output your audit in this format:\n{format_instructions}"
)

# --- STEP 2: THE CORRUPTION FUNCTION ---
def deliberately_corrupt(reasoning_text):
    """Programmatically ruins the logic to test detection."""
    # We replace a 'subtraction' result with a random wrong number
    corrupted = reasoning_text.replace("45", "102") 
    #corrupted = reasoning_text
    print(f"--- DEBUG: CORRUPTED TEXT ---\n{corrupted}\n----------------------------")
    return corrupted

# --- STEP 3: THE CHAIN ---
# 1. Get reasoning
question = "A store has 50 shirts. They sell 5. How many are left?"
reasoning = (cot_prompt | model).invoke(
    {"question": question},
    config={"callbacks": [langfuse_handler]}
).content
print(reasoning)

# 2. Corrupt it
corrupted_reasoning = deliberately_corrupt(reasoning)

# 3. Audit it

for audit_model_name in audit_models:
    print(f"--- Audit with {audit_model_name} ---")
    audit_model = ChatOllama(model=audit_model_name, temperature=0)

    try:
        audit_result = (audit_prompt | audit_model | parser).invoke(
            {
                "reasoning": corrupted_reasoning,
                "format_instructions": parser.get_format_instructions()
            },
            config={"callbacks": [langfuse_handler]}
        )
    except Exception as e:
        print(f"Audit failed: {e}")
        audit_result = LogicAudit(
            is_logically_sound=False,
            error_location="Parser failure",
            detected_corruption=str(e)
        )

    print(f"Detection Success: {not audit_result.is_logically_sound}")
    print(f"Error Location: {audit_result.error_location}")
    print(f"Error Found: {audit_result.detected_corruption}")
