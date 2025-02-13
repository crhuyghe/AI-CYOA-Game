import json
from openai import OpenAI

class GameManager:
    """Handles the progression of the game, including operations involving OpenAI."""
    def __init__(self, api_key):
        self._story_data = json.load("story_data.json")
        self.running_data = None

        self.story_list = [self._story_data[i]["title"] for i in range(len(self._story_data))]

        self.action_number = -1
        self._client = OpenAI(api_key=api_key)
        self._prompts = {}  # Include prompts for the AI model

    def select_game(self, index):
        """Sets the story index and performs initialization steps"""
        self.running_data = self._story_data[index]
        self.action_number = 8
        return self.running_data["introduction"]

    def next_action(self, action):
        """Progresses the game to the next action"""
        # Perform validation of action first

        # Then prompt AI for story interpretation of action

        # Then prompt AI for immediate consequences of action

        # Perform item, map, and character update checks

        # Return AI output and boolean to indicate whether self.action_number is 0

    def generate_conclusion(self):
        """Attempts to wrap up the story."""

    def _prompt_ai(self, messages):
        completion = self._client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        return completion.choices[0].message.content
