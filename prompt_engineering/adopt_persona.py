from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

# 0. Define scoring data structure with Pydantic
class EssayScore(BaseModel):
    score: int = Field(description="The score of the essay from 1 to 5, with 1 being very bad and 5 being very good.")
    reasoning: str = Field(description="A short justification for the score")

parser = JsonOutputParser(pydantic_object=EssayScore)

# 1. Initialize the Model
#model = ChatOllama(model="llama3.2:3b", temperature=0)
model = ChatOllama(model="ministral-3:8b", temperature=0)

# 2. Define the Prompt Template
system_template = """
You are a {persona}. 
Your output must be strictly limited to the data structure requested. 
Do not provide preamble, intro, or outro text.
"""

user_template = """
Grade the following essay:
---
{essay}
---

{format_instructions}
"""

prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_template),
    ("user", user_template)
])
#print(prompt_template)

# 3. Create a Chain
# This pipes the prompt into the model, then cleans the output to a string
chain = prompt_template | model | parser

# 4. Run the Experiment
essay_text = "I like chickens. Chickens are fluffy and they give tasty eggs."

personas = ["neutral AI assistant", "harsh academic grader", "first-grade teacher", "preschool teacher"]

for persona in personas:
    print(f"--- Scoring with persona: {persona} ---")
    response = chain.invoke({
        "persona": persona, 
        "essay": essay_text, 
        "format_instructions": parser.get_format_instructions()})
    print(f"{response}\n")

