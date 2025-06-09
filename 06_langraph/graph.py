from typing_extensions import TypedDict
from openai import OpenAI
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END

load_dotenv()

client = OpenAI()


class State(TypedDict):
    query: str
    llm_result: str | None


def chat_bot(state: State):

    query = state['query']

    llm_response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": query}
        ]
    )

    result = llm_response.choices[0].message.content
    state["llm_result"] = result

    return state


graph_builder = StateGraph(State)

graph_builder.add_node("chat_bot", chat_bot)

graph_builder.add_edge(START, "chat_bot")
graph_builder.add_edge("chat_bot", END)

graph = graph_builder.compile()


def main():
    user = input("> ")

    # Invoke the graph
    _state = {
        "query": user,
        "llm_result": None
    }

    graph_result = graph.invoke(_state)

    print("graph_result", graph_result)


main()
