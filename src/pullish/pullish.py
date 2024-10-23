import anthropic
import os
import argparse

from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")

class Pullish:

    character_limit: int = 4000
    client: anthropic.Anthropic

    def __init__(self, api_key: str = api_key):
        self.client = anthropic.Anthropic(
            api_key=api_key,
        )


    def parse_to_claude(self, text: str):
        message = self.client.messages.create(
            model="claude-3-5-sonnet-20240620",
            # model="claude-3-haiku-20240307",
            max_tokens=1000,
            temperature=0,
            system='I am a scientist trying to write about a grant proposal and I am trying to get funded. Clean up any grammatical mistakes in the following paragraph in the smoothest possible way. You are also allowed to reword to some degree, but avoid overly flowery languages and keep the document with the same tone. The document is written in typst, so you can keep the formatting specifically to typst. \n Only give me the rewritten version of the pargraph and absolutely nothing else. Do not add anything in front of your response such as  "Here is the answer to ....", otherwise it is an invalid answer. However, if you encounter typst commands such as #let and other similar syntax, leave them untouched.',
            messages=[{"role": "user", "content": [{"type": "text", "text": text}]}],
        )
        return message.content[0].text

    def format_file(self, file_path: str):
        file = open(file_path, "r")
        lines = file.readlines()
        current_buffer = ""
        input_buffer = []
        result = []
        for line in lines:
            if len(current_buffer) + len(line) > self.character_limit:
                input_buffer.append(current_buffer)
                result.append(self.parse_to_claude(current_buffer))
                current_buffer = ""
                current_buffer += line
            else:
                current_buffer += line

        if current_buffer != "":
            input_buffer.append(current_buffer)
            result.append(self.parse_to_claude(current_buffer))

        formatted_result = "".join(map(str, result)).split("\n")
        with open("test.typ", "w") as f:
            for line in formatted_result:
                f.write(line + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Pullish')
    parser.add_argument('file_path', type=str, help='Path to the file to be formatted')
    args = parser.parse_args()
    pullish = Pullish()
    pullish.format_file(args.file_path)