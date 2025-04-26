from openai import OpenAI
import os

class LLMService:
    def __init__(self, config):
        """
        Initializes the LLMService with the given configuration.
        Sets up the OpenAI client based on the baseUrl in the configuration.
        """
        self.config = config
        if not config['LLMCONFIG']['baseUrl']:
            # Use default OpenAI base URL
            self.client = OpenAI(api_key=os.environ.get("API_KEY"))
        else:
            # Use custom base URL
            self.client = OpenAI(
                base_url=config['LLMCONFIG']['baseUrl'],
                api_key=os.environ.get("API_KEY")
            )

    def getReviewFromLLM(self, diffData):
        """
        Sends a request to the LLM to review the provided diff data.
        Returns the review content or an error message if the request fails.
        """
        try:
            # Prepare the messages for the LLM
            messages = [
                {
                    "role": "system",
                    "content": self.config['LLMCONFIG']['systemPrompt']
                },
                {
                    "role": "user",
                    "content": self.config['LLMCONFIG']['userPrompt'].format(gitdiff=diffData),
                },
            ]

            # Send the request to the LLM
            completion = self.client.chat.completions.create(
                model=self.config['LLMCONFIG']['modelAlias'],
                messages=messages
            )
            return completion.choices[0].message.content
        except:
            # Handle any errors during the LLM request
            return "Failed to review the PR."
