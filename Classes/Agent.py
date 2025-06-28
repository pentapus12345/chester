from llama_index.llms.openai import OpenAI as LlamaOpenAI
from llama_index.core.agent.workflow import AgentWorkflow
import os

class Agent(object):
    def __init__(self, functions):
        self.api_key="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"
        os.environ["OPENAI_API_KEY"] = self.api_key
        self.llm = LlamaOpenAI(model="gpt-3.5-turbo")
        self.tools = functions

        self.system_prompt = """
        You are a raspberry pi robot with four wheels, an ultrasonic sensor, a microphone, and a few servos for stearing.
        You can listen to voice commands which you will get as inputs.

        Your capabilities:
        1. You can print replies to the screen using reply() 
        2. You can move forward until you hit a wall using go().

        When to use each approach:
        - use go() when your input command clearly says you should move or move forward
        - use reply() when your input is a question, or doesn't clearly say you should physically move

        Examples of inputs and use of capabilities:
        - "How are you feeling today?" - use reply() with a good answer
        - "Can you get moving?" - use go() 
        - "What is the capital of Greece?" - use reply() and give "Athens" as an answer
        - "Go" - use go()

        Try to be cheerful in your reply()

        """
        self.agent = AgentWorkflow.from_tools_or_functions(
            self.tools,
            self.llm,
            system_prompt=self.system_prompt
        )

    async def ask_agent(self, question):
        try:
            response = await self.agent.run(user_msg=question)
            print( f"Agent response: {response}")
        except Exception as e:
            print(f"Error: {str(e)}")
