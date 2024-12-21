import json
import uuid
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from llm_utils.chatbot import get_or_create_memory, get_system_prompt, llm, tools
from langgraph.prebuilt import create_react_agent
from datetime import datetime

# Create your views here.

@api_view(["POST"])
def send_message(request):
    data = json.loads(request.body)
    query = data['question']
    session_id = request.session.get('session_id', str(uuid.uuid4()))
    print(session_id, query)
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
    response_data = {"response": response_content}

    return Response(response_data, status=status.HTTP_200_OK)
