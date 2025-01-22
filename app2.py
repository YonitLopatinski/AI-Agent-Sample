import datetime
import os

from dotenv import load_dotenv
from langchain.agents import initialize_agent, AgentType
from langchain.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI

load_dotenv()

os.environ["OPENAI_API_KEY"] = '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'


# os.environ["OPENAI_API_BASE"] = 'https://api.groq.com/openai/v1'


# Perceives: User asks, "What's the weather today?"
# Processes: Checks an API for the weather.
# Acts: Responds with "It's sunny and 25°C."

# A chat assistant where:
# A retrieval agent fetches documents,
# A summarization agent processes them,
# A reasoning agent generates responses.

# Tool Functions
def get_current_time(action_input=None):
    """Returns the current time in H:MM AM/PM format."""
    now = datetime.datetime.now()
    return now.strftime("%I:%M %p")


def get_order_details(order_id: str):
    """Returns order details for a given order ID."""
    order_id = int(order_id)
    return f"Your order {order_id} has been Shipped. Tracking Info: ABC123XYZ"


def get_user_data(user_id: str):
    """Fetches user data for a given user ID."""
    user_id = int(user_id)  # Convert to integer
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
        # return_direct=True
    ),
    Tool(
        name="Order Lookup",
        func=get_order_details,
        description="Fetch order status and tracking info using order_id.",
        # return_direct=True
    ),
    Tool(
        name="Get User Data",
        func=get_user_data,
        description="Fetch user profile details based on user ID.",
        # return_direct=True
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

# Create Agent Executor
agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,  # Supports multiple tool executions
    verbose=True,
    handle_parsing_errors=True
)

# Run Test Query
try:
    # response = agent_executor.invoke({"input": "Where is my order 12345?"})
    # print("Agent Response:", response['output'])

    # response = agent_executor.invoke({"input": "What is the status of my order 123456 and return time"})
    # print("Agent Response:", response['output'])

    # response = agent_executor.invoke({"input": "What is the details of user 555 and status order 123456 "})
    # print("Agent Response:", response['output'])

    response = agent_executor.invoke({"input": "What is time is it?"})
    print("Agent Response:", response['output'])

    # response = agent_executor.invoke({"input": "tell me about user 123456?"})
    # print("Agent Response:", response['output'])
except Exception as e:
    print("Error occurred while invoking the agent:", str(e))
