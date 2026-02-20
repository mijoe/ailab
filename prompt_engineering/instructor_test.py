import instructor
from pydantic import BaseModel

class Person(BaseModel):
    name: str
    age: int
    occupation: str

client = instructor.from_provider("ollama/llama3-2-3b")

person = client.create(
    response_model=Person,
    messages=[
        {"role": "user", "content": "Extract: John"}
    ],
)

print(person)

# PydanticAI