import os

from dotenv import load_dotenv
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI

from sample_ai_agent.prompt import system_prompt
from tools import tools

load_dotenv()


def create_agent():
    """Initialize the AI Agent with tools and OpenAI's LLM."""

    llm = ChatOpenAI(model="llama-3.3-70b-versatile", temperature=0)

    # memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,  # Supports multiple tool executions
        # memory=memory,
        verbose=True,
        handle_parsing_errors=True
    )
    # agent.memory.chat_memory.messages.append(SystemMessage(content=str(system_prompt)))

    return agent
