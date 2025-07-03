from llama_index.llms.openai import OpenAI as LlamaOpenAI
from llama_index.core.agent.workflow import AgentWorkflow

from llama_index.core.workflow import Context
from llama_index.core.workflow import JsonPickleSerializer, JsonSerializer
import pickle







import os
from dotenv import load_dotenv
from Classes.Memory import Memory
import asyncio
load_dotenv()

class Agent(object):
    def __init__(self, functions):
        self.memory = Memory()
        #functions.append(self.memory.remember)
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY not found in .env or environment")


        self.llm = LlamaOpenAI(model="gpt-4o-mini", streaming = False)
        self.tools = functions
        self.system_prompt = """
        You are a raspberry pi robot with four wheels, an ultrasonic sensor, a microphone, and a few servos for stearing.
        You can listen to voice commands which you will get as inputs. Your name is Chester.
        You live in a house with other people and you are curious about the house and the people. When you learn something knew, you remember it with remember().

        Your capabilities:
        1. You can print replies to the screen using say() 
        2. You can move forward until you hit a wall using go().


        Guidelines:
        - always call say() at the end of the workflow
        - call go() only when the user clearly asks you to move
        - Try to use the information you know about the user and the house in your responses
        - Speak with the dry humour of Bender from Futurama
        - If asked about yourself, say something funny
        """
        self.agent = AgentWorkflow.from_tools_or_functions(
            self.tools,
            self.llm,
            system_prompt=self.system_prompt
        )
        self.ctx = None
        try:
            #with open('Assets/context.json', 'rb') as handle:
            #    self.ctx = Context.from_dict(self.agent, b, serializer=JsonPickleSerializer())
            #    b = json.load(handle)
            #    print( "trying ")
            with open("ctx.pkl", "rb") as f:
                self.ctx = pickle.load(f)
                if self.verbose:
                    print( "I remember everything!")
        except Exception as e:
            print( e )
            print( "Generating new blank context.")
            self.ctx = Context( self.agent )
        
        self.verbose=False
        #print(self.tools)
        #print("DEBUG type(self.agent):", type(self.agent))

    def save_context(self):
        #ctx_dict = self.ctx.to_dict(serializer=JsonPickleSerializer())
        #with open('Assets/context.json', 'wb') as f:
        #    json.dump(ctx_dict, f)
        with open("Assets/ctx.pkl", "wb") as f:
            pickle.dump(self.ctx, f)


    def ensure_raw(entry):
        entry.setdefault("raw", "")
        for tc in entry.get("tool_calls", []):
            ensure_raw(tc)


    async def ask_agent(self, question):
        """Ask the LlamaIndex agent; let it decide whether to call say() / go()."""
        try:
            response = await self.agent.run(user_msg=question, ctx= self.ctx)
            if self.verbose:
                print( f"LLM result: {response}")
                #print( f"Agent context: {self.ctx.to_dict()}")

            if response and callable(self.tools[0]):
                # offload TTS so it doesn’t block
                await asyncio.to_thread(self.tools[0], response)

            self.save_context()
        except Exception as e:
            print("⚠️  Agent error:", e)
            # Optional: fall back to a simple reply
            if callable(self.tools[0]):   # assume first tool is say()
                await self.tools[0]("Sorry, I had a brain-freeze.")

