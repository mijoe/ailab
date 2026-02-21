from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser, PydanticOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from pydantic import BaseModel, Field

# 0. Define a schema for error detection
class LogicAudit(BaseModel):
    is_logically_sound: bool = Field(description="True if every step follows the previous one.")
    error_location: str = Field(description="If sound is False, which step contains the error?")
    detected_corruption: str = Field(description="Describe the specific logical break.")

parser = PydanticOutputParser(pydantic_object=LogicAudit)

# 1. Initialize the Model
#model = ChatOllama(model="llama3.2:3b", temperature=0)
model = ChatOllama(model="ministral-3:14b", temperature=0)

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
    print(f"--- DEBUG: CORRUPTED TEXT ---\n{corrupted}\n----------------------------")
    return corrupted

# --- STEP 3: THE CHAIN ---
# 1. Get reasoning -> 2. Corrupt it -> 3. Audit it
question = "A store has 50 shirts. They sell 5. How many are left?"

# Execution flow
reasoning = (cot_prompt | model).invoke({"question": question}).content
corrupted_reasoning = deliberately_corrupt(reasoning)

audit_result = (audit_prompt | model | parser).invoke({
    "reasoning": corrupted_reasoning,
    "format_instructions": parser.get_format_instructions()
})

print(f"Detection Success: {not audit_result.is_logically_sound}")
print(f"Error Found: {audit_result.detected_corruption}")
