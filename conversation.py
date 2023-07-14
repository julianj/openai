#!/usr/bin/env python3
import openai
import os

"""
execute it like this:
(OPENAI_API_KEY=op://Private/OpenAICredential/credential  op run -- python3.11 conversation.py)

if conversation.py is executable and has shebang, it can be executed like this:
(OPENAI_API_KEY=op://Private/OpenAICredential/credential  op run -- ./conversation.py)

In this command, everything inside the parentheses ( ... ) runs in a subshell. The environment variable OPENAI_API_KEY is set only in this subshell and doesn't affect your main shell.

"""

openai.api_key = os.environ["OPENAI_API_KEY"]

# By default the code uses GPT-3.5. Setting this to True will switch to GPT4
GPT4 = False


class Conversation:
    """
    This class helps in keeping the context of the conversation.
    It's rudimentary and simply regulates the number of messages in the
    context window.

    It could be improved by:
    1. counting and limiting by the number of tokes instead
    of number of messages.
    2. Using the API to summarize the context and reduce its length.

    """

    # here's where we're going to store the conversation's context
    messages = []  
    
    # Here is where you can add some personality to your assistant, or
    # play with different prompting techniques to improve your results.
    initialContext = (
        "You are a helpful, polite, polymath. " 
        "Answer the user prompt being kindly."
    )

    def __init__(self):
        # Set the first message in the context 
        self._update("system", self.initialContext)

    def ask(self, prompt):
        # This function asks questions via the API.
  
        # adds the question with 'user' role to the context
        self._update("user", prompt)

        response = openai.ChatCompletion.create(
            model="gpt-4-0613" if GPT4 else "gpt-3.5-turbo-0613",
            messages=self.messages,  # sends all the context, including the last question
            temperature=0,
        )

        # adds the response with 'assistant' role to the context
        self._update("assistant", response.choices[0].message.content)

        # returns the response
        return response.choices[0].message.content

    def _update(self, role, content):
        # Keeps the context up to date

        self.messages.append(
            {
                "role": role,
                "content": content,
            }
        )

        # Tries to keep the context size manageable.
        if len(self.messages) > 20:
            self.messages.pop(1) # don't remove index 0 which contains the initial context

    def printContext(self):
        for i, item in enumerate(self.messages):
            if (item['role'] != "assistant"):
                print(i, '-', item['role'], '-', item['content'])

def main():
    conversation = Conversation()
    while True:
        # Use input() to read a line of text from standard input
        user_input = input("\nPlease enter your prompt: ")
        # Check if the user entered 'quit'
        if user_input.lower() == "quit":
            break
        # Otherwise, print the user's input
        else:
            #conversation.printContext()
            print("  ", conversation.ask(user_input))

    print("Exiting...")


if __name__ == "__main__":
    main()
