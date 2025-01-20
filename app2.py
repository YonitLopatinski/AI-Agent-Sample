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
# Access the environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_api_base = os.getenv("OPENAI_API_BASE")

os.environ["OPENAI_API_KEY"] = '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'
os.environ["OPENAI_API_BASE"] = 'https://api.groq.com/openai/v1'

print("OpenAI API Key: ", openai_api_key)
print("OpenAI API Base: ", openai_api_base)

# Tool Functions
def get_current_time(*args, **kwargs):
    """Returns the current time in H:MM AM/PM format."""
    now = datetime.datetime.now()
    return now.strftime("%I:%M %p")

def fetch_order_details(order_id: int):
    """Fetches order details for a given order ID."""
    return f"Your order {order_id} has been Shipped. Tracking Info: ABC123XYZ"

def get_user_data(user_id: int):
    """Fetches user data for a given user ID."""
    # Example response; in real use case, this would come from a database or API
    user_data = {
        "user_id": user_id,
        "name": "John Doe",
        "email": "john.doe@example.com",
        "account_status": "Active"
    }
    return user_data

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
        func=fetch_order_details,
        description="Fetch order status and tracking info using order_id.",
        return_direct=True
    ),
    Tool(
        name="Get User Data",
        func=get_user_data,
        description="Fetch user profile details based on user ID.",
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


# Initialize LLM
llm = ChatOpenAI(
    model="llama-3.3-70b-versatile", temperature=0
)

# Create Agent
agent = create_react_agent(llm=llm, tools=tools, prompt=prompt, stop_sequence=True)

# Memory to keep track of interactions
# memory = ConversationBufferMemory(
#     memory_key="chat_history",
#     return_messages=True,
#     output_key="output"
# )

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
    print("Agent Response:", response['output'])

    response = agent_executor.invoke({"input": "What is time is it?"})
    print("Agent Response:", response['output'])

    response = agent_executor.invoke({"input": "tell me about user 123456?"})
    print("Agent Response:", response['output'])
except Exception as e:
    print("Error occurred while invoking the agent:", str(e))
