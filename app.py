import os

from dotenv import load_dotenv
from langchain.agents import (
    AgentExecutor,
    create_react_agent,
)
from langchain.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI

# Load environment variables from .env file
load_dotenv()


def get_current_time(*args, **kwargs):
    """Returns the current time in H:MM AM/PM format."""
    import datetime
    now = datetime.datetime.now()
    return now.strftime("%I:%M %p")


def get_weather(*args, **kwargs):
    """Returns the weather"""
    return "38C"


# List of tools available to the agent
tools = [
    Tool(
        name="Time",  # Name of the tool
        func=get_current_time,  # Function that the tool will execute
        description="Useful for when you need to know the current time", # Description of the tool
    ),
    Tool(
        name="Weather",
        func=get_weather,
        description="Useful for when you need to know the weather",
    ),
]


prompt = PromptTemplate(
    input_variables=["input", "tools", "tool_names", "agent_scratchpad"],
    template="""
        Answer the following questions to the best of your ability. You can utilize the following tools for assistance:  
        {tools}  
        
        Follow this structured format for your responses:  
        
        Question: The question you need to answer.  
        Thought: Reflect on what needs to be done.  
        Action: Specify the action to take, selecting one from [{tool_names}].  
        Action Input: Provide the input for the selected action.  
        Observation: Document the result of the action.  
        ... (Repeat the Thought/Action/Action Input/Observation cycle as needed.)  
        
        **If you have gathered all the necessary information, do not take further actions. Instead, construct a complete and final answer in this format:**  
        
        Final Answer: [Your complete answer, summarizing all retrieved information.]  

        Let's start!  
        
        Question: {input}  
        Thought: {agent_scratchpad}
    """
)

os.environ["OPENAI_API_KEY"] = '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'
os.environ["OPENAI_API_BASE"] = 'https://api.groq.com/openai/v1'

# Initialize a ChatOpenAI model
llm = ChatOpenAI(
    # model="llama3.2:3b", base_url="http://localhost:11434/v1", temperature=0
    # model="mixtral-8x7b-32768", temperature=0
    model="llama-3.3-70b-versatile", temperature=0
)

# Create the ReAct agent using the create_react_agent function
agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt,
    stop_sequence=True,
)

# 👉 Why? This memory keeps track of past interactions, preventing redundant tool calls.
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    output_key="output"  # Recommended in newer versions
)

# Create an agent executor from the agent and tools
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True,
    handle_parsing_errors=True,
    return_intermediate_steps=True
)

# Run the agent with a test query
try:
    response = agent_executor.invoke({"input": "What weather is it now? and what time?"})
    if response:
        print("Agent Response:", response)
    else:
        print("Warning: Received an empty response from the agent.")
except Exception as e:
    print("Error occurred while invoking the agent:", str(e))
