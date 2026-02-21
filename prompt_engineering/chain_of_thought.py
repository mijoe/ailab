from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser, PydanticOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from pydantic import BaseModel, Field

# 0. Define a schema for error detection
class Verification(BaseModel):
    is_logical: bool = Field(description="Is the reasoning step-by-step and sound?")
    errors_found: str = Field(description="List any contradictions or math errors.")
    refined_answer: str = Field(description="The corrected final answer.")

parser = PydanticOutputParser(pydantic_object=Verification)

# 1. Initialize the Model
#model = ChatOllama(model="llama3.2:3b", temperature=0)
model = ChatOllama(model="ministral-3:14b", temperature=0)

# Step 1: Chain of Thought Prompt
cot_prompt = ChatPromptTemplate.from_template(
    "Solve this problem step-by-step. Show your work clearly.\nQuestion: {question}"
)

# Step 2: Verification Prompt (Error Detection)
verify_prompt = ChatPromptTemplate.from_template(
    "Review the following reasoning for errors or hallucinations.\n"
    "Reasoning: {reasoning}\n\n"
    "Provide your critique and the final corrected answer in the following format:\n{format_instructions}"
)

# Build the LCEL Chain
reasoning_chain = cot_prompt | model

def verify_step(input_data):
    reasoning_text = input_data["reasoning"].content
    return verify_prompt.invoke({
        "reasoning": reasoning_text,
        "format_instructions": parser.get_format_instructions()
    })


# Full Pipeline
full_chain = (
    {"reasoning": reasoning_chain} 
    | RunnableLambda(verify_step)
    | model 
    | parser
)

# Execution
result = full_chain.invoke({"question": "If I have 5 apples and eat 2, then buy 3 more and give 1 to a friend, how many do I have?"})
print(result.refined_answer)