import datetime

from langchain.tools import Tool


def get_current_time(action_input=None):
    """Returns the current time in H:MM AM/PM format."""
    now = datetime.datetime.now()
    return now.strftime("%I:%M %p")


def fetch_order_details(order_id: str):
    """Fetches order details for a given order ID."""
    order_id = int(order_id)  # Convert to integer
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


# Define tools
tools = [
    Tool(
        name="Time",
        func=get_current_time,
        description="Useful for when you need to know the current time."
    ),
    Tool(
        name="Order Lookup",
        func=fetch_order_details,
        description="Fetch order status and tracking info using order_id."
    ),
    Tool(
        name="Get User Data",
        func=get_user_data,
        description="Fetch user profile details based on user ID."
    )
]
