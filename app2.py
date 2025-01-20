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

# Mock database
ORDERS_DB = {
    98765: {  # user_id
        123456: {  # order_id
            "status": "Shipped",
            "tracking_info": "Tracking Number: ABC123XYZ",
        }
    }
}


# Tool Functions
def get_current_time(*args, **kwargs):
    """Returns the current time in H:MM AM/PM format."""
    now = datetime.datetime.now()
    return now.strftime("%I:%M %p")


def fetch_order_details(user_id: int, order_id: int):
    """Fetches order details for a given user and order ID."""
    user_orders = ORDERS_DB.get(user_id)
    if not user_orders:
        return "User ID not found. Please check your ID."
    order_details = user_orders.get(order_id)
    if not order_details:
        return "Order ID not found. Please verify your order number."
    return f"Your order #{order_id} has been {order_details['status']}. Tracking Info: {order_details['tracking_info']}"


# List of tools
tools = [
    Tool(
        name="Time",
        func=get_current_time,
        description="Useful for when you need to know the current time.",
    ),
    Tool(
        name="Order Lookup",
        func=lambda user_id, order_id: fetch_order_details(int(user_id), int(order_id)),
        description="Fetch order status and tracking info using user_id and order_id.",
    )
]

# Prompt Template
prompt = PromptTemplate(
    input_variables=["input", "tools", "tool_names", "agent_scratchpad"],
    template="""
        Answer the following questions using the available tools: {tools}.

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
    memory=memory,
    verbose=True,
    handle_parsing_errors=True,
    return_intermediate_steps=True
)

# Run Test Query
try:
    response = agent_executor.invoke({"input": "What is the status of my order 123456? My user ID is 98765."})
    print("Agent Response:", response)
except Exception as e:
    print("Error occurred while invoking the agent:", str(e))
