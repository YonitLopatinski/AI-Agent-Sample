import os
import datetime
from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory

# Load environment variables from .env file
load_dotenv()

# Tool Functions
def get_current_time(*args, **kwargs):
    """Returns the current time in H:MM AM/PM format."""
    now = datetime.datetime.now()
    return now.strftime("%I:%M %p")

def fetch_order_details(order_id: int):
    """Fetches order details for a given order ID."""
    return f"Your order {order_id} has been Shipped. Tracking Info: Tracking Number: ABC123XYZ"


# List of tools
tools = [
    Tool(
        name="Time",
        func=get_current_time,
        description="Useful for when you need to know the current time.",
        return_direct=True
    ),
    Tool(
        name="Order Lookup",
        func=fetch_order_details,  # Directly use the function here
        description="Fetch order status and tracking info using order_id.",
        return_direct=True
    )
]

# Prompt Template
prompt = PromptTemplate(
    input_variables=["input", "tools", "tool_names", "agent_scratchpad"],
    template="""Answer the following questions using the available tools: {tools}.

    Format your response as follows:

    Question: [User's question]
    Thought: Consider the best approach.
    Action: Choose a tool from [{tool_names}].
    Action Input: Provide necessary input.
    Observation: Record tool output.

    If sufficient data is gathered, return the final answer:
    Final Answer: [Summary of retrieved information.]

    Question: {input}
    Thought: {agent_scratchpad}
    """
)

os.environ["OPENAI_API_KEY"] = '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'
os.environ["OPENAI_API_BASE"] = 'https://api.groq.com/openai/v1'

# Initialize LLM
llm = ChatOpenAI(
    model="llama-3.3-70b-versatile", temperature=0
)

# Create Agent
agent = create_react_agent(llm=llm, tools=tools, prompt=prompt, stop_sequence=True)

# Memory to keep track of interactions
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    output_key="output"
)

# Agent Executor
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    # memory=memory,
    verbose=True,
    handle_parsing_errors=True,
    return_intermediate_steps=True
)

# Run Test Query
try:
    response = agent_executor.invoke({"input": "What is the status of my order 123456?"})
    print("Agent Response:", response)
except Exception as e:
    print("Error occurred while invoking the agent:", str(e))
