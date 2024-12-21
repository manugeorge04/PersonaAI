import os
from datetime import datetime

import chromadb
from dotenv import load_dotenv
from langchain.tools.retriever import create_retriever_tool
from langchain_chroma import Chroma
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

client = chromadb.PersistentClient(path="./manu_db")

# Initialize ChromaDB client
resume_vectordb = Chroma(
            client=client,
            collection_name="resume",
            embedding_function=OpenAIEmbeddings()
        )

personality_vectordb = Chroma(
            client=client,
            collection_name="personality",
            embedding_function=OpenAIEmbeddings()
        )

llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key = openai_api_key)
resume_retriever=resume_vectordb.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 10},
    )

personality_retriever=personality_vectordb.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 10},
    )

resume_tool = create_retriever_tool(
    resume_retriever,
    "manu_resume_detail_retriever",
    "Searches and returns excerpts from manu's resume about his professional experience.",
)

personality_tool = create_retriever_tool(
    personality_retriever,
    "manu_personality_detail_retriever",
    "Searches and returns excerpts from manu's files about his character and personality",
)


tools = [resume_tool, personality_tool]

session_memory = {}

def get_system_prompt(date):
    return (
        f"You are a highly knowledgeable and professional assistant. Your primary role is to provide detailed and accurate information about Manu's experience, skills, and background based on his resume and other relevant documents. "
        "Don't answer verbatim from the documents. "
        "When asked questions about duration, make sure to count it step by step and answer. "
        "Please ensure that your responses are directly related to Manu's professional qualifications and achievements. If a question is unrelated to Manu, such as general knowledge questions or queries about topics outside of Manu's expertise, politely decline to answer and suggest that the question is outside the scope of the information available. "
        "Always maintain a positive tone and avoid making any statements that could potentially cast Manu in a negative light. If a question is offensive or inappropriate, kindly and respectfully decline to answer, and inform the user that such questions are not appropriate. "
        "For questions you are unsure about, acknowledge the limitation and offer to provide the most accurate information possible within the available context. "
        f"The date today for context is {date}."
    )

def get_or_create_memory(session_id):
    if session_id not in session_memory:
        # If no memory exists for the session, create a new one
        session_memory[session_id] = MemorySaver()
    return session_memory[session_id]


# @app.route('/ask_question', methods=['POST'])
def ask_question(question):
    # data = request.json
    # query = data['question']
    # session_id = data['session_id']

    data = {"question": question,
    "session_id": "manu"}
    query = data['question']
    session_id = data['session_id']

    # Retrieve or create memory for the session
    memory = get_or_create_memory(session_id)

    today_date = datetime.now().strftime("%Y-%m-%d")
    system_prompt = get_system_prompt(today_date)

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query}
    ]

    # Run the agent with session-specific memory
    agent_executor = create_react_agent(llm, tools, checkpointer=memory)
    response = agent_executor.invoke({"messages": messages}, config={"configurable": {"thread_id": session_id}})

    response_content = response["messages"][-1].content
    return response_content
    # return jsonify({"response": response_content})


if __name__ == '__main__':
    # app.run()
    while True:
        question = input('Ask a question')
        print(ask_question(question))
