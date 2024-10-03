import anthropic
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('ANTHROPIC_API_KEY')

client = anthropic.Anthropic(
    api_key=api_key,
)

message = client.messages.create(
    model="claude-3-5-sonnet-20240620",
    max_tokens=1000,
    temperature=0,
    system="I am a scientist trying to write about a grant proposal and I am trying to get funded. Clean up any grammatical mistakes in the following paragraph in the smoothest possible way. You are also allowed to reword to some degree, but avoid overly flowery languages and keep the document with the same tone. The document is written in typst, so you can keep the formatting specifically to typst. Only give me the rewritten version of the pargraph and absolutely nothing else",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Driven by the rapid advancements in machine learning over the past decade, numerous studies in computer vision and biomechanics have demonstrated promising potential for optimizing athletic performance."
                }
            ]
        }
    ]
)
print(message.content)