# import config
# from langchain.prompts import PromptTemplate
# from langchain_openai import ChatOpenAI
#
# # Define LLM
# llm = ChatOpenAI(model="llama-3.3-70b-versatile", temperature=0)
#
# # Define CoT Prompt Template
# prompt = PromptTemplate(
#     input_variables=["question"],
#     template="""
#         🛠️ AI Assistant with Tool Access
#         📌 You must carefully analyze the question and determine if a tool is needed.
#
#          🧠 Chain of Thought (CoT) Reasoning
#         1️⃣ Understand the user's question.
#         2️⃣ Decide whether to answer directly or use a tool.
#         3️⃣ Invoke the tool if needed and use its result to form a response.
#
#          🛠️ Available Tools
#         🔹 👤 User Details – Retrieve user information.
#         🔹 📦 Order Lookup – Find order details when the user asks about an order.
#
#         ❓ User Question:
#         💬 {question}
#
#         ➡️ If a tool is needed, use it and provide the final answer.
#     """
# )
#
#
#
# # Tool: Order Lookup
# def find_order_details(order_id):
#     """Mock function to retrieve order details based on order ID."""
#     mock_orders = {
#         "11": {"status": "Shipped", "delivery_date": "2025-02-05"},
#         "12": {"status": "Processing", "delivery_date": "TBD"},
#         "13": {"status": "Delivered", "delivery_date": "2025-01-30"},
#     }
#     return mock_orders.get(order_id, "Order not found.")
#
#
# # Tool: User Details (Multiple Users)
# def get_user_details(user_id):
#     """Returns user data for a given user ID."""
#     users_data = {
#         "user_1": {"user_id": "user_1", "name": "Alice Smith", "email": "alice.smith@example.com", "account_status": "Inactive"},
#         "user_2": {"user_id": "user_2", "name": "Bob Johnson", "email": "bob.johnson@example.com", "account_status": "Suspended"},
#     }
#     return users_data.get(user_id, "User not found.")
#
#
# # Function to Get Answer
# def get_answer(question):
#     formatted_prompt = prompt.format(question=question)
#     response = llm.generate(formatted_prompt)
#     return response[0].text
#
#
# # Example Usage
# user_question = "What are mocks?"
# answer = get_answer(user_question)
# print(f"💬 Question: {user_question}")
# print(f"🤖 Answer: {answer}\n")
#
#
#
#
#
#
# #
# # user_question = "What is the email of user_003?"
# # answer = get_answer(user_question)
# # print(f"💬 Question: {user_question}")
# # print(f"🤖 Answer: {answer}\n")
#
# # user_question = "What is status of 13?"
# # answer = get_answer(user_question)
# # print(f"💬 Question: {user_question}")
# # print(f"🤖 Answer: {answer}\n")