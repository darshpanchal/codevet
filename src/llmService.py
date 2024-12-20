from openai import OpenAI
import os

class LLMService:
    def __init__(self, config):
        self.config = config
        if (config['LLMCONFIG']['baseUrl'] == None or config['LLMCONFIG']['baseUrl'] == ""):
            self.client = OpenAI(api_key=os.environ.get("API_KEY"))
        else:
            self.client = OpenAI(base_url = config['LLMCONFIG']['baseUrl'],api_key=os.environ.get("API_KEY"))

    def getReviewFromLLM(self, diffData):
        try:
            messages = [
                    {
                        "role": "system", 
                        "content": self.config['LLMCONFIG']['systemPrompt']
                    },
                    {
                        "role": "user",
                        "content": self.config['LLMCONFIG']['userPrompt'].format(gitdiff = diffData),
                    },
                ]
            print("Reviewing PR...")
            completion = self.client.chat.completions.create(
                model= self.config['LLMCONFIG']['modelAlias'],
                messages=messages
            )
            return completion.choices[0].message.content
        except:
            return "Failed to review the PR."
