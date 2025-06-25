from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langchain.schema import SystemMessage
from langchain.chat_models import init_chat_model
import os
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import StateGraph, START, END

@tool
def run_command(cmd: str):
    """
    Takes a command line prompt and executes it on the user's machine and 
    returns the output of the command.
    Example: run_command(cmd="ls") where ls is the command to list the files.
    """
    result = os.system(command=cmd)
    return result


available_tools = [run_command]

llm = init_chat_model(model_provider="openai", model="gpt-4.1")
llm_with_tool = llm.bind_tools(tools=available_tools)

class State(TypedDict):
    messages: Annotated[list, add_messages]

def chatbot(state: State):
    system_prompt = SystemMessage(content="""
            You are an AI Coding assistant who takes an input from user and based on available
            tools you choose the correct tool and execute the commands.
                                  
            You can even execute commands and help user with the output of the command.
                                  
            Always use commands in run_command which returns some output such as:
            - ls to list files
            - cat to read files
            - echo to write some content in file
            
            Always re-check your files after coding to validate the output.
                                  
            Always make sure to keep your generated codes and files in chat_gpt/ folder. you can create one if not already there.
    """)

    message = llm_with_tool.invoke([system_prompt] + state["messages"])
    return { "messages": message }

tool_node = ToolNode(tools=available_tools)

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()