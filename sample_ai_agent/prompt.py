from langchain_core.prompts import PromptTemplate

system_prompt = PromptTemplate(
    input_variables=["input", "tools", "tool_names", "agent_scratchpad"],
    template="""Answer the following questions using the available tools: {tools}.

    Format your response as follows:

    Question: [User's question]
    Thought: Consider the best approach.
    Action: Choose a tool from [{tool_names}].
    Action Input: Provide necessary input.
    Observation: Record tool output. if done stop using this tool again.

    If sufficient data is gathered, return the final answer:
    Final Answer: [Summary of retrieved information.]

    Question: {input}
    Thought: {agent_scratchpad}
    """
)