import os

from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()
os.environ["OPENAI_API_KEY"] = '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'

llm = ChatOpenAI(model="llama-3.3-70b-versatile", temperature=0)

prompt_template = """
    You are a knowledgeable AI assistant. 
    Your role is to respond to the user's inquiry with the most accurate and helpful information.  
    User's question: {question}
    Please provide a clear and short answer
"""
prompt = PromptTemplate(template=prompt_template, input_variables=["question"])


def get_answer(question):
    """
    Get an answer to the given question using the QA chain.
    """
    formatted_prompt = prompt.format(question=question)
    response = llm.invoke(formatted_prompt)
    return response.content


user_question = "What is Dell Technologies?"
answer = get_answer(user_question)
print(f"💬Question: {user_question}")
print(f"🤖Answer: {answer}")
