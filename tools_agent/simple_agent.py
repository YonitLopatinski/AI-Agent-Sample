import json
import config

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="llama-3.3-70b-versatile", temperature=0)

from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="llama-3.3-70b-versatile", temperature=0)

prompt = PromptTemplate(
    input_variables=["question"],
    template="""
        🛠️ You're an helpful AI Assistant 

        1️⃣ Use Thought to understand the user's question.
        2️⃣ Use Action to run one of the actions available to you

         🛠️ Your available actions are::
        🔹 📦 find_order_details – If an order lookup is required
                ``` 
                {{"function_name": "find_order_details", "function_params": {{"order_id": "ORDER_ID"}}}}
                ```
        🔹 👤 get_user_details – If user details are needed
                ``` 
                {{"function_name": "get_user_details", "function_params": {{"user_id": "USER_ID"}}}}
                ```
      
        
        ❓ User Question:
        💬 {question}

        ➡️ If a action is needed, return output JSON format ONLY

    """
)


def find_order_details(order_id):
    """Mock function to retrieve order details based on order ID."""
    mock_orders = {
        "11": {"status": "Shipped", "delivery_date": "2025-02-05"},
        "12": {"status": "Processing", "delivery_date": "TBD"},
        "13": {"status": "Delivered", "delivery_date": "2025-01-30"},
    }
    return mock_orders.get(order_id, "Order not found.")


def get_user_details(user_id):
    """Returns user data for a given user ID."""
    users_data = {
        "1": {"user_id": "1", "name": "Alice Smith", "email": "alice.smith@example.com",
                   "account_status": "Inactive"},
        "2": {"user_id": "2", "name": "Bob Johnson", "email": "bob.johnson@example.com",
                   "account_status": "Suspended"},
    }
    return users_data.get(user_id, "User not found.")


available_actions = {
    "find_order_details": find_order_details,
    "get_user_details": get_user_details
}


def execute_action(action_json):
    """Parses JSON and executes the correct function."""
    try:
        if not action_json:
            raise Exception("No action to execute")

        # Parse the action_json string into a dictionary
        action_data = json.loads(action_json)

        function_name = action_data['function_name']
        function_params = action_data['function_params']

        if function_name not in available_actions:
            raise Exception(f"Unknown action: {function_name}: {function_params}")

        action_function = available_actions[function_name]
        return function_name, action_function(**function_params)

    except json.JSONDecodeError:
        return "❌ Failed to parse tool response."


def get_answer(question):
    """Get response from LLM and execute tool if needed."""
    formatted_prompt = prompt.format(question=question)
    response = llm.invoke(formatted_prompt)

    # Try parsing JSON from response
    try:
        json_response = json.loads(response.content)
        if isinstance(json_response, dict) and "function_name" in json_response:
            return execute_action(response.content)  # Call tool function
    except json.JSONDecodeError:
        pass

    return response.content  # Return normal response if no tool is used


# user_question = "Where is my order 11?"
user_question = "Where is account status for user 1?"
answer = get_answer(user_question)
print(f"💬Question: {user_question}")
print(f"🤖Answer: {answer}")
