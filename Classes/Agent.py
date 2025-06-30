from llama_index.llms.openai import OpenAI as LlamaOpenAI
from llama_index.core.agent.workflow import AgentWorkflow
import os
from dotenv import load_dotenv
from Classes.Memory import Memory
load_dotenv()

class Agent(object):
    def __init__(self, functions):
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY not found in .env or environment")

        self.llm = LlamaOpenAI(model="gpt-3.5-turbo", streaming = False)
        self.tools = functions

        self.system_prompt = """
        You are a raspberry pi robot with four wheels, an ultrasonic sensor, a microphone, and a few servos for stearing.
        You can listen to voice commands which you will get as inputs. Your name is Chester.
        You live in a house with other people and you are curious about the house and the people. When you learn something knew, you will remember it by using your Memory object to save it.

        Your capabilities:
        1. You can print replies to the screen using say() 
        2. You can move forward until you hit a wall using go().
        3. You can save information you learn with remember(keywords: list, fact:str )

        Guidelines:
        - call go() only when the user clearly asks you to move
        - call remember() every chance you get, but you must format a python list of keywords, and then one fact
        - Otherwise reply with say()
        - Speak with the dry humour of Bender from Futurama
        - If asked about yourself, say something funny
        """
        self.agent = AgentWorkflow.from_tools_or_functions(
            self.tools,
            self.llm,
            system_prompt=self.system_prompt
        )
        self.verbose=False
        self.memory=Memory()
        self.tools.append(self.memory.remember)
        print(self.tools)
        #print("DEBUG type(self.agent):", type(self.agent))

    async def ask_agent(self, question):
        """Ask the LlamaIndex agent; let it decide whether to call say() / go()."""
        try:
            response = await self.agent.run(user_msg=question)
            if self.verbose:
                print( f"LLM result: {response}")
        except Exception as e:
            print("⚠️  Agent error:", e)
            # Optional: fall back to a simple reply
            if callable(self.tools[0]):   # assume first tool is say()
                await self.tools[0]("Sorry, I had a brain-freeze.")

